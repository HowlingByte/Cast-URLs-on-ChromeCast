import time
import pychromecast
import csv
import pyautogui

with open("List-Media.csv", encoding='utf-8', newline='') as csvfile:
    Medias=list(csv.reader(csvfile,delimiter=";")) 
    print("Medias link",Medias)

def start_cast():
    global cast
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[NameOfCast])
    print("Found {} chromecasts".format(len(chromecasts)))

    cast = chromecasts[0]
    cast.wait()
    print(cast.status)


# show an image
def show_media(url):
    global cast
    mc = cast.media_controller
    #si url contient "http" alors c'est une image
    if "jpg" in url:
        mc.play_media(url, 'image/jpeg')
    else:
        mc.play_media(url, 'image/jpeg')
    #
    mc.block_until_active()
    return mc.status

def stop_cast():
    global cast
    cast.quit_app()
    cast.disconnect()

def boucle(nombre):
    for x in range(nombre):
        show_media(Medias[x][0])
        time.sleep(TempsDePause)

### Main ###
NameOfCast = "Mat" #Name of your Chromecast
MediasNumber = len(Medias) #Number of medias in your list
TempsDePause = 5 #Time between each media
print("MediasNumber",MediasNumber) #Debug

start_cast() 

boucle(MediasNumber)

pyautogui.alert(text='Close?', title='Main', button='OK')
stop_cast()
