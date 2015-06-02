# coding: utf-8
from django.contrib import admin

from .models import Startup, CompanyRole, StartupMembers


class StartupMembersInline(admin.TabularInline):
    model = StartupMembers
    extra = 0
    raw_id_fields = ("user",)


class StartupAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'get_members')
    readonly_fields = ('get_members',)
    list_filter = ('created',)
    inlines = [StartupMembersInline]

    def get_members(self, obj):
        members = [unicode(m) for m in obj.members.all()]
        return ', '.join(members)
    get_members.short_description = u'Участники'


class CompanyRoleAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Startup, StartupAdmin)
admin.site.register(CompanyRole, CompanyRoleAdmin)
admin.site.register(StartupMembers)