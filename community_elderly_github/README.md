# 社区老年活动管理系统

Python Django 开发的社区老年活动管理系统，本科毕业设计。

## 技术

Django 4.2 + MySQL 8.0 + HTML/CSS/JS

## 功能

- 用户管理：注册登录、角色管理、启用/禁用
- 活动管理：发布编辑、分类、限额
- 报名签到：在线报名、活动签到
- 信息发布：通知公告、新闻资讯
- 数据统计：活动分析、导出

## 角色

管理员端：用户管理、活动审核、数据统计
老年用户端：浏览活动、报名签到、个人信息

## 运行

```
pip install -r requirements.txt
# 创建MySQL数据库 community_elderly
# 修改 settings.py 中的数据库密码
python manage.py migrate
python manage.py runserver
```

## 目录

- community_elderly/ 项目配置
- elderly_system/ 业务代码
- templates/ 前端模板
- static/ 静态文件

## 作者

徐圣智（姜惟皓） 22013210201 计算机21级
