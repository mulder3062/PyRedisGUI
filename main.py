#-*- coding:UTF-8 -*-

import os, site
site.addsitedir('/usr/local/Cellar/wxpython/3.0.1.1/lib/python2.7/site-packages')

import wx
print site.getsitepackages()
print wx.version()

class MainFrame(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(800,600))
		self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.Show(True)

def main():
	app = wx.App(True)
	frame = MainFrame(None, 'PyRedisGUI 환영합니다.')
	frame.Show(True)
	app.MainLoop()

if __name__ == '__main__':
	main()
