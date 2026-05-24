"""
为社区老年活动管理系统添加真实数据
包含：新闻、公告、活动等老年人感兴趣的内容
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'community_elderly.settings')
django.setup()

from django.contrib.auth import get_user_model
from elderly_system.models import News, Announcement, Activity, User

User = get_user_model()

def create_admin_user():
    """创建管理员用户"""
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@community.com',
            password='admin123456',
            role='admin',
            phone='13800138000'
        )
        print(f'✓ 创建管理员用户: {admin.username}')
        return admin
    else:
        admin = User.objects.get(username='admin')
        print(f'✓ 管理员用户已存在: {admin.username}')
        return admin

def create_elderly_users():
    """创建老年用户"""
    elderly_data = [
        {'username': 'zhang_hua', 'name': '张华', 'age': 68, 'phone': '13810001001'},
        {'username': 'li_ming', 'name': '李明', 'age': 72, 'phone': '13810001002'},
        {'username': 'wang_fang', 'name': '王芳', 'age': 65, 'phone': '13810001003'},
        {'username': 'zhao_jun', 'name': '赵军', 'age': 70, 'phone': '13810001004'},
        {'username': 'liu_yun', 'name': '刘云', 'age': 66, 'phone': '13810001005'},
    ]
    
    created_users = []
    for data in elderly_data:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                password='123456',
                first_name=data['name'],
                role='elder',
                age=data['age'],
                phone=data['phone'],
                area='阳光社区'
            )
            created_users.append(user)
            print(f'✓ 创建老年用户: {user.get_full_name()}')
        else:
            user = User.objects.get(username=data['username'])
            created_users.append(user)
            print(f'✓ 老年用户已存在: {user.get_full_name()}')
    
    return created_users

def add_news(admin):
    """添加新闻资讯 - 老年人关心的话题"""
    news_data = [
        {
            'title': '2026年养老金继续上调，涨幅约3.8%',
            'category': 'policy',
            'content': '''
            <p>根据人力资源社会保障部最新通知，2026年退休人员基本养老金将继续上调，
            预计涨幅约为3.8%。这是养老金连续第22年上涨。</p>
            <p><strong>调整范围：</strong>2025年12月31日前已按规定办理退休手续并按月领取基本养老金的退休人员。</p>
            <p><strong>调整办法：</strong>继续采取定额调整、挂钩调整与适当倾斜相结合的办法。</p>
            <p>此次调整将惠及全国约1.3亿退休人员，充分体现了党中央、国务院对广大退休人员的关怀。</p>
            ''',
            'is_top': True
        },
        {
            'title': '春季养生：老年人补钙吃什么好？',
            'category': 'health',
            'content': '''
            <p>春季是补钙的黄金时期。对于老年人来说，钙质流失加快，更需要注意补充。</p>
            <p><strong>推荐食物：</strong></p>
            <ul>
                <li><strong>牛奶和奶制品：</strong>每天300ml牛奶，是最好的钙源</li>
                <li><strong>豆制品：</strong>豆腐、豆浆、腐竹等</li>
                <li><strong>深绿色蔬菜：</strong>西兰花、油菜、小白菜</li>
                <li><strong>坚果类：</strong>芝麻、核桃、杏仁</li>
                <li><strong>海产品：</strong>虾皮、小鱼干、海带</li>
            </ul>
            <p><strong>温馨提示：</strong>补钙的同时要补充维生素D，多晒太阳，促进钙的吸收。</p>
            ''',
            'is_top': False
        },
        {
            'title': '社区老年人智能手机培训班开班啦！',
            'category': 'activity',
            'content': '''
            <p>为了让社区老年人更好地融入智能时代，享受科技带来的便利，社区服务中心特举办"智能手机使用培训班"。</p>
            <p><strong>培训内容：</strong></p>
            <ul>
                <li>微信的基本使用（发消息、打视频电话）</li>
                <li>支付宝的使用（付钱、缴水电费）</li>
                <li>手机拍照和视频通话</li>
                <li>防疫健康码的使用</li>
                <li>防范电信诈骗</li>
            </ul>
            <p><strong>培训时间：</strong>每周三、周五上午9:00-11:00</p>
            <p><strong>培训地点：</strong>社区活动中心二楼会议室</p>
            <p><strong>报名方式：</strong>到社区服务中心现场报名，或拨打热线电话：010-12345678</p>
            <p>名额有限，报满即止！欢迎各位老年朋友积极参加！</p>
            ''',
            'is_top': True
        },
        {
            'title': '警惕！新型保健品诈骗手段曝光',
            'category': 'notice',
            'content': '''
            <p>近期，社区接到多起老年人被骗案件，骗子以"免费体检"、"专家讲座"为名，
            实则推销高价保健品。特此提醒广大老年朋友：</p>
            <p><strong>常见诈骗手段：</strong></p>
            <ul>
                <li>冒充专家、医生举办"健康讲座"</li>
                <li>以"免费体检"为名，夸大病情</li>
                <li>承诺"包治百病"，高价推销保健品</li>
                <li>组织"免费旅游"，实则推销产品</li>
            </ul>
            <p><strong>防范建议：</strong></p>
            <ul>
                <li>身体不适要及时去正规医院就诊</li>
                <li>不要轻信"包治百病"的保健品</li>
                <li>购买药品和保健品要去正规药店</li>
                <li>遇到可疑情况及时与子女沟通或报警</li>
            </ul>
            <p><strong>报警电话：110</strong></p>
            ''',
            'is_top': False
        },
        {
            'title': '社区65岁以上老人可免费接种流感疫苗',
            'category': 'health',
            'content': '''
            <p>为关爱老年人健康，社区卫生服务中心启动2026年秋季流感疫苗接种工作。
            65岁以上老年人可免费接种流感疫苗。</p>
            <p><strong>接种对象：</strong>65岁及以上老年人（1961年12月31日前出生）</p>
            <p><strong>接种时间：</strong>2026年5月10日-6月30日，每周一至周五上午8:00-11:00</p>
            <p><strong>接种地点：</strong>社区卫生服务中心预防接种门诊（社区医院二楼）</p>
            <p><strong>携带证件：</strong>本人身份证或户口本</p>
            <p><strong>注意事项：</strong></p>
            <ul>
                <li>发热、急性疾病期暂缓接种</li>
                <li>对鸡蛋或疫苗成分过敏者不宜接种</li>
                <li>接种后留观30分钟</li>
            </ul>
            <p>欢迎各位老年朋友按时接种，保护身体健康！</p>
            ''',
            'is_top': False
        },
        {
            'title': '社区老年大学2026年秋季班招生简章',
            'category': 'activity',
            'content': '''
            <p>社区老年大学2026年秋季班开始招生啦！本学期开设以下课程：</p>
            <p><strong>课程安排：</strong></p>
            <ul>
                <li><strong>书法班：</strong>周一、周三上午9:00-11:00，学费200元/学期</li>
                <li><strong>绘画班：</strong>周二、周四上午9:00-11:00，学费200元/学期</li>
                <li><strong>太极拳班：</strong>每天早晨7:00-8:00（户外），学费150元/学期</li>
                <li><strong>合唱班：</strong>周三下午2:00-4:00，学费100元/学期</li>
                <li><strong>智能手机班：</strong>周五上午9:00-11:00，免费</li>
                <li><strong>健康养生班：</strong>周四下午2:00-4:00，免费</li>
            </ul>
            <p><strong>报名时间：</strong>5月15日-5月30日</p>
            <p><strong>报名地点：</strong>社区活动中心一楼服务台</p>
            <p><strong>咨询电话：</strong>010-87654321</p>
            <p>欢迎各位老年朋友报名参加，丰富晚年生活！</p>
            ''',
            'is_top': False
        },
        {
            'title': '全国两会：关注老龄化问题，推进养老服务发展',
            'category': 'policy',
            'content': '''
            <p>在2026年全国两会上，老龄化问题成为热议话题。政府工作报告提出，
            要加快推进养老服务体系建设，让老年人安享幸福晚年。</p>
            <p><strong>重点措施：</strong></p>
            <ul>
                <li>发展居家养老服务，推进适老化改造</li>
                <li>加强社区养老服务设施建设</li>
                <li>推广"时间银行"互助养老模式</li>
                <li>加强老年人健康管理，完善长期护理保险制度</li>
                <li>推进智慧养老，运用科技手段提升养老服务水平</li>
            </ul>
            <p>这些政策的出台，将让广大老年人享受到更好的养老服务，提升生活品质。</p>
            ''',
            'is_top': False
        },
        {
            'title': '五一劳动节社区文艺汇演通知',
            'category': 'notice',
            'content': '''
            <p>为庆祝五一劳动节，展现社区老年人风采，社区将举办"欢度五一"文艺汇演活动。</p>
            <p><strong>活动时间：</strong>2026年5月1日上午9:00-11:30</p>
            <p><strong>活动地点：</strong>社区广场</p>
            <p><strong>节目安排：</strong></p>
            <ul>
                <li>太极拳表演（社区太极拳队）</li>
                <li>大合唱《我和我的祖国》（社区合唱团）</li>
                <li>广场舞表演（夕阳红舞蹈队）</li>
                <li>书法展示（社区书法班）</li>
                <li>戏曲选段（社区戏曲爱好者）</li>
            </ul>
            <p>欢迎社区居民踊跃参加，共同庆祝五一劳动节！</p>
            <p>如有才艺展示的老年朋友，请于4月25日前到社区服务中心报名。</p>
            ''',
            'is_top': False
        }
    ]
    
    created_count = 0
    for data in news_data:
        if not News.objects.filter(title=data['title']).exists():
            news = News.objects.create(
                title=data['title'],
                content=data['content'],
                category=data['category'],
                author=admin,
                is_top=data['is_top'],
                publish_time=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            created_count += 1
            print(f'  ✓ 添加新闻: {news.title[:40]}...')
    
    print(f'✓ 共添加 {created_count} 条新闻')

def add_announcements(admin):
    """添加公告通知"""
    announcement_data = [
        {
            'title': '重要通知：社区将进行自来水管道维修',
            'ann_type': 'notice',
            'content': '''
            <p><strong>停水通知</strong></p>
            <p>因社区自来水管道维修需要，将对以下区域暂停供水：</p>
            <p><strong>停水区域：</strong>1号楼、2号楼、3号楼、5号楼</p>
            <p><strong>停水时间：</strong>2026年5月15日（周四）上午8:00至下午18:00</p>
            <p><strong>温馨提示：</strong></p>
            <ul>
                <li>请提前储备必要的生活用水</li>
                <li>停水期间请关闭家中水龙头，以免造成恢复供水时漏水</li>
                <li>恢复供水后，初期水质可能浑浊，请先放一段时间再使用</li>
            </ul>
            <p>由此给您带来的不便，敬请谅解！</p>
            <p>咨询电话：010-12345678</p>
            ''',
            'is_top': True
        },
        {
            'title': '社区体检活动开始报名',
            'ann_type': 'activity',
            'content': '''
            <p>为关爱社区老年人身体健康，社区联合社区卫生服务中心开展免费健康体检活动。</p>
            <p><strong>体检对象：</strong>65岁及以上社区老年人</p>
            <p><strong>体检项目：</strong></p>
            <ul>
                <li>一般检查：身高、体重、血压、心率</li>
                <li>血常规、尿常规</li>
                <li>肝功能、肾功能、血脂</li>
                <li>心电图</li>
                <li>腹部B超</li>
            </ul>
            <p><strong>体检时间：</strong>2026年5月20日-5月25日，每天上午7:30-11:00</p>
            <p><strong>体检地点：</strong>社区医院（社区服务中心东侧）</p>
            <p><strong>注意事项：</strong></p>
            <ul>
                <li>体检前一日清淡饮食，晚8点后禁食</li>
                <li>体检当日早晨空腹（不吃饭、不喝水）</li>
                <li>携带本人身份证</li>
                <li>穿宽松衣物，方便检查</li>
            </ul>
            <p><strong>报名方式：</strong>即日起至5月18日，到社区服务中心现场报名，或拨打热线：010-12345678</p>
            <p>名额有限，请尽快报名！</p>
            ''',
            'is_top': True
        },
        {
            'title': '关于规范电动车停放和充电的公告',
            'ann_type': 'notice',
            'content': '''
            <p>为消除消防安全隐患,保障社区居民生命财产安全,根据《消防法》和《物业管理条例》,
            社区将规范电动车停放和充电管理。</p>
            <p><strong>管理规定：</strong></p>
            <ul>
                <li>严禁在楼道、安全出口、疏散通道停放电动车</li>
                <li>严禁私拉乱接电线为电动车充电</li>
                <li>电动车必须停放在指定区域（车棚）</li>
                <li>充电须在集中充电区域进行</li>
            </ul>
            <p><strong>集中充电区域：</strong></p>
            <ul>
                <li>1号楼北侧车棚</li>
                <li>5号楼南侧车棚</li>
                <li>社区东门车棚</li>
            </ul>
            <p><strong>充电费用：</strong>0.5元/小时，扫码支付</p>
            <p>请大家自觉遵守，共同维护社区安全！</p>
            ''',
            'is_top': False
        },
        {
            'title': '社区"时间银行"互助养老项目启动',
            'ann_type': 'notice',
            'content': '''
            <p>为弘扬尊老敬老传统美德，社区推出"时间银行"互助养老项目。</p>
            <p><strong>什么是"时间银行"？</strong></p>
            <p>低龄老年人为高龄老年人提供志愿服务，服务时间存入"时间银行"，
            等自己年老需要帮助时，可以提取时间，享受同等时长的志愿服务。</p>
            <p><strong>服务内容：</strong></p>
            <ul>
                <li>陪伴聊天、读书读报</li>
                <li>代买菜、代缴费用</li>
                <li>陪同就医</li>
                <li>教用智能手机</li>
                <li>家务协助</li>
            </ul>
            <p><strong>报名条件：</strong>60-70岁身体健康、有奉献精神的老年人</p>
            <p><strong>报名方式：</strong>到社区服务中心填表报名</p>
            <p>让我们携手共建互助友爱的和谐社区！</p>
            ''',
            'is_top': False
        },
        {
            'title': '社区智能快递柜投入使用',
            'ann_type': 'system',
            'content': '''
            <p>为方便社区居民收取快递，社区在以下位置安装了智能快递柜：</p>
            <p><strong>快递柜位置：</strong></p>
            <ul>
                <li>社区东门入口处</li>
                <li>1号楼和2号楼之间</li>
                <li>5号楼北侧</li>
            </ul>
            <p><strong>使用方法：</strong></p>
            <ol>
                <li>收到取件短信后，到相应快递柜</li>
                <li>在屏幕上输入取件码，或扫描短信中的二维码</li>
                <li>柜门自动打开，取出快递</li>
                <li>关闭柜门即可</li>
            </ol>
            <p><strong>温馨提示：</strong></p>
            <ul>
                <li>快递免费存放24小时</li>
                <li>超过24小时，每小时收费0.5元</li>
                <li>如有问题，请拨打客服电话：400-123-4567</li>
            </ul>
            <p>如有使用困难，可到社区服务中心寻求帮助，志愿者将耐心指导。</p>
            ''',
            'is_top': False
        }
    ]
    
    created_count = 0
    for data in announcement_data:
        if not Announcement.objects.filter(title=data['title']).exists():
            announcement = Announcement.objects.create(
                title=data['title'],
                content=data['content'],
                ann_type=data['ann_type'],
                publisher=admin,
                is_top=data['is_top'],
                publish_time=datetime.now() - timedelta(days=random.randint(1, 20))
            )
            created_count += 1
            print(f'  ✓ 添加公告: {announcement.title[:40]}...')
    
    print(f'✓ 共添加 {created_count} 条公告')

def add_activities(admin):
    """添加活动 - 老年人感兴趣的活动"""
    activity_data = [
        {
            'title': '社区春季健步走活动',
            'activity_type': 'sports',
            'description': '''
            <p>为倡导健康生活方式，增强老年人体质，社区举办春季健步走活动。</p>
            <p><strong>活动路线：</strong>社区广场 → 社区公园 → 湖边步道 → 返回社区广场（全程约3公里）</p>
            <p><strong>集合时间：</strong>2026年5月18日（周六）上午7:00</p>
            <p><strong>集合地点：</strong>社区广场</p>
            <p><strong>活动福利：</strong></p>
            <ul>
                <li>免费提供矿泉水、毛巾</li>
                <li>完成全程者获得纪念品一份</li>
                <li>现场测量血压、心率</li>
            </ul>
            <p><strong>注意事项：</strong></p>
            <ul>
                <li>穿着运动鞋、运动服</li>
                <li>有心脑血管疾病者请谨慎参加</li>
                <li>如遇雨天，活动顺延</li>
            </ul>
            <p>欢迎各位老年朋友踊跃参加，走出健康，走出快乐！</p>
            ''',
            'location': '社区广场及附近公园',
            'start_time': datetime.now() + timedelta(days=8, hours=7),
            'end_time': datetime.now() + timedelta(days=8, hours=10),
            'register_deadline': datetime.now() + timedelta(days=6),
            'max_participants': 100,
            'status': 'open',
            'target_group': '社区老年人，年龄60岁以上'
        },
        {
            'title': '健康讲座：高血压的预防与调理',
            'activity_type': 'health',
            'description': '''
            <p>为帮助社区老年人科学防治高血压，社区邀请社区卫生服务中心张医生开展健康讲座。</p>
            <p><strong>讲座内容：</strong></p>
            <ul>
                <li>高血压的标准和分类</li>
                <li>高血压的危害</li>
                <li>合理饮食：低盐、低脂、高钾</li>
                <li>适量运动：散步、太极拳</li>
                <li>规范用药：按时服药，不随意停药</li>
                <li>定期测量血压的重要性</li>
            </ul>
            <p><strong>讲座时间：</strong>2026年5月22日（周三）下午2:30-4:00</p>
            <p><strong>讲座地点：</strong>社区活动中心二楼会议室</p>
            <p><strong>主讲人：</strong>张医生（社区卫生服务中心）</p>
            <p><strong>福利：</strong>现场免费测量血压，赠送限盐勺、健康手册</p>
            <p>欢迎各位老年朋友积极参加！</p>
            ''',
            'location': '社区活动中心二楼会议室',
            'start_time': datetime.now() + timedelta(days=12, hours=14, minutes=30),
            'end_time': datetime.now() + timedelta(days=12, hours=16),
            'register_deadline': datetime.now() + timedelta(days=10),
            'max_participants': 80,
            'status': 'open',
            'target_group': '社区老年人，尤其适合高血压患者'
        },
        {
            'title': '书法交流活动：楷书基础入门',
            'activity_type': 'culture',
            'description': '''
            <p>为传承中华优秀传统文化，丰富老年人精神文化生活，社区举办书法交流活动。</p>
            <p><strong>活动内容：</strong></p>
            <ul>
                <li>书法基础知识讲解</li>
                <li>楷书基本笔画练习</li>
                <li>现场示范和一对一指导</li>
                <li>作品交流和点评</li>
            </ul>
            <p><strong>活动时间：</strong>2026年5月25日（周六）上午9:00-11:00</p>
            <p><strong>活动地点：</strong>社区活动中心书画室</p>
            <p><strong>授课老师：</strong>王老（社区书法爱好者，退休教师）</p>
            <p><strong>温馨提示：</strong></p>
            <ul>
                <li>社区提供毛笔、墨汁、宣纸</li>
                <li>也可以自带书法用具</li>
                <li>零基础也可以参加</li>
            </ul>
            <p>欢迎喜欢书法的老年朋友踊跃参加！</p>
            ''',
            'location': '社区活动中心书画室',
            'start_time': datetime.now() + timedelta(days=15, hours=9),
            'end_time': datetime.now() + timedelta(days=15, hours=11),
            'register_deadline': datetime.now() + timedelta(days=13),
            'max_participants': 30,
            'status': 'open',
            'target_group': '社区老年人，书法爱好者'
        },
        {
            'title': '社区棋牌友谊赛',
            'activity_type': 'social',
            'description': '''
            <p>为增进社区老年人之间的友谊，丰富业余生活，社区举办棋牌友谊赛。</p>
            <p><strong>比赛项目：</strong></p>
            <ul>
                <li>中国象棋</li>
                <li>围棋</li>
                <li>扑克牌（升级、斗地主）</li>
                <li>麻将（友谊赛，不计输赢）</li>
            </ul>
            <p><strong>活动时间：</strong>2026年5月28日（周二）下午1:30-5:00</p>
            <p><strong>活动地点：</strong>社区活动中心一楼多功能厅</p>
            <p><strong>比赛规则：</strong></p>
            <ul>
                <li>采用淘汰赛制</li>
                <li>友谊第一，比赛第二</li>
                <li>裁判由社区志愿者担任</li>
            </ul>
            <p><strong>奖项设置：</strong></p>
            <ul>
                <li>各项目前三名获得奖品</li>
                <li>所有参与者获得纪念品</li>
            </ul>
            <p>欢迎各位老年朋友踊跃报名参加！</p>
            ''',
            'location': '社区活动中心一楼多功能厅',
            'start_time': datetime.now() + timedelta(days=18, hours=13, minutes=30),
            'end_time': datetime.now() + timedelta(days=18, hours=17),
            'register_deadline': datetime.now() + timedelta(days=16),
            'max_participants': 60,
            'status': 'open',
            'target_group': '社区老年人，棋牌爱好者'
        },
        {
            'title': '智能手机摄影技巧培训',
            'activity_type': 'learning',
            'description': '''
            <p>为帮助社区老年人掌握智能手机摄影技巧，记录美好生活，社区举办摄影技巧培训。</p>
            <p><strong>培训内容：</strong></p>
            <ul>
                <li>手机摄影基础设置</li>
                <li>构图技巧：三分法、对称、引导线</li>
                <li>光线运用：顺光、逆光、侧光</li>
                <li>拍摄模式：人像、风景、微距、夜景</li>
                <li>简单修图：裁剪、调色、滤镜</li>
            </ul>
            <p><strong>培训时间：</strong>2026年6月1日（周六）上午9:00-11:00</p>
            <p><strong>培训地点：</strong>社区活动中心二楼电脑室</p>
            <p><strong>授课老师：</strong>小李（社区志愿者，专业摄影师）</p>
            <p><strong>温馨提示：</strong></p>
            <ul>
                <li>请携带智能手机</li>
                <li>社区提供少量备用手机</li>
                <li>手把手教学，包教包会</li>
            </ul>
            <p>欢迎各位老年朋友积极参加，用镜头记录美好生活！</p>
            ''',
            'location': '社区活动中心二楼电脑室',
            'start_time': datetime.now() + timedelta(days=22, hours=9),
            'end_time': datetime.now() + timedelta(days=22, hours=11),
            'register_deadline': datetime.now() + timedelta(days=20),
            'max_participants': 40,
            'status': 'open',
            'target_group': '社区老年人，智能手机用户'
        },
        {
            'title': '端午节包粽子活动',
            'activity_type': 'culture',
            'description': '''
            <p>为弘扬传统文化，增进邻里感情，社区举办端午节包粽子活动。</p>
            <p><strong>活动内容：</strong></p>
            <ul>
                <li>讲解端午节来历和习俗</li>
                <li>现场教学包粽子（蜜枣粽、肉粽）</li>
                <li>煮粽子、品尝自己的劳动成果</li>
                <li>制作香囊、五彩绳</li>
            </ul>
            <p><strong>活动时间：</strong>2026年6月5日（周三）上午9:00-12:00</p>
            <p><strong>活动地点：</strong>社区活动中心一楼厨房</p>
            <p><strong>温馨提示：</strong></p>
            <ul>
                <li>社区提供粽叶、糯米、馅料等食材</li>
                <li>可以自带拿手馅料</li>
                <li>包好的粽子可以带回家</li>
                <li>注意卫生，勤洗手</li>
            </ul>
            <p><strong>名额：</strong>30人</p>
            <p>欢迎各位老年朋友踊跃参加，感受传统节日氛围！</p>
            ''',
            'location': '社区活动中心一楼厨房',
            'start_time': datetime.now() + timedelta(days=26, hours=9),
            'end_time': datetime.now() + timedelta(days=26, hours=12),
            'register_deadline': datetime.now() + timedelta(days=24),
            'max_participants': 30,
            'status': 'open',
            'target_group': '社区老年居民'
        },
        {
            'title': '关爱独居老人：上门慰问活动',
            'activity_type': 'social',
            'description': '''
            <p>为弘扬尊老敬老传统美德，社区组织志愿者开展"关爱独居老人"上门慰问活动。</p>
            <p><strong>活动内容：</strong></p>
            <ul>
                <li>上门看望独居老人</li>
                <li>陪老人聊天、读报纸</li>
                <li>帮忙打扫卫生、整理物品</li>
                <li>检查家电、燃气安全</li>
                <li>教老人使用智能手机</li>
                <li>赠送生活物资（米、面、油）</li>
            </ul>
            <p><strong>活动时间：</strong>2026年6月10日（周一）上午9:00-12:00</p>
            <p><strong>集合地点：</strong>社区服务中心</p>
            <p><strong>招募对象：</strong>社区志愿者（低龄老年人、社区居民）</p>
            <p><strong>报名方式：</strong>到社区服务中心报名，或拨打热线：010-12345678</p>
            <p>让我们用实际行动关爱独居老人，让他们感受到社区大家庭的温暖！</p>
            ''',
            'location': '社区内独居老人家中',
            'start_time': datetime.now() + timedelta(days=31, hours=9),
            'end_time': datetime.now() + timedelta(days=31, hours=12),
            'register_deadline': datetime.now() + timedelta(days=28),
            'max_participants': 20,
            'status': 'open',
            'target_group': '社区志愿者、低龄老年人'
        }
    ]
    
    created_count = 0
    for data in activity_data:
        if not Activity.objects.filter(title=data['title']).exists():
            activity = Activity.objects.create(
                title=data['title'],
                activity_type=data['activity_type'],
                description=data['description'],
                location=data['location'],
                start_time=data['start_time'],
                end_time=data['end_time'],
                register_deadline=data['register_deadline'],
                max_participants=data['max_participants'],
                current_participants=0,
                status=data['status'],
                creator=admin,
                target_group=data['target_group']
            )
            
            # 创建对应的活动统计记录
            from elderly_system.models import ActivityStats
            ActivityStats.objects.create(activity=activity)
            
            created_count += 1
            print(f'  ✓ 添加活动: {activity.title[:40]}...')
    
    print(f'✓ 共添加 {created_count} 个活动')

def main():
    """主函数"""
    print('='*60)
    print('社区老年活动管理系统 - 数据初始化')
    print('='*60)
    print()
    
    print('[1/4] 创建管理员用户...')
    admin = create_admin_user()
    print()
    
    print('[2/4] 创建老年用户...')
    elderly_users = create_elderly_users()
    print()
    
    print('[3/4] 添加新闻资讯...')
    add_news(admin)
    print()
    
    print('[4/4] 添加公告通知...')
    add_announcements(admin)
    print()
    
    print('[5/4] 添加活动...')
    add_activities(admin)
    print()
    
    print('='*60)
    print('✓ 数据初始化完成！')
    print('='*60)
    print()
    print('管理员账号：admin')
    print('管理员密码：admin123456')
    print()
    print('老年用户账号示例：')
    print('  用户名：zhang_hua  密码：123456')
    print('  用户名：li_ming    密码：123456')
    print()

if __name__ == '__main__':
    main()
