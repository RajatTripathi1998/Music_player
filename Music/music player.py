import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk

from tkinter import filedialog

from mutagen.mp3 import MP3
from pygame import mixer

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")


statusbar = ttk.Label(root, text='Welcome to Melody', relief= SUNKEN , anchor=W,font='Times 15 bold')
statusbar.pack(side=BOTTOM, fill = X)

# Create Menubar

menubar=Menu(root)
root.config(menu=menubar)

#Create SubMenu
subMenu=Menu(menubar,tearoff=0)
playlist=[]
#it contains the full path + filename
#playlistbox- contains just the filename
#fullpth-filename is required to play the music inside play_music

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index=0
    playlistbox.insert(index,filename)
    playlist.insert(index,filename_path)
    index +=1
    
menubar.add_cascade(label='File',menu=subMenu)
subMenu.add_command(label='Open', command=browse_file)
subMenu.add_command(label='Exit',command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About Melody','This is a music player')

subMenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=subMenu)
subMenu.add_command(label='About us',command=about_us)
mixer.init()

root.title('Melody')
root.iconbitmap(r'melody.ico')

leftframe=Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30)

playlistbox=Listbox(leftframe)
playlistbox.pack()

addBtn=ttk.Button(leftframe,text="Add",command=browse_file)
addBtn.pack(side=LEFT)

def del_song():
    selected_song=playlistbox.curselection()
    selected_song=int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delBtn=ttk.Button(leftframe,text="Del",command=del_song)
delBtn.pack(side=LEFT)

rightframe=Frame(root)
rightframe.pack(pady=30)

topframe=Frame(rightframe)
topframe.pack()

lengthlabel=ttk.Label(topframe,text='Total Length: --:--')
lengthlabel.pack(pady=5)

currenttimelabel=ttk.Label(topframe,text='Current Time:  --:--',relief=GROOVE)
currenttimelabel.pack()



def show_details(play_song):
    file_data=os.path.splitext(play_song)
    
    if file_data[1]=='.mp3':
        audio= MP3(play_song)
        total_length=audio.info.length
    else:
        a=mixer.Sound(play_song)
        total_length=a.get_length()
    mins,secs=divmod(total_length,60)
    mins=round(mins)
    secs=round(secs)
    timeformat='{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text'] = "Total Length" + '  -  ' + timeformat
    
    t1=threading.Thread(target=start_count, args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    #it will return FALSE when we press the stop button
    #continue: Ignores all the statements below it we check music is paused or not
    current_time=0
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,secs=divmod(current_time,60)
            mins=round(mins)
            secs=round(secs)
            timeformat='{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + '  -  ' + timeformat
            time.sleep(1)
            current_time +=1
        
        
def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused=FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song=playlistbox.curselection()
            selected_song=int(selected_song[0])
            play_it=playlist(selected_song[0])
            print(play_it)
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('Song does not found')
           
def stop_music():
    mixer.music.stop()
    statusbar['text'] = 'Music Stopped'

paused=FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = 'Music paused'


def set_vol(val):
    volume=float(val)/100
    mixer.music.set_volume(volume)

def rewind_music():
    play_music()
    statusbar['text'] = 'Music Rewind'


muted=FALSE

def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        volumeBtn.config(image=volumePhoto)
        scale.set(70)
        muted=FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.config(image=mutePhoto)
        scale.set(0)
        muted=TRUE

middleframe= Frame(rightframe,bg='yellow')
middleframe.pack(padx=30,pady=30)

playphoto=PhotoImage(file='play.png')
playBtn=ttk.Button(middleframe,image=playphoto,command=play_music)
playBtn.pack(side = LEFT , padx=5, pady=5)

stopPhoto=PhotoImage(file='stop.png')
stopBtn=ttk.Button(middleframe,image=stopPhoto,command=stop_music)
stopBtn.pack(side = LEFT , padx=5, pady=5)

pausePhoto= PhotoImage(file='pause.png')
pauseBtn = ttk.Button(middleframe , image=pausePhoto,command=pause_music)
pauseBtn.pack(side = LEFT , padx=5, pady=5)

rewindPhoto= PhotoImage(file='rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto,command=rewind_music)
rewindBtn.pack()

mutePhoto= PhotoImage(file='mute.png')
volumePhoto= PhotoImage(file='volume.png')
volumeBtn =ttk.Button(bottomframe, image=volumePhoto,command=mute_music)
volumeBtn.pack(side = TOP , padx=5, pady=5)

bottomframe= Frame(rightframe)
bottomframe.pack(padx=5,pady=5)

scale=ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL, command=set_vol)
scale.set(70)
scale.pack()


def on_closing():
    stop_music()
    root.destroy()
      
root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()
