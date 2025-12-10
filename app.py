import wx
from flashcards_manager import (
    load_flashcards,
    add_flashcard,
    delete_all_flashcards,
)


class AddFlashcardDialog(wx.Dialog):
    def __init__(self):
        super().__init__(None, title="Add Flashcard")

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        main_sizer.Add(wx.StaticText(self, label="Front:"), 0, wx.ALL, 5)
        self.front_ctrl = wx.TextCtrl(self)
        main_sizer.Add(self.front_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(wx.StaticText(self, label="Back:"), 0, wx.ALL, 5)
        self.back_ctrl = wx.TextCtrl(self)
        main_sizer.Add(self.back_ctrl, 0, wx.EXPAND | wx.ALL, 5)

        btn_sizer = self.CreateSeparatedButtonSizer(wx.OK | wx.CANCEL)
        main_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)
        self.Fit()


class FlashcardViewer(wx.Frame):
    def __init__(self):
        super().__init__(None, title="View Flashcards", size=(400, 300))

        self.flashcards = load_flashcards()
        self.index = 0

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        if not self.flashcards:
            wx.MessageBox("No flashcards available.", "Info")
            self.Close()
            return

        self.front_label = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER)
        self.back_label = wx.StaticText(panel, label="", style=wx.ALIGN_CENTER)

        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.front_label.SetFont(font)
        self.back_label.SetFont(font)

        vbox.Add(self.front_label, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        vbox.Add(self.back_label, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        reveal_btn = wx.Button(panel, label="Reveal Back")

        next_btn = wx.Button(panel, label="Next")
        close_btn = wx.Button(panel, label="Close")
        next_btn.SetBackgroundColour("#88E788")
        reveal_btn.SetBackgroundColour("#88E788")
        close_btn.SetBackgroundColour("#88E788")


        reveal_btn.Bind(wx.EVT_BUTTON, self.on_reveal)
        next_btn.Bind(wx.EVT_BUTTON, self.on_next)
        close_btn.Bind(wx.EVT_BUTTON, self.on_close)

        vbox.Add(reveal_btn, 0, wx.CENTER | wx.ALL, 5)
        vbox.Add(next_btn, 0, wx.CENTER | wx.ALL, 5)
        vbox.Add(close_btn, 0, wx.CENTER | wx.ALL, 5)

        panel.SetSizer(vbox)

        self.show_card()

    def show_card(self):
        card = self.flashcards[self.index]
        self.front_label.SetLabel(f"Front: {card['front']}")
        self.back_label.SetLabel("")

    def on_reveal(self, event):
        card = self.flashcards[self.index]
        self.back_label.SetLabel(f"Back: {card['back']}")

    def on_next(self, event):
        self.index += 1
        if self.index >= len(self.flashcards):
            wx.MessageBox("End of flashcards.", "Done")
            self.Close()
            return
        self.show_card()

    def on_close(self, event):
        self.Close()


# Main Window
class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Flashcards", size=(600, 400))

        panel = wx.Panel(self)
        panel.SetBackgroundColour("#88E788")

        vbox = wx.BoxSizer(wx.VERTICAL)

        btn_add = wx.Button(panel, label="Add Flashcard")
        btn_add.SetBackgroundColour("#FFEFF1")

        btn_view = wx.Button(panel, label="View Flashcards")
        btn_view.SetBackgroundColour("#FFEFF1")
        
        btn_delete = wx.Button(panel, label="Delete All Flashcards")
        btn_delete.SetBackgroundColour("#FFEFF1")

        btn_exit = wx.Button(panel, label="Exit")
        btn_exit.SetBackgroundColour("#FFEFF1")


        btn_add.Bind(wx.EVT_BUTTON, self.on_add)
        btn_view.Bind(wx.EVT_BUTTON, self.on_view)
        btn_delete.Bind(wx.EVT_BUTTON, self.on_delete)
        btn_exit.Bind(wx.EVT_BUTTON, self.on_exit)


        for btn in (btn_add, btn_view, btn_delete, btn_exit):
            vbox.Add(btn, 0, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(vbox)

    def on_add(self, event):
        dialog = AddFlashcardDialog()
        if dialog.ShowModal() == wx.ID_OK:
            front = dialog.front_ctrl.GetValue().strip()
            back = dialog.back_ctrl.GetValue().strip()

            if not front or not back:
                wx.MessageBox("Both fields are required.", "Error")
            else:
                add_flashcard(front, back)
                wx.MessageBox("Flashcard added!", "Success")

        dialog.Destroy()

    def on_view(self, event):
        viewer = FlashcardViewer()
        viewer.Show()

    def on_delete(self, event):
        confirm = wx.MessageDialog(
            self,
            "Are you sure you want to delete ALL flashcards?",
            "Confirm",
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING,
        )
        if confirm.ShowModal() == wx.ID_YES:
            delete_all_flashcards()
            wx.MessageBox("All flashcards deleted.", "Done")

    def on_exit(self, event):
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    win = MainWindow()
    win.Show()
    app.MainLoop()

    
