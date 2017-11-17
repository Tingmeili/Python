# -*- coding: utf-8 -*-
# __author__ = 'xinjiu.qiao'
import sys
import os
import re
import subprocess
import time
import urllib, urllib2
import json
import chardet
import random
import logging
import thread, threading
from urllib import quote
from crash_catch import crash_catch
from Analysis import request
import PerformanceTestThread
import string
# from DB.testing_result_storage import operator_db
# couter_lock = threading.Lock()  # 定义多线程锁
class AdbUtils(request):
    def __init__(self):
        try:
            print "start"
            # global times, screen_path
            # screen_path=r'd:\\'
            self.paths = self.redconfi()
            self.screen_paths = os.path.join(self.paths,'screenshot')# 存放图片的路径
            self.log_paths = os.path.join(self.paths,'faillog')
            self.clearpath = os.path.join(self.paths,'ClearNotification.apk')
            self.PerformanceTest_paths = os.path.join(self.paths,'PerformanceTest')#存放性能测试结果路径
            print self.log_paths
            print self.screen_paths
            # self.log_path = self.path + 'faillog'
            self.appinfo = "[{'nodeName': u'CD_VAL55_9908_POP4-10_4G_6.0.1_36c4ee', 'task_id': 'aec17180-39d1-11e6-a80c-4439c491faaf'," \
                           " 'deviceid': '140', 'apkPath': r'D:\\apk\\com.qxtimes.ring_313_883.apk'," \
                           " 'server_address': 'http://172.26.50.50:50000', 'serial_no': " \
                           "'ae0881c0-39d1-11e6-a9d3-4439c491faaf', 'app_resource': " \
                           "'\\\\172.26.50.50\\AppstoreData\\upload_apk\\20160624140541\\error_type7_1.txt'," \
                           " 'mainActivity': 'com.qxtimes.ring.activity.IconActivity_', 'result': '1'," \
                           " 'versioncode': '7', 'appinfo_id': 11192, 'deviceno': 'f76ce3d'," \
                           " 'packageName': 'com.qxtimes.ring', 'uid': '180','run_performance':1}]"
            self.appinfo = eval(self.appinfo)
            print self.appinfo[0]
            # self.appinfo = eval(self.appinfo)2cf4e032
            # self.pid=''
            # print type(self.appinfo)
            print self.redconfi()
            # self.appinfo = [eval(self.GetJenkinsVar("params"))]
            self.deviceID = 'f76ce3d'
            # self.remount_server = self.appinfo[0].get('server_address', 'http://172.26.50.50:5000')
            # print type(self.appinfo), self.appinfo[0]

        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            self.log_interface(a)
    def Sso_interface(self):
        try:
            test = request()
            print self.get_taken
            # data = test.get_request(url='http://10.115.101.181:5000/sso/user.action',param=self.get_taken)
            # couter_lock.release()
            logging.getLogger().info('start to run Sso_interface')
            # return data.get('data')['sid']
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            logging.getLogger().info(a)
    def Appinfo_interface(self, param):
        try:
        # if couter_lock.acquire():
            print param
            test = request()
            # test.get_request("%s/update_appInfo" % self.remount_server, param)
            # couter_lock.release()
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            logging.getLogger().info('start to run appinfo_interface')
            logging.getLogger().info(a)
    def log_interface(self, param):
        try:
            # if couter_lock.acquire():
                print param
                test = request()
                # test.get_request("%s/write_logs" % self.remount_server, param)
                # couter_lock.release()
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            logging.getLogger().info('start to run log_interface')
            logging.getLogger().info(a)
    def get_cur_info(self):
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except:
            f = sys.exc_info()[2].tb_frame.f_back
        return (f.f_code.co_name, f.f_lineno)  # 返回调用函数名，与行数

    def read_thread(self):
        '''
            实现多线程，以连接的设备作为线程数，同时对多个手机进行测试
        '''
        list_appinfos = self.appinfo
        list_num = self.GetDeviceno()
        list_thread = []
        for index, i in enumerate(list_appinfos):
            self.run_log(i)
            if i.get('deviceno') in list_num:
                i = threading.Thread(target=self.installApk, args=(index, i))#创建线程
                #　python提供了两个模块来实现多线程thread 和threading ，thread 有一些缺点，在threading 得到了弥补
                #t1 = threading.Thread(target=music,args=(u'爱情买卖',))  target的值为调用的函数的名字,args给函数传的参数
                list_thread.append(i)
            else:
                a = {'level': 'info',
                     'msg': '[' + str(self.get_cur_info()[1]) + ']' + 'No find ' + i.get('deviceno') + ' to test'}#不正确的信息打印到log日志中
                # print a
                self.log_interface(a)
                # print 'No find '+i.get('deviceno')+' to test'
                s = {'faillog': ' ', 'result': '7', 'appinfo_id': i.get('appinfo_id'), 'screenshot': ' ','pid':''}
                self.update_interface(s)#把一些状态信息更新到数据库中
                # 20160720 Chi Xiaobo: set Salve offline

        return list_thread
    def GetDeviceno(self):  #
        '''
        返回电脑现在连上的设备的devices_id
        '''
        list_deviceid = []  # 存放devicesid的列表
        getdevice_adb = 'adb devices'
        print os.system('adb devices')
        list_devices = os.popen(getdevice_adb).readlines()[1:-1]
        #os.system可以执行系统命令，但是不能命令执行后的输出和返回值
        #通过 os.popen() 返回的是 file read 的对象，对其进行读取 read() 的操作可以看到执行的输出。但是怎么读取程序执行的返回值呢
         #利用os.popen()函数调用系统命令nmap进行扫描，并用grep命令对扫描结果关键内容进行提取
         #这样通过 commands.getstatusoutput() 一个方法就可以获得到返回值和输出，非常好用(import commands )
        for list_device in list_devices:
            if re.findall('device', list_device):
                list_deviceid.append(list_device.split()[0].strip())
            else:
                a = {'level': 'info',
                     'msg': '[' + str(self.get_cur_info()[1]) + ']' + 'Status of ' + list_device.split()[0] + ' is ' +
                            list_device.split()[1]}
                self.log_interface(a)
                # print 'Status of ' + list_device.split()[0] + ' is ' + list_device.split()[1]
                # print 'Please make sure connection of the phone is correct '
        return list_deviceid

    def Run(self):
        '''
            启动多线程方式进行
        '''
        threads = []
        a = self.read_thread()
        for t in a:
            t.setDaemon(True)
            t.start()
            threads.append(t)
            #setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。
            #这时候，要是主线程A执行结束了，就不管子线程B是否完成,一并和主线程A退出.这就是setDaemon方法的含义
            #如果不设置这个，主程序运行完了以后，还是会继续运行子程序
        for j in threads:
            j.join(timeout=600)
            if j.is_alive():
                s = {'faillog': '', 'result': '7', 'appinfo_id': self.appinfo[0].get('appinfo_id'), 'screenshot': '','pid':''}
                self.update_interface(s)
            else:
                break
        #j.join()
        #join（）的作用是，在子线程完成运行之前，这个子线程的父线程将一直被阻塞。
        #原型：join([timeout])

        #里面的参数是可选的，代表线程运行的最大时间，即如果超过这个时间，不管这个此线程有没有执行完毕都会被回收，然后主线程或函数都会接着执行的。
        #is_alive:返回本进程是否是 alive 状态
        #
        #threading.active_count()   返回当前处于 active 状态的线程的数目
        #threading.current_thread()     返回调用者当前的 Thread 对象
        #threading.enumerate()  返回当前处于 active 状态的线程组成的列表
        #threading.stack_size([size])    返回创建线程时分配的栈空间大小，或通过参数进行设定








    def Getinfo(self, string_appinfo,appinfo):
        '''
         获取到命令行得到的结果，存入到一个列表中
        '''
        info,stderr,returncode = self.run_command(string_appinfo,appinfo)#,packagename = self.appinfo[0].get('packageName'))
        return info
    def finduiobject(self,appinfo,pid):
        '''
            判断手机里面是否已经装入了findUiobject包
        '''
        try:
            self.run_log(appinfo)
            adb_push = r"adb -s "+self.deviceID+" push "+self.paths+"\\findUiobject.jar "+"/data/local/tmp"
            find_file = r"adb -s " + self.deviceID + " shell ls /data/local/tmp/findUiobject.jar "
            push_info = str(self.Getinfo(find_file,appinfo))
            print push_info
            logging.getLogger().info(push_info)
            if re.findall('No',push_info):
                self.Getinfo(adb_push,appinfo)
            else:
                pass
            self.handle_Uibutton(appinfo,pid)
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            self.log_interface(a)
            self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':pid}
            # self.Appinfo_interface(h)
    def apk_process(self,appinfo):
        '''
        判断当前运行的apk是否是需要运行的apk
        :param appinfo:
        :return:
        '''
        try:
            adb_data = "adb -s " +  appinfo.get('deviceno') + " shell ps | findstr " + appinfo.get('packageName')
            adb_info = self.Getinfo('adb -s '+appinfo.get('deviceno')+' shell dumpsys activity | findstr "mFocusedActivity"',appinfo)
            print type(adb_info)
            print adb_info
            if adb_info:
                if adb_info.split('/')[0].split(' ')[-1] == appinfo.get('packageName'):
                    return adb_data
                else:
                    return False
            else:
                pass
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            print a
            self.log_interface(a)
            self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
            # self.Appinfo_interface(h)
            self.check_apk(appinfo)

    def check_apk(self,appinfo):
        '''
        当app安装，启动，点击失败后判断是否手机里面还存在apk，若存在则卸载
        :param appinfo:
        :return:
        '''
        adb_check='adb -s '+appinfo.get('deviceno')+' shell pm list package'
        packagedata = self.Getinfo(adb_check,appinfo)
        packagename = 'package:'+appinfo.get('packageName')+'\r\r\n'
        if packagename in packagedata:
            print packagename
            self.UninStallapk(appinfo)
        else:
            pass
    def handle_Uibutton(self,appinfo,pid):
        '''
            当启动app后，点击app里面的指定按钮，比如：取消，立即体验，允许等
        '''
        textname=quote(open(r'ButtonUi.txt').read().decode('gbk').encode('utf-8'))
        # textname=quote('小游戏')
        print chardet.detect(textname)
        try:
            run_findui="adb -s "+self.deviceID+" shell uiautomator runtest findUiobject.jar -c findObject.findUiobject -e text "+textname
            # run_findui="adb shell uiau tomator runtest AutoRunner.jar -c com.tcl.uiautomatortest.MainActivity -e k "+textname
            self.run_log(appinfo)
            logging.getLogger().info(run_findui)
            result_adb=str(self.Getinfo(run_findui,appinfo))
            button_coordinate=re.findall('\d*, \d* - \d*, \d*',result_adb)
            print button_coordinate
            logging.getLogger().info(button_coordinate)
            if len(button_coordinate)==0:
                # print '1'
                self.ClickApk(appinfo,pid)
            else:
                button = str(button_coordinate[0]).split(',')
                buttons = button[1].split('-')
                buttonx = (int(button[0])+int(buttons[1]))/2
                buttony = (int(button[2])+int(buttons[0]))/2
                click_button='adb -s ' + self.deviceID + ' shell input tap ' + str(buttonx)+ ' ' + str(buttony)
                logging.getLogger().info(click_button)
                os.system(click_button)
                data = "adb -s " + self.deviceID + " shell ps | findstr " + appinfo.get('packageName')
                print data
                logging.getLogger().info(data)
                logging.getLogger().info('start to run crash')
                test = crash_catch(appinfo.get('deviceno'))
                time1 = test.phone_time()
                crashinfo = test.time_with_pkg(appinfo.get('packageName'))
                # if self.Getinfo(data):
                if crashinfo == None or crashinfo - time1 > 120 or crashinfo - time1 < 0:
                    self.ClickApk(appinfo,pid)
                else:
                    self.updateinfo = {'faillog': '', 'result': '4', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': self.ScreenshotApk(appinfo),'pid':pid}

                    self.check_apk(appinfo)
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            print a
            self.log_interface(a)
            self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':pid}
            # self.Appinfo_interface(h)
            self.check_apk(appinfo)
    def except_msg(self):
        s = sys.exc_info()
        print "Error %s happened in line %d at crash_catch" % (s[1],s[2].tb_lineno)
    def run_command(self,command,appinfo,timeout=60):
        self.run_log(appinfo)
        logging.getLogger().info('start to run: '+command)
        try:
            proc = subprocess.Popen(command,bufsize=0,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            poll_seconds = .250
            deadline = time.time() + timeout
            while time.time() < deadline and proc.poll() == None:
                time.sleep(poll_seconds)
            if proc.poll() == None:
                proc.terminate()
                stdout,stderr = ('cmd timeout','')
                return stdout,stderr,0
            stdout,stderr = proc.communicate()
            return stdout.strip(),stderr,proc.returncode
        except:
            self.except_msg()
        finally:
            logging.getLogger().info('end to run: '+command)
    def return_allapk(self,appinfo):
        '''
        返回手机上已经安装的所有包名
        :param appinfo:
        :return:
        '''
        list_package = []
        clearmonkey_apk = 'package:apptest.szc.servicetest'
        packages_cmd = "adb -s " + self.deviceID + " shell pm list packages -3"
        strout = self.Getinfo(packages_cmd,appinfo)
        packages = strout.split('\r\r\n')
        for i in packages:
            if clearmonkey_apk != i:
                list_package.append(i)
        return list_package
    def uninstallallapk(self,appinfo):
        '''
        删除手机上所以安装的apk
        :param appinfo:
        :return:
        '''
        packages = self.return_allapk(appinfo)
        print packages

        for i in packages:
            match = re.match('package:(.*)',i)
            # if i:
            #     package =  i.split('package:')[1]
            #     clear_apkdata = "adb -s " +self.deviceID+" shell pm clear "+ package
            #     self.Getinfo(clear_apkdata,appinfo)

            if match:
                uninstall_apk = "adb -s "+self.deviceID+" uninstall " + match.group(1)
                self.Getinfo(uninstall_apk,appinfo)
    def installApk(self, index, appinfo):
        '''
         检测app是否安装成功
        '''
        string_result = "update apps set result=1 where packagename='" + appinfo.get('packageName') + \
                        "' and versioncode='" + appinfo.get('versioncode') + "'"
        # self.DepositMysql(string_result)

        print 'installApk start time : %f' % time.time()

        # self.run_log(appinfo)
        logging.getLogger().info("Start to install "+appinfo.get('packageName')+" the apk")
        s = {'faillog': ' ', 'result': '1', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': ' ','pid':''}
        self.update_interface(s)
        try:
            rm_apk = "adb -s "+ self.deviceID + " shell rm data/local/tmp/*.apk"
            self.run_command(rm_apk,appinfo)
            # string_apkPath = "adb -s " + self.deviceID + " install -r -g " + appinfo.get('apkPath')
            self.uninstallallapk(appinfo)
            # string_apkPaths = "adb -s " + self.deviceID + " install -r " + appinfo.get('apkPath')
            string_apkPath = "adb -s " + self.deviceID + " install -r " + appinfo.get('apkPath')
            print string_apkPath
            logging.getLogger().info(string_apkPath)
            # os.system(string_apkPath)
            install_info = self.run_command(string_apkPath,appinfo)
            print install_info
            if re.findall('cmd timeout',install_info[0]):
                nofinddevices = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
                self.update_interface(nofinddevices)
            else:
                return_appinfo = self.return_allapk(appinfo)
                packages = 'package:'+appinfo.get('packageName')
                # if packages in return_appinfo and (re.findall('Success', install_info[0]) or 'rm: /data/local/tmp' in install_info[0]):
                if packages in return_appinfo and (re.findall('Success', install_info[0]) or 'rm: /data/local/tmp' in install_info[0]):
                    a = {'level': 'info', 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Install "+appinfo.get('packageName')+" is success"}
                    self.log_interface(a)
                    self.LaunchApp(appinfo)
                    self.UninStallapk(appinfo)
                else:
                    # self.ScreenshotApk(appinfo)
                    # s = "update apps set result=2 where packagename='" + self.get_appinfo().get('packageName') + \
                    #     "' and versioncode='" + self.get_appinfo().get('versioncode') + "'"
                    # self.DepositMysql(s)

                    install_failure = re.findall('INSTALL_[A-Z|_]{2,}',install_info[0])
                    if install_failure:
                        s = {'faillog': self.output_log(appinfo), 'result': '2', 'appinfo_id': appinfo.get('appinfo_id'),
                             'screenshot':'','pid':'','error_desc':install_failure[0]}
                        self.update_interface(s)
                    else:
                        h = {'faillog': self.output_log(appinfo), 'result': '2', 'appinfo_id': appinfo.get('appinfo_id'),
                             'screenshot':'','pid':'','error_desc':install_info[0]+install_info[1]}
                        self.update_interface(h)
                    self.check_apk(appinfo)
                    print 'installApk end time : %f' % time.time()
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            self.log_interface(a)
            self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
            # self.Appinfo_interface(h)
            self.check_apk(appinfo)

    def LaunchApp(self, appinfo):
        '''
         检测启动app，查看是否正确
        '''
        print 'LaunchApp start time : %f' % time.time()

        self.run_log(appinfo)
        logging.getLogger().info("Start to Launch "+appinfo.get('packageName')+" the app")
        try:
            if appinfo.get('mainActivity') == None or appinfo.get('mainActivity') == '':
                self.launchtime = ''
                self.updateinfo = {'faillog': '', 'result': '6', 'appinfo_id': appinfo.get('appinfo_id'),
                         'screenshot': '','pid':'','error_desc':'The mainActivity is empty'}
                # self.Appinfo_interface(b)
            else:
                start_app = "adb -s " + self.deviceID + " shell am start -W " + appinfo.get(
                    'packageName') + "/" + appinfo.get('mainActivity')
                # print start_app
                launch_info = self.Getinfo(start_app,appinfo)
                launch_time = re.findall('TotalTime: \d*',launch_info)
                self.launchtime = launch_time[0].split(' ')[-1]
                pid = self.output_logpid(appinfo)
                time.sleep(1)
                # adb_info = self.apk_process(appinfo)
                # data = "adb -s " + self.deviceID + " shell ps | findstr " + appinfo.get('packageName')
                # print data
                print 'crash_catch start time : %f' % time.time()
                logging.getLogger().info('start to run crash')
                test = crash_catch(appinfo.get('deviceno'))
                time1 = test.phone_time()
                crashinfo = test.time_with_pkg(appinfo.get('packageName'))
                print 'crash_catch end time : %f' % time.time()
                # if adb_info:
                logging.getLogger().info(crashinfo)
                if crashinfo == None or crashinfo - time1 > 120 or crashinfo - time1 < 0:
                    # logging.getLogger().info(adb_info)
                    a = {'level': 'info', 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Launch "+appinfo.get('packageName')+" is success"}
                    self.log_interface(a)
                    self.splash_screen(appinfo,pid)
                else:
                    # s = "update apps set result=3 where packagename='" + self.get_appinfo().get('packageName') + \
                    #     "' and versioncode='" + self.get_appinfo().get('versioncode') + "'"
                    # self.DepositMysql(s)
                    self.updateinfo = {'faillog': self.output_log(appinfo), 'result': '3', 'appinfo_id': appinfo.get('appinfo_id'),
                         'screenshot': self.ScreenshotApk(appinfo),'pid':pid}
                    # self.Appinfo_interface(s)
                    self.check_apk(appinfo)

                print 'LaunchApp end time : %f' % time.time()
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            self.log_interface(a)
            self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
            # self.Appinfo_interface(h)
            self.check_apk(appinfo)

    def splash_screen(self, appinfo,pid):
        '''
        进行滑屏操作（闪屏页）
        :param appinfo:
        :param pid:
        :return:
        '''
        restart_install = "adb -s " + self.deviceID + " install -r -g " + appinfo.get('apkPath')
        restart_launch = "adb -s " + self.deviceID + " shell am start -n " + appinfo.get(
                    'packageName') + "/" + appinfo.get('mainActivity')
        adb_version = 'adb  -s ' + self.deviceID + ' shell getprop ro.build.version.sdk'
        result_version = self.Getinfo(adb_version,appinfo)
        print result_version
        if int(result_version) >= 23:
            self.Getinfo(restart_install,appinfo)
            self.Getinfo(restart_launch,appinfo)
        else:
            pass
        print 'splash_screen start time : %f' % time.time()
        self.screen = self.ScreenshotApk(appinfo)
        if self.apk_process(appinfo):
            pass
        else:
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            log = {'level': 'warning',
                    'msg': 'This app is not the current app :'+self.screen}
            self.log_interface(log)
        times = 0
        # self.run_log(appinfo)
        x = self.Get_ScreenSize(appinfo)[0] / 2 + self.Get_ScreenSize(appinfo)[0] / 4
        y = self.Get_ScreenSize(appinfo)[1] / 2
        print x, y
        while (times < 6):
            times = times + 1
            try:
                splash_adb = 'adb -s ' + self.deviceID + " shell input swipe " + str(x) + ' ' + str(
                    y) + ' 0 ' + str(y)
                logging.getLogger().info(splash_adb)
                print splash_adb
                self.Getinfo(splash_adb,appinfo)
            except:
                s = sys.exc_info()
                # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
                a = {'level': 'error',
                     'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
                self.log_interface(a)
                self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
                # self.Appinfo_interface(h)
        self.finduiobject(appinfo,pid)

        print 'splash_screen end time : %f' % time.time()
    def Mkdir_Performance(self,appinfo):
        '''
        创建文件夹
        :return:
        '''
        todaylocaltime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        filedir_name = appinfo.get('packageName') + self.deviceID + todaylocaltime
        filedir_path = os.path.join(self.PerformanceTest_paths,filedir_name)
        try:
            os.mkdir(filedir_path)
        except:
            logging.getLogger().info("The file has already existed")
        return filedir_path
    def dict_Performance(self,appinfo):
        '''
        创造性能测试结果txt文档，并组合成新字典返回
        :param appinfo:
        :return:
        '''
        filedir_path = self.Mkdir_Performance(appinfo)
        dynamical_result_path = os.path.join(filedir_path,'dynamical_result_path.txt')
        monkey_test_result_path = os.path.join(filedir_path,'monkey_test_result_path.txt')
        trffic_datas_file = os.path.join(filedir_path,'trffic_datas_file.txt')
        dict_appinfo = {'mainActivity': appinfo.get('mainActivity'), 'packageName': appinfo.get('packageName'),
               'dynamical_result_path': dynamical_result_path,
               'monkey_test_result_path': monkey_test_result_path,
               'trffic_datas_file': trffic_datas_file}
        return dict_appinfo
    def update_interface(self,dictappinfo,appinfo=None,PerformanceInfo=None):
        '''
        组装测试结果信息，进行数据库更新
        :param dictappinfo:
        :param appinfo:
        :param PerformanceInfo:
        :return:
        '''
        if PerformanceInfo:
            update_appinfo = {'faillog': dictappinfo.get('faillog'), 'result': dictappinfo.get('result'),
                          'appinfo_id': dictappinfo.get('appinfo_id'),
                          'screenshot': dictappinfo.get('screenshot'),'pid':dictappinfo.get('pid'),
                          'dynamical_result_path': PerformanceInfo.get('dynamical_result_path'),
                          'monkey_test_result_path':PerformanceInfo.get('monkey_test_result_path'),
                          'trffic_datas_file':PerformanceInfo.get('trffic_datas_file'),
                          'launchtime':self.launchtime,
                          'run_performance':appinfo.get('run_performance')}
            self.Appinfo_interface(update_appinfo)
        else:
            update_appinfo = {'faillog': dictappinfo.get('faillog'), 'result': dictappinfo.get('result'),
                          'appinfo_id': dictappinfo.get('appinfo_id'),
                          'screenshot': dictappinfo.get('screenshot'),'pid':dictappinfo.get('pid'),
                          'dynamical_result_path': '',
                          'monkey_test_result_path':'',
                          'trffic_datas_file':'',
                          'launchtime':'',
                          'run_performance':self.appinfo[0].get('run_performance')}
            self.Appinfo_interface(update_appinfo)
    def ClearNotification(self,appinfo):
        '''
        做monkey测试时用此apk解决下拉框问题
        :return:
        '''
        all_package = self.return_allapk(appinfo)
        the_apk = 'package:apptest.szc.servicetest'
        install_apk = 'adb -s '+self.deviceID+' install -r '+self.clearpath
        launch_apk = "adb -s " + self.deviceID + " shell am start -W apptest.szc.servicetest/apptest.szc.servicetest.MainActivity"
        try:
            if the_apk in all_package:
                pass
            else:
                self.Getinfo(install_apk,appinfo)
            self.Getinfo(launch_apk,appinfo)
        except:
            self.except_msg()
    def UninStallapk(self, appinfo):
        '''
         每次运行完成后对apk进行卸载,如果失败则尝试三次机会进行卸载
        '''
        if appinfo.get('run_performance'):
            self.ClearNotification(appinfo)
            test = PerformanceTestThread
            newdict_info = self.dict_Performance(appinfo)
            test.run_collections(newdict_info,self.deviceID)
        print 'unInstallApk start time : %f' % time.time()
        self.run_log(appinfo)
        times = 0
        while (times < 3):
            try:
                times = times + 1
                # packageNames = self.get_appinfo().get('packageName').replace(' ', '')
                string_packageName = "adb -s " + self.deviceID + " uninstall " + appinfo.get('packageName')
                # print packageNames
                logging.getLogger().info(string_packageName)
                uninstall_info = str(self.Getinfo(string_packageName,appinfo))
                # os.system("adb -s "+self.deviceID+" shell input keyevent 3")
                # print re.findall('Success',uninstall_info)
                if re.findall('Success', uninstall_info):  # 判断adb执行命令的信息中是否存在success，有则表明卸载成功
                    a = {'level': 'info', 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "uninstall "+appinfo.get('packageName')+" success"}
                    self.log_interface(a)
                    break
                else:
                    a = {'level': 'info', 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "uninstall "+appinfo.get('packageName')+" failure"}
                    self.log_interface(a)
                    break
                print 'unInstallApk end time : %f' % time.time()
            except:
                s = sys.exc_info()
                # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
                a = {'level': 'error',
                     'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
                self.log_interface(a)
                self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
                # self.Appinfo_interface(h)
            finally:
                if appinfo.get('run_performance'):
                    self.update_interface(self.updateinfo,appinfo=appinfo,PerformanceInfo=newdict_info)
                else:
                    self.update_interface(self.updateinfo,appinfo=appinfo)
    def ClickApk(self, appinfo,pid):
        '''
         对apk正常启动后做点击操作，点击三次，点击后再对apk的进程做出判断，看是否存在
        '''
        # print type(appinfo)
        # a=self.deviceID
        # print a
        self.run_log(appinfo)
        logging.getLogger().info("Start to click "+appinfo.get('packageName')+" the apk")
        Get_ScreenNumber = self.Get_ScreenSize(appinfo)
        times = 0
        screen = self.screen + ',' + self.ScreenshotApk(appinfo)
        if self.apk_process(appinfo):
            pass
        else:
            log = {'level': 'warning',
                    'msg': 'This app is not the current app :'+screen}
            self.log_interface(log)
        while (times < 3):
            times = times + 1
            LeftScreen_Size = random.uniform(0, Get_ScreenNumber[0])
            RightScreen_Size = random.uniform(0, Get_ScreenNumber[1])
            ClickApp_adb = 'adb -s ' + self.deviceID + ' shell input tap ' + str(LeftScreen_Size) + ' ' + str(
                RightScreen_Size)
            self.Getinfo(ClickApp_adb,appinfo)
            logging.getLogger().info(ClickApp_adb)
            print ClickApp_adb
            time.sleep(3)
        # packageNames = self.get_appinfo().get('packageName')
        # data = "adb -s " + self.deviceID + " shell ps | findstr " + appinfo.get('packageName')
        # print data
        # adb_info = self.apk_process(appinfo)
        # logging.getLogger().info(adb_info)
        logging.getLogger().info('start to run crash')
        test = crash_catch(appinfo.get('deviceno'))
        time1 = test.phone_time()
        crashinfo = test.time_with_pkg(appinfo.get('packageName'))
        logging.getLogger().info(crashinfo)
        # if adb_info:
        print time1,'######'
        print crashinfo,'*****'
        if crashinfo == None or crashinfo - time1 > 120 or crashinfo - time1 < 0:
            try:
                # s = "update apps set result=6 where packagename='" + self.get_appinfo().get('packageName') + \
                #   "' and versioncode='" + self.get_appinfo().get('versioncode') + "'"
                # self.DepositMysql(s)
                self.updateinfo = {'faillog': '', 'result': '6', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':pid}
                # self.Appinfo_interface(s)
            except:
                s = sys.exc_info()
                # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
                a = {'level': 'error',
                     'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
                print a
                self.log_interface(a)
                self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
                # self.Appinfo_interface(h)
                # self.ScreenshotApk(devicesid)
                self.check_apk(appinfo)
        else:
            # s = "update apps set result=4 where packagename='"+self.get_appinfo().get('packageName')+\
            #     "' and versioncode='"+self.get_appinfo().get('versioncode')+"'"
            # self.DepositMysql(s)
            self.updateinfo = {'faillog': self.output_log(appinfo), 'result': '4', 'appinfo_id': appinfo.get('appinfo_id'),
                 'screenshot': self.ScreenshotApk(appinfo),'pid':pid}
            # self.Appinfo_interface(s)
            self.check_apk(appinfo)
    def run_log(self,appinfo):
        try:
            todaylocaltime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            log_path = os.path.join(self.log_paths,
                                   appinfo.get('packageName') + self.deviceID + todaylocaltime + '.log')
            logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_path,
                        filemode='a')
        except:
            print  sys.exc_info()[1]
    def output_logpid(self,appinfo):
        '''
            返回运行apk的pid值，若没有则返回空
        '''
        try:
            self.run_log(appinfo)
            apkpid_adb='adb -s ' + self.deviceID + ' shell ps | findstr '+appinfo.get('packageName')
            progress_info=self.Getinfo(apkpid_adb,appinfo)
            print progress_info
            logging.getLogger().info(apkpid_adb)
            if progress_info:
                apk_pid= progress_info.split()[1]#存入测试apk的pid值
                return apk_pid
            else:
                return ''
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            self.log_interface(a)
            self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
            # self.Appinfo_interface(h)
    def output_log(self, appinfo):
        todaylocaltime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        log_txt = os.path.join(self.log_paths,
                               appinfo.get('packageName') + self.deviceID + todaylocaltime + '.txt')
        # log_txts = os.path.join(self.log_path,
        #                         appinfo.get('packageName') + self.deviceID + todaylocaltime + '.txt')
        log_adb = 'adb -s ' + self.deviceID + ' logcat -d -v time > ' + log_txt
        self.Getinfo(log_adb,appinfo)
        return log_txt

    def Get_ScreenSize(self, appinfo):
        '''
         截取手机屏幕大小，返回手机屏幕尺寸
        '''
        try:
            self.run_log(appinfo)
            logging.getLogger().info("Get_ScreenSize")
            Screen_Size = 'adb -s ' + self.deviceID + ' shell dumpsys window windows | findstr mFrame'
            # list_ScreenSizes = os.popen(Screen_Size).readlines()
            ScreenSizes = self.Getinfo(Screen_Size,appinfo)
            list_ScreenSizes = ScreenSizes.split('\n')
            logging.getLogger().info(list_ScreenSizes)
            rex = r'mFrame=\[-?\d*?,\d*?\]\[(\d*?,\d*?)\]'
            LeftScreen_Size = []
            RightScreen_Size = []
            print list_ScreenSizes
            if list_ScreenSizes == []:
                print 'the devices not find'
                logging.getLogger().info("the devices not find")
            else:
                for list_ScreenSize in list_ScreenSizes:
                    regx = re.search(rex, list_ScreenSize)
                    if not regx:
                        print 'list_ScreenSize', list_ScreenSize
                    else:
                        s = regx.group(1).split(',')
                        LeftScreen_Size.append(int(s[0]))
                        RightScreen_Size.append(int(s[1]))
            LeftScreen_Size.remove(max(LeftScreen_Size))
            RightScreen_Size.remove(max(RightScreen_Size))
            logging.getLogger().info("return the ScreenSize")
            print max(LeftScreen_Size), max(RightScreen_Size)
            return max(LeftScreen_Size), max(RightScreen_Size)
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            self.log_interface(a)
            self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
            # self.Appinfo_interface(h)

    def ScreenshotApk(self, appinfo):
        '''
         截图操作，主要是当执行安装，启动，点击失败时执行截图,返回图片名称
        '''
        self.run_log(appinfo)
        todaylocaltime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        try:
            # packageNames = self.get_appinfo().get('packageName').replace(' ', '')
            string_picpath = r"adb -s " + appinfo.get(
                'deviceno') + " shell /system/bin/screencap -p /sdcard/" + appinfo.get('packageName') + appinfo.get(
                'deviceno') + todaylocaltime + '.png'
            os.system(string_picpath)
            print string_picpath
            logging.getLogger().info(string_picpath)
            string_picpaths = r'adb -s ' + self.deviceID + ' pull /sdcard/' + appinfo.get(
                'packageName') + self.deviceID + todaylocaltime + '.png ' + self.screen_paths
            # s = "update apps set result=4 , screenshot='" + self.screen_path + "' where packagename='" + \
            #     self.get_appinfo().get('packageName') + "' and versioncode='" + self.get_appinfo().get(
            #     'versioncode') + "'"
            # print s
            # self.DepositMysql(s)
            self.Getinfo(string_picpaths,appinfo)
            logging.getLogger().info(string_picpaths)
            # print string_picpaths
        except:
            s = sys.exc_info()
            # print "Error %s happened on %d" % (s[1],s[2].tb_lineno)
            a = {'level': 'error',
                 'msg': '[' + str(self.get_cur_info()[1]) + ']' + "Error %s happended on %d in adbshell.py" % (s[1],s[2].tb_lineno)}
            self.log_interface(a)
            self.updateinfo = {'faillog': '', 'result': '7', 'appinfo_id': appinfo.get('appinfo_id'), 'screenshot': '','pid':''}
            # self.Appinfo_interface(h)
        # return self.screen_path+'/'+appinfo.get('packageName')+todaylocaltime+'.png'
        # return os.path.join(self.screen_path,
        #                     appinfo.get('packageName') + self.deviceID + todaylocaltime + '.png')
        return appinfo.get('packageName') + self.deviceID + todaylocaltime + '.png'
if __name__ == '__main__':
    test = AdbUtils()
    test.Run()
    # test.finduiobject({'deviceno':'KJA6MJORJVPVS8OB'},312)
    # tests=request()
    # quest1=tests.get_request( 'http://127.0.0.1:5000/update_appInfo',param={'faillog':'faillog', 'result': 'result', 'appinfo_id': 'appinfo_id', 'screenshot': 'screenshot'})
    # appinfo={'mainActivity':'com.lantern.launcher.ui.MainActivity','packageName':'com.snda.wifilocating','versioncode':'4.5.1','apkPath':r"d:\xin.apk",'deviceno':'KJA6MJORJVPVS8OB'}
    # threads = []
    # a = test.test()
    # print test.Get_ScreenSize({'deviceno':'KJA6MJORJVPVS8OB'})
    # test.splash_screen(appinfo)
    # print test.ClickApk(r"d:\xin.apk")
    # print test.output_log(appinfo)
    # print test.Get_ScreenSize(appinfo)
