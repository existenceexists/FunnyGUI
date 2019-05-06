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


class InputBox(widget.Widget):
	def __init__(
			self,
			width=200,
			backspaceKeys=(pygame.K_BACKSPACE,),
			fontFace=None,
			fontSize=14,
			borderLineColor=(0,0,100),
			backgroundColor=(0,0,0),
			borderLineWidth=4,
			textNormalColor=(100,0,0),
			textFocusedColor=(255,255,0),
			textHighlightedColor=(255,0,0),
			textPositionX=22):
		widget.Widget.__init__(self)
		self.focused=False
		self.highlighted=False
		self.dirty=True
		self.backspaceKeys=list(backspaceKeys)
		self.textNormalColor=textNormalColor
		self.textFocusedColor=textFocusedColor
		self.textHighlightedColor=textHighlightedColor
		if fontFace is None:
			fontFace=pygame.font.match_font("freesans,sansserif,microsoftsansserif,arial,dejavusans,verdana,timesnewroman,helvetica")
		if fontFace is None:
			fontFace=pygame.font.match_font(pygame.font.get_fonts()[0])
		self.font=pygame.font.Font(fontFace,fontSize)
		linesize=self.font.get_linesize()
		self.rect=pygame.Rect((0,0,width,linesize+borderLineWidth))
		boxImg=pygame.Surface(self.rect.size).convert_alpha()
		boxImg.fill(backgroundColor)
		if (borderLineWidth > 0):
			pygame.draw.rect(boxImg,borderLineColor,self.rect,borderLineWidth)
		self.emptyImg=boxImg.convert_alpha()
		self.image=boxImg
		self.highlighted=0
		self.text=''
		self.textDefaultPosition=(textPositionX,(self.rect.height-linesize)//2)

	def update(self,event):
		if event.type==pygame.MOUSEMOTION:
			self.OnMouseMove(event.pos)
		elif event.type==pygame.MOUSEBUTTONDOWN:
                	self.OnMouseClick(event.pos)
		elif event.type==pygame.KEYDOWN:
                	self.OnKeyPressed(event)
		if self.dirty:
			self.CreateImage()
			self.dirty=False
			return self.rect

	def draw(self,surface):
		surface.blit(self.image,self.rect)

	def CreateImage(self):
		text=self.text
		if self.focused:
			text+='|'
			color=self.textFocusedColor
		elif self.highlighted:
			color=self.textHighlightedColor
		else: 
			color=self.textNormalColor
		textPosition=list(self.textDefaultPosition)
		size=self.font.size(text)
		if (size[0] > (self.rect.width-2*self.textDefaultPosition[0])):
			textPosition[0]=((self.rect.width-self.textDefaultPosition[0])-size[0])
		textImg=self.font.render(text,1,color)
		self.image.blit(self.emptyImg,(0,0))
		self.image.blit(textImg,textPosition)

	def Click(self):
		self.focused=True
		self.SetDirty(True)
		if (not self.container is None):
			self.container.SetFocus(True)

	def SetText(self,newText):
		self.text=newText
		self.SetDirty(True)

	def GetText(self):
		return self.text

	def OnKeyPressed(self,event):
		if self.focused:
			if event.key in self.backspaceKeys:
				#strip of last character
				newText=self.text[:-1]
				self.SetText(newText)
				return True
			# add the unicode character to the text
			newText=self.text + event.unicode
			self.SetText(newText)
			return True

	def OnMetaPressed(self,event):
		if self.focused and event.key in self.focusCycleKeys:
			#don't respond to the focus cycle keys
			return
		if self.focused and event.key in self.backspaceKeys:
			#strip of last character
			newText=self.text[:-1]
			self.SetText(newText)
			return True

	def OnMouseClick(self,pos):
		if self.rect.collidepoint(pos):
			self.Click()
			return True
		elif self.focused:
			self.SetFocus(False)
			return True

	def OnMouseMove(self,pos):
		if self.rect.collidepoint(pos):
			if not self.highlighted:
				self.SetHoverHighlight(True)
				return True
		elif self.highlighted:
			self.SetHoverHighlight(False)
			return True
