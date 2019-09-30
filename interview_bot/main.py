from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import speech_recognition as sr
from os import system
import random
import time
from threading import Thread
import time
from interviewProgram import startInterview


def getstatus():
    fh = open('new.txt','r')
    return fh.read()


class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 1

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
            #pass
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)




def showTalk():
    root.configure(background='black')
    #global ShowTextFrame
    Analyseframe = Frame(root,borderwidth = 0,highlightthickness = 0)
	#newframe.grid(row = 2)
    Analyseframe.grid(row=0 , column=0,padx=250, pady=50)
    lbl = ImageLabel(Analyseframe,borderwidth = 0,highlightthickness = 0)
    lbl.grid(row = 1, column =1)
    lbl.load('talk3.gif')


def chooseframe(CVframe):
    CVframe.grid_forget()
    showTalk()




def callback_threaded(event):
    global entry_name, entry_cpi,entry_projects1,entry_projects2,entry_projects3
    global entry_programingLanguages, entry_POR1,entry_POR2,entry_POR3
    name = entry_name.get()
    cpi = entry_cpi.get()
	
    project1 = entry_projects1.get()
    project2 = entry_projects2.get()
    project3 = entry_projects3.get()
    programmingLanguages = entry_programingLanguages.get()
    POR1 = entry_POR1.get()
    POR2 = entry_POR2.get()
    POR3 = entry_POR3.get()
	
    th0 = Thread(target = chooseframe, args = (CVframe,) )
    th0.daemon = True
    th0.start()

    th1 = Thread(target=callback1,args=(10,name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3,))
    th1.daemon = True
    th1.start()

def do_that(name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3):
    time.sleep(1)
    firstname = list(name.split(' '))[0]

    saynew = "Hi  "+ name + ", hope you are comfortable!"
    system('say %s' % (saynew))
    time.sleep(1)
    startInterview(root,name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3)



def do_something(name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3):
    for c in range(10**2):
        c = c+1
    th2 = Thread(target=callback2,args=(10,name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3))
    th2.daemon = True
    th2.start()
    


def callback1(i,name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3):
    #total = sum(1 for _ in range(10**8)) # <-- slow
    #showinfo(str(total))
    #print (total)
    #Thread(target=callback).stop()
    i =0
    if getstatus() != '5':
        print("thread 1 is running")
        print("inside 1 ",getstatus())

        do_something(name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3)
        print ("\n-----Done here----\n")
        target = open('new.txt','w')
        target.write(str(i))
        i += 1
       



def callback2(i,name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3):
    #total = sum(1 for _ in range(10**8)) # <-- slow
    #showinfo(str(total))
    #print (total)
    #Thread(target=callback).stop()
    i =0
    if getstatus() != '8':
        print("thread 2 is running")
        print("inside 2 ",getstatus())

        do_that(name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3)
        target = open('new.txt','w')
        target.write(str(i))
        





	






global root

root = Tk()
root.configure(background='black')
root.minsize(width=800, height=500)

CVframe = Frame(root, background = 'black')
CVframe.grid(row = 1)

name = Label(CVframe,text="Name:",background = 'black',fg = 'white')
cpi = Label(CVframe,text="Easy/Medium/Tough:",background = 'black',fg = 'white')
projects = Label(CVframe,text="Title of Most Important Projects:", background='black',fg = 'white')
programmingLanguages = Label(CVframe,text="Strong Technical Points(separate by commas): ",background='black',fg = 'white')
POR = Label(CVframe,text="Position of Responsibility: ",background='black',fg = 'white')


entry_name = Entry(CVframe, bd=3)
entry_cpi = Entry(CVframe, bd=3)
entry_projects1 = Entry(CVframe, bd=3)
entry_projects2 = Entry(CVframe, bd=3)
entry_projects3 = Entry(CVframe, bd=3)

entry_programingLanguages = Entry(CVframe,bd=3)

entry_POR1 = Entry(CVframe, bd=3)
entry_POR2 = Entry(CVframe, bd=3)
entry_POR3 = Entry(CVframe, bd=3)

#sticky N E S W north east south west

name.grid(row=0,column = 0,sticky = E,padx=10, pady=10)
entry_name.grid(row = 0, column = 1,padx=10, pady=10)

cpi.grid(row=1,column = 0,sticky =E,padx=10, pady=10)
entry_cpi.grid(row=1,column = 1,padx=10, pady=10)

projects.grid(row = 2,column = 0,sticky =E,padx=10, pady=5 )
entry_projects1.grid(row=3,column = 1,sticky = E,padx=10, pady=5)
entry_projects2.grid(row=4,column = 1,sticky = E,padx=10, pady=5)
entry_projects3.grid(row=5,column = 1,sticky = E,padx=10, pady=5)

programmingLanguages.grid(row = 8,column=0,sticky = E,padx=10, pady=10 )
entry_programingLanguages.grid(row = 8,column = 1,sticky = E,padx=10, pady=10)

POR.grid(row = 10,column = 0,sticky = E,padx=10, pady=5)
entry_POR1.grid(row = 11,column=1,sticky = E,padx=10, pady=5)
entry_POR2.grid(row = 12,column=1,sticky = E,padx=10, pady=5)
entry_POR3.grid(row = 13,column=1,sticky = E,padx=10, pady=10)


#entry_1.focus_set()



submit = Button(CVframe, text = 'submit',padx = 50,fg= 'black',activeforeground = 'gray')
submit.grid(row = 20, column = 1)
submit.bind("<Button-1>",callback_threaded)






# Converseframe = Frame(root)
# Converseframe.grid(row = 1)
root.title('Smart Interview Bot')
root.mainloop()




############# UI END ############################################
