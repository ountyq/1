# 社区老年活动管理系统

基于 Python Django 的社区老年活动管理系统，为2026届本科毕业设计项目。

## 技术栈

- **后端框架**：Django 4.2
- **数据库**：MySQL 8.0
- **前端**：HTML5 + CSS3 + JavaScript（原生）
- **Python**：3.11

## 系统模块

| 模块 | 功能说明 |
|------|----------|
| 用户管理 | 注册登录、个人信息、角色管理、账户启用/禁用 |
| 活动管理 | 活动发布、编辑、分类、限额、状态管理 |
| 报名签到 | 在线报名、活动签到、名额控制 |
| 信息发布 | 通知公告、新闻资讯、分类检索 |
| 数据统计 | 活动统计、用户分析、数据导出 |

## 系统角色

- **管理员**：用户管理、活动审核发布、数据统计、系统设置
- **老年用户**：浏览活动、在线报名、活动签到、个人信息维护

## 系统截图

> 答辩演示时补充截图

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 创建MySQL数据库
mysql -u root -p -e "CREATE DATABASE community_elderly CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 3. 修改 settings.py 中的数据库密码

# 4. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 5. 启动服务
python manage.py runserver
```

## 项目结构

```
community_elderly/
├── community_elderly/   # Django 项目配置
├── elderly_system/      # 核心应用
├── templates/           # 前端模板
├── static/              # 静态资源
├── requirements.txt     # 依赖清单
└── manage.py            # Django 管理入口
```

## 作者

- 徐圣智（姜惟皓）
- 计算机科学与技术 2021级
- 学号：22013210201
