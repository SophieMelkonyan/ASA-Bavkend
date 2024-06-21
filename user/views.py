from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.views import FormView
from django.contrib.auth import authenticate, login
from .form import EmailForm, CustomUserCreationForm,ProfileUpdateForm,PostForm,Special_Form
from .generate_token import account_activation_token
from .tasks import send_simple_email
from django.contrib import messages
from .models import Post, Special_Post

User = get_user_model()

class EmailView(FormView):
    template_name = "users/send_simple_email.html"
    form_class = EmailForm
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        body = form.cleaned_data["body"]

        send_simple_email.apply_async(kwargs={"body": body, "subject": subject, "email": email, "count": 10})
        return response

class RegistrationView(CreateView):
    form_class = CustomUserCreationForm
    model = User
    template_name = "users/Login.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        user.is_active = False
        user.save()

        subject = "Authenticate your Profile"
        token = account_activation_token.make_token(user)
        message = render_to_string("users/authentication.html", {
            "user": user,
            "domain": get_current_site(self.request).domain,
            "token": token
        })
        email = EmailMessage(subject=subject, body=message, from_email=settings.EMAIL_HOST_USER, to=[user.email])
        email.send(fail_silently=False)
        messages.success(self.request, 'We send you email please check!')

        return response


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            request.user.profile.post_counts += 1
            request.user.profile.save()
            return redirect('user:profile')
    else:
        form = PostForm()
    return render(request, 'post/create_post.html', {'form': form})


@login_required
def create_story(request):
    if request.method == 'POST':
        form = Special_Form(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            request.user.profile.story_counts += 1
            request.user.profile.save()
            post.save()
            return redirect('user:profile')
    else:
        form = PostForm()
    return render(request, 'post/create_story.html', {'form': form})

class ValidateUserLink(TemplateView):
    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        pk = kwargs.get("pk")
        user = User.objects.get(pk=pk)
        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("user:login")
        return HttpResponse("Your token is invalid")

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('user:profile')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('user:register')
    return render(request, "users/Login.html")

@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        posts = Post.objects.filter(user=profile)
        story = Special_Post.objects.filter(user=profile)
        context['profile'] = profile
        context['posts'] = posts
        context['storys'] = story
        if not profile.image:
            context['image_url'] = None
        else:
            context['image_url'] = profile.image.url
        return context

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/update.html', {'form': form})


@login_required
def delete_profile(request):
    user = request.user
    user.delete()
    messages.success(request, 'Your profile has been deleted successfully.')
    return redirect('user:register')
