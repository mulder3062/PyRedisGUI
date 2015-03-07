# -*- coding:UTF-8 -*-

import os, sys
import wx
import redis
import ConfigParser

CONFIG = ConfigParser.ConfigParser()
CONFIG.read('config.ini')


class LeftPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour("gray")
        self.Bind(wx.EVT_SIZE, self.OnSize, self)

        self.initTree()

    def initTree(self):
        # self.tree = MyTreeCtrl(self,
        #                        style = wx.TR_HAS_BUTTONS
        #                        | wx.TR_EDIT_LABELS
        #                        #| wx.TR_MULTIPLE
        #                        #| wx.TR_HIDE_ROOT
        #                        )
        self.tree = wx.TreeCtrl(self, -1,
                                style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_BUTTONS)

        self.root = self.tree.AddRoot("The Root Item")
        firstChild = self.tree.AppendItem(self.root, 'first child')
        secondChild = self.tree.AppendItem(self.root, 'second child')
        thirdChild = self.tree.AppendItem(self.root, 'third child')

        self.tree.AppendItem(firstChild, 'first-1')
        self.tree.AppendItem(firstChild, 'first-2')
        self.tree.AppendItem(firstChild, 'first-3')

        self.tree.Expand(self.root)

        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self.tree)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self.tree)

    def OnItemExpanded(self, evt):
        print 'OnItemExpanded ', evt

    def OnItemCollapsed(self, evt):
        print 'OnItemCollapsed ', evt

    def OnSelChanged(self, evt):
        print 'OnSelChanged ', evt

    def OnActivate(self, evt):
        print 'OnActivate ', evt

    def OnSize(self, event):
        # self.Layout()
        self.tree.SetSize(self.GetSize())


class RightPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour("red")
        self.initTextCtrl()
        self.Bind(wx.EVT_SIZE, self.OnSize, self)

    def OnSize(self, event):
        #self.Layout()
        self.control.SetSize(self.GetSize())

        # print self.GetSize(), " : ",   self.control.GetSize()

    def initTextCtrl(self):
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.control.write('pyRedisGUI\n\n')
        r = redis.StrictRedis(host=CONFIG.get('Section1', 'host')
                              , port=CONFIG.get('Section1', 'port')
                              , db=CONFIG.get('Section1', 'db'))

        # db 갯수 얻기
        self.control.write('INFO\n')
        self.control.write(r.info().__str__())

        # r.set('foo', 'bar')
        # self.control.write('''redis test
        # foo = %s''' % r.get('foo'))

        keys = r.keys('office*')
        for key in keys:
            self.control.write('{0} = {1}\n'.format(key, 'bar'))


class MySplitter(wx.SplitterWindow):
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, style = wx.SP_LIVE_UPDATE)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnSashChanging)

    def OnSashChanging(self, evt):
        #print self.GetChildren()
        pass


class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        self.initToolbar()
        self.initMenubar()
        self.initStatusbar()
        self.initSplitWindow()
        self.show()

    def initStatusbar(self):
        self.CreateStatusBar(style=0)
        self.SetStatusText("Welcome PyRedisGUI")

    def initSplitWindow(self):
        # splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        splitter = MySplitter(self)

        splitter.SetSashGravity(0.3)

        leftP = LeftPanel(splitter)
        rightP = RightPanel(splitter)

        # split the window
        splitter.SplitVertically(leftP, rightP)
        splitter.SetMinimumPaneSize(200)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def initToolbar(self):
        def OnToolClick(event):
            #tb = self.GetToolBar()
            tb = event.GetEventObject()
            tb.EnableTool(10, not tb.GetToolEnabled(10))
        def OnToolRClick(event):
            pass

        TBFLAGS = (wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        tb = self.CreateToolBar(TBFLAGS)
        tsize = (24, 24)
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        paste_bmp= wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)
        tb.SetToolBitmapSize(tsize)

        tb.AddLabelTool(10, "New", new_bmp, shortHelp="New", longHelp="Long help for 'New'")
        self.Bind(wx.EVT_TOOL, OnToolClick, id=10)
        self.Bind(wx.EVT_TOOL_RCLICKED, OnToolRClick, id=10)

        tb.AddLabelTool(20, "Open", open_bmp, shortHelp="Open", longHelp="Long help for 'Open'")
        self.Bind(wx.EVT_TOOL, OnToolClick, id=20)
        self.Bind(wx.EVT_TOOL_RCLICKED, OnToolRClick, id=20)

        tb.AddSeparator()
        tb.AddSimpleTool(30, copy_bmp, "Copy", "Long help for 'Copy'")
        self.Bind(wx.EVT_TOOL, OnToolClick, id=30)
        self.Bind(wx.EVT_TOOL_RCLICKED, OnToolRClick, id=30)

        tb.AddSimpleTool(40, paste_bmp, "Paste", "Long help for 'Paste'")
        self.Bind(wx.EVT_TOOL, OnToolClick, id=40)
        self.Bind(wx.EVT_TOOL_RCLICKED, OnToolRClick, id=40)

        # tb.AddSeparator()

        tb.AddStretchableSpace()
        tb.Realize()

    def initMenubar(self):
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenuQuit = fileMenu.Append(wx.ID_ANY, 'Quit', 'Quit application')
        fileMenu.Append(wx.ID_ANY, 'Connect', 'Connection..')
        fileMenu.Append(wx.ID_ANY, 'Disconnect', 'Disconnection..')
        self.Bind(wx.EVT_MENU, self.onQuit, fileMenuQuit)
        menubar.Append(fileMenu, '&File')

        self.SetMenuBar(menubar)


    def show(self):
        self.SetSize((800, 600))
        self.SetTitle('Simple menu')
        self.Centre()
        self.Show(True)

    def onQuit(self, e):
        self.Close()


def main():
    print 'wxpython version : {}'.format(wx.version())
    app = wx.App(False)
    frame = MainFrame(None, 'Welcome to PyRedisGUI')
    app.MainLoop()


if __name__ == '__main__':
    main()
