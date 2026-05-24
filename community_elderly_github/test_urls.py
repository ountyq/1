"""测试URL配置是否正确"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_elderly.settings')
django.setup()

from django.urls import resolve, Resolver404

test_urls = [
    '/admin/news/',
    '/admin/news/create/',
    '/admin/news/1/edit/',
    '/admin/news/1/delete/',
]

print('测试URL配置...')
for url in test_urls:
    try:
        resolver_match = resolve(url)
        print(f'✓ {url} -> {resolver_match.func.__name__} (name={resolver_match.url_name})')
    except Resolver404:
        print(f'✗ {url} -> 404 Not Found')

print('\n✅ URL配置测试完成')
