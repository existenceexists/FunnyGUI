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


class Button(widget.Widget):
	def __init__(
			self, 
			text, 
			container=None,
			fontFace=None, 
			fontSize=14,
			normalColor=(100,0,0),
			highlightedColor=(255,0,0),
			focusedColor=(255,255,0), 
			normalBackgroundColor=None, # if background color is None the area outside the text will be transparent
			highlightedBackgroundColor=None,
			focusedBackgroundColor=None, 
			onClickCallback=None, 
			callbackArgs=()):
		widget.Widget.__init__(self, container)
		
		self.onClickCallback = onClickCallback
		self.callbackArgs = callbackArgs
		if fontFace is None:
			fontFace=pygame.font.match_font("freesans,sansserif,microsoftsansserif,arial,dejavusans,verdana,timesnewroman,helvetica")
		if fontFace is None:
			fontFace=pygame.font.match_font(pygame.font.get_fonts()[0])
		self.font = pygame.font.Font(fontFace, fontSize)
		self.text = text
		self.normalColor = normalColor
		self.highlightedColor = highlightedColor
		self.focusedColor = focusedColor
		self.normalBackgroundColor = normalBackgroundColor
		self.highlightedBackgroundColor = highlightedBackgroundColor
		self.focusedBackgroundColor = focusedBackgroundColor
		self.CreateImages()
		self.image = self.normalImage
		self.rect = self.normalRect

	def update(self,event):
                if event.type==pygame.MOUSEMOTION:
			self.OnMouseMove(event.pos)
                elif event.type==pygame.MOUSEBUTTONDOWN:
                	self.OnMouseClick(event.pos)
		if self.dirty:
			self.ChangeImage()
			self.dirty=False
			return self.rect

	def draw(self,surface):
		surface.blit(self.image,self.rect)

	def Click(self):
		self.SetDirty(1)
		if self.onClickCallback:
			self.onClickCallback(*self.callbackArgs)

 	def OnMouseClick(self, pos):
		if self.rect.collidepoint(pos):
			self.Click()
			return True
		elif self.focused:
			self.OnLoseFocus()
			return True

 	def OnMouseMove(self, pos):
		if self.rect.collidepoint(pos):
			if not self.highlighted:
				self.OnHighlight()
				return True # the widget needs to be repainted
		elif self.highlighted:
			self.OnUnhighlight()
			return True # the widget needs to be repainted

 	def OnHighlight(self):
		self.SetHoverHighlight(True)

 	def OnUnhighlight(self):
		self.SetHoverHighlight(False)

 	def OnGetFocus(self):
		widget.Widget.OnGetFocus(self)

 	def OnLoseFocus(self):
		widget.Widget.OnLoseFocus(self)

	def ChangeImage(self):
		"""Change image, choose from normal, highlighted and focused image."""
		pos = self.rect.topleft # TODO: topleft or center ?
		if self.focused and self.focusedImage:
			self.image = self.focusedImage
			self.rect = self.focusedRect # It is not needed as all the rects are the same, but we do it because of subclasses
		elif self.highlighted and self.highlightedImage:
			self.image = self.highlightedImage
			self.rect = self.highlightedRect # It is not needed as all the rects are the same, but we do it because of subclasses
		else:
			self.image = self.normalImage
			self.rect = self.normalRect # It is not needed as all the rects are the same, but we do it because of subclasses
		self.rect.topleft = pos

	def CreateImages(self):
		"""Create 3 button's images for normal, highlighted and focused state."""
		if self.normalBackgroundColor is None:
			self.normalImage = self.font.render(self.text, 1, self.normalColor) # the area outside the text will be transparent
		else:
			self.normalImage = self.font.render(self.text, 1, self.normalColor, self.normalBackgroundColor)
		self.normalRect = self.normalImage.get_rect()
		if self.highlightedBackgroundColor is None:
			self.highlightedImage = self.font.render(self.text, 1, self.highlightedColor) # the area outside the text will be transparent
		else:
			self.highlightedImage = self.font.render(self.text, 1, self.highlightedColor, self.highlightedBackgroundColor)
		self.highlightedRect = self.highlightedImage.get_rect()
		if self.focusedBackgroundColor is None:
			self.focusedImage = self.font.render(self.text, 1, self.focusedColor) # the area outside the text will be transparent
		else:
			self.focusedImage = self.font.render(self.text, 1, self.focusedColor, self.focusedBackgroundColor)
		self.focusedRect = self.focusedImage.get_rect()
