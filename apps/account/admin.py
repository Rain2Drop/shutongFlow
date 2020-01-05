from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import ShutongDept, ShutongUser, ShutongRole, ShutongUserRole


class ShutongDeptAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'leader')


class ShutongRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


class ShutongUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'alias', 'email', 'phone', 'dept', 'is_active', 'is_superuser')
    search_fields = ('username', 'alias', 'email', 'phone')
    list_filter = ('dept', 'is_active', 'is_superuser')
    ordering = ('-id',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('alias', 'email', 'phone', 'dept')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'alias', 'password1', 'password2', 'dept', 'phone', 'email'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["username"]
        else:
            return []


class ShutongUserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')


admin.site.register(ShutongDept, ShutongDeptAdmin)
admin.site.register(ShutongRole, ShutongRoleAdmin)
admin.site.register(ShutongUser, ShutongUserAdmin)
admin.site.register(ShutongUserRole, ShutongUserRoleAdmin)

admin.site.site_header = '用户管理'
admin.site.site_title = '用户管理'
