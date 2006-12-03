#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Post To Del.icio.us Epiphany Extension
# Copyright (C) 2006 Ross Burton <ross@burtonini.com>
#               2006 Johan Dahlin <jdahlin@async.com.br>
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

EGG_TB_MODEL_NAME_KNOWN = 1 << 2

class DeliciousPlugin(object):
    def __init__(self):
        self._window_data = {}

        self._register_icon()

        shell = epiphany.ephy_shell_get_default()
        model = shell.get_toolbars_model(False)
        flags = model.get_name_flags('DeliciousPost')
        model.set_name_flags('DeliciousPost', flags | EGG_TB_MODEL_NAME_KNOWN)

    def _register_icon(self):
        # Add the icons we use to the theme.  A nice little hack because I'm too
        # lazy to install icons correctly at the moment.
        set = gtk.IconSet()
        for (pixels, size) in ((16, gtk.ICON_SIZE_MENU), (22, gtk.ICON_SIZE_SMALL_TOOLBAR), (24, gtk.ICON_SIZE_LARGE_TOOLBAR), (32, gtk.ICON_SIZE_BUTTON)):
            source = gtk.IconSource()
            source.set_filename (os.path.join(os.path.dirname(__file__), "delicious%d.png" % pixels))
            source.set_size_wildcarded(False)
            source.set_size(size)
            set.add_source(source)
        f = gtk.IconFactory()
        f.add('delicious', set)
        f.add_default()

    def _find_group(self, window):
        for group in window.get_ui_manager().get_action_groups():
            if group.get_name() == "SpecialToolbarActions":
                return group
        else:
            raise AssertionError("Cannot find SpecialToolbarActions group")

    def _delicious_post_activate_cb(self, action, window):
        embed = window.get_active_embed()

        siteurl = urllib.quote(embed.get_location(toplevel=True))
        sitetitle = urllib.quote(embed.get_title())

        url = "http://del.icio.us/post?v=4;url=%s;title=%s" % (siteurl, sitetitle)
        embed.load_url(url)

    def attach(self, window):
        _ui_str = """
        <ui>
          <menubar name="menubar">
            <menu name="ToolsMenu" action="Tools">
              <menuitem name="DeliciousPost" action="DeliciousPost"/>
            </menu>
          </menubar>
        </ui>
        """
        actions = [('DeliciousPost', 'delicious', 'Post to _Del.icio.us',
                     None, 'Post to Del.icio.us', self._delicious_post_activate_cb)]
        group = self._find_group(window)
        group.add_actions(actions, window)

        ui_manager = window.get_ui_manager()

        self._window_data[window] = ui_manager.add_ui_from_string(_ui_str)

    def detach(self, window):
        ui_id = self._window_data.pop(window)

        ui_manager = window.get_ui_manager()
        ui_manager.remove_ui(ui_id)
        ui_manager.ensure_update()

    # Not supported yet in Epiphany
    def finalize(self):
        shell = epiphany.ephy_shell_get_default()
        model = shell.get_toolbars_model(False)
        name_flags = model.get_name_flags('DeliciousPost')
        model.set_name_flags('DeliciousPost', name_flags & ~EGG_TB_MODEL_NAME_KNOWN)

plugin = DeliciousPlugin()

def attach_window(window):
    plugin.attach(window)

def detach_window(window):
    plugin.detach(window)
