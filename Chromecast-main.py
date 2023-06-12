import time
import pychromecast
import csv
import pyautogui
import tkinter as tk

global cast
global NameOfCast
global TempsDePause
global Medias
global text1
global text2
global text3
global checkbox_var

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

# Share an image (from a URL) to the Chromecast
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
# Stop the media playing on the Chromecast and disconnect
def stop_cast():
    global cast
    cast.quit_app()
    cast.disconnect()
# Loop through the images in the list (url(s) inside of csv file)
def loop(number, Repetition=1, EndAfterLoop = False):
    for i in range(Repetition):
        for x in range(number):
            show_media(Medias[x][0])
            time.sleep(TempsDePause)
    if EndAfterLoop == True:
        stop_cast()

####
#UI
####
def UI():
    def Send():
        global NameOfCast
        global TempsDePause
        NameOfCast = text1.get()
        TempsDePause = int(text2.get())
        Repetition = int(text3.get())
        print("NameOfCast:",NameOfCast)
        print("TempsDePause:",TempsDePause)
        start_cast() 
        if checkbox_var.get() == 1:
            loop(len(Medias), Repetition, EndAfterLoop = True)
        else:
            loop(len(Medias), Repetition)
        

    # create UI
    root = tk.Tk()
    root.title("Chromecast-URL")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(background='red')
        
    #text 
    text1_label = tk.Label(root, text="Name of Chromecast:")
    text1_label.pack()
    text1 = tk.Entry(root)
    text1.pack()
    text2_label = tk.Label(root, text="Time between photos (s):")
    text2_label.pack()
    text2 = tk.Entry(root)
    text2.pack()
    text3_label = tk.Label(root, text="Repetition:")
    text3_label.pack()
    text3 = tk.Entry(root)
    text3.pack()

    #create another checkbox
    checkbox_var = tk.IntVar(value=1)
    checkbox1 = tk.Checkbutton(root, text="End connection after loop", variable=checkbox_var)
    checkbox1.pack()

    # Create the submit button
    submit_button = tk.Button(root, text="Submit", command=Send)
    submit_button.pack()

    # Start the main event loop
    root.mainloop()

UI()