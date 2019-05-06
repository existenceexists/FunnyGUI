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


class Label(widget.Widget):
	def __init__(
			self,
			text,
			fontFace=None,
			fontSize=14,
			color=(200,200,200),
			backgroundColor=None,
			container=None):
		widget.Widget.__init__(self,container)
		self.color=color
		self.backgroundColor=backgroundColor
		if fontFace is None:
			fontFace=pygame.font.match_font("freesans,sansserif,microsoftsansserif,arial,dejavusans,verdana,timesnewroman,helvetica")
		if fontFace is None:
			fontFace=pygame.font.match_font(pygame.font.get_fonts()[0])
		self.font=pygame.font.Font(fontFace,fontSize)
		self.__text=text
		self.createImage()

	def update(self,event):
		if not self.dirty:
			return
		self.dirty=False

	def draw(self,surface):
		surface.blit(self.image,self.rect)

	def SetText(self,text):
		position=self.rect.topleft
		self.__text=text
		self.SetDirty(1)
		self.createImage()
		self.rect.move_ip(position)

	def createImage(self):
		if self.backgroundColor is None:# transparent background
			self.image=self.font.render(self.__text,1,self.color)
		else :
			self.image=self.font.render(self.__text,1,self.color,self.backgroundColor)
		self.rect=self.image.get_rect()

    
