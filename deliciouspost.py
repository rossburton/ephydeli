#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Post To Del.icio.us Epiphany Extension
# Copyright (C) 2006 Ross Burton <ross@burtonini.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import os.path
import urllib

import gobject
import gtk

import epiphany

def post_cb(action, window):
    embed = window.get_active_embed()

    siteurl = urllib.quote(embed.get_location(toplevel=True))
    sitetitle = urllib.quote(embed.get_title())

    url = "http://del.icio.us/post?v=4;url=%s;title=%s" % (siteurl, sitetitle)
    embed.load_url (url)

_ui_str = """
<ui>
  <menubar name="menubar">
    <menu name="ToolsMenu" action="Tools">
      <menuitem name="DeliciousPost" action="DeliciousPost"/>
    </menu>
  </menubar>
</ui>
"""

_actions = [('DeliciousPost', 'delicious', 'Post to _Del.icio.us', None, 'Post to Del.icio.us', post_cb)]
_window_data = {}

def init_plugin():
    # Add the icons we use to the theme.  A nice little hack because I'm too
    # lazy to install icons correctly at the moment.
    filename = os.path.join(os.path.dirname(__file__), "delicious.png")

    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file(filename)
    except gobject.GError, e:
        print e
        return

    # Register stockicon
    f = gtk.IconFactory()
    f.add('delicious', gtk.IconSet(pixbuf))
    f.add_default()

    shell = epiphany.ephy_shell_get_default()
    model = shell.get_toolbars_model(False)
    model.set_name_flags("DeliciousPost", 4) # EGG_TB_MODEL_NAME_KNOWN

def find_group(window):
    for group in window.get_ui_manager().get_action_groups():
        if group.get_name() == "SpecialToolbarActions":
            return group
    else:
        raise AssertionError("Cannot find SpecialToolbarActions group")

def attach_window(window):
    group = find_group(window)
    group.add_actions(_actions, window)

    ui_manager = window.get_ui_manager()

    _window_data[window] = ui_manager.add_ui_from_string(_ui_str)

def detach_window(window):
    uid_id = _window_data.pop(window)

    ui_manager = window.get_ui_manager()
    ui_manager.remove_ui(ui_id)
    ui_manager.ensure_update()

init_plugin()
