# pyinstaller -F -i favicon.ico Reminder.py --noconsole

import os
import win32api
import win32con
import win32gui_struct
import win32gui

import time
from win10toast import ToastNotifier
import threading
import sys
from control import DEBUG

Main = None

class SysTrayIcon(object):
    QUIT = 'QUIT'
    SPECIAL_ACTIONS = [QUIT]
    FIRST_ID = 1
    def __init__(self,
                 icon,
                 hover_text,
                 menu_options,
                 on_quit=None,
                 default_menu_index=None,
                 window_class_name=None,
                 mythread=None):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        self.mythread = mythread
        self.icon = icon
        self.hover_text = hover_text
        self.on_quit = on_quit

        menu_options = menu_options + (('退出', None, self.QUIT),)
        self._next_action_id = self.FIRST_ID
        self.menu_actions_by_id = set()
        self.menu_options = self._add_ids_to_menu_options(list(menu_options))
        self.menu_actions_by_id = dict(self.menu_actions_by_id)
        del self._next_action_id

        self.default_menu_index = (default_menu_index or 0)
        self.window_class_name = window_class_name or "SysTrayIconPy"

        message_map = {win32gui.RegisterWindowMessage("TaskbarCreated"): self.refresh_icon,
                       win32con.WM_DESTROY: self.destroy,
                       win32con.WM_COMMAND: self.command,
                       win32con.WM_USER+20 : self.notify,}
        # 注册窗口类。
        window_class = win32gui.WNDCLASS()
        window_class.hInstance = win32gui.GetModuleHandle(None)
        window_class.lpszClassName = self.window_class_name
        window_class.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        window_class.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        window_class.hbrBackground = win32con.COLOR_WINDOW
        window_class.lpfnWndProc = message_map #也可以指定wndproc.
        self.classAtom = win32gui.RegisterClass(window_class)

    def show_icon(self):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        # 创建窗口。
        hinst = win32gui.GetModuleHandle(None)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(self.classAtom,
                                          self.window_class_name,
                                          style,
                                          0,
                                          0,
                                          win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT,
                                          0,
                                          0,
                                          hinst,
                                          None)
        win32gui.UpdateWindow(self.hwnd)
        self.notify_id = None
        self.refresh_icon()
        
        win32gui.PumpMessages()

    def show_menu(self):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        menu = win32gui.CreatePopupMenu()
        self.create_menu(menu, self.menu_options)
        #win32gui.SetMenuDefaultItem(menu, 1000, 0)
        
        pos = win32gui.GetCursorPos()
        # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
        win32gui.SetForegroundWindow(self.hwnd)
        win32gui.TrackPopupMenu(menu,
                                win32con.TPM_LEFTALIGN,
                                pos[0],
                                pos[1],
                                0,
                                self.hwnd,
                                None)
        win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def destroy(self, hwnd, msg, wparam, lparam):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        if self.on_quit: self.on_quit(self) #运行传递的on_quit
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0) # 退出托盘图标

    # WM_MOUSEMOVE
    # WM_LBUTTONDOWN
    # WM_LBUTTONUP
    # WM_LBUTTONDBLCLK
    # WM_RBUTTONDOWN
    # WM_RBUTTONUP
    # WM_RBUTTONDBLCLK
    # WM_MBUTTONDOWN
    # WM_MBUTTONUP
    # WM_MBUTTONDBLCLK
    # 这里是托盘的事件触发，可能的鼠标事件如上
    def notify(self, hwnd, msg, wparam, lparam):

        if lparam == win32con.WM_LBUTTONDBLCLK: # 双击左键
            pass #self.execute_menu_option(self.default_menu_index + self.FIRST_ID)
        elif lparam == win32con.WM_RBUTTONUP: # 单击右键
            self.show_menu()
        elif lparam == win32con.WM_LBUTTONUP: # 单击左键
            pass

            # nid = (self.hwnd, 0)
            # win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
            # win32gui.PostQuitMessage(0) # 退出托盘图标
            # if Main: Main.root.deiconify()
        return True

    def _add_ids_to_menu_options(self, menu_options):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        result = []
        for menu_option in menu_options:
            option_text, option_icon, option_action = menu_option
            if callable(option_action) or option_action in self.SPECIAL_ACTIONS:
                self.menu_actions_by_id.add((self._next_action_id, option_action))
                result.append(menu_option + (self._next_action_id,))
            else:
                result.append((option_text,
                               option_icon,
                               self._add_ids_to_menu_options(option_action),
                               self._next_action_id))
            self._next_action_id += 1
        return result
        
    def refresh_icon(self, **data):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        hinst = win32gui.GetModuleHandle(None)
        if os.path.isfile(self.icon): # 尝试找到自定义图标
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst,
                                       self.icon,
                                       win32con.IMAGE_ICON,
                                       0,
                                       0,
                                       icon_flags)
        else: # 找不到图标文件 - 使用默认值
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        if self.notify_id: message = win32gui.NIM_MODIFY
        else: message = win32gui.NIM_ADD
        self.notify_id = (self.hwnd,
                          0,
                          win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP,
                          win32con.WM_USER+20,
                          hicon,
                          self.hover_text)
        win32gui.Shell_NotifyIcon(message, self.notify_id)

    def create_menu(self, menu, menu_options):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        for option_text, option_icon, option_action, option_id in menu_options[::-1]:
            if option_icon:
                option_icon = self.prep_menu_icon(option_icon)
            
            if option_id in self.menu_actions_by_id:                
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                wID=option_id)
                win32gui.InsertMenuItem(menu, 0, 1, item)
            else:
                submenu = win32gui.CreatePopupMenu()
                self.create_menu(submenu, option_action)
                item, extras = win32gui_struct.PackMENUITEMINFO(text=option_text,
                                                                hbmpItem=option_icon,
                                                                hSubMenu=submenu)
                win32gui.InsertMenuItem(menu, 0, 1, item)

    def prep_menu_icon(self, icon):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        # 首先加载图标。
        ico_x = win32api.GetSystemMetrics(win32con.SM_CXSMICON)
        ico_y = win32api.GetSystemMetrics(win32con.SM_CYSMICON)
        hicon = win32gui.LoadImage(0, icon, win32con.IMAGE_ICON, ico_x, ico_y, win32con.LR_LOADFROMFILE)

        hdcBitmap = win32gui.CreateCompatibleDC(0)
        hdcScreen = win32gui.GetDC(0)
        hbm = win32gui.CreateCompatibleBitmap(hdcScreen, ico_x, ico_y)
        hbmOld = win32gui.SelectObject(hdcBitmap, hbm)
        # 填满背景。
        brush = win32gui.GetSysColorBrush(win32con.COLOR_MENU)
        win32gui.FillRect(hdcBitmap, (0, 0, 16, 16), brush)
        # "GetSysColorBrush返回缓存的画笔而不是分配新的画笔。"
        #  - 暗示没有DeleteObject
        # 画出图标
        win32gui.DrawIconEx(hdcBitmap, 0, 0, hicon, ico_x, ico_y, 0, 0, win32con.DI_NORMAL)
        win32gui.SelectObject(hdcBitmap, hbmOld)
        win32gui.DeleteDC(hdcBitmap)
        
        return hbm

    def command(self, hwnd, msg, wparam, lparam):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        id = win32gui.LOWORD(wparam)
        self.execute_menu_option(id)
        
    def execute_menu_option(self, id):

        if DEBUG: print(sys._getframe(0).f_code.co_name,id)

        if id == 3:
            self.mythread.set_auto()
        elif id == 4:
            os.system("start python " + os.getcwd() + "\\bin\\work.py")

        menu_action = self.menu_actions_by_id[id]      
        if menu_action == self.QUIT:
            win32gui.DestroyWindow(self.hwnd)
        else:
            menu_action(self)
 
