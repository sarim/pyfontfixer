#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pyfontfixer.py
#       
#       Copyright 2010 Sarim Khan <sarim2005@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


import gtk, pango ,os
from BeautifulSoup import BeautifulStoneSoup as BTS , Tag

class  pyfontfixer:

    def __init__(self):
        filename =  "/usr/share/pyfontfixer/gui.xml"
        self.builder = gtk.Builder()
        self.builder.add_from_file(filename)
        self.builder.connect_signals(self)
        self.builder.get_object ("window1").set_title("pyfontfixer")
        self.fontbutton1 = self.builder.get_object ("fontbutton1")
        self.fontbutton2 = self.builder.get_object ("fontbutton2")
        self.fontbutton3 = self.builder.get_object ("fontbutton3")
        self.fontbutton4 = self.builder.get_object ("fontbutton4")
        self.fontbutton5 = self.builder.get_object ("fontbutton5")
        self.fontbutton6 = self.builder.get_object ("fontbutton6")

    def on_button1_clicked (self,widget):
		self.sans[0].string = pango.FontDescription(self.fontbutton1.get_font_name()).get_family()
		self.sans[1].string = pango.FontDescription(self.fontbutton2.get_font_name()).get_family()
		self.serif[0].string = pango.FontDescription(self.fontbutton3.get_font_name()).get_family()
		self.serif[1].string = pango.FontDescription(self.fontbutton4.get_font_name()).get_family()
		self.monospace[0].string = pango.FontDescription(self.fontbutton5.get_font_name()).get_family()
		self.monospace[1].string = pango.FontDescription(self.fontbutton6.get_font_name()).get_family()

		savefonts(self.mathcs,self.alias,self.sans,self.serif,self.monospace)

    def on_button2_clicked (self,widget):
		resetfonts(self)
    def on_button3_clicked (self,widget):
		about = gtk.AboutDialog()
		about.set_program_name("pyfontfixer: Font Family Optimizer")
		about.set_version("0.2")
		about.set_copyright("(c) Sarim Khan")
		about.set_comments("""Font Family Optimizer aka pyfontfixer is a python app similar to “font fixer” in Windows but pyfontfixer offers you more flexible options for font setting which can set your First and Second font for “Sans” , "Sans-Serif" and "Monospace" Font-Family""")
		about.set_website("http://code.google.com/p/pyfontfixer/")
#		about.set_logo(gtk.gdk.pixbuf_new_from_file("battery.png"))
		about.run()
		about.destroy()
    def on_button4_clicked (self,widget):
		gtk.main_quit()
    def on_window1_delete_event	(self,widget,jani_na):
		gtk.main_quit()
    def on_window1_destroy_event(self,widget):
		gtk.main_quit()
def resetfonts(app) :
	xml = """<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">
	<fontconfig>
	</fontconfig>"""
	try :
		xml = open( os.getenv('HOME') + "/.fonts.conf").read()
	except:
		print ""

	soup = BTS(xml)
	app.mathcs   = soup.findAll('match')
	app.alias  = soup.findAll('alias')
	if len(app.alias) == 0 :
		xmls = open("/etc/fonts/conf.avail/60-latin.conf").read()
		soups = BTS(xmls)
		app.alias = soups.findAll('alias')
		firstime = True
		
	for alisstem in app.alias :
		if alisstem.family.string == "serif" :
			app.serif = alisstem.prefer.findAll('family')
		if  alisstem.family.string == "sans-serif" :
			app.sans = alisstem.prefer.findAll('family')
		if  alisstem.family.string == "monospace" :
			app.monospace = alisstem.prefer.findAll('family')
			
	app.fontbutton1.set_font_name(str(app.sans[0].string) + " 12")
	app.fontbutton2.set_font_name(str(app.sans[1].string) + " 12")
	app.fontbutton3.set_font_name(str(app.serif[0].string) + " 12")
	app.fontbutton4.set_font_name(str(app.serif[1].string) + " 12")
	app.fontbutton5.set_font_name(str(app.monospace[0].string) + " 12")
	app.fontbutton6.set_font_name(str(app.monospace[1].string) + " 12")

def savefonts(mathcs,alias,sans,serif,monospace) :
	newxml = """<?xml version="1.0"?><!DOCTYPE fontconfig SYSTEM "fonts.dtd">
	<fontconfig>
	</fontconfig>"""
	fsoup = BTS(newxml)
	fntcnf = fsoup.fontconfig
	for maiem in mathcs :
		fntcnf.insert(0,"\n")
		fntcnf.insert(1,maiem)
	for alaitem in alias :
		fntcnf.insert(0,"\n")
		fntcnf.insert(1,alaitem)
	outputfile = open(os.getenv('HOME') + "/.fonts.conf","w")
	outputfile.write(str(fsoup))
	outputfile.close()
			
app = pyfontfixer()
resetfonts(app)
gtk.main()
