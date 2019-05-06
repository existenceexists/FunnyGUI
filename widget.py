#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright © 2017 František Brožka <sentientfanda@gmail.com>
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

from __future__ import absolute_import

import pygame


class Widget(pygame.sprite.Sprite):
	def __init__(self,container=None):
		pygame.sprite.Sprite.__init__(self)
		self.container=container
		self.focused=False
		self.highlighted=False
		self.dirty=True

	def Destroy(self):
		self.container=None
		del self.container
		pygame.sprite.Sprite.kill(self)

	def SetFocus(self,value):
		self.focused=value
		self.SetDirty(True)

	def SetHoverHighlight(self,value):
		self.highlighted=value
		self.SetDirty(True)

	def OnGetFocus(self):
		self.SetFocus(True)

	def OnLoseFocus(self):
		self.SetFocus(False)

	def SetDirty(self,value):
		self.dirty=value
		if not self.container is None:
			self.container.SetDirty(value)