class TestTaskbarIcon:
    def __init__(self):

        # 注册一个窗口类
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32gui.GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbarDemo"
        wc.lpfnWndProc = {win32con.WM_DESTROY: self.OnDestroy, }
        classAtom = win32gui.RegisterClass(wc)
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(classAtom, "Taskbar Demo", style,
                                          0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT,
                                          0, 0, hinst, None)
        hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
        nid = (self.hwnd, 0, win32gui.NIF_ICON, win32con.WM_USER + 20, hicon, "Demo")
        win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
 
    def showMsg(self, title, msg):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        nid = (self.hwnd,  # 句柄
               0,  # 托盘图标ID
               win32gui.NIF_INFO,  # 标识
               0,  # 回调消息ID
               0,  # 托盘图标句柄
               "TestMessage",  # 图标字符串
               msg,  # 气球提示字符串
               0,  # 提示的显示时间
               title,  # 提示标题
               win32gui.NIIF_INFO  # 提示用到的图标
               )
        win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, nid)
 
    def OnDestroy(self, hwnd, msg, wparam, lparam):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)  # Terminate the app.

class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.is_running = True
        self.auto_website_open = False

    def stop(self):
        self.is_running = False

    def set_auto(self):
        self.auto_website_open = not self.auto_website_open
        self.t.showMsg("Course Reminder", "自动打开网页功能" + ("已开启" if self.auto_website_open else "已关闭"))

    def run(self):

        if DEBUG: print ("开始线程")

        self.t = TestTaskbarIcon()
        self.t.showMsg("Course Reminder", "程序已最小化到托盘")

        import work

        tmp = work.get_course(1, 0)

        # print(tmp)

        while(1):

            if self.is_running == False:
                break

            # 提醒功能

            time.sleep(10)
        if DEBUG: print ("退出线程")

class _Main:
    def main(self):
        import tkinter as tk
        self.root = tk.Tk()

        icons = 'favicon.ico'
        hover_text = "couser reminder" #悬浮于图标上方时的提示
        menu_options = (('作者 zzy', None, self.switch_icon),
                        ('配置 参阅README.md', None, self.switch_icon),
                        ('自动打开网页', None, self.switch_icon),
                        ('课程查询', None, self.switch_icon))
        # menu_options = (('一级选项', None, self.switch_icon),('二级选项', None, (('选项', None, self.switch_icon),)))
 
        self.thread1 = myThread()
        self.thread1.start()
 
        self.sysTrayIcon = SysTrayIcon(icons, hover_text, menu_options, on_quit = self.exit, default_menu_index = 1, mythread = self.thread1)

        self.root.bind("<Unmap>", lambda event: self.Unmap() if self.root.state() == 'iconic' else False)
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        self.root.resizable(0,0)
        self.Unmap()

        self.root.mainloop()

    def switch_icon(self, _sysTrayIcon):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        _sysTrayIcon.refresh_icon()
        #点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = self.sysTrayIcon

    def Unmap(self):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        self.root.withdraw()
        self.sysTrayIcon.show_icon()

    def exit(self, _sysTrayIcon = None):

        if DEBUG: print(sys._getframe(0).f_code.co_name)

        self.root.destroy()
        self.thread1.stop()
        print ('exit...')

if __name__ == '__main__':

    import multiprocessing
    multiprocessing.freeze_support()

    Main = _Main()
    Main.main()
