from tkinter import ttk
from moviepy.audio.io.AudioFileClip import AudioFileClip
from tkinter import *
from mutagen.easyid3 import EasyID3
from pytube import YouTube,Playlist
from pytube.cli import on_progress
import os
import string
import threading
destination = os.path.join(os.path.expanduser("~"), "Music")


def dory2mp3():
    def setplaylist():
        oList = Playlist(playlist.get())
        for oContent in oList.videos:
            threading.Thread(target=downloadStream,
                             args=(oContent, destination, oList.length)).start()

            # prints address of each YouTube object in the playlist
    def setsong():
        url = playlist.get()
        oVideo=YouTube(url)
        threading.Thread(target=downloadStream,
                         args=(oVideo, destination, 1)).start()

    def downloadStream(oContent, destination, iPlaylistLength):
        if oContent.age_restricted:
            print("Age restricted")
            return
        
        try:
            #Get best quality audio-stream and convert it to mp3
            oStream = oContent.streams.get_audio_only()
        except:
            print("Stream couldn't be accessed")
            return
        oContent.register_on_progress_callback(my_progress_function)
        sFileName=destination +"/"+ remove_invalid_chars(oContent.title) + ".mp3"
        print("started Downloading Video:"+oContent.title )
        
        oVideo=oStream.download(output_path=destination)
        oAudio = AudioFileClip(oVideo)
        oAudio.write_audiofile(sFileName)
        try:
            #Get best quality audio-stream and convert it to mp3
            oAudioMetadata = EasyID3(sFileName)
            oAudioMetadata['title'] = oContent.title
            oAudioMetadata['artist'] = oContent.author 
            oAudioMetadata.save()
        except:
            print("Stream couldn't be accessed")
            return
        
        # Add metadata using mutagen



        oAudio.close()
        #remove uncecessary mp4
        os.remove(oVideo)
    def remove_invalid_chars(filename):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return ''.join(c for c in filename if c in valid_chars)
    def my_progress_function(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining

        #progress = round(bytes_downloaded / total_size * 100)
        print(f"Downloaded {bytes_downloaded} out of {total_size} bytes)")
    window = Tk()
    window.title("Dory2mp3")
    window.iconbitmap("dory.ico")

    tab_control = ttk.Notebook(window)

    tab1 = ttk.Frame(tab_control)

    tab2 = ttk.Frame(tab_control)

    tab_control.add(tab1, text='Download')

    tab_control.add(tab2, text='About')

    playlist = Entry(tab1, width=40)
    playlist.place(rely=0.5, relx=0.5, x=0, y=0, anchor=CENTER)

    btn1 = Button(tab1, text='Download Playlist', command=setplaylist)

    btn1.place(rely=1.0, relx=1.0, x=0, y=0, anchor=SE)

    btn2 = Button(tab1, text='Download 1 Song', command=setsong)

    btn2.place(rely=1.0, relx=0, x=0, y=0, anchor=SW)

    lbl_j = Label(tab2, text="Created for my beloved dory")
    lbl_j.place(rely=0.5, relx=0.6, x=0, y=0, anchor=CENTER)

    lbl_c = Label(tab2, text="©2023 Michael Schmid")
    lbl_c.place(rely=1, relx=1, x=0, y=0, anchor=SE)

    tab_control.pack(expand=1, fill='both')

    photo = PhotoImage(file="dory.gif", format="gif -index 15", )
    canvas = Canvas(tab2, width=85, height=100)
    canvas.pack()

    canvas.create_image(0, 0, anchor=NW, image=photo)
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


dory2mp3()
