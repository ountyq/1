"""
全面检查社区老年活动管理系统的所有问题
"""
import os
import sys
import django
from datetime import datetime

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_elderly.settings')
django.setup()

from django.test import TestCase, Client
from django.urls import reverse
from elderly_system.models import User, News, Announcement, Activity, Registration
from django.core.files.uploadedfile import SimpleUploadedFile

def check_data_integrity():
    """检查数据完整性"""
    print('='*60)
    print('1. 检查数据完整性')
    print('='*60)
    
    # 检查用户数据
    admin_count = User.objects.filter(role='admin').count()
    elderly_count = User.objects.filter(role='elder').count()
    print(f'✓ 管理员用户: {admin_count} 个')
    print(f'✓ 老年用户: {elderly_count} 个')
    
    # 检查新闻数据
    news_count = News.objects.count()
    news_with_html = News.objects.filter(content__contains='<').count()
    print(f'✓ 新闻总数: {news_count} 条')
    print(f'✓ 包含HTML的新闻: {news_with_html} 条')
    
    # 检查时间合理性
    now = datetime.now()
    future_activities = Activity.objects.filter(start_time__gt=now).count()
    past_activities = Activity.objects.filter(start_time__lt=now).count()
    print(f'✓ 未来活动: {future_activities} 个')
    print(f'✓ 过去活动: {past_activities} 个')
    
    # 检查公告数据
    ann_count = Announcement.objects.count()
    print(f'✓ 公告总数: {ann_count} 条')
    
    print()

def check_template_rendering():
    """检查模板渲染问题"""
    print('='*60)
    print('2. 检查模板渲染问题')
    print('='*60)
    
    # 检查是否有模板文件缺失
    import os
    template_dir = 'templates/user'
    required_templates = [
        'base.html',
        'home.html',
        'activities.html',
        'activity_detail.html',
        'news.html',
        'news_detail.html',
        'announcements.html',
        'profile.html',
        'my_registrations.html'
    ]
    
    for template in required_templates:
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f'✓ {template}')
        else:
            print(f'✗ 缺失: {template}')
    
    print()

def check_html_rendering():
    """检查HTML内容是否正确渲染"""
    print('='*60)
    print('3. 检查HTML内容渲染')
    print('='*60)
    
    # 检查新闻内容
    news_list = News.objects.all()[:5]
    for news in news_list:
        if '<' in news.content and '>' in news.content:
            print(f'✓ 新闻包含HTML: {news.title[:30]}...')
        else:
            print(f'  新闻无HTML: {news.title[:30]}...')
    
    # 检查公告内容
    ann_list = Announcement.objects.all()[:5]
    for ann in ann_list:
        if '<' in ann.content and '>' in ann.content:
            print(f'✓ 公告包含HTML: {ann.title[:30]}...')
        else:
            print(f'  公告无HTML: {ann.title[:30]}...')
    
    print()

def check_urls_accessible():
    """检查URL是否可访问"""
    print('='*60)
    print('4. 检查URL配置')
    print('='*60)
    
    client = Client()
    
    # 测试公开页面
    urls = [
        ('/user/activities/', '活动列表'),
        ('/user/news/', '新闻列表'),
        ('/user/announcements/', '公告列表'),
    ]
    
    for url, name in urls:
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f'✓ {name}: {url} (200 OK)')
            else:
                print(f'✗ {name}: {url} ({response.status_code})')
        except Exception as e:
            print(f'✗ {name}: {url} (错误: {str(e)[:50]})')
    
    print()

def check_date_reasonableness():
    """检查日期合理性"""
    print('='*60)
    print('5. 检查日期合理性')
    print('='*60)
    
    now = datetime.now()
    
    # 检查新闻发布时间
    news_list = News.objects.all()
    for news in news_list:
        if news.publish_time > now:
            print(f'⚠ 未来发布: {news.title[:30]}... ({news.publish_time})')
        else:
            days_ago = (now - news.publish_time).days
            print(f'✓ {news.title[:30]}... ({days_ago}天前)')
    
    print()
    
    # 检查活动开始时间
    activities = Activity.objects.all()
    for act in activities:
        if act.start_time < act.register_deadline:
            print(f'⚠ 报名时间晚于开始时间: {act.title[:30]}...')
        else:
            print(f'✓ {act.title[:30]}... (报名截止早于开始)')
    
    print()

def fix_common_issues():
    """修复常见问题"""
    print('='*60)
    print('6. 修复常见问题')
    print('='*60)
    
    # 修复：确保活动统计记录存在
    from elderly_system.models import ActivityStats
    activities_without_stats = Activity.objects.filter(stats__isnull=True)
    for act in activities_without_stats:
        ActivityStats.objects.create(activity=act)
        print(f'✓ 创建统计记录: {act.title[:30]}...')
    
    if not activities_without_stats.exists():
        print('✓ 所有活动都有统计记录')
    
    print()

def main():
    """主函数"""
    print()
    print('█'*60)
    print('  社区老年活动管理系统 - 全面检查')
    print('█'*60)
    print()
    
    check_data_integrity()
    check_template_rendering()
    check_html_rendering()
    check_ urls_accessible()
    check_date_reasonableness()
    fix_common_issues()
    
    print('█'*60)
    print('  检查完成！')
    print('█'*60)
    print()
    print('建议：')
    print('1. 启动开发服务器: python manage.py runserver')
    print('2. 访问 http://127.0.0.1:8000/user/activities/ 查看效果')
    print('3. 登录测试: admin / admin123456')
    print()

if __name__ == '__main__':
    main()
