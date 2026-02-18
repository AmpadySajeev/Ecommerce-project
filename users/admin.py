from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):

     add_form = CustomUserCreationForm
     form = CustomUserChangeForm
     model = CustomUser
     list_display = ['email', 'name','is_staff', 'is_active',]
     list_filter = ('is_active', 'is_staff',)
     ordering = ('email',)

     fieldsets = (
          (None, {'fields' : ('email','name','password')}),
          ('Permissions', {'fields' : ('is_staff', 'is_active')}),
     )

     add_fieldsets = (
          (None, {
               'classes' : ('wide',),
               'fields' : ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')
          }),
     )
     search_fields = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
