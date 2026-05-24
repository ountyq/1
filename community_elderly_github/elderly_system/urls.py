from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path('', views.index, name='index'),

    # 认证
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # ========== 管理员端 ==========
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # 用户管理
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/users/<int:user_id>/toggle/', views.admin_user_toggle, name='admin_user_toggle'),

    # 活动管理
    path('admin/activities/', views.admin_activities, name='admin_activities'),
    path('admin/activities/create/', views.admin_activity_create, name='admin_activity_create'),
    path('admin/activities/<int:act_id>/edit/', views.admin_activity_edit, name='admin_activity_edit'),
    path('admin/activities/<int:act_id>/delete/', views.admin_activity_delete, name='admin_activity_delete'),
    path('admin/activities/<int:act_id>/export/', views.export_registrations, name='export_registrations'),

    # 报名管理
    path('admin/registrations/', views.admin_registrations, name='admin_registrations'),
    path('admin/registrations/<int:reg_id>/sign_in/', views.admin_sign_in, name='admin_sign_in'),

    # 公告管理
    path('admin/announcements/', views.admin_announcements, name='admin_announcements'),
    path('admin/announcements/create/', views.admin_announcement_create, name='admin_announcement_create'),
    path('admin/announcements/<int:ann_id>/delete/', views.admin_announcement_delete, name='admin_announcement_delete'),

    # 数据统计
    path('admin/statistics/', views.admin_statistics, name='admin_statistics'),
    path('admin/statistics/export/', views.admin_statistics_export, name='admin_statistics_export'),

    # 新闻管理
    path('admin/news/', views.admin_news, name='admin_news'),
    path('admin/news/create/', views.admin_news_create, name='admin_news_create'),
    path('admin/news/<int:news_id>/edit/', views.admin_news_edit, name='admin_news_edit'),
    path('admin/news/<int:news_id>/delete/', views.admin_news_delete, name='admin_news_delete'),

    # ========== 老年用户端 ==========
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/activities/', views.user_activities, name='user_activities'),
    path('user/activities/<int:act_id>/', views.user_activity_detail, name='user_activity_detail'),
    path('user/activities/<int:act_id>/register/', views.user_register_activity, name='user_register_activity'),
    path('user/activities/<int:act_id>/cancel/', views.user_cancel_registration, name='user_cancel_registration'),
    path('user/my_registrations/', views.user_my_registrations, name='user_my_registrations'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/announcements/', views.user_announcements, name='user_announcements'),

    # 用户端新闻
    path('user/news/', views.user_news, name='user_news'),
    path('user/news/<int:news_id>/', views.user_news_detail, name='user_news_detail'),
]
