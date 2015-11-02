import urwid
import subprocess
import os
import sys
import asyncio
from datetime import datetime
import weakref
from urwid.raw_display import Screen




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
    txt = urwid.Text(u"Hello World!!!!")
    fill = urwid.Filler(txt,'top')
    urwid_loop = urwid.MainLoop(
        fill,
        event_loop = urwid.AsyncioEventLoop(loop=asyncio.get_event_loop()),
        unhandled_input=unhandled,
        )
    urwid_loop.run()

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice, u'\n'])
    done = urwid.Button(u'Ok')
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
    raise urwid.ExitMainLoop()



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

choices = u'Chapman Cleese Gilliam Idle Jones Palin'.split()

main = urwid.Padding(menu(u'Pythons', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
urwid_loop = urwid.MainLoop(top,palette=[('reversed','standout','')],event_loop=urwid.AsyncioEventLoop(loop=asyncio.get_event_loop()))
urwid_loop.run()