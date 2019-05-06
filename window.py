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

from . import widget


class Window(widget.Widget):
	def __init__(
			self,
			container=None,
			width=500,
			height=500,
			backgroundColor=None): # if background color is None the area will be transparent
		widget.Widget.__init__(self,container)
		self.widgets=[]
		self.CreateImage(width,height,backgroundColor)

	def update(self,event):
		newEvent=event
		if hasattr(event,"pos"):
			eventDict=dict(event.dict)
			pos=list(eventDict["pos"])
			pos[0]=pos[0]-self.rect.x
			pos[1]=pos[1]-self.rect.y
			eventDict["pos"]=pos
			newEvent=pygame.event.Event(event.type,eventDict)
		for widget in self.widgets:
			widget.update(newEvent)
		if self.dirty:
			self.dirty=False
			self.ChangeImage()
			return self.rect

	def draw(self,surface):
		surface.blit(self.image,self.rect)

	def add(self,widget):
		widget.container=self
		self.widgets.append(widget)
		self.ChangeImage()
		self.SetDirty(True)

	def CreateImage(self,width,height,backgroundColor):
		"""Create image of the window widget without contained widgets."""
		self.image=pygame.Surface((width,height)).convert_alpha()
		if not backgroundColor is None:
			self.image.fill(backgroundColor)
		self.rect=self.image.get_rect()
		pygame.gfxdraw.rectangle(self.image,self.rect,(255,255,255,255))
		self.emptyImage=self.image.copy()

	def ChangeImage(self):
		"""Create image of the window widget with contained widgets."""
		self.image=self.emptyImage.copy()
		for widget in self.widgets:
			self.image.blit(widget.image,widget.rect)
