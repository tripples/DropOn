
#! /usr/bin/env python
"""
main.py
TODO :
write usage
and documentation
"""
from notify import *
from Tkinter import *
import pyinotify
import urllib2
import choose
import social
import os
import slog
import socialfs
"""
Watchdog : main file watching SocialFs directory
EventHandler will handle all events on SocialFS directory
Get choice from user using choose module
"""
wm = pyinotify.WatchManager() # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE # watched events

Images = ['.jpg','.gif','.jpeg','.png']
Videos = ['.flv','.mp4','.mkv']
Email = ['gmail','yahoo','rediff']
choices=list()

def distinguish(filePath):
    slog.info("distinguish" + str(filePath))
    File=open(filePath,"r")
    content=File.read()
    filePath=filePath.split('/').pop()
    if content.find('@')>=0 and content.find('.com')>=0:
        return "emailid"
    elif content.find('youtube')>=0:
        return "youtube"
    elif any(ext in filePath for ext in Images):
        return "image"
    elif any(ext in filePath for ext in Videos):
        return "video"
    elif filePath.count('.pdf'):
        print "This is a pdf file and being removed"
    else:
        return "regular"

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        global choices
        slog.info("Entered process_in_create"+str(event.pathname))
        if event.pathname.split("/")[0]=='.':
            print "Hidden file: %s" ,event.pathname
        else:
            #notify(event.pathname.split("/").pop())
            filetype=distinguish(event.pathname)
            social.update(choose.choose(filetype), filetype, event.pathname)
            os.remove(event.pathname)
        slog.info(internet_on())

    def process_IN_DELETE(self, event):
        slog.info("Removing:" + str(event.pathname))

    def process_IN_MODIFY(self, event):
        slog.info("Modifying" + str(event.pathname))

f_path = os.path.expanduser('~/') + 'SocialFS'
slog.info(f_path)
handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(f_path, mask, rec=True)
notifier.loop()
