from django.contrib import admin
from .models import Member, MemberRelationship

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_sponsor_name')
    list_filter = ('sponsor',)
    search_fields = ('user__username', 'user__email')

    def get_sponsor_name(self, obj):
        return obj.sponsor.user.username if obj.sponsor else None

    get_sponsor_name.short_description = 'Sponsor'

@admin.register(MemberRelationship)
class MemberRelationshipAdmin(admin.ModelAdmin):
    list_display = ('get_parent_name', 'get_child_name')

    def get_parent_name(self, obj):
        return obj.parent.user.username

    def get_child_name(self, obj):
        return obj.child.user.username

    get_parent_name.short_description = 'Parent'
    get_child_name.short_description = 'Child'

    list_filter = ('parent',)