from Tkinter import * # get a widget object
import tkFont
import sys
import os
sys.path.append(os.environ['FUZZY_ADVENTURE'])
from executable import *

def quit(): # a custom callback handler
    print('Hello, I must be going...') # kill windows and process
    sys.exit()

def handler(name):
    print(name)

def temp():
    handler('spam')

root = Tk()
#Button(root, text='Exit', command=handler('spam')).pack(side=LEFT, expand=YES, fill=X)
root.title('Fuzzy Adventure')
#root.iconbitmap('saplogo.ico')
root.minsize(600,100)
root.resizable(width=FALSE, height=FALSE)
root.configure(background='#3F464D')


e = Entry(font=('Baskerville Old Face', 13))
e.pack(fill=X, padx=20, pady=5)

l = Label(background='#3F464D', fg='#D1D9E0')
l.pack()


def query(event):
    question = e.get()
    print question
    if question is not '' and question is not None:
        answer, lat_type = FuzzyAdventure.to_sql(question)
        l.config(text=answer)
    
def quit(event): 
    l.config(text='I must be going, my planet needs me!')
    print('I must be going, my planet needs me!') # event gives widget, x/y, etc.
    sys.exit()


l2 = Label(bg='#67717A')
l2.pack(side=BOTTOM, fill=X, padx=20, pady=(10,5))
l2.bind('<B1-Motion>', quit)

button_font = tkFont.Font(family='Baskerville Old Face', size=11)
widget = Button(None, text='Answer Me!', relief='groove', bg='#67717A', fg='#D1D9E0', bd=0, font=button_font)
widget.pack(padx=5, pady=5)

widget.bind('<Button-1>', query)

root.mainloop()


"""
class HelloCallable:
    def __init__(self): # __init__ run on object creation
        self.msg = 'Hello __call__ world'
    def __call__(self):
        print(self.msg) # __call__ run later when called
        sys.exit() # class object looks like a function
widget = Button(None, text='Hello event world', command=HelloCallable())
widget.pack()
widget.mainloop()
"""