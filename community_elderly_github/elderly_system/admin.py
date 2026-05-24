from django.contrib import admin
from .models import User, Activity, Registration, Announcement, ActivityStats, News


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'role', 'phone', 'area', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    search_fields = ['username', 'first_name', 'phone']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'activity_type', 'status', 'start_time', 'current_participants', 'max_participants']
    list_filter = ['status', 'activity_type']
    search_fields = ['title']


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'status', 'register_time', 'sign_in_time']
    list_filter = ['status']


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'ann_type', 'is_top', 'publish_time']


@admin.register(ActivityStats)
class ActivityStatsAdmin(admin.ModelAdmin):
    list_display = ['activity', 'total_registered', 'total_signed_in', 'sign_in_rate']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'source', 'is_top', 'views', 'publish_time']
    list_filter = ['category', 'is_top']
    search_fields = ['title', 'content', 'source']
    list_editable = ['is_top', 'views']
    fields = ['title', 'category', 'source', 'content', 'cover', 'is_top', 'views']
    list_per_page = 20
