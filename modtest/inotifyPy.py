# __author__ = 'Administrator'
# # Notifier example from tutorial
# #
# # See: http://github.com/seb-m/pyinotify/wiki/Tutorial
# #
# import pyinotify
#
# wm = pyinotify.WatchManager()  # Watch Manager
# mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events
#
# class EventHandler(pyinotify.ProcessEvent):
#     def process_IN_CREATE(self, event):
#         print "Creating:", event.pathname
#
#     def process_IN_DELETE(self, event):
#         print "Removing:", event.pathname
#
# handler = EventHandler()
# notifier = pyinotify.Notifier(wm, handler)
# wdd = wm.add_watch('/tmp', mask, rec=True)
#
# notifier.loop()

#!/usr/bin/python
import os
import pyinotify

wm = pyinotify.WatchManager()
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE

class PTmp(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Create: %s " % os.path.join(event.path, event.name)
    def process_IN_DELETE(self, event):
        print "Delete: %s " % os.path.join(event.path, event.name)


notifier = pyinotify.Notifier(wm, PTmp())

wdd = wm.add_watch('/home/dave/projects', mask, rec=True)

while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        break




