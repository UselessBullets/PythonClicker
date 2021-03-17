import sys
import subprocess
import tkinter as tk
from tkinter import ttk # And God said "Let there be an almost idetical clone of the tk class so that if one tries to understand they shall perish"
from tkinter import *
from tkinter.ttk import *
import time
import math
import ClickerEngine as ce



# loads the game class to engine
engine = ce.game()

def buyUpgradeFunc(index):
    engine.buyUpgrade(index)
    createButtons()

def loadButtonFunc():
    engine.loadSave()
    createButtons()

def updateText():
    cpsDisplay.config(text = "CPS:" + str(math.floor(engine.calcCPS())))
    amountDisplay.config(text = "Cookies:" + str(math.floor(engine.cookies)))
    clickUpgradeCost.config(text="Price:"+str(engine.calcPowerPrice()))
    clickPower.config(text="Power of Clicks:"+str(round(engine.powerAmount * (engine.rateModifiers[0]))))
    autoAmountDisplay.config(text="Number of Auto:"+str(engine.autoAmount))
    autoCostDisplay.config(text="Price:"+str(engine.calcAutoPrice()))

    #upgradeText()

def dynUpgrade():
    x = 0
    for pair in buttonDesc:
        pair[0].config(text="Buy:" + engine.upgrades[x].name)
        pair[1].config(text="Name:" + engine.upgrades[x].name + "\nCost:" + str(engine.upgrades[x].price) + "\nDescription: " + engine.upgrades[x].description)
        x += 1

#Make window
root = tk.Tk()
root.config(bg="#33393b")
root.wm_geometry("640x720")
root.title('Clicker')

root.tk.call("lappend", "auto_path", "./resources/awthemes-10.2.1")
root.tk.call("package", "require", "awdark")

s = ttk.Style(root)
s.theme_use("awdark")

imgCookie = PhotoImage(file = r"./resources/cookie.png")
Cookieimage = imgCookie.subsample(20,20)

#Make frame
frame = ttk.Frame(root, relief="sunken")
frame.grid(row=0,column=0,sticky="news")
#Cookie Button
cookieButton = ttk.Button(frame, text='Cookies',command = lambda: engine.changeCookies(engine.powerAmount * (engine.rateModifiers[0])), image=Cookieimage)
cookieButton.pack(padx=50,pady=10)
#Count cookies and display
amountDisplay = ttk.Label(frame, text="Cookies:"+str(engine.cookies),font="Courier")
amountDisplay.pack()

#CPS Display
cpsDisplay = ttk.Label(frame, text = "CPS:" + str(math.floor(engine.calcCPS())), font="Courier")
cpsDisplay.pack()


#Upgrade Button
clickUpgradeButton = ttk.Button(frame, text='Click Power + 1',command = lambda: engine.changePower(1))
clickUpgradeButton.pack(padx=50,pady=20)
#Count power and display
clickUpgradeCost = ttk.Label(frame, text="Price:"+str(engine.calcPowerPrice()), font="Courier")
clickPower = ttk.Label(frame, text="Power of Clicks:"+str(engine.powerAmount * (1 + engine.rateModifiers[0])))
clickUpgradeCost.pack()
clickPower.pack()

#Auto Button and Display
autoClickerButton = ttk.Button(frame, text='Auto + 1',command = lambda: engine.changeAutoAmount(1))
autoClickerButton.pack(padx=50,pady=20)

autoAmountDisplay = ttk.Label(frame, text="Number of Auto:"+str(engine.autoAmount))
autoCostDisplay = ttk.Label(frame, text="Price:"+str(engine.calcAutoPrice()))
autoCostDisplay.pack()
autoAmountDisplay.pack()

#Save and load buttons
saveButton = ttk.Button(frame, text='Save',command = engine.saveGame)
loadButton = ttk.Button(frame, text='Load',command = loadButtonFunc)
saveButton.pack(pady=(10,0))
loadButton.pack(pady=(2,5))

#Upgrades
upgradeFrame = ttk.Frame(root, relief="sunken")
upgradeFrame.grid(row=0, column=2, sticky="n")

upgradeTitle = ttk.Label(upgradeFrame, text="Upgrades", font=("TkDefaultFont",20))
upgradeTitle.pack(pady=(5,0),anchor="n")

buttonDesc = []
maxButtons = 4

def createButtons():
    global buttonDesc
    for pair in buttonDesc: #Removes all old buttons from window in prep for the new ones. Without this they dont go away after they are removed from the list
        pair[0].pack_forget()
        pair[1].pack_forget()

    buttonDesc = [] #Resets list
    # TODO figure out how to fucking achieve dynamic lambda creation
    lambHell = [lambda:buyUpgradeFunc(0),lambda:buyUpgradeFunc(1),lambda:buyUpgradeFunc(2),lambda:buyUpgradeFunc(3),lambda:buyUpgradeFunc(4),lambda:buyUpgradeFunc(5),lambda:buyUpgradeFunc(6),lambda:buyUpgradeFunc(7)]

    if len(engine.upgrades) >= maxButtons:
        for x in range(0, maxButtons):
            pair = (ttk.Button(upgradeFrame, text="Upgrade", command=lambHell[x]), ttk.Label(upgradeFrame, text="Upgrade Description", wraplength=200, justify = "left"))
            pair[0].pack(pady=(15,0),expand=True,anchor="n")
            pair[1].pack(padx=5,pady=(0,5),anchor="n")
            buttonDesc.append(pair)
    elif len(engine.upgrades) < maxButtons:
        for x in range(0, len(engine.upgrades)):
            pair = (ttk.Button(upgradeFrame, text="Upgrade", command=lambHell[x]), ttk.Label(upgradeFrame, text="Upgrade Description", wraplength=200, justify = "left"))
            pair[0].pack(pady=(15,0),expand=True,anchor="n")
            pair[1].pack(padx=5,pady=(0,5),anchor="n")
            buttonDesc.append(pair)

    dynUpgrade()

createButtons()



#Main Game Loop
deltaTime = 0
while True:
    startTime = time.time()
    
    updateText()
    
    engine.changeCookies(engine.calcCPS()*deltaTime) #Current cps multiplied by the number of seconds it took to complete last frame
    root.update() #Allows window to function

    deltaTime = time.time() - startTime #Time it took for the frame to "render"
