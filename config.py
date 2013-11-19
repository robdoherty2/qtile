#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note that since qtile configs are just python scripts, you can check for
# syntax and runtime errors by just running this file as is from the command
# line, e.g.:
#
#    python config.py

from libqtile.manager import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

'''
import subprocess
import os

@hook.subscribe.startup
def dbus_register():
	"""
	registers Qtile with gnome-session. Without it, a 
	°Something has gone wrong!² message shows up a short 
	while after logging in. dbus-send must be on your $PATH.
	"""
	x = os.environ['DESKTOP_AUTOSTART_ID']
	subprocess.Popen(['dbus-send',
			  '--session',
			  '--print-reply=string',
			  '--dest=org.gnome.SessionManager',
			  '/org/gnome/SessionManager',
			  'org.gnome.SessionManager.RegisterClient',
			  'string:qtile',
			  'string:' + x])

'''

@hook.subscribe.client_new
def dialogs(window):
	if(window.window.get_wm_type() == 'dialog'
	   or window.window.get_wm_transient_for()):
		window.floating = True

##-> Theme + widget options
class Theme(object):
	bar = {
		'size': 24,
		'background': '15181a',
	}
	widget = {
		'font': 'Open Sans',
		'fontsize': 10,
		'background': bar['background'],
		'foreground': 'eeeeee',
	}
	graph = {
		'background': '000000',
		'border_width': 0,
		'border_color': '000000',
		'line_width': 1,
		'margin_x': 1,
		'margin_y': 1,
		'width': 200,
	}

	groupbox = widget.copy()
	groupbox.update({
		'padding': 2,
		'borderwidth': 3,
	})

	sep = {
		'background': bar['background'],
		'foreground': '444444',
		'height_percent': 75,
	}

	systray = widget.copy()
	systray.update({
		'icon_size: 16'
		'padding': 2,
	})

	battery = widget.copy()
	battery_text = widget.copy()
	battery_text.update({
		'charge_char': '↑ ',
		'discharge_char': '↓ ',
		'format': '{char}{hour:d}:{min:02d}',
        })

	window_name = widget.copy()
	window_name.update({
		'fontsize': 12,
	})

	clock = widget.copy()
	clock.update({
		'fontsize': 12,
		'foreground': 'eeeeee',
	})


# The screens variable contains information about what bars are drawn where on
# each screen. If you have multiple screens, you'll need to construct multiple
# Screen objects, each with whatever widgets you want.
#
# Below is a screen with a top bar that contains several basic qtile widgets.
screens = [Screen(top = bar.Bar([
        # This is a list of our virtual desktops.
        widget.GroupBox(**Theme.groupbox),

        # A prompt for spawning processes or switching groups. This will be
        # invisible most of the time.
        widget.Prompt(),

	widget.CPUGraph(graph_color='18BAEB', fill_color='1667EB.3', **Theme.graph),
	widget.MemoryGraph(graph_color='00FE81', fill_color='00B25B.3', **Theme.graph),
	widget.SwapGraph(graph_color='5E0101', fill_color='FF5656', **Theme.graph),
	# NetGraph not in current version of qtile ...?
	#widget.NetGraph(graph_color='ffff00', fill_color='4d4d00', interface='wlan0',  **Theme.graph),

        # Current window name.
	widget.CurrentLayout(**Theme.widget),
        widget.WindowName(**Theme.window_name),
        #widget.Volume(),
        #widget.BatteryIcon(**Theme.battery),
	#widget.Battery(**Theme.battery),
        widget.Systray(**Theme.systray),
        widget.Clock('%Y-%m-%d %a %I:%M %p', **Theme.clock),
    ], 20))
]

# Super_L (the Windows key) is typically bound to mod4 by default, so we use
# that here.
mod = "mod4"
alt = "mod1"
# The keys variable contains a list of all of the keybindings that qtile will
# look through each time there is a key pressed.
keys = [
	# Log out; note that this doesn't use mod4: that's intentional in case mod4
	# gets hosed (which happens if you unplug and replug your usb keyboard
	# sometimes, or on system upgrades). This way you can still log back out
	# and in gracefully.
	Key([mod, 'control'], 'l', lazy.spawn('gnome-screensaver-command -l')),
	
	#Key(["mod1", "shift"], "l", lazy.logout()),  #lazy.spawn('gnome-session-save --force-logout')),
	# shutdown
	Key([alt, "control"], "q", lazy.shutdown()), #spawn('sudo shutdown -h now')),
	# restart qtile
	Key([mod, "shift"], "r",     lazy.restart()),

	# layout/tile interactions
	Key([mod], "k",              lazy.layout.down()),
	Key([mod], "j",              lazy.layout.up()),
	Key([mod], "h",              lazy.layout.previous()),
	Key([mod], "l",              lazy.layout.previous()),
	Key([mod, "shift"], "space", lazy.layout.rotate()),
	Key([mod, "shift"], "Return",lazy.layout.toggle_split()),
	Key(["mod1"], "Tab",         lazy.nextlayout()),
	Key([mod], "x",              lazy.window.kill()),

	# inc ratio of current window
	Key(["mod1"], "e", lazy.layout.increase_ratio()),

	# dec ratio of current window
	Key(["mod1"], "q", lazy.layout.decrease_ratio()),

	# interact with prompts
	Key([mod], "r",              lazy.spawncmd()),
	Key([mod], "g",              lazy.switchgroup()),

	# start specific apps
	Key([mod], "f",              lazy.spawn("firefox")),
	Key([mod], "c",              lazy.spawn("google-chrome")),
	Key([mod], "e",              lazy.spawn("emacs")),	    
	Key([mod], "Return",         lazy.spawn("gnome-terminal")),

	# Change the volume if your keyboard has special volume keys.
	Key(
		[], "XF86AudioRaiseVolume",
		lazy.spawn("amixer -c 0 -q set Master 2dB+")
	),
	Key(
		[], "XF86AudioLowerVolume",
		lazy.spawn("amixer -c 0 -q set Master 2dB-")
	),
	Key(
		[], "XF86AudioMute",
		lazy.spawn("amixer -c 0 -q set Master toggle")
	),

	# Also allow changing volume the old fashioned way.
	Key([mod], "equal", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
	Key([mod], "minus", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
]

# This allows you to drag windows around with the mouse if you want.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position_floating(),
	     start=lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(),
	     start=lazy.window.get_size()),
	Click([mod], "Button2", lazy.window.bring_to_front())
]

# Next, we specify group names, and use the group name list to generate an appropriate
# set of bindings for group switching.
groups = [Group(str(i)) for i in (1, 2, 3, 4, 5)]
for i in groups:
	keys.append(
		Key([mod], i.name, lazy.group[i.name].toscreen())
	)
	keys.append(
		Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
	)

#   Layouts Config
# -------------------

# Layout Theme
layout_theme = {
	"border_width": 4,
	"margin": 3,
	"border_focus": "#005F0C",
	"border_normal": "#555555"
}

layouts = [
	layout.Max(**layout_theme),
	layout.RatioTile(**layout_theme),
	layout.Stack(stacks=2, **layout_theme),
	layout.Tile(shift_windows=True, **layout_theme),
]


# Automatically float these types. This overrides the default behavior (which
# is to also float utility types), but the default behavior breaks our fancy
# gimp slice layout specified later on.
floating_layout = layout.Floating(auto_float_types=[
	"notification",
	"toolbar",
	"splash",
	"dialog",
], **layout_theme)
