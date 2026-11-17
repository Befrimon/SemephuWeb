from django import forms
from django.contrib import admin
from .models import Course, CoursePoint, Map, Punch, Result, User


class CoursePointInline(admin.TabularInline):
    model = CoursePoint
    extra = 0


class UserAdminForm(forms.ModelForm):
    new_password = forms.CharField(label='Пароль', required=False, widget=forms.PasswordInput,
                                   help_text='При редактировании оставьте пустым, чтобы не менять.')
    class Meta:
        model = User
        fields = ('user_name', 'push_hash', 'is_active', 'is_staff', 'is_superuser')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    fields = ('user_name', 'new_password', 'push_hash', 'is_active', 'is_staff', 'is_superuser')
    list_display = ('user_name', 'is_active', 'is_staff')
    search_fields = ('user_name',)

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('new_password')
        if password:
            obj.set_password(password)  # в БД попадает только хеш
        elif not change:
            obj.set_unusable_password()
        super().save_model(request, obj, form, change)


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'author', 'date_added')
    search_fields = ('name', 'location', 'author')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'map', 'public', 'creator')
    list_filter = ('public', 'category')
    inlines = [CoursePointInline]


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'time', 'place', 'public')
    list_filter = ('public',)


admin.site.register(Punch)
