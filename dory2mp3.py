from tkinter import ttk
import tkinter
from pytube import YouTube
from pytube import Playlist
import os
import time

import threading
from tkinter import * 

global amount_of_songs
amount_of_songs = 0
global downloaded_songs
downloaded_songs = 0

#prints each video url, which is the same as iterating through playlist.video_urls




destination= os.path.join(os.path.expanduser("~"), "Music")
def dory2mp3():
    def setplaylist():
        print('test')
        playlist_entered = Playlist(playlist.get())
        for url in playlist_entered:
            global amount_of_songs
            amount_of_songs +=1
            lbl_progress.configure(text=str(downloaded_songs)+" von "+ str(amount_of_songs))
            urlstr = str(url)
            print(urlstr)
            
            lbl_progress.configure(text=str(downloaded_songs)+" von "+ str(amount_of_songs))
            threading.Thread(target=downloadmpthree, args=(url,destination)).start()
         
            #prints address of each YouTube object in the playlist
    def setsong():
        vid=playlist.get()
        threading.Thread(target=downloadmpthree, args=(vid,destination)).start()

    def downloadmpthree(vid,destination):
        yt = YouTube(vid)
        
        # extract only audio
        video = yt.streams.filter(only_audio=True).first()
        
        # check for destination to save file
    

        
        # download the file
        out_file = video.download(output_path=destination)

        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        try:
            os.rename(out_file, new_file)
        except:
            time.sleep(0.001)
        # result of success
        print(yt.title + " has been successfully downloaded.")
        global downloaded_songs
        downloaded_songs +=1
        lbl_progress.configure(text=str(downloaded_songs)+" von "+ str(amount_of_songs))
    window = Tk()
    window.title("Dory2mp3")
    window.iconbitmap("dory.ico")

    tab_control = ttk.Notebook(window)

    tab1 = ttk.Frame(tab_control)

    tab2 = ttk.Frame(tab_control)



    tab_control.add(tab1, text='Download')

    tab_control.add(tab2, text='About')
  
    


    playlist=Entry(tab1,width=40)
    playlist.place(rely=0.5, relx=0.5, x=0, y=0, anchor=CENTER)
    lbl_progress = Label(tab1,text= str(downloaded_songs) +"von"+ str(amount_of_songs))
    lbl_progress.place(rely=0, relx=1, x=0, y=0, anchor=NE)


    btn1 = Button(tab1, text= 'Download Playlist', command=setplaylist)

    btn1.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    btn2 = Button(tab1, text= 'Download 1 Song', command=setsong)

    btn2.place(rely=1.0, relx=0, x=0, y=0, anchor=SW)

    lbl_j = Label(tab2,text= "Created for my beloved dory")
    lbl_j.place(rely=0.5, relx=0.6, x=0, y=0, anchor=CENTER)


    lbl_c = Label(tab2,text="©2022 Michael Schmid" )
    lbl_c.place(rely=1, relx=1, x=0, y=0, anchor=SE)






    tab_control.pack(expand=1, fill='both')


    photo = PhotoImage(file="dory.gif", format="gif -index 15", )
    canvas = Canvas(tab2, width = 85, height = 100)
    canvas.pack()

    canvas.create_image(0, 0, anchor = NW, image=photo)
    canvas.place(relx=0.0, rely=1.0, anchor=SW)

    window.geometry('450x160')
    window.resizable(False, False)
    window.mainloop()
    try:
        window.attributes('-topmost', 1)
        window.update()
        window.attributes('-topmost', 0)
        window.iconify()
        window.deiconify()
        

    except:
        print("closed")
    #The Motion Tracking Part of the Software shouldnt freeze up the rest of the application, required sepperate Thread

dory2mp3()

