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

import widget


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
