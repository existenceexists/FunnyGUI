#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    This file is part of FunnyGUI.
    FunnyGUI is widget toolkit for pygame.
    Copyright (C) 2017 František Brožka
    email: sentientfanda@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pygame


class Widget(pygame.sprite.Sprite):
	def __init__(self, container=None):
		pygame.sprite.Sprite.__init__(self)

		self.container = container
		self.focused = 0
		self.highlighted = 0
		self.dirty = 1

 	def Destroy(self):
		self.container = None
		del self.container
		pygame.sprite.Sprite.kill(self)

	def SetFocus(self, val):
		self.focused = val
		self.SetDirty(True)

 	def SetHoverHighlight(self, value):
		self.highlighted = value
		self.SetDirty(True)

 	def OnGetFocus(self):
		self.SetFocus(True)

 	def OnLoseFocus(self):
		self.SetFocus(False)

 	def SetDirty(self, value):
		self.dirty = value
		if not self.container is None:
			self.container.SetDirty(value)
