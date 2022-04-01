import pyautogui
import time
import cv2
import random
from time import gmtime, strftime
import numpy

def pressKey(key):
    pyautogui.keyDown(key)
    time.sleep(random.uniform( 0.25, 0.55 ))
    pyautogui.keyUp(key)

# Function to cast fishing rod ingame
def castFishingRod(count):
    print(strftime("%H:%M:%S", gmtime()), f"Casting fishing rod. Counter: {count}")

    # Cast fishing rod ingame
    pressKey('e')
    time.sleep(random.uniform(4.5, 6.5))

# screen resolution
screenWidth, screenHeight= pyautogui.size()
print(strftime("%H:%M:%S", gmtime()), "Starting the bot in 5 seconds.")
time.sleep(5)
state = 0
count = 0

while(1):
    if state == 0:
        count = count + 1
        castFishingRod(count)
        state = 1
        start = time.time()
    else:
        elapse = time.time() - start
        if elapse > 20:
            state = 0
            print(strftime("%H:%M:%S", gmtime()), "Time elapsed. Recasting now.")
        else:
            location = pyautogui.locateOnScreen(f'resources/{screenHeight}/fishing_pop.png', confidence=0.7, grayscale=False, region=(int(screenWidth/2) - 100, int(screenHeight/2) - 150, 200, 200))
            if location != None:
                time.sleep(random.uniform(0.25, 1.0))
                pressKey('e')
                print(strftime("%H:%M:%S", gmtime()), "Fish caught! Wait 10s to cast again.")
                time.sleep(random.uniform(2.5, 5))
                count = count + 1
                castFishingRod(count)
                state = 0