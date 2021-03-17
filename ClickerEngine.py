import tkinter as tk
import time
import math
import json
import jsonpickle
from json import JSONEncoder


class upgrade():
    name = "Auto Upgrade"
    description = "Each auto does double CPS."
    price = 1
    upgradeType = 1 #0 is manual clicking, 1 are autos
    multiplier = 2

    def __init__(self, name = "Auto Upgrade", description = "Each auto does double CPS.", price = 1, upgradeType = 1, multiplier = 2):
        self.name = name
        self.description = description
        self.price = price
        self.upgradeType = upgradeType
        self.multiplier = multiplier

class game():
    cookies = 0
    powerAmount = 1
    autoAmount = 0
    boughtUpgrades = []

    gift = upgrade(name="Gift", description="I wanted to test if this would work", price=-100, multiplier=1)
    autoUp1 = upgrade(name="Auto Upgrade (1)", price=10)
    autoUp2 = upgrade(name="Auto Upgrade (2)", price=50)
    autoUp3 = upgrade(name="Auto Upgrade (3)", price=100)
    autoUp4 = upgrade(name="Auto Upgrade (4)", price=500, multiplier=4, description="Each auto does quadruple CPS.")
    clickUp1 = upgrade(name="Power Upgrade (1)", price=20, multiplier=2, description="Doubles the power of clicks.", upgradeType=0)
    clickUp2 = upgrade(name="Power Upgrade (2)", upgradeType=0, multiplier=3, description="Triples the power of clicks.", price=300)

    upgrades = [gift,autoUp1,clickUp1,autoUp2,autoUp3,clickUp2,autoUp4]

    rateModifiers = [1.0, 1.0] #Clicker, Auto

    #Functions
    def calcPowerPrice(self):
        """Calculates and then returns the current price of a power upgrage"""

        self.calcRateMod()
        return 5 * (2**(self.powerAmount-1)) #Starts at a price of 5 and doubles every additional purchase

    def calcCPS(self): #sets the cps variable to the value it should currently be
        """Calculates and then returns the current CPS"""

        return (self.autoAmount * (self.rateModifiers[1]))

    def changeCookies(self, amount): #adds the amount specified to the cookie variable
        """Adds the specified amount to the total cookie amount"""

        self.cookies += amount

    def changePower(self, amount): #checks if you can afford the power increase and then increases the power amount
        """Determines how many of the specief amount a powerupgrades that can be purchased and
        then adds them to your power amount"""

        for x in range(0,amount):
            if (self.cookies >= self.calcPowerPrice()):
                self.changeCookies(-1 * self.calcPowerPrice())
                self.powerAmount += 1

    def calcAutoPrice(self):
        """Calculates and then returns the current price of an auto clicker"""

        return 10 * (2**(self.autoAmount)) #Starts at a price of 10 and doubles every additional purchase
    
    def calcRateMod(self): #sets the rate mods to the values they should currently be
        """Calculates the current value the rate mod should be and then changes it to be that value"""

        self.rateModifiers = [1.0,1.0]
        for x in self.boughtUpgrades:
            if x.upgradeType == 0:
                self.rateModifiers[0] = self.rateModifiers[0] * x.multiplier
            elif x.upgradeType == 1:
                self.rateModifiers[1] = self.rateModifiers[1] * x.multiplier

    def changeAutoAmount(self, amount): #Tries to buy the specified amount of autos but will not exceed the amount possible
        """Determines how many of the specief amount of Autos that can be purchased and
        then adds them to your Auto amount"""

        for x in range(0,amount):
            if self.cookies >= self.calcAutoPrice():
                self.cookies -= self.calcAutoPrice()
                self.autoAmount += 1
    
    def buyUpgrade(self, index): #Buys upgrade, removes it from the avaliable upgrades and adds it to the purchased upgrades list
        """Attempts to buy upgrade from the specifed index and then adds that upgrade to your bought upgrades list,
         removes it from the upgrades list, and deducts the price of the upgrade"""

        if (self.upgrades[index] != 0 and self.upgrades[index].price <= self.cookies):
            self.cookies -= self.upgrades[index].price
            self.boughtUpgrades.append(self.upgrades[index])
            del self.upgrades[index]
        self.calcRateMod()

    def saveGame(self): #saves current game conditions to save.txt
        """Saves the current game variables to save.txt in a json format"""

        save = [self.cookies, self.powerAmount, self.autoAmount, self.boughtUpgrades, self.upgrades, self.rateModifiers]
        save[3] = jsonpickle.encode(self.boughtUpgrades, unpicklable=True)
        save[4] = jsonpickle.encode(self.upgrades, unpicklable=True)
        with open("save.txt", "w") as writer:
            json.dump(save,writer,indent=4)
            writer.close
            print("Game Saved")

    def loadSave(self): #loads saved game conditions to save.txt and then assigns them to the game variables
        """Loads the json formated variables and sets them to the current game variables"""

        with open("save.txt", "r") as reader:
            self.boughtUpgrades = []
            self.upgrades = []

            save = json.load(reader)
            self.cookies = save[0]
            self.powerAmount = save[1]
            self.autoAmount = save[2]
            self.boughtUpgrades = jsonpickle.decode(save[3])
            self.upgrades = jsonpickle.decode(save[4])
            self.rateModifiers = save [5]
            reader.close
            print("Save Loaded")
