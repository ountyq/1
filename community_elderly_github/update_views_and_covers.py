"""更新浏览量和封面，确保数据完整"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_elderly.settings')
django.setup()

from elderly_system.models import News, Announcement
from django.core.files import File

# 更新新闻浏览量 - 设置更真实的浏览量数据
news_views = {
    '2026年养老金继续上调': 1258,
    '春季养生：老年人补钙吃什么好？': 892,
    '社区老年人智能手机培训班开班啦！': 756,
    '警惕！新型保健品诈骗手段曝光': 1034,
    '社区65岁以上老人可免费接种流感疫苗': 645,
    '社区老年大学2026年秋季班招生简章': 523,
    '全国两会：关注老龄化问题，推进养老服务发展': 1876,
    '五一劳动节社区文艺汇演通知': 432,
}

print("正在更新新闻浏览量...")
for news in News.objects.all():
    for key, views in news_views.items():
        if key in news.title:
            news.views = views
            news.save()
            print(f"✓ {news.title[:30]}... 浏览量更新为: {views}")
            break

# 为没有封面的新闻添加封面
print("\n正在检查并更新新闻封面...")
for news in News.objects.all():
    if not news.cover:
        # 根据分类选择封面
        category_covers = {
            'policy': 'media/news_covers/news_001.jpg',
            'health': 'media/news_covers/news_002.jpg',
            'activity': 'media/news_covers/news_003.jpg',
            'notice': 'media/news_covers/news_004.jpg',
            'other': 'media/news_covers/news_005.jpg',
        }
        cover_path = category_covers.get(news.category, 'media/news_covers/news_001.jpg')
        try:
            with open(cover_path, 'rb') as f:
                news.cover.save(os.path.basename(cover_path), File(f))
            print(f"✓ 为新闻添加封面: {news.title[:30]}...")
        except FileNotFoundError:
            print(f"✗ 封面文件未找到: {cover_path}")

# 确保所有公告都有封面
print("\n正在检查并更新公告封面...")
for ann in Announcement.objects.all():
    if not ann.cover:
        ann_type_covers = {
            'notice': 'media/announcement_covers/ann_001.jpg',
            'activity': 'media/announcement_covers/ann_002.jpg',
            'system': 'media/announcement_covers/ann_004.jpg',
        }
        cover_path = ann_type_covers.get(ann.ann_type, 'media/announcement_covers/ann_001.jpg')
        try:
            with open(cover_path, 'rb') as f:
                ann.cover.save(os.path.basename(cover_path), File(f))
            print(f"✓ 为公告添加封面: {ann.title[:30]}...")
        except FileNotFoundError:
            print(f"✗ 封面文件未找到: {cover_path}")

print("\n✅ 数据更新完成！")
