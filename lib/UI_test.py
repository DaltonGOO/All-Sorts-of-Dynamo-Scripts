#ui library for Revit dynamo 
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Windows.Forms import Application, Button, Form, Label, TextBox, CheckBox, RadioButton, CheckedListBox, ListBox, MessageBox, FormBorderStyle, FormStartPosition, FormClosingEventHandler, FormClosedEventHandler, FormClosedEventArgs, DialogResult, CheckState, TabControl, TabPage, TabControlAction, TabPage
from System.Drawing import Point, Size, Color, Font, FontStyle, ContentAlignment, TextFormatFlags

class UI_test(Form):
    def __init__(self):
        self.Text = "UI_test"
        self.Size = Size(600, 600)
        self.StartPosition = FormStartPosition.CenterScreen
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.BackColor = Color.White
        self.MaximizeBox = False
        self.MinimizeBox = False
        self.ControlBox = False
        self.FormClosing += self.Form_Closing
        self.FormClosed += self.Form_Closed
        self.Controls.Add(self.Create_TabControl())
        self.Controls.Add(self.Create_Button())
        self.Controls.Add(self.Create_Label())
        self.Controls.Add(self.Create_TextBox())
        self.Controls.Add(self.Create_CheckBox())
        self.Controls.Add(self.Create_RadioButton())
        self.Controls.Add(self.Create_CheckedListBox())
        self.Controls.Add(self.Create_ListBox())
        self.Show()
    def Create_TabControl(self):
        self.TabControl = TabControl()
        self.TabControl.Location = Point(10, 10)
        self.TabControl.Size = Size(580, 580)
        self.TabControl.TabPages.Add(self.Create_TabPage())
        return self.TabControl
    def Create_TabPage(self):
        self.TabPage = TabPage()
        self.TabPage.Text = "TabPage"
        self.TabPage.Controls.Add(self.Create_Label())
        self.TabPage.Controls.Add(self.Create_TextBox())
        self.TabPage.Controls.Add(self.Create_CheckBox())
        self.TabPage.Controls.Add(self.Create_RadioButton())
        self.TabPage.Controls.Add(self.Create_CheckedListBox())
        self.TabPage.Controls.Add(self.Create_ListBox())
        return self.TabPage
    def Create_Button(self):
        self.Button = Button()
        self.Button.Text = "Button"
        self.Button.Location = Point(10, 600)
        self.Button.Size = Size(580, 30)
        self.Button.Click += self.Button_Click
        return self.Button

#create one page with textbox
def Create_TabPage(self):
    self.TabPage = TabPage()
    self.TabPage.Text = "TabPage"
    self.TabPage.Controls.Add(self.Create_Label())
    self.TabPage.Controls.Add(self.Create_TextBox())
    self.TabPage.Controls.Add(self.Create_CheckBox())
    self.TabPage.Controls.Add(self.Create_RadioButton())
    self.TabPage.Controls.Add(self.Create_CheckedListBox())
    self.TabPage.Controls.Add(self.Create_ListBox())
    return self.TabPage

UI_test()
Application.Run()
