# Course-reminder

网课时代的实用小程序(x

## 运行方法

    安装python后直接双击main.pyw直接运行即可。

    可能依赖win32api模块，判断方法，在命令行运行python main.pyw，查看依赖报错。
    如果缺少依赖，可运行pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn 安装该模块。

## 功能

    课程查询：右键托盘，单机"课程查询"选项
    到点提醒上课,需参照下方说明配置
    可选择是否自动打开网页，可右键托盘在"自动打开网页"选项中关闭功能。

## 配置

    course.cvs的下的开课链接需要自行修改，默认是百度。
    course.cvs中与课表不符合的课程请自行修改。
    csv文件可直接用Office或者WPS打开。
    但是建议直接文本编辑工具打开，防止兼容出错，编码为GB 2312,不要有多余空行

    如需开机自启请复制main.py的快捷方式至 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
    
## 管理员
    
    \bin\control.py 中有三个Early的功能是用来做时间测试的。
    可将当前时间设为实际时间的Early_days天后，Early_hours小时后，Early_minute分钟后
