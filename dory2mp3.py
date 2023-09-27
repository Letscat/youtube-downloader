import customtkinter
from pytube import YouTube,Playlist
from pytube.cli import on_progress
from proglog import ProgressBarLogger
from mutagen.easyid3 import EasyID3
from moviepy.audio.io.AudioFileClip import AudioFileClip
import threading
import string
import os

fDownload=0
fDownloaded=0
sDestination = os.path.join(os.path.expanduser("~"), "Music")
fConvert=0
fConverted=0

def prepare_content(oInput):
    if "list=" in oInput:
        oList=Playlist(oInput)
        for oContent in oList.videos:
            threading.Thread(target=downloadStream,
                             args=(oContent, sDestination, oList.length)).start()
            
    else:
        oVideo=YouTube(oInput)
        threading.Thread(target=downloadStream,
                         args=(oVideo, sDestination, 1)).start()
        
    def downloadStream(oContent, destination, iPlaylistLength):
        global fDownload
        
        if oContent.age_restricted:
            print("Age restricted")
            return
        
        try:
            #Get best quality audio-stream and convert it to mp3
            oStream = oContent.streams.get_audio_only()
            
        except:
            print("Stream couldn't be accessed")
            return
        fDownload+=round(oStream.filesize_mb,1)
        oContent.register_on_progress_callback(my_progress_function)
        sFileName=destination +"/"+ remove_invalid_chars(oContent.title) + ".mp3"
        print("started Downloading Video:"+oContent.title )
        
        oVideo=oStream.download(output_path=destination)
        oAudio = AudioFileClip(oVideo)
        oAudio.write_audiofile(sFileName,logger=logger)
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
        global fDownloaded
        global fDownload
        
        if bytes_remaining > 9437184:
            fDownloaded+=9
        else:
            fDownloaded+=round(len(chunk)/1048576,1)

        #progress = round(bytes_downloaded / total_size * 100)
        pb['value'] = 100*fDownloaded/fDownload
        lbl_Progress['text']=fDownloaded,"/",fDownload," MB"
    class MyBarLogger (ProgressBarLogger):
        def bars_callback (self, bar, attr, value,old_value=0):
            global fConvertSize
            global fConverted
            if old_value is None:
                fConvertSize+=self.bars [bar] ['total']
                return 
            fConverted+=value-old_value
            pb1['value'] = 100*fConverted/fConvertSize
    logger = MyBarLogger ()
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dory2Mp3")
        self.geometry("500x250")
        self.grid_columnconfigure((0, 1), weight=1)
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Video / Playlist")
        self.entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)
        self.button = customtkinter.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

    def button_callback(self):
        print("button pressed")
        oInput=self.entry.get()
        if oInput=="":
            print("No Input Entered")
            return
        prepare_content(oInput)

app = App()
app.mainloop()

    