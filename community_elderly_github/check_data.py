"""检查数据完整性"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_elderly.settings')
django.setup()

from elderly_system.models import News, Announcement

print("=" * 60)
print("新闻资讯检查")
print("=" * 60)
for n in News.objects.all():
    print(f"\n标题: {n.title}")
    print(f"  - 来源: {n.source}")
    print(f"  - 浏览量: {n.views}")
    print(f"  - 封面: {n.cover.url if n.cover else '无封面'}")

print("\n" + "=" * 60)
print("公告检查")
print("=" * 60)
for a in Announcement.objects.all():
    print(f"\n标题: {a.title}")
    print(f"  - 封面: {a.cover.url if a.cover else '无封面'}")

print("\n" + "=" * 60)
print("媒体文件检查")
print("=" * 60)
import os
media_root = 'media'
for root, dirs, files in os.walk(media_root):
    for file in files:
        filepath = os.path.join(root, file)
        print(f"✓ {filepath}")
