import time
import pychromecast
import csv
import pyautogui
import tkinter as tk
from threading import Thread

global cast
global mc
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

def start_cast(stop_connection = False):
    if stop_connection == False:
        global cast
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[NameOfCast])
        print("Found {} chromecasts".format(len(chromecasts)))
        cast = chromecasts[0]
        cast.wait()
        print(cast.status)
    elif stop_connection == True:
        try:
            cast.quit_app()
            cast.disconnect()
            print("Connection closed", cast.status)
        except:
            pass

# Share an image (from a URL) to the Chromecast
def show_media(url, x=0, duration=10): #duration is in seconds, by default set at 10 (for mp4)
    global cast
    global mc
    mc = cast.media_controller
    #si url contient "http" alors c'est une image
    if "jpg" in url:
        mc.play_media(url, 'image/jpeg')
        mc.block_until_active()
    #if mp4, play video and wait for it to finish (get time from CSV file)
    elif "mp4" in url:
        mc.play_media(url, 'video/mp4')
        mc.block_until_active()
        if Medias[x][1] != "":
            duration = int(Medias[x][1])
            print("Found duration in csv file (", duration ,"s)")
        else:
            print("No duration found in csv file, set to default (", duration ,"s)")
        time.sleep(int(duration))

    else:
        mc.play_media(url, 'image/jpeg')
        mc.block_until_active()
    return mc.status

# Loop through the images in the list (url(s) inside of csv file)
def loop(number, Repetition=1, EndAfterLoop = False):
    for i in range(Repetition):
        for x in range(number):
            show_media(Medias[x][0], x)
            
            time.sleep(TempsDePause)
    if EndAfterLoop == True:
        start_cast(stop_connection = True)

def clear_log(): # Clear the log file
        with open("log.txt", "w") as file:
            file.write("")
##### UI ####
def UI():
    def Send():
        global NameOfCast
        global TempsDePause
        NameOfCast = text1.get()
        TempsDePause = int(text2.get())
        Repetition = int(text3.get())
        print("NameOfCast:",NameOfCast)
        print("TempsDePause:",TempsDePause)
        
        # Save the inputs to a text file
        with open("log.txt", "w") as file:
            file.write(f"Name of Chromecast: {NameOfCast}\n")
            file.write(f"Time between photos (s): {TempsDePause}\n")
            file.write(f"Repetition: {Repetition}\n")
            file.write(f"End after loop: {checkbox_var.get()}\n")

        thread = Thread(target=start_and_loop, args=(Repetition,))
        thread.start()

    def start_and_loop(Repetition):
        start_cast()
        if checkbox_var.get() == 1:
            loop(len(Medias), Repetition, EndAfterLoop=True)
        else:
            loop(len(Medias), Repetition)    

    def quit():
        print("Quit")
        start_cast(stop_connection = True)
        time.sleep(1)
        root.destroy()

    # create UI
    root = tk.Tk()
    root.title("Chromecast-URL")
    root.geometry("400x300")
    root.resizable(False, False)
    root.configure(background='#2B2B2B')
        
    # Load previous input values from file
    try:
        with open("log.txt", "r") as file:
            lines = file.readlines()
            # Write the values of the file to variables
            name_of_chromecast = lines[0].split(":")[1].strip()
            time_between_photos = lines[1].split(":")[1].strip()
            repetition = lines[2].split(":")[1].strip()
            #end_after_loop = lines[3].split(":")[1].strip()
            
            # Set the values in the input fields
            text1_label = tk.Label(root, text="Name of Chromecast:")
            text1_label.pack()
            text1 = tk.Entry(root)
            text1.insert(0, name_of_chromecast)
            text1.pack()
            text2_label = tk.Label(root, text="Time between photos (s):")
            text2_label.pack()
            text2 = tk.Entry(root)
            text2.insert(0, time_between_photos)
            text2.pack()
            text3_label = tk.Label(root, text="Repetition:")
            text3_label.pack()
            text3 = tk.Entry(root)
            text3.insert(0, repetition)
            text3.pack()
      
    except:
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

    # Create the quit button
    quit_button = tk.Button(root, text="Quit and end connection", command=quit)
    quit_button.pack()

    # Create the clear log button
    clear_log_button = tk.Button(root, text="Clear log", command=clear_log)
    clear_log_button.pack()
    
    # When the window is closed, quit the application
    root.protocol("WM_DELETE_WINDOW", quit)

    # Start the main event loop
    root.mainloop()
    
UI()
