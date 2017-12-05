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


class Label(widget.Widget):
	def __init__(
			self, text, fontFace=None, fontSize=14,
			color=(200,200,200), backgroundColor=None, container=None):
		widget.Widget.__init__(self, container)

		self.color = color
		self.backgroundColor = backgroundColor
		if fontFace is None:
			fontFace = utils.getFontFilename()
		self.font = pygame.font.Font(fontFace, fontSize)
		self.__text = text
		self.createImage()

	def update(self,event):
		if not self.dirty:
			return
		self.dirty = 0

	def SetText(self, text):
		""" The rect must be placed with i.e. somelabel.rect.move_ip(...)
		after each call to this method."""
		position = self.rect.topleft
		self.__text = text
		self.SetDirty(1)
		self.createImage()
		self.rect.move_ip(position)

	def createImage(self):
		if self.backgroundColor is None :
			self.image = self.font.render(self.__text, 1, self.color)
		else :
			self.image = self.font.render(self.__text, 1, self.color,
				self.backgroundColor)
		self.rect  = self.image.get_rect()

    
