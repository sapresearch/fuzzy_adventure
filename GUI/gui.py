from Tkinter import * # get a widget object
import tkFont
from fuzzy_adventure.executable import *

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
root.wm_iconbitmap('@'+'SAP-Logo.xbm')
root.minsize(600,100)
root.resizable(width=FALSE, height=FALSE)
root.configure(background='#3F464D')


e = Entry(font=('Helvetica', 13), justify='center')
e.pack(fill=X, padx=20, pady=5)
e.focus_set()

answer_label_font = tkFont.Font(family='Helvetica', size=13)
answer_label = Label(background='#3F464D', fg='#D1D9E0', font=answer_label_font)
answer_label.pack()

def query(event):
    question = e.get()
    print question
    if question is not '' and question is not None:
        try:
            answer, lat_type = FuzzyAdventure.to_sql(question)
        except:
            answer = None
        finally:
            if answer is None: answer = 'No answer found'
            answer_label.config(text=answer)
    else:
    	answer_label.config(text='')
    print answer_label['text']
    
def quit(event): 
    answer_label.config(text='I must be going, my planet needs me!')
    print('I must be going, my planet needs me!')
    sys.exit()

def copy(event):
    answer = answer_label['text']
    if answer is not '' and answer is not None:
		root.clipboard_clear()
		root.clipboard_append(answer)

l2 = Label(bg='#67717A')
l2.pack(side=BOTTOM, fill=X, padx=20, pady=(10,5))
l2.bind('<B1-Motion>', quit)

button_font = tkFont.Font(family='Helvetica', size=11)
widget = Button(master=None, text='Answer Me!', bg='#67717A', fg='#D1D9E0', bd=1, font=button_font, relief='flat')
widget.pack(padx=5, pady=5)

widget.bind('<Button-1>', query)
widget.bind('<Button-3>', copy)
e.bind('<Return>', query)
root.bind('<Escape>', quit)
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