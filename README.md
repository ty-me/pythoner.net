![logo](http://pythoner.net/static/images/logo.png)

感谢名单
-------
特别感谢以下开发者贡献代码：

+ [cbsheng](https://github.com/cbsheng)


简介
---

新的分支用于重构，移除部分功能。开发完成后，老站点的数据将会迁移到新站点上。

Version
-------
+ 1.4.0


开发环境配置
------------
+ 运行scripts目录下的setupenv.sh文件，将会自动安装配置所需环境
+ 设置本地环境变量:export env=DEV
+ mv settings.example.py settings.py 并修改数据库的相关配置信息
+ python manage.py syncdb 生成数据表结构
+ python manage.py runserver 8080

=======

