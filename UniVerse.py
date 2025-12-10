import wx
import time
import threading

from app import MainWindow  


# TO-DO LIST 
class TodoFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="To-Do List", size=(600, 400))

        panel = wx.Panel(self)
        panel.SetBackgroundColour("#FFFF81") 

        wx.StaticText(panel, label="To-Do List", pos=(220, 20))

    
        self.task_input = wx.TextCtrl(panel, pos=(20, 70), size=(380, 25))

       
        add_btn = wx.Button(panel, label="Add", pos=(420, 70), size=(120, 25))
        add_btn.Bind(wx.EVT_BUTTON, self.add_task)

        
        self.task_list = wx.ListBox(panel, pos=(20, 110), size=(520, 200))

       
        del_btn = wx.Button(panel, label="Remove Once Completed", pos=(20, 330), size=(200, 30))
        del_btn.Bind(wx.EVT_BUTTON, self.delete_task)

        
        clear_btn = wx.Button(panel, label="Clear All", pos=(340, 330), size=(200, 30))
        clear_btn.Bind(wx.EVT_BUTTON, self.clear_tasks)

# TO-DO LIST buttons
    def add_task(self, event):
        task = self.task_input.GetValue()
        self.task_list.Append(task)
        self.task_input.SetValue("")

    def delete_task(self, event):
        sel = self.task_list.GetSelection()
        if sel != wx.NOT_FOUND:
            self.task_list.Delete(sel)

    def clear_tasks(self, event):
        self.task_list.Clear()


# POMODORO TIMER
class PomodoroFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Pomodoro Timer", size=(600, 400))

        panel = wx.Panel(self)
        panel.SetBackgroundColour("#FFCCCC")  

       
        self.timer_text = wx.StaticText(panel, label="25:00", style=wx.ALIGN_CENTER)
        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.timer_text.SetFont(font)

        
        self.start_btn = wx.Button(panel, label="Start")
        self.stop_btn = wx.Button(panel, label="Stop")
        self.reset_btn = wx.Button(panel, label="Reset")

        self.start_btn.Bind(wx.EVT_BUTTON, self.start_timer)
        self.stop_btn.Bind(wx.EVT_BUTTON, self.stop_timer)
        self.reset_btn.Bind(wx.EVT_BUTTON, self.reset_timer)

        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.timer_text, 0, wx.ALIGN_CENTER | wx.ALL, 20)
        vbox.Add(self.start_btn, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.stop_btn, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.reset_btn, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)

        
        self.running = False
        self.work_time = 25 * 60     
        self.break_time = 5 * 60     
        self.current_time = self.work_time

        self.Show()

#POMODORO buttons
    def start_timer(self, event):
        if not self.running:
            self.running = True
            t = threading.Thread(target=self.run_timer)
            t.start()

    def stop_timer(self, event):
        self.running = False

    def reset_timer(self, event):
        self.running = False
        self.current_time = self.work_time
        self.update_display()

    def run_timer(self):
        # Work countdown
        while self.running and self.current_time > 0:
            mins = self.current_time // 60
            secs = self.current_time % 60
            wx.CallAfter(self.timer_text.SetLabel, f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            self.current_time -= 1

        if self.running and self.current_time == 0:
            wx.CallAfter(self.timer_text.SetLabel, "Break Time!")
            time.sleep(1)
            self.current_time = self.break_time

            
            while self.running and self.current_time > 0:
                mins = self.current_time // 60
                secs = self.current_time % 60
                wx.CallAfter(self.timer_text.SetLabel, f"{mins:02d}:{secs:02d}")
                time.sleep(1)
                self.current_time -= 1

        
        if self.running:
            wx.CallAfter(self.timer_text.SetLabel, "Done!")

    def update_display(self):
        mins = self.current_time // 60
        secs = self.current_time % 60
        self.timer_text.SetLabel(f"{mins:02d}:{secs:02d}")


# UNIVERSE homepage
app = wx.App()
frame = wx.Frame(None, title="UniVerse", size=(400, 300))

panel = wx.Panel(frame)
panel.SetBackgroundColour("#87CEFA")

heading = wx.StaticText(panel, label="UniVerse", pos=(140, 20))
heading_font = wx.Font(46, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
heading.SetFont(heading_font)

btn1 = wx.Button(panel, label="To-Do List")
btn1.SetBackgroundColour("#FFD966")
btn1.SetForegroundColour("#5A4A00")

btn2 = wx.Button(panel, label="Pomodoro Timer")
btn2.SetBackgroundColour("#FFB3B3")
btn2.SetForegroundColour("#7A0000")

btn3 = wx.Button(panel, label="Flashcards")
btn3.SetBackgroundColour("#B6F2B6")
btn3.SetForegroundColour("#003F00")

button_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
for btn in [btn1, btn2, btn3]:
    btn.SetFont(button_font)
    btn.SetMinSize((200, 50))


# Linking the TO-DO List Button with homepage
def open_todo(event):
    todo_window = TodoFrame(parent=frame)
    todo_window.Show()

btn1.Bind(wx.EVT_BUTTON, open_todo)


# Linking POMODORO button to homepage
def open_pomodoro(event):
    PomodoroFrame()

btn2.Bind(wx.EVT_BUTTON, open_pomodoro)


# Linking FLASHCARDS button to homepage
def open_flashcards(event):
    win = MainWindow()
    win.Show()

btn3.Bind(wx.EVT_BUTTON, open_flashcards)


# Homepage Alignment
elements = wx.BoxSizer(wx.VERTICAL)
for item in [heading, btn1, btn2, btn3]:
    elements.Add(item, 0, wx.ALIGN_CENTER | wx.ALL, 20)

panel.SetSizer(elements)

frame.Show()
app.MainLoop()
