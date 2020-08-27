# Course-reminder

网课时代的实用小程序(x

## 运行方法

安装python后直接双击main.pyw直接运行即可。

可能依赖win32api模块，判断方法，在命令行运行python main.pyw，查看依赖报错。
如果缺少依赖，可运行pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn 安装该模块。

## 功能

课程查询：右键托盘，单击"课程查询"选项
到点提醒上课,需参照下方说明配置
可选择是否自动打开网页，可右键托盘在"自动打开网页"选项中关闭功能。

注：
    开课提醒时间是在课开始前五分钟。
    本托盘小插件无主界面，仅在托盘显示图标。
    托盘除了主进程外，还有一个控制win10通知的附属进程（无图标的那个）。
        
## 配置

用文本编辑工具打开course.cvs中的开课链接（默认是百度），若课表与自己的不符请自行删改。
修改后可以用Office或者WPS预览是否错位。
不建议直接用Office或者WPS直接打开修改。

注：编码格式为GB 2312,不要有多余空行
    如需开机自启请复制main.pyw的快捷方式至 C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup
    
## 开发测试
    
\bin\control.py 中有三个Early的功能是用来做时间模拟测试的。
可将当前时间设为实际时间的Early_days天后，Early_hours小时后，Early_minutes分钟后

注：
    control.py是打开时候预先读入的
    程序运行过程中修改不会有效果
