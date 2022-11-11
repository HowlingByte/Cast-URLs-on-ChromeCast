import time
import pychromecast
import csv

with open("List-Media.csv", encoding='utf-8', newline='') as csvfile:
    Media=list(csv.reader(csvfile,delimiter=";")) 
    print("Media link",Media)

def start_cast():
    global cast
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[NameOfCast])
    print("Found {} chromecasts".format(len(chromecasts)))

    cast = chromecasts[0]
    cast.wait()
    print(cast.status)


# show an image
def show_image(url):
    global cast
    mc = cast.media_controller
    mc.play_media(url, 'image/jpeg')
    mc.block_until_active()
    return mc.status

def stop_cast():
    global cast
    cast.quit_app()
    cast.disconnect()



NameOfCast = "Mat"
start_cast()
show_image(Media[2][0])

time.sleep(10)
stop_cast()