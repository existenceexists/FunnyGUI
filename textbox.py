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


class TextBox(widget.Widget):
	def __init__(
			self,
			width=200,
			backspaceKeys=(pygame.K_BACKSPACE,), 
			fontFace=None, fontSize=14,
			borderLineColor=(0,0,100),
			backgroundColor=(0,0,0),
			borderLineWidth=4, 
			textNormalColor=(100,0,0), 
			textFocusedColor=(255,255,0), 
			textHighlightedColor=(255,0,0), 
			textPositionX=22):
		
		widget.Widget.__init__(self)
		self.focused = False
		self.highlighted = False
		self.dirty = True
		self.backspaceKeys = list(backspaceKeys)
		
		self.textNormalColor = textNormalColor
		self.textFocusedColor = textFocusedColor
		self.textHighlightedColor = textHighlightedColor
		
		if fontFace is None:
			fontFace=pygame.font.match_font("freesans,sansserif,microsoftsansserif,arial,dejavusans,verdana,timesnewroman,helvetica")
		if fontFace is None:
			fontFace=pygame.font.match_font(pygame.font.get_fonts()[0])
		self.font = pygame.font.Font(fontFace, fontSize)
		linesize = self.font.get_linesize()
		
		self.rect = pygame.Rect((
			0, 0, width,
			#linesize + 2*f_config.TEXT_BOX_BORDER_LINE_WIDTH))
			linesize + borderLineWidth))
		boxImg = pygame.Surface(self.rect.size).convert_alpha()
		boxImg.fill(backgroundColor)
		#color = f_config.TEXT_BOX_LINE_COLOR
		"""
		rect = pygame.Rect((
			self.rect.left, self.rect.top,
			self.rect.width - f_config.TEXT_BOX_BORDER_LINE_WIDTH +3,
			self.rect.height - f_config.TEXT_BOX_BORDER_LINE_WIDTH +3))
		"""
		if (borderLineWidth > 0):
			pygame.draw.rect(boxImg, borderLineColor, self.rect, borderLineWidth)

		self.emptyImg = boxImg.convert_alpha()
		self.image = boxImg

		self.highlighted = 0
		self.text = ''
		#self.textPos = (22, 2)
		#self.textDefaultPosition = f_config.TEXT_BOX_TEXT_DEFAULT_POSITION
		self.textDefaultPosition = (
			textPositionX,
			#0 + borderLineWidth)
			#(self.rect.height - linesize)//2 + 3)
			(self.rect.height - linesize)//2)

	def update(self, event):
                if event.type=pygame.MOUSEMOTION:
			self.OnMouseMove(event.pos)
                elif event.type=pygame.MOUSEBUTTONDOWN:
                	self.OnMouseClick(event.pos)
                elif event.type=pygame.KEYDOWN:
                	self.OnKeyPressed(event)
		if self.dirty:
			self.CreateImage()
			self.dirty=False
			return self.rect

	def draw(self,surface):
		surface.blit(self.image,self.rect)

	def CreateImage(self):
		text = self.text
		if self.focused:
			text += '|'
			color = self.textFocusedColor
		elif self.highlighted:
			color = self.textHighlightedColor
		else: 
			color = self.textNormalColor
		
		textPosition = list(self.textDefaultPosition)
		size = self.font.size(text)
		#if (size[0] > (self.rect.width - self.textDefaultPosition[0] - 20)):
		#if (size[0] > (self.rect.width - self.textDefaultPosition[0] - 22)):
		if (size[0] > (self.rect.width - 2*self.textDefaultPosition[0])):
			textPosition[0] = ((self.rect.width - self.textDefaultPosition[0]) - size[0])

		textImg = self.font.render(text, 1, color)
		self.image.blit(self.emptyImg, (0,0))
		#self.image.blit(textImg, self.textPos)
		self.image.blit(textImg, textPosition)

	def Click(self):
		self.focused=True
		self.SetDirty(True)
		if (not self.container is None):
			self.container.SetFocus(True)

	def SetText(self, newText):
		self.text = newText
		self.SetDirty(True)
		"""
		if ((not self.container is None) and (not self.container.container is None)):
			print self.container, self.container.dirty
			self.container.container.dirty = 1
			print "self.container.dirty = 1"
		"""

	def GetText(self):
		return self.text

	def OnKeyPressed(self, event):
		if self.focused:
			if event.key in self.backspaceKeys:
				#strip of last character
				newText = self.text[:-1]
				self.SetText(newText)
				return True
			# add the unicode character to the text
			newText = self.text + event.unicode
			self.SetText(newText)
			return True

	def OnMetaPressed(self, event):
		if self.focused and event.key in self.focusCycleKeys:
			#don't respond to the focus cycle keys
			return
		if self.focused and event.key in self.backspaceKeys:
			#strip of last character
			newText = self.text[:-1]
			self.SetText(newText)
			return True

	def OnMouseClick(self, pos):
		if self.rect.collidepoint(pos):
			self.Click()
			#print "textBox.OnMouseClick-if collidepoint,", pos
			return True
		elif self.focused:
			self.SetFocus(False)
			#print "textBox.OnMouseClick-elif focused,", pos
			return True

	def OnMouseMove(self, pos):
		if self.rect.collidepoint(pos):
			if not self.highlighted:
				self.SetHoverHighlight(True)
				return True
		elif self.highlighted:
			self.SetHoverHighlight(False)
			return True
