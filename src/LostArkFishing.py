from datetime import datetime
from math import floor
import pyautogui
import time
import random
import math
import os
from time import gmtime, strftime
from PyQt5.Qt import QThread, pyqtSignal
from PIL import Image, ImageFont, ImageDraw

class LostArkFishing(QThread):
    loggerSignal = pyqtSignal(object) # Signal to emit logging messages
    endSignal = pyqtSignal(int) # Signal to emit terminated state

    bait_buff_duration = 900 # seconds
    bait_addConsume = 60 # energy added every time you catch a fish

    def __init__(self, fish_key='e', bait_key='d', energy=10500, autorepair=False, roundrepair=50, assetPath=None):
        super().__init__()
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.state = 0
        self.count = 0
        self.fish_key = fish_key
        self.bait_key = bait_key
        self.energy = energy
        self.currentEnergy = int(energy)
        self.autorepair = autorepair
        self.autorepairMod = int(roundrepair)
        self.startBaitTime = None
        if assetPath is None:
            self.assetPath = f'resources/{self.screenHeight}'
        else :
            self.assetPath = assetPath

        if self.checkPrerequisites() == False:
            self.message("Missing prerequisites. Stopping bot now.")
            self.terminated()

    def checkPrerequisites(self):
        if os.path.exists(f"{self.assetPath}/fishing_pop.png") == False:
            self.message("Missing fishing pop. Please download it from the game.")
            return False

        if os.path.exists(f"{self.assetPath}/repair_tool.png") == False:
            self.message("Missing repair tool. Auto repair desactivated.")
            self.autorepair = False

        if os.path.exists(f"{self.assetPath}/ok.png") == False:
            self.message("Missing OK button. Auto repair desactivated.")
            self.autorepair = False      

        if os.path.exists(f"{self.assetPath}/bait.png") == False:
            self.message("Missing bait buff. Throw bait desactivated.")
            self.bait_key = None

    def pressKey(self, key):
        pyautogui.keyDown(key)
        time.sleep(random.uniform( 0.25, 0.55 ))
        pyautogui.keyUp(key)

    # Function to cast fishing rod ingame
    def castRod(self, count):
        self.message(f"Casting fishing rod. ({self.count})")

        # Cast fishing rod ingame
        self.pressKey(self.fish_key)
        time.sleep(random.uniform(4.5, 6.5))

    def repairFishingRod(self):
        # Open pet inventory
        self.message("Opening pet inventory (ALT + P).")
        pyautogui.keyDown('alt')
        pyautogui.keyDown('p')
        pyautogui.keyUp('p')
        pyautogui.keyUp('alt')

        # Sleep random amount of time
        time.sleep(random.uniform(1.0, 2.0))

        repairtool_icon_location = pyautogui.locateOnScreen(f"{self.assetPath}/repair_tool.png", confidence=0.75, grayscale=True)
        if repairtool_icon_location == None:
            self.message("Could not find repair tool icon. Cannot repair fishing rod.")
            self.message("Pressing ESC, closing pet window.")
            pyautogui.keyDown('esc')
            pyautogui.keyUp('esc')
            return

        # Small repair button offset
        self.message("Clicking on Pet Function: remote repair.")
        repair_icon_point = pyautogui.center(repairtool_icon_location)
        moveToX1 = repair_icon_point.x
        moveToY1 = repair_icon_point.y
        pyautogui.moveTo(moveToX1, moveToY1, random.uniform(0.1, 0.5))
        pyautogui.click(x=moveToX1, y=moveToY1, clicks=0, button='left')
        time.sleep(random.uniform(0.125, 0.5))
        pyautogui.click(x=moveToX1, y=moveToY1, clicks=1, button='left')

        # Sleep random amount of time
        time.sleep(random.uniform(1.0, 2.0))

        # Repair All offset
        self.message("Clicking on Repair All button.")
        xOffset = 0.384 
        yOffset = 0.688
        moveToX2 = round(self.screenWidth * xOffset)
        moveToY2 = round(self.screenHeight * yOffset)
        pyautogui.moveTo(moveToX2, moveToY2, random.uniform(0.1, 0.5))
        pyautogui.click(x=moveToX2, y=moveToY2, clicks=0, button='left')
        time.sleep(random.uniform(0.125, 0.5))
        pyautogui.click(x=moveToX2, y=moveToY2, clicks=1, button='left')

        # Sleep random amount of time
        time.sleep(random.uniform(1.5, 2.25))

        ok_btn_location = pyautogui.locateOnScreen(f"{self.assetPath}/ok.png", confidence=0.75, grayscale=True)
        if ok_btn_location == None:
            self.message("Could not find OK button. Cannot repair fishing rod.")
            self.message("Pressing ESC, closing repair window.")
            pyautogui.keyDown('esc')
            pyautogui.keyUp('esc')
            time.sleep(random.uniform(1.0, 1.5))
            self.message("Pressing ESC, closing pet window.")
            pyautogui.keyDown('esc')
            pyautogui.keyUp('esc')
            return

        # Repair OK offset
        self.message("Clicking on OK button.")
        ok_btn_point = pyautogui.center(ok_btn_location)
        moveToX3 = ok_btn_point.x
        moveToY3 = ok_btn_point.y
        pyautogui.moveTo(moveToX3, moveToY3, random.uniform(0.1, 0.5))
        pyautogui.click(x=moveToX3, y=moveToY3, clicks=0, button='left')
        time.sleep(random.uniform(0.125, 0.5))
        pyautogui.click(x=moveToX3, y=moveToY3, clicks=1, button='left')

        # Sleep random amount of time
        time.sleep(random.uniform(1.0, 2.0))

        # Press ESC
        self.message("Pressing ESC, closing repair window.")
        pyautogui.keyDown('esc')
        pyautogui.keyUp('esc')

        # Sleep random amount of time
        time.sleep(random.uniform(1.0, 2.0))

        # Press ESC
        self.message("Pressing ESC, closing pet window.")
        pyautogui.keyDown('esc')
        pyautogui.keyUp('esc')

    def throw_bait(self):
        if self.bait_key is None or self.bait_key == "":
            return

        if self.isUnderBaitBuff() == False:
            if self.startBaitTime == None:
                self.startBaitTime = datetime.now()
                elapsedTime = self.bait_buff_duration + 1
            else:
                elapsedTime = datetime.now() - self.startBaitTime
                elapsedTime = elapsedTime.total_seconds()

            if elapsedTime > self.bait_buff_duration:
                self.startBaitTime = datetime.now()
                self.pressKey(self.bait_key)
                self.message("Throwing bait.")
                time.sleep(random.uniform(2.5, 3.5))

    def isUnderBaitBuff(self):
        if self.bait_key is None:
            return False

        bait_icon_location = pyautogui.locateOnScreen(f"{self.assetPath}/bait.png", confidence=0.75, grayscale=False, region=(math.floor(self.screenWidth/4), math.floor(self.screenHeight/4 * 3), math.floor(self.screenWidth/2), math.floor(self.screenHeight/4 * 3 + 200)))
        if bait_icon_location == None:
            return False
        return True

    def message(self, msg):
        self.loggerSignal.emit("%s %s" % (strftime("%H:%M:%S", gmtime()), msg))

    def terminated(self):
        self.endSignal.emit(self.state)

    def run(self):
        self.message("Starting the bot in 5 seconds.")
        time.sleep(5)
        self.repairFishingRod()

        while True:
            if self.state == 0:
                self.count = self.count + 1
                self.throw_bait()
                self.castRod(self.count)
                self.state = 1
                self.start = datetime.now()
            else:
                time.sleep(0.1) # Sleep for 100ms, ensure CPU not 100% usage
                elapse = datetime.now() - self.start
                if elapse.total_seconds() > 20:
                    self.state = 0
                    self.message("Time elapsed. Recasting now.")
                else:
                    location = pyautogui.locateOnScreen(f'{self.assetPath}/fishing_pop.png', confidence=0.75, grayscale=False, region=(int(self.screenWidth/2) - 100, int(self.screenHeight/2) - 150, 200, 200))
                    if location != None:
                        time.sleep(random.uniform(0.25, 1.0))
                        self.pressKey(self.fish_key)
                        time_wait = random.uniform(5, 5.5)
                        self.message(f"Fish caught! Wait {time_wait}s to cast again.")
                        time.sleep(time_wait)
                        self.currentEnergy = self.currentEnergy - 60

                        if self.isUnderBaitBuff():
                            self.currentEnergy = self.currentEnergy - 60

                        if self.autorepair:
                            if self.count % self.autorepairMod == 0:
                                self.repairFishingRod()

                        if self.currentEnergy < 60:
                            self.message("Low energy. Stopping bot now.")
                            self.terminated()
                        
                        self.state = 0

#def main():
#    lostArkFishing = LostArkFishing()
#    lostArkFishing.execute()
#
#
#if __name__ == "__main__":
#    main()