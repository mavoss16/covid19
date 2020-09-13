import csv
# import numpy as np
import wx
import pdb
import os
import numpy as np

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from datetime import datetime

class dataDict:
    def __init__(self, county, tested, positive, recovered, dead):
        self.county = county
        self.tested = tested
        self.positive = positive
        self.recovered = recovered
        self.dead = dead
        self.county_history = []
        self.tested_history = []
        self.positive_history = []
        self.recovered_history = []
        self.dead_history = []
        self.single_tested_history = []
        self.single_positive_history = []
        self.single_recovered_history = []
        self.single_dead_history = []
    def append_history(self):
        self.county_history.append(self.county)
        self.tested_history.append(self.tested)
        self.positive_history.append(self.positive)
        self.recovered_history.append(self.recovered)
        self.dead_history.append(self.dead)


def fix_single_history(dict_to_fix):
    for county in dict_to_fix:
        for date in range(len(dict_to_fix[county].tested_history)):
            if date > 0:
                dict_to_fix[county].single_tested_history.append(dict_to_fix[county].tested_history[date] - dict_to_fix[county].tested_history[date - 1])
        for date in range(len(dict_to_fix[county].positive_history)):
            if date > 0:
                dict_to_fix[county].single_positive_history.append(dict_to_fix[county].positive_history[date] - dict_to_fix[county].positive_history[date - 1])
        for date in range(len(dict_to_fix[county].recovered_history)):
            if date > 0:
                dict_to_fix[county].single_recovered_history.append(dict_to_fix[county].recovered_history[date] - dict_to_fix[county].recovered_history[date - 1])
        for date in range(len(dict_to_fix[county].dead_history)):
            if date > 0:
                dict_to_fix[county].single_dead_history.append(dict_to_fix[county].dead_history[date] - dict_to_fix[county].dead_history[date - 1])
    return dict_to_fix

def read_csv(file):
    """
    'Reader' function, but for a single column of amplitudes and
    no time information.
    """
    with open(file,'r') as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        
        # county = np.zeros(len(data))
        # tested = np.zeros(len(data))
        # positive = np.zeros(len(data))
        # recovered = np.zeros(len(data))
        # dead = np.zeros(len(data))
        
        county = []
        tested = []
        positive = []
        recovered = []
        dead = []
        
        for i, foo in enumerate(data):
            # county[i] = foo[0]
            # tested[i] = foo[1]
            # positive[i] = foo[2]
            # recovered[i] = foo[3]
            # dead[i] = foo[4]
            if i > 0:
                county.append(foo[0])
                try:
                    tested.append(int(foo[1]))
                except:
                    tested.append(foo[1])
                    # print('error')
                try:
                    positive.append(int(foo[2]))
                except:
                    if foo[2] == '':
                        positive.append(0)
                    else:
                        positive.append(foo[2])
                        # print('error')
                try:
                    recovered.append(int(foo[3]))
                except:
                    if foo[3] == '':
                        recovered.append(0)
                    else:
                        recovered.append(foo[3])
                        # print('error')
                try:
                    dead.append(int(foo[4]))
                except:
                    if foo[4] == '':
                        dead.append(0)
                    else:
                        dead.append(foo[4])
                        # print('error')
        
        return county, tested, positive, recovered, dead


def create_dict(county, tested, positive, recovered, dead):
    data_dict = {}
    for i in range(len(county)):
        data_dict[county[i]] = dataDict(county[i], tested[i], positive[i], recovered[i], dead[i])
        data_dict[county[i]].append_history()
    
    return data_dict

def update_dict(data_dict, county, tested, positive, recovered, dead):
    for i in range(len(county)):
        data_dict[county[i]].county = county[i]
        data_dict[county[i]].tested = tested[i]
        data_dict[county[i]].positive = positive[i]
        data_dict[county[i]].recovered = recovered[i]
        data_dict[county[i]].dead = dead[i]
        data_dict[county[i]].append_history()
        
    return data_dict

    
def pull_dates(filename, date_list):
    date = filename[:filename.find('.csv')]
    a = datetime.strptime(date, '%m-%d')
    x = mdates.date2num(a) 
    date_list.append(x)
    
    return date_list

