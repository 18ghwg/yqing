# 南科疫情自动打卡-观后无感

**说明**

本程序为南京科技职业学院疫情自动打卡web

项目框架：Flask

第一次使用程序请导入根目录的`yqing.sql`在你的数据库中

配置根目录的`config.py`文件，修改数据库地址、数据表名、账号、密码

**配置完全部文件后**

1、在程序目录打开控制台执行

`pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`

等待模块安装完成即可，必须得安装指定版本的模块，不要安装最新的模块
2、在控制台执行命令`flask db init`进行数据库初始化，再执行`flask db migrate`构建数据库迁移文件，最后执行`flask db upgrade`上传已经创建的数据库表

3、在控制台输入命令`python app.py`运行疫情打卡web项目

到这里本程序就已经安装并运行成功了

**如何在服务器上安装：**

在宝塔面板上安装`python项目管理器`

点击添加项目
![img_1.png](img.png)
python版本最好是3.9以上(如果没有请在管理器内下载python指定版本)<br>
跟我一样填写即可，如果项目启动有问题，请修改`运行项目的用户`为`root`<br>
第一个勾一定要打上，第二个看你需求

**<<--管理员后台-->>**

域名地址/admin<br>
账号：123456<br>
密码：abcd<br>




