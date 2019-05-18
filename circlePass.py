from os import path
from random import *
from math import sqrt
from collections import Counter
import Tkinter as tk
import tkFileDialog
import tkMessageBox
import sys
import time

CANVAS_SIZE   = 500
CIRCLE_COUNTS = [4,4,4]
BOX_COUNTS    = [4,7,10]
VARIATIONS    = ["Phone","Facebook","Bank"]

## set up timer --------------------------------------------------##
def startTimer():
    return float(round(time.time() * 1000))
def endTimer(start):
    return (float(round(time.time()*1000)) - start)/1000
## -------------------------------------------------------------- ##

def center(win):
    '''center the GUI window'''
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width =  width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    if win.attributes('-alpha') == 0:
        win.attributes('-alpha', 1.0)
    win.deiconify()

def putOnTop(event):
    '''makes the GUI window remain on top'''
    event.widget.unbind('<Visibility>')
    event.widget.withdraw()
    event.widget.deiconify()
    event.widget.update()
    event.widget.lift()
    center(event.widget)
    event.widget.bind('<Visibility>', putOnTop)

def getClosestPoint(point,points):
    '''Returns index of closest point from 'point' in points list'''
    distances = [(pow(p[0]-point[0],2) + \
                  pow(p[1]-point[1],2),p) for p in points]
    return points.index(min(distances)[1])

