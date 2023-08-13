from setuptools import setup

APP=['dory2mp3.py']
DATA_FILES = ['dory.gif','dory.ico']
OPTIONS = {
    'argv_emulation': False,
     'includes': ['Threading','os','pytube','tkinter','time','mutagen.easyid3','moviepy.editor '],}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app':OPTIONS},
    setup_requires=['py2app']
)