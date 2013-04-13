![logo](http://pythoner.net/static/images/logo.png)

感谢名单
-------
特别感谢以下开发者贡献代码（排名不分先后）：

+ [cbsheng](https://github.com/cbsheng)


简介
---

<http://pythoner.net>是TY在11年用django开发,现正式开源，以便各位去其糟粕

Version
-------
+ 1.4.0

新特性
-----
+ 升级到django 1.4.2
+ 新增豆瓣账号登陆

依赖模块
-------
+ Django 1.4.2
+ PIL
+ DjangoVerifyCode  0.2.2

开发环境配置
------------
+ 运行scripts目录下的setupenv.sh文件，将会自动安装配置所需环境
+ 设置本地环境变量:export env=DEV
+ mv settings.example.py settings.py 并修改数据库的相关配置信息
+ python manage.py syncdb 生成数据表结构
+ python manage.py runserver 8080

### html文件命名
+ 被包含的文件通常以name.inc.html命名,如:``` paginator.inc.html ```
+ 标签模板文件通常以name.tag.html命名,如:``` wiki_click.tag.html ```
+ 用于现实列表的文件通常以name_list.html命名,如:``` wiki_list.html ```

=======

