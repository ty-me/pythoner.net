![logo](http://pythoner.net/static/images/logo.png)

简介
---
<http://pythoner.net>是TY在11年初刚开始完全使用python时用django(1.3)开发,现正式开源，以便各位去其糟粕

----
### 代码整理中,稍后奉上...
----

Version
-------
+ 1.3.1

新特性
-----
+ 新增豆瓣账号登陆

依赖模块
-------
+ Django 1.3
+ PIL
+ DjangoVerifyCode  0.2.2

开发环境配置
------------
+ 运行scripts目录下的setupenv.sh文件，将会自动安装配置所需环境
+ 完成后设置本地环境变量:export site=local
+ 修改settings.py中数据库的相关配置信息
+ python manage.py syncdb 生成数据表结构
+ python manage.py runserver 8080

### html文件命名
+ 被包含的文件通常以name.inc.html命名,如:``` paginator.inc.html ```
+ 标签模板文件通常以name.tag.html命名,如:``` wiki_click.tag.html ```
+ 用于现实列表的文件通常以name_list.html命名,如:``` wiki_list.html ```

=======

