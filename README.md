pythoner.net
============

简介
---
<http://pythoner.net>是TY在10年用django(1.3)开发,现正式开放源代码
欢迎大家Fork


新特性
-----
+ 新增豆瓣账号登陆

####第三方模块####
+ Django 1.3
+ PIL
+ DjangoVerifyCode  0.2.2

编码规范
--------
为便于更多人了解和使用源代码,请将可能依据以下规范编写代码.

##### 导入
请遵循一下优先级导入模块：python内置模块>第三方模块>django内置模块>自定义模块
想到一点写一点吧

##### 函数命名
pass

##### html文件命名
被包含的文件通常以name.inc.html命名,如:``` paginator.inc.html ```
标签模板文件通常以name.tag.html命名,如:``` wiki_click.tag.html ```
用于现实列表的文件通常以name_list.html命名,如:``` wiki_list.html ```