class MyCanvas():
    "A custom tk canvas container"

    def __init__(self,parent,username,passType,numC,numB):
        '''create canvas'''
        # initialize attributes
        self.PASS_TYPE   = passType
        self.NUM_CIRCLES = numC
        self.NUM_BOXES   = numB
        self.CIRCLE_SIZE = int((CANVAS_SIZE/self.NUM_BOXES-\
                               (CANVAS_SIZE/self.NUM_BOXES/5))/2)
        self.BOX_SIZE    = CANVAS_SIZE/self.NUM_BOXES
        self.username = username
        self.canvas = tk.Canvas(parent,width=CANVAS_SIZE,height=CANVAS_SIZE)
        self.canvas.config(background="black")
        self.dragData = {"x":0,"y":0,"circle":0}
        self.circles = {}
        self.boxCentres = []
        self.start = 0    # will be set to startTimer
        self.training = 0 # number of times trained
        self.attempts = 0 # number of password attempts
        self.hidden = True
        self.stats = []
        
        # draw grid
        self.setupGrid()
        
        # add interactions
        self.canvas.tag_bind("circle","<ButtonPress-1>",self.onCirclePress)
        self.canvas.tag_bind("circle","<ButtonRelease-1>",self.onCircleRelease)
        self.canvas.tag_bind("circle","<B1-Motion>",self.onCircleMotion)

        self._password = self._generatePassword()
        
    def show(self):
        self.generateCircles()
        self.canvas.grid(column=0,row=0,columnspan=3)
        self.hidden = False

    def hide(self):
        self.canvas.grid_forget()
        self.hidden = True

    def _generatePassword(self):
        '''generate a unique password'''
        password = []
        for _ in range(0,self.NUM_CIRCLES):
            password.append(1+int(random()*len(self.boxCentres)))
        password.sort()
        return password
        
    def displayPassword(self):
        '''displays a message box that shows the password'''
        tkMessageBox.showinfo(self.PASS_TYPE+" password - Training "+\
            str(self.training+1),"You have been assigned \nthe following "+\
            self.PASS_TYPE+" password:\n"+\
            ','.join([str(p) for p in self._password])+\
            "\nDrag and drop the circles into the correct squares.")
   
    def displayStart(self):
        '''displays a message box that shows the password'''
        tkMessageBox.showwarning("Get Ready!",\
            "Please enter your "+self.PASS_TYPE+" password.")
        self.start = startTimer()

    def setupGrid(self):
        ''' create canvas grid'''
        
        # clear canvas
        self.canvas.delete("all")
        
        # draw lines
        jump = self.BOX_SIZE
        for i in range(0,self.NUM_BOXES):
            self.canvas.create_line(i*jump,0,\
                           i*jump,CANVAS_SIZE,fill="blue")
            self.canvas.create_line(0,i*jump,\
                           CANVAS_SIZE,i*jump,fill="blue")
        # get box centres
        for i in range(0,self.NUM_BOXES):    
            for j in range(self.NUM_BOXES):
                self.boxCentres.append((((j*jump)+(jump/2)),\
                                       ((i*jump)+(jump/2))))
        # draw numbers
        for i,c in enumerate(self.boxCentres):
            self.canvas.create_text(c[0],c[1],anchor="n",\
                                    text=str(i+1),fill="white")

    def generateCircles(self):
        '''generate circles'''
        
        #clear previous circles
        self.circles = {}
        self.canvas.delete("circle")
        
        # randomly assign circle locations 
        locations = []
        for i in range(0,self.NUM_CIRCLES):
            while 1:
                overlapping = False
                point = self.boxCentres[int(random()*len(self.boxCentres))]
                for loc in locations:
                    if point==loc:
                        overlapping = True
                        break
                if not overlapping:
                    break
            locations.append((point[0],point[1]))

        # draw circles and add to circles dictionary
        for loc in locations:
            self.circles[\
            self.canvas.create_oval(loc[0]-self.CIRCLE_SIZE,\
                                    loc[1]-self.CIRCLE_SIZE,\
                                    loc[0]+self.CIRCLE_SIZE,\
                                    loc[1]+self.CIRCLE_SIZE,\
                                    outline="white", width=3,\
                                    fill="red", tags="circle")] = loc

    def checkBounds(self,event):
        '''check if mouse is within bounds'''
        if event.x<self.BOX_SIZE/3 or event.x>CANVAS_SIZE-self.BOX_SIZE/3 or \
           event.y<self.BOX_SIZE/3 or event.y>CANVAS_SIZE-self.BOX_SIZE/3:
            if self.dragData["circle"]:
                self.canvas.itemconfig(self.dragData["circle"], fill="red")
                self.canvas.coords(self.dragData["circle"],\
                           event.x-self.CIRCLE_SIZE,\
                           event.y-self.CIRCLE_SIZE,\
                           event.x+self.CIRCLE_SIZE,\
                           event.y+self.CIRCLE_SIZE)
                newX = self.boxCentres[getClosestPoint(\
                    (event.x,event.y),self.boxCentres)][0]
                newY = self.boxCentres[getClosestPoint(\
                    (event.x,event.y),self.boxCentres)][1]
                self.canvas.coords(self.dragData["circle"],\
                           newX-self.CIRCLE_SIZE,\
                           newY-self.CIRCLE_SIZE,\
                           newX+self.CIRCLE_SIZE,\
                           newY+self.CIRCLE_SIZE)
                self.circles[self.dragData["circle"][0]] = (newX, newY)
                self.dragData["circle"] = 0
                self.dragData["x"] = 0
                self.dragData["y"] = 0
            return False
        return True

    def onCirclePress(self,event):
        '''record circle and location'''
        if not self.checkBounds(event): return
        self.dragData["circle"] = self.canvas.find_closest(\
            event.x, event.y, halo=self.CIRCLE_SIZE)
        self.canvas.itemconfig(self.dragData["circle"], fill="green")
        self.canvas.coords(self.dragData["circle"],\
                           event.x-int(self.CIRCLE_SIZE*1.2),\
                           event.y-int(self.CIRCLE_SIZE*1.2),\
                           event.x+int(self.CIRCLE_SIZE*1.2),\
                           event.y+int(self.CIRCLE_SIZE*1.2))
        self.dragData["x"] = event.x
        self.dragData["y"] = event.y
        
    def onCircleRelease(self,event):
        '''end drag of a circle'''
        if not self.checkBounds(event): return
        self.canvas.itemconfig(self.dragData["circle"], fill="red")
        self.canvas.coords(self.dragData["circle"],\
                           event.x-self.CIRCLE_SIZE,\
                           event.y-self.CIRCLE_SIZE,\
                           event.x+self.CIRCLE_SIZE,\
                           event.y+self.CIRCLE_SIZE)
        newX = self.boxCentres[getClosestPoint(\
                    (event.x,event.y),self.boxCentres)][0]
        newY = self.boxCentres[getClosestPoint(\
                    (event.x,event.y),self.boxCentres)][1]
        self.canvas.coords(self.dragData["circle"],\
                           newX-self.CIRCLE_SIZE,\
                           newY-self.CIRCLE_SIZE,\
                           newX+self.CIRCLE_SIZE,\
                           newY+self.CIRCLE_SIZE)
        self.circles[self.dragData["circle"][0]] = (newX, newY)
        self.dragData["circle"] = 0
        self.dragData["x"] = 0
        self.dragData["y"] = 0

    def onCircleMotion(self,event):
        '''handle dragging of a circle'''
        if not self.checkBounds(event): return
        deltaX = event.x - self.dragData["x"]
        deltaY = event.y - self.dragData["y"]
        self.canvas.move(self.dragData["circle"],deltaX,deltaY)
        self.dragData["x"] = event.x
        self.dragData["y"] = event.y

    def circles2Password(self):
        '''generates password from the circle locations'''
        attempt = []
        for _,loc in self.circles.iteritems():
            closestPoint = getClosestPoint(loc,self.boxCentres)
            attempt.append(1+closestPoint)
        return attempt

    def confirmPassword(self):
        '''initial confirmation to check if user has the assigned password memorized'''
        # add data to stats
        attempt = self.circles2Password()
        success = Counter(attempt) == Counter(self._password)
        if success:
            tkMessageBox.showinfo("Password Correct",\
                                  "Press 'Ok' to continue...")
            self.training+=1
            self.hide()
            return True
        else:
            tkMessageBox.showinfo("Password Incorrect","Your password is\n"+\
            ','.join([str(p) for p in self._password])+"\nPlease Try Again!")
            return False

    def verifyPassword(self):
        '''verifies if attempted password matches assigned password'''
        endTime = str(endTimer(self.start))
        # add data to stats
        attempt = self.circles2Password()
        success = Counter(attempt) == Counter(self._password)
        numCorr = str(len(self._password))
        if success==True: success='yes' 
        else:
            success='no'
            diff = Counter(attempt) - Counter(self._password)
            numCorr = str(len(self._password)-len(diff))
        self.stats = [self.username, self.PASS_TYPE, str(len(self._password)),\
                      str(self.NUM_BOXES),success,numCorr,endTime]
        self.saveStats()
        # prompt to try again
        if success=='no':
            if self.attempts == 0:
                tkMessageBox.showwarning("Login Failed!",\
                    "Time spent logging in:\n\n    "+endTime+" sec."+\
                    "\n\n    Please try your "+self.PASS_TYPE+\
                    "\n    password again.")
                self.start = startTimer()
            elif self.attempts == 1:
                tkMessageBox.showwarning("Login Failed!",\
                    "Time spent logging in:\n\n    "+endTime+" sec."+\
                    "\n\n    Please try your "+self.PASS_TYPE+\
                    "\n    password one last time.")
                self.start = startTimer()
            else:
                tkMessageBox.showwarning("Login Failed!",\
                    "Time spent logging in:\n\n    "+endTime+" sec."+\
                    "\n\n    No more attempts. Click 'Ok' to continue...")
                self.hide()
                return True
            self.attempts+=1
            return False
        else:
            tkMessageBox.showinfo("Login Successful!",\
                  "Time spent logging in:\n\n    "+endTime+" sec."+\
                "\n\n    Good Job! Click 'Ok' to continue...")
            self.hide()
            self.start = startTimer()
            return True

    def saveStats(self):
        if not self.stats:
            return
        exists = path.exists("stats.csv")
        csv = open("stats.csv",'a')
        if not exists:
            csv.write("username passType numCircles "+\
                      "numBoxes success numCorrect time(sec)")
        csv.write('\n'+' '.join(self.stats))
        csv.close()
        del self.stats[:]

