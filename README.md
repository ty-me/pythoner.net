![logo](http://pythoner.net/static/images/logo.png)

## 是的，我正在重构

简介
---

分支名matt来自于电影《火星救援》主人公Matta Damon
新的分支用于重构，移除部分功能。开发完成后，老站点的数据将会迁移到新站点上。


开发环境配置
------------
+ 运行scripts目录下的setupenv.sh文件，将会自动安装配置所需环境
+ 设置本地环境变量:export env=DEV
+ mv settings.example.py settings.py 并修改数据库的相关配置信息
+ python manage.py syncdb 生成数据表结构
+ python manage.py runserver 8080

=======

