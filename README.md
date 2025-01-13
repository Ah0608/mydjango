# AWESOME——爬虫工具后台
**主要功能：**
 - 代理池：每天自动定时采集网上免费节点，并且转化为本地socks5/http代理。
 - 笔记：支持Markdown的增添、修改、删除、搜索功能，支持代码高亮。
 - 工作计划：添加工作报告、日程安排、项目记录计划，并且首页显示今日计划。
 - 调用平台：基于windows平台定时调度python脚本、支持date、interval、cron类型。
   必须指定python解释器路径、项目环境变量路径。
 - 工具：包含自制工具和在线爬虫工具集合。

**1、安装**

clone项目后，使用pip安装：pip install requirements.txt

**2、创建数据库**

终端执行：
```bash
python manage.py makemigrations
python manage.py migrate
```
注意：运行命令前需要注释 dispatchplatform/views.py 中的代码否则报错。
```python
# scheduler.add_jobstore(DjangoJobStore(), "default")  
# # crawl_trigger = CronTrigger.from_crontab('00 12 * * *')  
# scheduler.add_job(crawl, trigger=crawl_trigger, id='proxy_crawl', max_instances=5, replace_existing=True)  
# check_trigger = IntervalTrigger(hours=6)  
# scheduler.add_job(multi_thread_check_proxy, trigger=check_trigger, id='proxy_check', max_instances=5,  
#                   replace_existing=True, # multi_thread_check_proxy方法我已经注释掉  
#                   args=['https://www.baidu.com'])  
# scheduler.start()
```
**3、创建超级用户**

终端执行：(密码长度需大于8位)
```bash
python manage.py createsuperuser
```
**4、执行**

终端执行：
```bash
python manage.py runserver
```
浏览器打开: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 就可以看到效果了。
