import wx
import wx.lib.scrolledpanel as scrolled
import wx.grid as gridlib

from Tabulator import *
from constants import *
from Race import *

import time
import thread

class ElectionFrame(wx.Frame):
  
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(900, 680))
            
        self.InitUI()
        self.Centre()
        self.Show()     
        
    def InitUI(self):
        # Create Status Bar
        self.CreateStatusBar()

        # Create Menu Bar
        menubar = wx.MenuBar()

        # File Menu
        filemenu = wx.Menu()

        loadc = filemenu.Append(wx.ID_ANY, "Load &Candidates", "Load candidates file")
        loadb = filemenu.Append(wx.ID_ANY, "Load &Ballots", "Load ballots file")
        quit = filemenu.Append(wx.ID_ANY, "E&xit", "Terminate the program")
        
        self.Bind(wx.EVT_MENU, self.OnQuit, quit)

        menubar.Append(filemenu, '&File')

        # Help Menu
        helpmenu = wx.Menu()

        about = helpmenu.Append(wx.ID_ANY, "&About", "Information about the program")

        menubar.Append(helpmenu, '&Help')

        # Set Menu Bar
        self.SetMenuBar(menubar)

        # Outside Panel
        backgroundPanel = wx.Panel(self)
        backgroundPanel.SetSizer(wx.BoxSizer(wx.VERTICAL))
        backgroundPanel.SetBackgroundColour((200,200,200))

        # Load the candidates panel
        self.election = Election(self)
        self.election.loadBallotsFromJSONFile("ballots.json")
        self.election.loadCandidatesFromJSONFile("candidates2013.json")


        self.candidatesPanel = CandidatesPanel(backgroundPanel, self.election.candidates[SENATOR], self)
        self.candidatesPanel.SetBackgroundColour((240,240,240))
        backgroundPanel.GetSizer().Add(self.candidatesPanel, 1, wx.EXPAND | wx.ALL, 3)

        # Load information panel
        infoPanel = InfoPanel(backgroundPanel)
        infoPanel.SetBackgroundColour((240,240,240))

        backgroundPanel.GetSizer().Add(infoPanel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)

        self.election.startRace(SENATOR)

    def OnQuit(self, e):
        self.next()

    def next(self):
        status = self.election.iterateRace() 
        while(status == CONTINUE):
            time.sleep(.0001)
            self.candidatesPanel.refresh()
            status = self.election.iterateRace()
            self.Update()
        # if (status != CONTINUE):
        #     return
        # else:
        #     print("Iterating")
        #     time.sleep(.0001)
        #     # thread.start_new_thread(self.candidatesPanel.refresh, ())
        #     self.candidatesPanel.refresh()


class CandidatesPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, candidates, frame):
        scrolled.ScrolledPanel.__init__(self, parent)
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))

        # for i in range(len(candidates)):
        #     name = wx.StaticText(self, label=candidates[i])
        #     self.GetSizer().Add(name, 0, wx.ALL, 5)
        self.frame = frame
        self.candidates = candidates
        self.grid = gridlib.Grid(self)
        datasource = CandidatesTable(candidates)
        self.grid.SetTable(datasource)
        self.grid.AutoSize()
        self.grid.SetColSize(0, 30)
        self.grid.SetColSize(3, 100)
        self.GetSizer().Add(self.grid, 1, wx.EXPAND)

        self.SetAutoLayout(1)
        self.SetupScrolling()

        # raw_input()
        # datasource.candidates[0].name = "sup"

        # Figure out why scrolling doesn't work with grid
        # grid.EnableScrolling()

    def refresh(self):
        self.candidates.sort(key=lambda x: -1 * (x.score + x.quotaPlace))
        self.grid.Refresh()
        # self.frame.next()

class CandidatesTable(wx.grid.PyGridTableBase):
    def __init__(self, candidates):
        wx.grid.PyGridTableBase.__init__(self)
        self.candidates = candidates

    def GetNumberRows(self):
        """Return the number of rows in the grid"""
        return len(self.candidates)

    def GetNumberCols(self):
        """Return the number of columns in the grid"""
        return 4

    def IsEmptyCell(self, row, col):
        """Return True if the cell is empty"""
        return False

    def GetTypeName(self, row, col):
        """Return the name of the data type of the value in the cell"""
        return None

    def GetValue(self, row, col):
        """Return the value of a cell"""
        if col == 0:
            return self.candidates[row].number
        elif col == 1:
            return self.candidates[row].name
        elif col == 2:
            return self.candidates[row].party
        elif col == 3:
            return self.round(self.candidates[row].score,4)

    def SetValue(self, row, col, value):
        """Set the value of a cell"""
        pass

    def round(self, num, places):
        return int(num * (10 ** places))/float(10 ** places)

class InfoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))

        quota = wx.StaticText(self, label='QUOTA')
        self.GetSizer().Add(quota, 1, wx.ALL, 5)

