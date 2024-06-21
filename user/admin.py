from django.contrib import admin
from django.utils.safestring import mark_safe

from .views import User
from .models import Post

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username","is_premium")
    search_fields = ("username",)

    fieldsets = (
        (
            "GENERAL",
            {"fields": ("email", "password", "username" )},
        ),
        (
            "INFO",
            {
                "fields": (
                    "is_premium",
                    "is_active",
                    "is_superuser",


                )
            },
        ),
    )

from django.contrib import admin
from django.utils.html import format_html
from .models import Profile

from django.contrib import admin
from django.utils.html import format_html
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_premium", "get_image")
    search_fields = ("user__username",)
    readonly_fields = ("is_premium", "get_image")

    fieldsets = (
        ("GENERAL", {"fields": ("user", "description", "image")}),
        ("COUNTS", {"fields": ("followers", "post_counts", "story_counts")}),
    )

    def is_premium(self, obj):
        return obj.user.is_premium if obj.user else False

    is_premium.boolean = True

    def get_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        else:
            return 'No Image'

    get_image.short_description = 'Image Preview'




admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Post)