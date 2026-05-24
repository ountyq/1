"""
生成新闻和公告的封面图片
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 确保媒体目录存在
media_root = 'media'
news_cover_dir = os.path.join(media_root, 'news_covers')
announcement_cover_dir = os.path.join(media_root, 'announcement_covers')

os.makedirs(news_cover_dir, exist_ok=True)
os.makedirs(announcement_cover_dir, exist_ok=True)

def create_cover(filename, title, category, size=(800, 400), bg_color=None):
    """创建一个简单的封面图片"""
    # 根据分类选择背景色
    if bg_color is None:
        color_map = {
            '政策资讯': (70, 130, 180),  #  Steel Blue
            '健康养生': (60, 179, 113),  #  Medium Sea Green
            '活动动态': (255, 165, 0),   #  Orange
            '社区通知': (220, 20, 60),   #  Crimson
            '通知公告': (30, 144, 255),  #  Dodger Blue
            '活动提醒': (50, 205, 50),   #  Lime Green
            '系统消息': (128, 128, 128),  #  Gray
        }
        bg_color = color_map.get(category, (100, 100, 100))
    
    # 创建图片
    img = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(img)
    
    # 添加渐变效果（简单模拟）
    for i in range(size[1]):
        alpha = int(50 * (i / size[1]))
        draw.line([(0, i), (size[0], i)], fill=(255, 255, 255, alpha))
    
    # 保存图片
    img.save(filename)
    print(f"✓ 已生成封面: {filename}")
    return filename

# 新闻封面
news_covers = [
    ('news_001.jpg', '2026年养老金上调通知', '政策资讯'),
    ('news_002.jpg', '社区健康养生讲座', '健康养生'),
    ('news_003.jpg', '春节社区文艺汇演', '活动动态'),
    ('news_004.jpg', '社区路灯维修通知', '社区通知'),
    ('news_005.jpg', '老年人权益保障法解读', '政策资讯'),
    ('news_006.jpg', '秋季健康养生指南', '健康养生'),
    ('news_007.jpg', '社区运动会圆满成功', '活动动态'),
    ('news_008.jpg', '垃圾分类新规定', '社区通知'),
]

print("正在生成新闻封面...")
for filename, title, category in news_covers:
    filepath = os.path.join(news_cover_dir, filename)
    if not os.path.exists(filepath):
        create_cover(filepath, title, category)

# 公告封面
announcement_covers = [
    ('ann_001.jpg', '停水通知', '通知公告'),
    ('ann_002.jpg', '健康体检活动', '活动提醒'),
    ('ann_003.jpg', '端午节活动通知', '活动提醒'),
    ('ann_004.jpg', '系统维护公告', '系统消息'),
    ('ann_005.jpg', '暴雨天气提醒', '通知公告'),
    ('ann_006.jpg', '文明养犬倡议', '通知公告'),
]

print("\n正在生成公告封面...")
for filename, title, category in announcement_covers:
    filepath = os.path.join(announcement_cover_dir, filename)
    if not os.path.exists(filepath):
        create_cover(filepath, title, category)

print("\n✅ 所有封面图片生成完成！")
