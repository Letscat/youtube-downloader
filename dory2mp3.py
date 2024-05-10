import customtkinter
from pytube import YouTube,Playlist
from pytube.cli import on_progress
from proglog import ProgressBarLogger
from mutagen.easyid3 import EasyID3
from moviepy.audio.io.AudioFileClip import AudioFileClip
import threading
import string
import os
fDownloaded=0
fDownload=0
sDestination = os.path.join(os.path.expanduser("~"), "Music")

def is_video(oInput):
    try:
        oContent=YouTube(oInput)
        oContent.register_on_progress_callback(my_progress_function)
        threading.Thread(target=download,args=(oContent, sDestination)).start()
    except:
        oPlaylist=Youtube(oInput)
        for oContent in oPlaylist.videos:
            oContent.register_on_progress_callback(my_progress_function)
            threading.Thread(target=download,args=(oContent,sDestination)).start() 
    
def download(oContent,sDestination):
    global fDownloadSize
    fDownloadSize+=round(oStream.filesize_mb,1)
    if oContent.age_restricted:
        print("Age restricted")
        return
    try:
        #Get best quality audio-stream and convert it to mp3
        oStream = oContent.streams.get_audio_only()
        
    except:
        print("Stream couldn't be accessed")
        return
    oVideo=oStream.download(output_path=sDestination)
    oAudio = AudioFileClip(oVideo)
    sFileName=sDestination +"/"+ remove_invalid_chars(oContent.title) + ".mp3"
    oAudio.write_audiofile(sFileName)

def remove_invalid_chars(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)
def my_progress_function(stream, chunk, bytes_remaining):
    print(2311)
    
    global fDownloaded
    global fDownload
    if bytes_remaining > 9437184:
        fDownloaded+=9
    else:
        fDownloaded+=round(len(chunk)/1048576,1)
    progress = round(round(fDownloaded / fDownload * 100))
    print(23111)
    app.progressBarDownloaded.set(progress)
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dory2Mp3")
        self.geometry("500x250")
        self.grid_columnconfigure((0, 1), weight=1)
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Video / Playlist")
        self.entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        self.button = customtkinter.CTkButton(self, text="Download", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        self.progressBarDownloaded=customtkinter.CTkProgressBar(self)
        self.progressBarDownloaded.grid(row=2, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        self.progressBarDownloaded.set(0)

    def button_callback(self):
        oInput=self.entry.get()
        if oInput=="":
            print("No Input Entered")
            return
        
        is_video(oInput)

app = App()
app.mainloop()

    