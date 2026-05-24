# 初始化脚本 - 创建管理员账号和测试数据
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_elderly.settings')
django.setup()

from elderly_system.models import User, Activity, Announcement, ActivityStats
from datetime import datetime, timedelta

print("=" * 50)
print("开始初始化数据...")
print("=" * 50)

# 创建管理员账号
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        password='admin123456',
        first_name='系统管理员',
        role='admin',
        email='admin@community.com'
    )
    print("✅ 创建管理员账号：admin / admin123456")
else:
    print("⚠️  管理员账号已存在")

# 创建测试老年用户
test_users = [
    {'username': 'sun_jianhua', 'first_name': '孙建华', 'phone': '13900010001', 'age': 68, 'area': '东城区'},
    {'username': 'zhou_yuzhen', 'first_name': '周玉珍', 'phone': '13900010002', 'age': 72, 'area': '西城区'},
    {'username': 'wu_fangping', 'first_name': '吴芳萍', 'phone': '13900010003', 'age': 65, 'area': '东城区'},
]
for u in test_users:
    if not User.objects.filter(username=u['username']).exists():
        User.objects.create_user(
            username=u['username'],
            password='123456',
            first_name=u['first_name'],
            phone=u['phone'],
            age=u['age'],
            area=u['area'],
            role='elder'
        )
        print(f"✅ 创建测试用户：{u['username']} / 123456 ({u['first_name']})")

# 创建示例活动
admin_user = User.objects.get(username='admin')
now = datetime.now()

activities_data = [
    {
        'title': '社区广场舞比赛',
        'activity_type': 'sports',
        'description': '欢迎广大老年朋友参加本次广场舞比赛！比赛分健身舞、民族舞等组别，不限年龄，报名有礼。',
        'location': '社区活动广场',
        'start_time': now + timedelta(days=3, hours=9),
        'end_time': now + timedelta(days=3, hours=11),
        'register_deadline': now + timedelta(days=2),
        'max_participants': 50,
        'target_group': '60-80岁老年人',
        'status': 'open',
    },
    {
        'title': '老年健康知识讲座',
        'activity_type': 'health',
        'description': '邀请社区医院专家主讲高血压、糖尿病日常管理知识，现场免费测量血压血糖。',
        'location': '社区服务中心三楼会议室',
        'start_time': now + timedelta(days=5, hours=14),
        'end_time': now + timedelta(days=5, hours=16),
        'register_deadline': now + timedelta(days=4),
        'max_participants': 80,
        'target_group': '全体老年居民',
        'status': 'open',
    },
    {
        'title': '手工编织兴趣班',
        'activity_type': 'culture',
        'description': '学习中国传统手工编织技艺，制作精美手工品，材料费用由社区承担。',
        'location': '老年活动室',
        'start_time': now + timedelta(days=7, hours=10),
        'end_time': now + timedelta(days=7, hours=12),
        'register_deadline': now + timedelta(days=6),
        'max_participants': 20,
        'target_group': '有兴趣的老年朋友',
        'status': 'open',
    },
]

for ad in activities_data:
    if not Activity.objects.filter(title=ad['title']).exists():
        act = Activity.objects.create(**ad, creator=admin_user)
        ActivityStats.objects.create(activity=act)
        print(f"✅ 创建活动：{ad['title']}")

# 创建示例公告
if not Announcement.objects.exists():
    Announcement.objects.create(
        title='欢迎使用社区老年活动管理系统！',
        content='亲爱的社区居民朋友们，社区老年活动管理系统正式上线啦！\n\n您可以在这里查看各类社区活动信息、在线报名参与，活动当天出示二维码签到。\n\n如有任何问题请联系社区工作人员。',
        ann_type='notice',
        is_top=True,
        publisher=admin_user,
    )
    print("✅ 创建示例公告")

print("\n" + "=" * 50)
print("🎉 数据初始化完成！")
print("\n账号信息：")
print("  管理员：admin / admin123456")
print("  测试用户1：user1 / 123456 (张大爷)")
print("  测试用户2：user2 / 123456 (李奶奶)")
print("  测试用户3：user3 / 123456 (王大妈)")
print("=" * 50)
