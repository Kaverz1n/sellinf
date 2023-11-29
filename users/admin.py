from django.contrib import admin

from users.models import User, ConfirmationCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone', 'nickname', 'is_upgraded',)
    list_filter = ('is_upgraded',)
    search_fields = ('phone', 'nickname',)


@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'display_user_phone', 'code',)

    def display_user_phone(self, obj):
        return obj.user.phone