# init_data_func()

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title='COVID Kim', size=(800,500))
        
        # Dummy variables
        self.cumulative = True
        self.picked_choice = 0
        self.cur_sel = 'Linn'
        
        data_dict, self.county, self.date_list= self.init_data()
        self.data_dict = fix_single_history(data_dict)
        
        self.notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        
        self.current_panel = wx.Panel(self.notebook)
        self.history_panel = wx.Panel(self.notebook)
        
        self.notebook.AddPage(self.current_panel, "Latest Data", False)
        self.notebook.AddPage(self.history_panel, "Time History", True)
        
        self.create_current_panel()
        self.create_history_panel()
    
    def init_data(self):
        counter = 0
        date_list = []
        for filename in os.listdir(os.path.join(os.getcwd(), 'Daily-Data')):
            county, tested, positive, recovered, dead = read_csv('Daily-Data\\'+filename)
            # print('starting {}'.format(filename))
            if counter == 0:
                data_dict = create_dict(county, tested, positive, recovered, dead)
            else:
                data_dict = update_dict(data_dict, county, tested, positive, recovered, dead)
            date_list = pull_dates(filename, date_list)
            counter += 1
        
        county.sort()
        return data_dict, county, date_list
        
    def create_current_panel(self):
        
        # Create Widgets
        self.current_panel.county_choice = wx.Choice(self.current_panel, id=wx.ID_ANY, choices=self.county, style=wx.CB_SORT)
        self.current_panel.county_choice.Bind(wx.EVT_CHOICE, self.on_county_choice)
        
        self.tested_textctrl = wx.TextCtrl(self.current_panel, id=wx.ID_ANY, value='', style=wx.TE_RIGHT)
        self.positive_textctrl = wx.TextCtrl(self.current_panel, id=wx.ID_ANY, value='', style=wx.TE_RIGHT)
        self.recovered_textctrl = wx.TextCtrl(self.current_panel, id=wx.ID_ANY, value='', style=wx.TE_RIGHT)
        self.sick_textctrl = wx.TextCtrl(self.current_panel, id=wx.ID_ANY, value='', style=wx.TE_RIGHT)
        self.dead_textctrl = wx.TextCtrl(self.current_panel, id=wx.ID_ANY, value='', style=wx.TE_RIGHT)
        
        # Create Sizers and Place everything
        fgs = wx.FlexGridSizer(6,2,5,5)
        
        fgs.Add(wx.StaticText(self.current_panel, id=wx.ID_ANY, label='County'), -1)
        fgs.Add(self.current_panel.county_choice, -1)
        fgs.Add(wx.StaticText(self.current_panel, id=wx.ID_ANY, label='Tested'), -1)
        fgs.Add(self.tested_textctrl, -1)
        fgs.Add(wx.StaticText(self.current_panel, id=wx.ID_ANY, label='Positive'), -1)
        fgs.Add(self.positive_textctrl, -1)
        fgs.Add(wx.StaticText(self.current_panel, id=wx.ID_ANY, label='Recovered'), -1)
        fgs.Add(self.recovered_textctrl, -1)
        fgs.Add(wx.StaticText(self.current_panel, id=wx.ID_ANY, label='Currently Sick'), -1)
        fgs.Add(self.sick_textctrl, -1)
        fgs.Add(wx.StaticText(self.current_panel, id=wx.ID_ANY, label='Dead'), -1)
        fgs.Add(self.dead_textctrl, -1)
        
        self.current_panel.SetSizer(fgs)
        
    def create_history_panel(self):
        self.history_panel.county_choice = wx.Choice(self.history_panel, id=wx.ID_ANY, choices=self.county, style=wx.CB_SORT)
        self.history_panel.county_choice.Bind(wx.EVT_CHOICE, self.on_county_choice)
        stat_choice = wx.Choice(self.history_panel, id=wx.ID_ANY, choices=['Tested', 'Positive', 'Recovered', 'Currently Sick', 'Dead'])
        self.history_panel.county_choice.SetSelection(56)
        stat_choice.Bind(wx.EVT_CHOICE, self.on_stat_choice)
        stat_choice.SetSelection(self.picked_choice)
        data_type_choice = wx.Choice(self.history_panel, id=wx.ID_ANY, choices=['Cumulative', 'Daily'])
        data_type_choice.Bind(wx.EVT_CHOICE, self.on_data_type_choice)
        data_type_choice.SetSelection(0)
        
        # Initialize Plots
        self.history_panel.figure = Figure()
        self.history_panel.axes = self.history_panel.figure.add_subplot(111)
        self.history_panel.canvas = FigureCanvas(self.history_panel, -1, self.history_panel.figure)
        
        bs = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(6,1,5,5)
        
        fgs.Add(wx.StaticText(self.history_panel, id=wx.ID_ANY, label='County'), -1)
        fgs.Add(self.history_panel.county_choice, -1)
        fgs.Add(wx.StaticText(self.history_panel, id=wx.ID_ANY, label='Statistic'), -1)
        fgs.Add(stat_choice, -1)
        fgs.Add(wx.StaticText(self.history_panel, id=wx.ID_ANY, label='Data Type'), -1)
        fgs.Add(data_type_choice, -1)
        
        bs.Add(fgs)
        bs.Add(self.history_panel.canvas, -1)
        
        self.history_panel.SetSizer(bs)
        
    def on_county_choice(self, event):
        self.cur_sel = self.county[event.GetSelection()]
        # pdb.set_trace()
        # Update TextCtrl Widgets
        self.tested_textctrl.SetValue(str(self.data_dict[self.cur_sel].tested))
        self.positive_textctrl.SetValue(str(self.data_dict[self.cur_sel].positive))
        self.recovered_textctrl.SetValue(str(self.data_dict[self.cur_sel].recovered))
        self.sick_textctrl.SetValue(str(self.data_dict[self.cur_sel].positive - self.data_dict[self.cur_sel].recovered - self.data_dict[self.cur_sel].dead))
        self.dead_textctrl.SetValue(str(self.data_dict[self.cur_sel].dead))
        # Update Choice Widgets
        self.current_panel.county_choice.SetSelection(event.GetSelection())
        self.history_panel.county_choice.SetSelection(event.GetSelection())
        
        self.sort_data_to_plot(self.picked_choice)
        
    
    def on_stat_choice(self, event):
        self.picked_choice = event.GetSelection()
        self.sort_data_to_plot(self.picked_choice)
    
    def sort_data_to_plot(self, picked_choice):
        chosen_county = self.cur_sel
        if picked_choice == 0:
            if self.cumulative:
                chosen_stat = self.data_dict[chosen_county].tested_history
            else:
                chosen_stat = self.data_dict[chosen_county].single_tested_history
        elif picked_choice == 1:
            if self.cumulative:
                chosen_stat = self.data_dict[chosen_county].positive_history
            else:
                chosen_stat = self.data_dict[chosen_county].single_positive_history
        elif picked_choice == 2:
            if self.cumulative:
                chosen_stat = self.data_dict[chosen_county].recovered_history
            else:
                chosen_stat = self.data_dict[chosen_county].single_recovered_history
        elif picked_choice == 3:
            if self.cumulative:
                chosen_stat = np.array(self.data_dict[chosen_county].positive_history) - np.array(self.data_dict[chosen_county].recovered_history) - np.array(self.data_dict[chosen_county].dead_history)
            else:
                chosen_stat = np.array(self.data_dict[chosen_county].single_positive_history) - np.array(self.data_dict[chosen_county].single_recovered_history) - np.array(self.data_dict[chosen_county].single_dead_history)
        elif picked_choice == 4:
            if self.cumulative:
                chosen_stat = self.data_dict[chosen_county].dead_history
            else:
                chosen_stat = self.data_dict[chosen_county].single_dead_history
        
        self.plot_results(self.date_list, chosen_stat)
    
    def on_data_type_choice(self, event):
        if event.GetSelection() == 0:
            self.cumulative = True
            self.sort_data_to_plot(self.picked_choice)
        elif event.GetSelection() == 1:
            self.cumulative = False
            self.sort_data_to_plot(self.picked_choice)
    
    def plot_results(self, date_list, chosen_stat):
        self.history_panel.axes.clear()
        self.history_panel.axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        if self.cumulative:
            self.history_panel.axes.plot(date_list, chosen_stat, 'r')
        else:
            self.history_panel.axes.plot(date_list[1:], chosen_stat, 'r')
        self.history_panel.axes.set_xlabel('Days')
        self.history_panel.axes.set_ylabel('Cases')
        if self.cumulative:
            self.history_panel.axes.set_ylim(bottom=0)
        self.history_panel.axes.grid()
        self.history_panel.canvas.draw()

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
