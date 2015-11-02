import urwid
import subprocess
import os
import sys
import asyncio
from datetime import datetime
import weakref
from urwid.raw_display import Screen


loop = asyncio.get_event_loop()

# ----- Widget Setup, from urwid example ----

def build_widgets():
    input1 = urwid.Edit('What is your name?')
    input2 = urwid.Edit('What is your quest?')
    input3 = urwid.Edit('What is the airspeed of an unladen swallow?')

    inputs = [input1,input2,input3]


    def update_clock(widget_ref):
        widget = widget_ref()
        if not widget:
            #widget is dead; the main loop is destroyed
            return
        
        widget.set_text(datetime.now().isoformat())

        loop.call_later(1,update_clock,widget_ref)
    
        clock = urwid.Text('')

        update_clock(weakref.ref(clock))

        return urwid.Filler(urwid.Pile([clock] + inputs), 'top')
def unhandled(key):
    if key == 'ctrl c':
        raise urwid.ExitMainLoop



def demo1():
    main_widget = build_widgets()
    urwid_loop = urwid.MainLoop(
        main_widget,
        event_loop = urwid.AsyncioEventLoop(loop=loop),
        unhandled_input=unhandled,
        )
    urwid_loop.run()

demo1()



def mainMenu():
    pass

def addCalendarEvent():
    pass

def viewCalendar():
    pass

def viewLog():
    pass


def startup():
    pass