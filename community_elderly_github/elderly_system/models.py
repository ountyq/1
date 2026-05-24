"""
社区老年活动管理系统 - 数据库模型
包含：用户、活动、报名签到、公告、数据统计
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """用户模型 - 扩展Django默认用户"""
    ROLE_CHOICES = (
        ('admin', '社区管理员'),
        ('elder', '老年用户'),
    )
    role = models.CharField('角色', max_length=10, choices=ROLE_CHOICES, default='elder')
    phone = models.CharField('手机号', max_length=11, unique=True, null=True, blank=True)
    age = models.IntegerField('年龄', null=True, blank=True)
    area = models.CharField('居住片区', max_length=100, null=True, blank=True)
    avatar = models.ImageField('头像', upload_to='avatars/', null=True, blank=True)
    family_phone = models.CharField('家属手机号', max_length=11, null=True, blank=True)
    is_active = models.BooleanField('是否激活', default=True)
    created_at = models.DateTimeField('注册时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = '用户列表'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class Activity(models.Model):
    """活动模型"""
    STATUS_CHOICES = (
        ('draft', '待发布'),
        ('open', '报名中'),
        ('ongoing', '进行中'),
        ('finished', '已结束'),
        ('cancelled', '已取消'),
    )
    TYPE_CHOICES = (
        ('sports', '文体运动'),
        ('health', '健康讲座'),
        ('culture', '文化娱乐'),
        ('social', '社交联谊'),
        ('learning', '学习教育'),
        ('other', '其他'),
    )
    title = models.CharField('活动名称', max_length=200)
    activity_type = models.CharField('活动类型', max_length=20, choices=TYPE_CHOICES, default='other')
    description = models.TextField('活动介绍', blank=True)
    location = models.CharField('活动地点', max_length=200)
    start_time = models.DateTimeField('开始时间')
    end_time = models.DateTimeField('结束时间')
    register_deadline = models.DateTimeField('报名截止时间')
    max_participants = models.IntegerField('最大参与人数', default=50)
    current_participants = models.IntegerField('当前报名人数', default=0)
    poster = models.ImageField('活动海报', upload_to='posters/', null=True, blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                related_name='created_activities', verbose_name='创建者')
    target_group = models.CharField('面向人群', max_length=200, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'activity'
        verbose_name = '活动'
        verbose_name_plural = '活动列表'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def is_full(self):
        # 实时计算：基于报名记录而非手动维护的字段，避免数据不一致
        from django.db.models import Count
        actual_count = self.registrations.exclude(status='cancelled').count()
        return actual_count >= self.max_participants

    @property
    def remaining_spots(self):
        from django.db.models import Count
        actual_count = self.registrations.exclude(status='cancelled').count()
        return max(0, self.max_participants - actual_count)


class Registration(models.Model):
    """报名签到模型"""
    STATUS_CHOICES = (
        ('registered', '已报名'),
        ('signed_in', '已签到'),
        ('cancelled', '已取消'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='registrations', verbose_name='用户')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE,
                                 related_name='registrations', verbose_name='活动')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='registered')
    register_time = models.DateTimeField('报名时间', auto_now_add=True)
    sign_in_time = models.DateTimeField('签到时间', null=True, blank=True)
    qr_code = models.ImageField('签到二维码', upload_to='qrcodes/', null=True, blank=True)

    class Meta:
        db_table = 'registration'
        verbose_name = '报名记录'
        verbose_name_plural = '报名记录列表'
        unique_together = ('user', 'activity')
        ordering = ['-register_time']

    def __str__(self):
        return f"{self.user.username} - {self.activity.title}"


class Announcement(models.Model):
    """公告模型"""
    TYPE_CHOICES = (
        ('notice', '通知公告'),
        ('activity', '活动提醒'),
        ('system', '系统消息'),
    )
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    ann_type = models.CharField('类型', max_length=20, choices=TYPE_CHOICES, default='notice')
    cover = models.ImageField('封面图片', upload_to='announcement_covers/', null=True, blank=True)
    publisher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  related_name='announcements', verbose_name='发布者')
    is_top = models.BooleanField('是否置顶', default=False)
    publish_time = models.DateTimeField('发布时间', auto_now_add=True)
    target_activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='announcements', verbose_name='关联活动')

    class Meta:
        db_table = 'announcement'
        verbose_name = '公告'
        verbose_name_plural = '公告列表'
        ordering = ['-is_top', '-publish_time']

    def __str__(self):
        return self.title


class News(models.Model):
    """新闻资讯模型"""
    CATEGORY_CHOICES = (
        ('policy', '政策资讯'),
        ('health', '健康养生'),
        ('activity', '活动动态'),
        ('notice', '社区通知'),
        ('other', '其他'),
    )
    title = models.CharField('新闻标题', max_length=200)
    content = models.TextField('新闻内容')
    category = models.CharField('新闻分类', max_length=20, choices=CATEGORY_CHOICES, default='other')
    source = models.CharField('来源', max_length=100, default='社区发布', blank=True)
    cover = models.ImageField('封面图片', upload_to='news_covers/', null=True, blank=True)
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True,
                               related_name='news_list', verbose_name='作者')
    is_top = models.BooleanField('是否置顶', default=False)
    views = models.IntegerField('浏览次数', default=0)
    publish_time = models.DateTimeField('发布时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'news'
        verbose_name = '新闻资讯'
        verbose_name_plural = '新闻资讯列表'
        ordering = ['-is_top', '-publish_time']

    def __str__(self):
        return self.title


class ActivityStats(models.Model):
    """活动统计中间表"""
    activity = models.OneToOneField(Activity, on_delete=models.CASCADE,
                                    related_name='stats', verbose_name='活动')
    total_registered = models.IntegerField('总报名人数', default=0)
    total_signed_in = models.IntegerField('总签到人数', default=0)
    sign_in_rate = models.FloatField('签到率', default=0.0)
    updated_at = models.DateTimeField('统计更新时间', auto_now=True)

    class Meta:
        db_table = 'activity_stats'
        verbose_name = '活动统计'
        verbose_name_plural = '活动统计列表'

    def __str__(self):
        return f"{self.activity.title} 统计"

    def recalculate(self):
        """重新计算统计数据"""
        self.total_registered = self.activity.registrations.exclude(status='cancelled').count()
        self.total_signed_in = self.activity.registrations.filter(status='signed_in').count()
        if self.total_registered > 0:
            self.sign_in_rate = round(self.total_signed_in / self.total_registered * 100, 2)
        else:
            self.sign_in_rate = 0.0
        self.save()
