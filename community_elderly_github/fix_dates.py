"""
修复新闻和公告的发布时间 - 使其更符合实际情况
"""
import os
import sys
import django
from datetime import datetime

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_elderly.settings')
django.setup()

from elderly_system.models import News, Announcement, Activity

def fix_news_dates():
    """修复新闻发布时间"""
    print('正在修复新闻发布时间...')
    
    news_dates = {
        '2026年养老金继续上调，涨幅约3.8%': datetime(2026, 3, 15),  # 两会后发布
        '春季养生：老年人补钙吃什么好？': datetime(2026, 3, 20),  # 春季开始前
        '社区老年人智能手机培训班开班啦！': datetime(2026, 3, 25),  # 春季开班
        '警惕！新型保健品诈骗手段曝光': datetime(2026, 4, 5),  # 防范诈骗宣传
        '社区65岁以上老人可免费接种流感疫苗': datetime(2026, 4, 10),  # 流感疫苗接种季
        '社区老年大学2026年秋季班招生简章': datetime(2026, 4, 15),  # 提前招生宣传
        '全国两会：关注老龄化问题，推进养老服务发展': datetime(2026, 3, 12),  # 两会期间
        '五一劳动节社区文艺汇演通知': datetime(2026, 4, 20),  # 节前通知
    }
    
    for title, pub_time in news_dates.items():
        try:
            news = News.objects.get(title=title)
            news.publish_time = pub_time
            news.save()
            print(f'  ✓ {title[:30]}... -> {pub_time.strftime("%Y-%m-%d")}')
        except News.DoesNotExist:
            print(f'  ✗ 未找到新闻: {title}')
    
    print('✓ 新闻发布时间修复完成！\n')

def fix_announcement_dates():
    """修复公告发布时间"""
    print('正在修复公告发布时间...')
    
    announcement_dates = {
        '重要通知：社区将进行自来水管道维修': datetime(2026, 5, 8),  # 停水前通知
        '社区体检活动开始报名': datetime(2026, 5, 5),  # 体检前通知
        '关于规范电动车停放和充电的公告': datetime(2026, 4, 1),  # 安全管理
        '社区"时间银行"互助养老项目启动': datetime(2026, 4, 15),  # 项目启动
        '社区智能快递柜投入使用': datetime(2026, 3, 1),  # 设施投入使用
    }
    
    for title, pub_time in announcement_dates.items():
        try:
            ann = Announcement.objects.get(title=title)
            ann.publish_time = pub_time
            ann.save()
            print(f'  ✓ {title[:30]}... -> {pub_time.strftime("%Y-%m-%d")}')
        except Announcement.DoesNotExist:
            print(f'  ✗ 未找到公告: {title}')
    
    print('✓ 公告发布时间修复完成！\n')

def fix_activity_dates():
    """修复活动开始时间"""
    print('正在修复活动开始时间...')
    
    activity_dates = {
        '社区春季健步走活动': {
            'start': datetime(2026, 5, 18, 7, 0),
            'end': datetime(2026, 5, 18, 10, 0),
            'deadline': datetime(2026, 5, 16, 18, 0),
        },
        '健康讲座：高血压的预防与调理': {
            'start': datetime(2026, 5, 22, 14, 30),
            'end': datetime(2026, 5, 22, 16, 0),
            'deadline': datetime(2026, 5, 20, 18, 0),
        },
        '书法交流活动：楷书基础入门': {
            'start': datetime(2026, 5, 25, 9, 0),
            'end': datetime(2026, 5, 25, 11, 0),
            'deadline': datetime(2026, 5, 23, 18, 0),
        },
        '社区棋牌友谊赛': {
            'start': datetime(2026, 5, 28, 13, 30),
            'end': datetime(2026, 5, 28, 17, 0),
            'deadline': datetime(2026, 5, 26, 18, 0),
        },
        '智能手机摄影技巧培训': {
            'start': datetime(2026, 6, 1, 9, 0),
            'end': datetime(2026, 6, 1, 11, 0),
            'deadline': datetime(2026, 5, 30, 18, 0),
        },
        '端午节包粽子活动': {
            'start': datetime(2026, 6, 5, 9, 0),
            'end': datetime(2026, 6, 5, 12, 0),
            'deadline': datetime(2026, 6, 3, 18, 0),
        },
        '关爱独居老人：上门慰问活动': {
            'start': datetime(2026, 6, 10, 9, 0),
            'end': datetime(2026, 6, 10, 12, 0),
            'deadline': datetime(2026, 6, 8, 18, 0),
        },
    }
    
    for title, dates in activity_dates.items():
        try:
            activity = Activity.objects.get(title=title)
            activity.start_time = dates['start']
            activity.end_time = dates['end']
            activity.register_deadline = dates['deadline']
            activity.save()
            print(f'  ✓ {title[:30]}... -> {dates["start"].strftime("%Y-%m-%d %H:%M")}')
        except Activity.DoesNotExist:
            print(f'  ✗ 未找到活动: {title}')
    
    print('✓ 活动开始时间修复完成！\n')

def main():
    """主函数"""
    print('='*60)
    print('修复新闻、公告和活动的发布时间')
    print('='*60)
    print()
    
    fix_news_dates()
    fix_announcement_dates()
    fix_activity_dates()
    
    print('='*60)
    print('✓ 所有时间修复完成！')
    print('='*60)
    print()
    print('现在新闻和公告的发布时间更加合理了：')
    print('  - 养老金上调新闻：3月15日（两会后）')
    print('  - 春季养生新闻：3月20日（春季前）')
    print('  - 五一活动通知：4月20日（节前通知）')
    print('  - 管道维修通知：5月8日（停水前2天）')
    print()

if __name__ == '__main__':
    main()
