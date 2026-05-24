"""
更新现有数据：为新闻添加来源和封面，为公告添加封面
"""
import os
import sys
import django

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_elderly.settings')
django.setup()

from django.contrib.auth import get_user_model
from elderly_system.models import News, Announcement
from django.core.files import File

User = get_user_model()

def update_news():
    """为现有新闻添加来源和封面"""
    news_list = News.objects.all()
    
    # 定义来源和封面的映射
    news_updates = {
        '2026年养老金继续上调': {'source': '人力资源社会保障部', 'cover': 'media/news_covers/news_001.jpg'},
        '春季养生：老年人补钙': {'source': '健康养生网', 'cover': 'media/news_covers/news_002.jpg'},
        '社区老年人智能手机培训班': {'source': '社区服务中心', 'cover': 'media/news_covers/news_003.jpg'},
        '警惕！新型保健品诈骗': {'source': '社区派出所', 'cover': 'media/news_covers/news_004.jpg'},
        '社区65岁以上老人可免费接种': {'source': '社区卫生服务中心', 'cover': 'media/news_covers/news_005.jpg'},
        '社区老年大学2026年秋季班': {'source': '社区老年大学', 'cover': 'media/news_covers/news_006.jpg'},
        '全国两会：关注老龄化问题': {'source': '新华社', 'cover': 'media/news_covers/news_007.jpg'},
        '老年人防跌倒指南': {'source': '中国疾控中心', 'cover': 'media/news_covers/news_008.jpg'},
    }
    
    for news in news_list:
        for key, value in news_updates.items():
            if key in news.title:
                # 更新来源
                if not news.source or news.source == '社区发布':
                    news.source = value['source']
                
                # 更新封面
                if not news.cover:
                    try:
                        with open(value['cover'], 'rb') as f:
                            news.cover.save(os.path.basename(value['cover']), File(f))
                        print(f'✓ 已更新新闻封面: {news.title}')
                    except FileNotFoundError:
                        print(f'✗ 封面文件未找到: {value["cover"]}')
                
                news.save()
                print(f'✓ 已更新新闻: {news.title} (来源: {news.source})')
                break

def update_announcements():
    """为现有公告添加封面"""
    ann_list = Announcement.objects.all()
    
    # 定义封面的映射（根据实际公告标题）
    ann_updates = {
        '欢迎使用社区老年活动管理系统': 'media/announcement_covers/ann_004.jpg',
        '自来水管道维修': 'media/announcement_covers/ann_001.jpg',
        '社区体检活动': 'media/announcement_covers/ann_002.jpg',
        '时间银行': 'media/announcement_covers/ann_003.jpg',
        '电动车停放': 'media/announcement_covers/ann_005.jpg',
        '智能快递柜': 'media/announcement_covers/ann_006.jpg',
    }
    
    for ann in ann_list:
        for key, cover_path in ann_updates.items():
            if key in ann.title:
                # 更新封面
                if not ann.cover:
                    try:
                        with open(cover_path, 'rb') as f:
                            ann.cover.save(os.path.basename(cover_path), File(f))
                        print(f'✓ 已更新公告封面: {ann.title}')
                    except FileNotFoundError:
                        print(f'✗ 封面文件未找到: {cover_path}')
                
                ann.save()
                break

if __name__ == '__main__':
    print('开始更新数据...')
    update_news()
    print()
    update_announcements()
    print('\n✅ 数据更新完成！')
