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





def main():
    def setplaylist():
        print('test')
        playlist_entered = Playlist(playlist.get())
        for url in playlist_entered:
            global amount_of_songs
            amount_of_songs +=1
            lbl_progress.configure(text=str(downloaded_songs)+" von "+ str(amount_of_songs))
            urlstr = str(url)
            print(urlstr)
            destination= os.path.join(os.path.expanduser("~"), "Music")
            lbl_progress.configure(text=str(downloaded_songs)+" von "+ str(amount_of_songs))
            threading.Thread(target=downloadmpthree, args=(url,destination)).start()
         
            #prints address of each YouTube object in the playlist
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

    window.title("Youtube Downloader")

    
    lbl1 = Label(text= "Select Playlist")
    lbl1.place(rely=0.0, relx=0.5, x=0, y=0, anchor=N)
    btn_download = Button(text= 'Download Playlist', command=setplaylist)

    lbl_progress = Label(text= str(downloaded_songs) +"von"+ str(amount_of_songs))
    lbl_progress.place(rely=1, relx=0, x=0, y=0, anchor=SW)
    
    playlist = Entry(width=40)
    label_playlist = Label( text="Url")
    playlist.place(rely=0.3, relx=0.5, x=0, y=0, anchor=N)
    label_playlist.place(rely=0.3, relx=0.9, x=0, y=0, anchor=N)

    btn_download.place(rely=1, relx=1, x=0, y=0, anchor=SE)









    window.geometry('450x100')
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


main()

