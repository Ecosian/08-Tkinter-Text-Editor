import tkinter as tk
import time
from tkinter import *
from tkinter import filedialog, messagebox, font, colorchooser, simpledialog
import os
from datetime import datetime
from time import strftime
from turtle import *

PROGRAM_NAME = "Untitled"

window = Tk()
window.geometry('800x550+0+0')
window.title(PROGRAM_NAME)
window.iconbitmap('texteditor.ico')
menu_bar = Menu(window)
file_menu = Menu(menu_bar, tearoff=0)
edit_menu = Menu(menu_bar, tearoff=0)
tool_menu = Menu(menu_bar, tearoff=0)
about_menu = Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Edit', menu=edit_menu)
menu_bar.add_cascade(label='Tools', menu=tool_menu)
menu_bar.add_cascade(label='About', menu=about_menu)

new_file_icon = PhotoImage(file='new_file.png')
open_file_icon = PhotoImage(file='open_file.gif')
save_file_icon = PhotoImage(file='save.gif')
cut_icon = PhotoImage(file='cut.gif')
copy_icon = PhotoImage(file='copy.gif')
paste_icon = PhotoImage(file='paste.gif')
undo_icon = PhotoImage(file='undo.gif')
redo_icon = PhotoImage(file='redo.gif')
exit_file_icon = PhotoImage(file='exit_file.gif')
about_icon = PhotoImage(file='about.gif')
clock_icon = PhotoImage(file='clock.gif')
digi_clock = PhotoImage(file='digitalclock.png')
wordcount_icon = PhotoImage(file='wordcount.gif')

#Python Turtle Analog Clock Setup
def jump(distanz, winkel=0):
    penup()
    right(winkel)
    forward(distanz)
    left(winkel)
    pendown()

def hand(laenge, spitze):
    fd(laenge*1.15)
    rt(90)
    fd(spitze/2.0)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze)
    lt(120)
    fd(spitze/2.0)

def make_hand_shape(name, laenge, spitze):
    reset()
    jump(-laenge*0.15)
    begin_poly()
    hand(laenge, spitze)
    end_poly()
    hand_form = get_poly()
    register_shape(name, hand_form)

def clockface(radius):
    reset()
    pensize(7)
    for i in range(60):
        jump(radius)
        if i % 5 == 0:
            fd(25)
            jump(-radius-25)
        else:
            dot(3)
            jump(-radius)
        rt(6)

def setup():
    global second_hand, minute_hand, hour_hand, writer
    mode("logo")
    make_hand_shape("second_hand", 135, 25)
    make_hand_shape("minute_hand",  105, 25)
    make_hand_shape("hour_hand", 80, 25)
    clockface(160)
    second_hand = Turtle()
    second_hand.shape("second_hand")
    second_hand.color("black", "black")
    minute_hand = Turtle()
    minute_hand.shape("minute_hand")
    minute_hand.color("black", "black")
    hour_hand = Turtle()
    hour_hand.shape("hour_hand")
    hour_hand.color("black", "black")
    for hand in second_hand, minute_hand, hour_hand:
        hand.resizemode("user")
        hand.shapesize(1, 1, 3)
        hand.speed(0)
    ht()
    writer = Turtle()
    writer.ht()
    writer.pu()
    writer.bk(85)

def week(t):
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return week[t.weekday()]

def month(z):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    a = z.year
    b = months[z.month - 1]
    c = z.day
    return "%d %s %d" % (c, b, a)

def tick():
    t = datetime.today()
    sekunde = t.second + t.microsecond*0.000001
    minute = t.minute + sekunde/60.0
    stunde = t.hour + minute/60.0
    try:
        tracer(False)  
        writer.clear()
        writer.home()
        writer.forward(65)
        writer.write(week(t),
                     align="center", font=("Arial", 14, "bold"))
        writer.back(150)
        writer.write(month(t),
                     align="center", font=("Arial", 14, "bold"))
        writer.forward(85)
        tracer(True)
        second_hand.setheading(6*sekunde)
        minute_hand.setheading(6*minute)
        hour_hand.setheading(30*stunde)
        tracer(True)
        ontimer(tick, 1000)
    except Terminator:
        pass  

#Analog Clock Run
def analog():
    tracer(False)
    setup()
    tracer(True)
    tick()
    return "EVENTLOOP"

#Digital Clock
def digital():
    root = Tk()
    root.title("Digi Clock")
    root.resizable(0,0)
    myClock = Label(root)
    myClock['text'] = 'HH:MM:SS'
    myClock.pack()
    myClock['font'] = ('Calibri', 15)

    strftime('%H:%M:%S')

    def tic():
        myClock['text'] = strftime('        The Time Now Is        '+'''
     %H:%M:%S %p    ''')

    tic()

    def tac():
        tic()
        myClock.after(1000, tac)

    tac()

#warning messagebox user commands new file
def warning():
  context = content_text.get('1.0', END)
  if context != '\n':
    warning = messagebox.askyesno('Warning', 'Have you saved any work before you continue')
    if warning:
      return True
    else:
      return False

#new file command
def new_file(event=None):
  if warning():
    content_text.delete('1.0', END)
    window.title('Untitled')
    saveBoxName.delete('1.0', END)
    saveBoxName.insert(END, "Enter Path of File(.txt)")
  else:
    return True

#open a file with text from a directory
def open_file(event=None):
  path = filedialog.askopenfilename(initialdir="/", filetypes = (("All Files", "*.*"), ("Text Files", "*.txt"), ("Word Files", "*.docx")))
  data = open(path,"r").read()
  content_text.insert('1.0', data)
  window.title(os.path.basename(path))
  saveBoxName.delete('1.0', END)
  saveBoxName.insert('1.0', path)
  return

