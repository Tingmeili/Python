# -*- coding: utf-8 -*-
import exceptions
import wx
import logging
import re
import sqlite3


class MuffledCalulator:
	muffled = False #这里默认关闭屏蔽
	def calc(self,expr):
		try:
			return eval(expr)
		except ZeroDivisionError:
			if self.muffled:
				print 'Divsion by zero is illagal'
			else:
				raise
def test_exception():
	'''
	   捕获异常，做出一定的动作，保证后面的程序执行下去，程序不会因为发生异常而停止
	'''
	print "***"
	try:

		fl=open('/home/test/ting.txt')
	except IOError:
		print "file not exist"
	print "^^^"


	try:
		x = input('Enter the first number: ')
		y = input('Enter the second number: ')
		print x/y
	except ZeroDivisionError:
		print "输入的数字不能为0！"
	except TypeError:           # 对字符的异常处理
		print "请输入数字！"


	#一个块捕捉多个异常
	#我们当然也可以用一个块来捕捉多个异常：
	#复制代码

	try:
		x = input('Enter the first number: ')
		y = input('Enter the second number: ')
		print x/y
	except (ZeroDivisionError,TypeError,NameError):
		print "你的数字不对！"

def test_logging():
	pass


def test_re():
	pass



def test_wx():
	'''
	  GUI
	'''
	global filename
	global contents
	def load(event):
		file = open(filename.GetValue())
		contents.SetValue(file.read())
		file.close()
	def save(event):
		file = open(filename.GetValue(),'w')
		file.write(contents.GetValue())
		file.close()
	app=wx.App()
	win = wx.Frame(None,title = "编辑器", size=(1000,500))#位置和尺寸都包括一对数值：位置包括x 和y坐标，而尺寸包括宽和高
	bkg = wx.Panel(win)
	loadButton = wx.Button(bkg, label = '打开')
	loadButton.Bind(wx.EVT_BUTTON,load)
	saveButton = wx.Button(bkg, label = '保存')
	saveButton.Bind(wx.EVT_BUTTON,save)
	filename = wx.TextCtrl(bkg)
	#filename = wx.TextCtrl(win, pos = (5,5),size = (750,25))
	contents = wx.TextCtrl(bkg,style = wx.TE_MULTILINE | wx.HSCROLL)#wx.TE_MULTILINE来获取多行文件区，以及 wx.HSCROLL来获取水平滚动条。
	hbox = wx.BoxSizer()
	hbox.Add(filename, proportion =1, flag = wx.EXPAND)
	hbox.Add(loadButton, proportion =0,flag = wx.LEFT, border = 5)
	hbox.Add(saveButton, proportion =0,flag = wx.LEFT, border = 5)

	vbox = wx.BoxSizer(wx.VERTICAL)
	vbox.Add(hbox,proportion = 0,flag = wx.EXPAND | wx.ALL, border = 5)
	vbox.Add(contents, proportion = 1,flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border = 5)

	bkg.SetSizer(vbox)
	win.Show()
	app.MainLoop()


def SqLite():
	'''
		数据库操作
	'''
	conn=sqlite3.connect('test.db')# create db
	cu=conn.cursor() #创建游标，游标可以用来对数据库进行操作

	#创建数据表

	cu.execute("""create table Tlog(
			id integer primary key,
			pid integer,
			name varchar(10) UNIQUE


		)""")

	#插入数据
	cu.execute("insert into Tlog values(0,0,'name1')")
	cu.execute("insert into Tlog values(1,0,'name1')")

	conn.commit() #完成插入并且做出某些更改后确保已经进行了提交，这样才可以将这些修改真正地保存到文件中。



if __name__=='__main__':
	#test_exception()
	#test_logging()
	#test_t=test_wx()
	SqLite()
