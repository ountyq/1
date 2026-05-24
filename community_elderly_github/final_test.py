"""完整功能测试"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_elderly.settings')
django.setup()

from django.test import Client
from elderly_system.models import News, Announcement

print('=' * 60)
print('开始完整功能测试...')
print('=' * 60)

client = Client()
logged_in = client.login(username='admin', password='admin123456')
print(f'\n1. 管理员登录: {"✓ 成功" if logged_in else "✗ 失败"}')

# 测试URL访问
test_cases = [
    ('新闻列表', '/admin/news/'),
    ('发布新闻', '/admin/news/create/'),
    ('编辑新闻1', '/admin/news/1/edit/'),
    ('编辑新闻2', '/admin/news/2/edit/'),
    ('用户端新闻列表', '/user/news/'),
    ('用户端新闻详情', '/user/news/1/'),
    ('公告列表', '/admin/announcements/'),
    ('公告列表(用户端)', '/user/announcements/'),
]

print('\n2. URL访问测试:')
for name, url in test_cases:
    response = client.get(url)
    status = '✓ 成功' if response.status_code == 200 else f'✗ 失败({response.status_code})'
    print(f'   {name}: {status}')

# 验证数据完整性
print('\n3. 数据完整性检查:')
print(f'   新闻总数: {News.objects.count()} 条')
print(f'   公告总数: {Announcement.objects.count()} 条')

# 检查新闻数据
print('\n   新闻数据检查:')
for news in News.objects.all()[:3]:
    has_source = '✓' if news.source else '✗'
    has_views = '✓' if news.views > 0 else '✗'
    has_cover = '✓' if news.cover else '✗'
    print(f'   {news.title[:20]}... | 来源:{has_source} 浏览:{has_views}({news.views}) 封面:{has_cover}')

# 检查公告数据
print('\n   公告数据检查:')
for ann in Announcement.objects.all()[:3]:
    has_cover = '✓' if ann.cover else '✗'
    print(f'   {ann.title[:20]}... | 封面:{has_cover}')

print('\n' + '=' * 60)
print('测试完成！')
print('=' * 60)
