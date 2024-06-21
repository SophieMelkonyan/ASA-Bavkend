from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Special_Post

User = get_user_model()


class EmailForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea())


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords should be identical.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150)

    class Meta:
        model = Profile
        fields = ['description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username

        self.fields['image'].widget.attrs.update({'class': 'custom-file-input'})

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']

        if commit:
            user.save()
            profile.save()
        return profile


from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'What event you have'})
        self.fields['description'].widget.attrs.update({'placeholder': 'You can describe it here'})



class Special_Form(forms.ModelForm):
    class Meta:
        model = Special_Post
        fields = ['title', 'image']

    def __init__(self, *args, **kwargs):
        super(Special_Form, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'placeholder': '#happy'})