class CanvasGroup():
    "contains all canvases and methods to manage them"
    
    def __init__(self,canvasFrame,buttonFrame,rootFrame):
        '''initialize Canvas Group
        canvasFrame: the tk frame where the 3 canvases are displayed
        buttonFrame: the tk frame where the buttons are displayed
        rootFrame: the root tk frame'''
        self.frame = canvasFrame
        self.root = rootFrame
        self.confirm = tk.Button(buttonFrame,width=CANVAS_SIZE/30,text="Confirm",\
                                 command=self.confirmPassword)
        self.exit    = tk.Button(buttonFrame,width=CANVAS_SIZE/30,text="Exit",\
                                 command=lambda: sys.exit(0))
        self.confirm.pack(side=tk.TOP)
        self.exit.pack(side=tk.TOP)
        self.runMain()

    def reset(self,username):
        self.username = username
        self.canvas = []
        for i in range(0,3):
            self.canvas.append(MyCanvas(\
                self.frame,self.username,VARIATIONS[i],\
                CIRCLE_COUNTS[i],BOX_COUNTS[i]))
        self.current = 0
        self.order = [0,1,2]
        shuffle(self.order)
        self.phase = 1 # 1,2,3 = training / 4,5,6 = testing
        self.confirm.configure(text="Confirm",command=self.confirmPassword)
        self.confirm['state'] = "normal"
        
    def initiate(self):
        self.canvas[self.current].show()
        self.canvas[self.current].displayPassword()

    def confirmPassword(self):
        confirmed = self.canvas[self.current].confirmPassword()
        if confirmed:
            self.canvas[self.current].hide()
            if self.canvas[self.current].training < 3:
                self.canvas[self.current].show()
                self.canvas[self.current].displayPassword()
            else: # final training stage for current password
                self.phase+=1
                if self.phase<4:
                    self.current = self.phase-1
                    self.canvas[self.current].show()
                    self.canvas[self.current].displayPassword()
                else: # FINAL password confirmed to be memorized
                    self.current = self.order[0]
                    self.canvas[self.current].show()
                    self.confirm.configure(text="Login",command=self.verifyPassword)
                    self.canvas[self.current].displayStart()
                                 
    def verifyPassword(self):
        verified = self.canvas[self.current].verifyPassword()
        if verified: 
            self.canvas[self.current].hide()
            if self.phase != 6:
                self.current = self.order[self.phase-3]
                self.canvas[self.current].show()
                self.canvas[self.current].displayStart()
                self.phase+=1
            else: # FINAL password has been verified
                if tkMessageBox.askyesno("Thank you!","Try Another Round?"):
                    self.runMain()
                else: sys.exit(0)

    def runMain(self):
        '''display username prompt and run the password tester'''
        
        def go(username):
            if username.get() != "":
                prompt.withdraw()
                root.deiconify()
                root.lift()
                root.focus_force()
                self.reset(username.get())
                self.initiate()

        center(root)
        self.confirm['state'] = tk.DISABLED
        prompt = tk.Toplevel(self.root)
        prompt.title("Welcome!")
        prompt.resizable(0,0)
        prompt.bind('<Visibility>',putOnTop)
        
        frameA   = tk.Frame(prompt)
        label    = tk.Label(prompt,text="Please enter a username:\n")
        username = tk.Entry(prompt)
        username.insert(0,""); username.focus()
        submit   = tk.Button(prompt,width=8,text="Submit",\
                             command=lambda:go(username))
        prompt.overrideredirect(1)
        frameA.pack()
        label.pack(side=tk.LEFT)
        username.pack(side=tk.LEFT)
        username.bind('<Return>',lambda event:go(username))
        submit.pack(side=tk.LEFT)
        center(prompt)
                
if __name__=="__main__":

    # create root window
    root = tk.Tk()
    root.title("Circle-Pass v0.6")
    root.geometry(str(CANVAS_SIZE)+'x'+\
                  str(CANVAS_SIZE+(CANVAS_SIZE/8)))
    root.resizable(0,0)

    # create frames
    canvasFrame = tk.Frame(root,width=CANVAS_SIZE,height=CANVAS_SIZE)
    buttonFrame = tk.Frame(root)
    
    # place frames
    canvasFrame.grid(column=0,row=0,columnspan=3)
    buttonFrame.grid(column=0,row=1,columnspan=3)

    canvases = CanvasGroup(canvasFrame,buttonFrame,root)
    root.mainloop()
