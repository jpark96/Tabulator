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

        quota = self.election.startRace(SENATOR)

        # Load information panel
        self.infoPanel = InfoPanel(backgroundPanel, quota)
        self.infoPanel.frame = self
        self.infoPanel.SetBackgroundColour((240,240,240))

        backgroundPanel.GetSizer().Add(self.infoPanel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 3)

        self.candidatesPanel.datasource.update()
        self.candidatesPanel.datasource.quota = quota

    def redistribute(self):
        thread.start_new_thread(self.next, ())

    def next(self):
        status = self.election.iterateRace() 
        self.infoPanel.redistributeButton.Disable()

        while(status == CONTINUE):
            time.sleep(.001)
            self.candidatesPanel.refresh()
            status = self.election.iterateRace()
            wx.Yield()
            # self.Update()
        self.infoPanel.redistributeButton.Enable()



class CandidatesPanel(scrolled.ScrolledPanel):
    def __init__(self, parent, candidates, frame):
        scrolled.ScrolledPanel.__init__(self, parent)
        self.SetSizer(wx.BoxSizer(wx.VERTICAL))

        # for i in range(len(candidates)):
        #     name = wx.StaticText(self, label=candidates[i])
        #     self.GetSizer().Add(name, 0, wx.ALL, 5)
        self.frame = frame
        self.parent = parent
        self.candidates = candidates
        self.grid = gridlib.Grid(self)
        self.datasource = CandidatesTable(self, candidates, self.grid, BarRenderer)
        self.grid.SetTable(self.datasource)
        self.grid.AutoSize()
        self.grid.SetColSize(0, 30)
        self.grid.SetColSize(3, 100)
        self.grid.SetColSize(4, 200)
        self.GetSizer().Add(self.grid, 1, wx.EXPAND)

        self.SetAutoLayout(1)
        self.SetupScrolling()

    def refresh(self):
        self.candidates.sort(key=lambda x: -1 * (x.score + x.quotaPlace))
        self.grid.Refresh()

class BarRenderer(wx.grid.PyGridCellRenderer):
    def __init__(self, table, color):
        wx.grid.PyGridCellRenderer.__init__(self)
        self.table = table
        self.color = color
        self.rowSize = 50

    def Draw(self, grid, attr, dc, rect, row, col, isSelected):
        self.dc = dc
        self.dc.BeginDrawing()
        self.dc.SetPen(wx.Pen("grey",style=wx.TRANSPARENT))
        self.dc.SetBrush(wx.Brush("blue", wx.SOLID))
        # set x, y, w, h for rectangle
        self.length = grid.GetColSize(col)
        self.height = grid.GetRowSize(row)
        self.percentage = self.table.getPercentage(row)
        self.dc.DrawRectangle(rect.x,rect.y,self.length*self.percentage,self.height)
        self.dc.EndDrawing()
        self.dc.BeginDrawing()
        self.dc.SetPen(wx.Pen("grey",style=wx.TRANSPARENT))
        self.dc.SetBrush(wx.Brush("white", wx.SOLID))
        self.dc.DrawRectangle(rect.x+self.length*self.percentage,rect.y,self.length*(1-self.percentage),self.height)
        self.dc.EndDrawing()

class CandidatesTable(wx.grid.PyGridTableBase):
    def __init__(self, parent, candidates, grid, barRenderer):
        wx.grid.PyGridTableBase.__init__(self)
        self.candidates = candidates
        self.parent = parent
        self.grid = grid
        self.barRenderer = barRenderer
        self.quota = 1
        self.lastScore = {}
        # Set a special renderer for displaying the bar 

        self.update()
    def GetNumberRows(self):
        """Return the number of rows in the grid"""
        return len(self.candidates)

    def GetNumberCols(self):
        """Return the number of columns in the grid"""
        return 5

    def IsEmptyCell(self, row, col):
        """Return True if the cell is empty"""
        return False

    def GetTypeName(self, row, col):
        """Return the name of the data type of the value in the cell"""
        return None

    def GetValue(self, row, col):
        """Return the value of a cell"""
        try:
            if col == 0:
                return self.candidates[row].number
            elif col == 1:
                return self.candidates[row].name
            elif col == 2:
                return self.candidates[row].party
            elif col == 3:
                return self.round(self.candidates[row].score,4)
            elif col == 4:
                return ""
        except:
            pass

    def SetValue(self, row, col, value):
        """Set the value of a cell"""
        pass

    def getPercentage(self,row):
        try:
            self.lastScore[row] = self.candidates[row].score/self.quota
            return self.lastScore[row]
        except:
            return self.lastScore[row]

    def round(self, num, places):
        return int(num * (10 ** places))/float(10 ** places)

    def update(self):
        attr = wx.grid.GridCellAttr()
        renderer = self.barRenderer(self, "blue")
        attr.SetReadOnly(True)
        attr.SetRenderer(renderer)
        self.grid.SetColAttr(4, attr)


class InfoPanel(wx.Panel):
    def __init__(self, parent, quota):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.quota = quota
        self.SetSizer(wx.BoxSizer(wx.HORIZONTAL))

        quota = wx.StaticText(self, label='QUOTA: ' + str(self.quota))
        self.GetSizer().Add(quota, 1, wx.ALL, 5)

        self.redistributeButton = wx.Button(self, wx.ID_ANY, label='redistribute')
        self.GetSizer().Add(self.redistributeButton, 0, wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.redistribute, self.redistributeButton)

    def redistribute(self, evt):
        self.frame.redistribute()

