from distutils.core import setup # Need this to handle modules
import py2exe 
from tkinter import ttk
from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube
from pytube import Playlist
from tkinter import *
from mutagen.easyid3 import EasyID3
import os
import threading

setup(windows=['dory2mp3.py'])