#save file user has to enter the path in the box at the bottom of the window
def save_file(event=None):
  savefile = open(str(saveBoxName.get('1.0', 'end-1c')), 'w+')
  text = content_text.get('1.0', 'end-1c')
  savefile.write(str(text))
  savefile.close()

#save file as... filedialog appears
def save_as_file(event=None):
  name = filedialog.asksaveasfile(mode='w+', defaultextension="*.txt")
  text2save = str(content_text.get(0.0, END))
  name.write(text2save)
  text = path.get('1.0', 'end-1c')
  saveBoxName.insert(str(path))
  saveBoxName.close()
  name.close()

#Font types the text font will change
def Courier():
  global text
  content_text.config(font="Courier")
def Arial():
  global text
  content_text.config(font="Arial")
def Calibri():
  global text
  content_text.config(font="Calibri")
def Times():
  global text
  content_text.config(font="Times")
def Symbol():
  global text
  content_text.config(font="Symbol")
def Algerian():
  global text
  content_text.config(font="Algerian")
def Coral():
  global text
  content_text.config(font="Coral")

#File Menu commands...
file_menu.add_command(label="New", accelerator='Ctrl+n', compound='left', image=new_file_icon, underline=0, command=new_file)
file_menu.add_command(label="Open", accelerator='Ctrl+o', compound='left', image=open_file_icon, underline=0, command=open_file)
file_menu.add_command(label="Save", accelerator='Ctrl+s', compound='left', image=save_file_icon, underline=0, command=save_file)
file_menu.add_command(label="Save As", accelerator='Ctrl+Shift+s', compound='left', image=save_file_icon, underline=0, command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator='Alt-F4', compound='left', image=exit_file_icon, underline=0, command=window.destroy)

#editing menu commands...
def undo():
    content_text.event_generate("<<Undo>>")
    return "break"

def redo():
    content_text.event_generate("<<Redo>>")
    return 'break'

def cut():
    content_text.event_generate("<<Cut>>")
    return "break"

def copy():
    content_text.event_generate("<<Copy>>")
    return "break"

def paste():
    content_text.event_generate("<<Paste>>")
    return "break"

def select_all(event=None):
    content_text.tag_add(SEL, "1.0", END)

#edit menu commands...
edit_menu.add_command(label="Undo", accelerator='Ctrl+z', 
    compound='left', image=undo_icon, underline=0, command=undo)
edit_menu.add_command(label="Redo", accelerator='Ctrl+y', 
    compound='left', image=redo_icon, underline=0, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", accelerator='Ctrl+x', 
    compound='left', image=cut_icon, underline=0, command=cut)
edit_menu.add_command(label="Copy", accelerator='Ctrl+c', 
    compound='left', image=copy_icon, underline=0, command=copy)
edit_menu.add_command(label="Paste", accelerator='Ctrl+v', 
    compound='left', image=paste_icon, underline=0, command=paste)
edit_menu.add_command(label="Select All", accelerator='Ctrl+a', command=select_all)

#help or about the program
def about():
  messagebox.showinfo('About', '''This Program is a Text Editor.
Enter the path of a file with (.txt) at the end in the text box at the bottom.
For Example (C:\ADMIN\Desktop\hello.txt)
A text file will be created of the (.txt) file you entered in the box at the bottom.
So "hello" named file will be created on your Desktop.'''
              )
#tool
def wordCount(event=None):
  userText = content_text.get("1.0", END)
  wordList = userText.split()
  number_of_words = len(wordList)
  messagebox.showinfo('Word Count', 'Words: ' + str(number_of_words))

#about menu commands...
about_menu.add_command(label="About", compound='left', image=about_icon, underline=0, command=about)

#tool menu commands...
tool_menu.add_command(label="Show Word Count", compound='left', image=wordcount_icon, underline=0, command=wordCount)
tool_menu.add_separator()
tool_menu.add_radiobutton(label="Analog Clock", compound='left', image=clock_icon, underline=0, command=analog)
tool_menu.add_command(label="Digital Clock", compound='left', image=digi_clock, underline=0, command=digital)
tool_menu.add_separator()
tool_menu.add_radiobutton(label="Courier",command=Courier)
tool_menu.add_radiobutton(label="Arial",command=Arial)
tool_menu.add_radiobutton(label="Calibri",command=Calibri)
tool_menu.add_radiobutton(label="Times New Roman",command=Times)
tool_menu.add_radiobutton(label="Symbol",command=Symbol)
tool_menu.add_radiobutton(label="Algerian",command=Algerian)
tool_menu.add_radiobutton(label="Coral",command=Coral)

#TEXTBOX Frame
content_text = Text(window, wrap='word', undo=100)
content_text.pack(expand='yes', fill='both')

yscroll = Scrollbar(content_text, orient=VERTICAL)
content_text.configure(yscrollcommand=yscroll.set)
yscroll.config(command=content_text.yview)
yscroll.pack(side='right', fill='y')

xscroll = Scrollbar(content_text, orient=HORIZONTAL)
content_text.configure(xscrollcommand=xscroll.set)
xscroll.config(command=content_text.xview)
xscroll.pack(side='bottom', fill='x')

#keyboard shortcuts
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-s>', save_file)
content_text.bind('<Control-Shift-s>', save_as_file)
content_text.bind('<Control-w>', wordCount)

#the textbox at the bottom where directory path is inserted or path has to be written
saveBoxName = Text(window, width=100, height=1)
saveBoxName.insert(END, "Path Of The Text File")
saveBoxName.pack()

#Running the program
window.config(menu=menu_bar)
window.mainloop()
