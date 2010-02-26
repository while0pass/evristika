#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Copyright (C) 2010 Andrey V. Panov
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see "http://www.gnu.org/licenses/".
import fontforge
import sys, re, getopt
import unicodedata

strip_suff = re.compile("\..*$", re.I)

def extrema_points(glyf):
  global font, subref, point_bot, point_left, point_top, point_right, point_num
  if  not(subref):
    point_bot = (0.0, 32768.0, 0)
    point_top = (0.0, -32768.0, 0)
    point_left = (32768.0, 0.0, 0)
    point_right = (-32768.0, 0.0, 0)
  for contour in font[glyf].foreground:
    for point in contour:
      #print point.x+shift_x, point.y+shift_y, point_num
      if point.y+shift_y < point_bot[1]:
        point_bot = (point.x+shift_x, point.y+shift_y, point_num)
      if point.y+shift_y > point_top[1]:
        point_top = (point.x+shift_x, point.y+shift_y, point_num)
      if point.x+shift_x < point_left[0]:
        point_left = (point.x+shift_x, point.y+shift_y, point_num)
      if point.x+shift_x > point_right[0]:
        point_right = (point.x+shift_x, point.y+shift_y, point_num)
      point_num += 1

def ref_data(ref, ref_cont, glyfname):
  global shift_x, shift_y, cont_num, point_num, ref_type, basedata, accdata, point_bot, point_left, point_top, point_right
  #print ref[0], ref_cont,  len(font[ref[0]].references)
  #shift_x += ref[1][4]
  #shift_y += ref[1][5]
  cont_num_prev = cont_num
  cont_num += ref_cont
  reftemp = extrema_points(ref[0])
  if ref_type == 'Ll' or ref_type == 'Lu':
    basedata += (point_bot, point_left, point_top, point_right, \
    range(cont_num_prev,cont_num), glyfname)
  elif ref_type == 'Mn' or ref_type == 'Sk' or ref_type == 'Lm':
    accdata += (point_bot, point_left, point_top, point_right, \
    range(cont_num_prev,cont_num), glyfname),

def dig_subrefs(refs, glyfname):
  global font, shift_x, shift_y, cont_num, point_num, ref_type, basedata, accdata, cont_num_prev
  for ref in refs:
    shift_x += ref[1][4]
    shift_y += ref[1][5]
    ref_cont = len(font[ref[0]].foreground)
    ref_ref = font[ref[0]].references
    if ref_cont > 0:
      cont_num += ref_cont
      reftemp = extrema_points(ref[0])
      shift_x -= ref[1][4]
      shift_y -= ref[1][5]
    elif len(ref_ref) >= 1:
      dig_subrefs(ref_ref, glyfname)
      shift_x -= ref[1][4]
      shift_y -= ref[1][5]

def usage():
  print " -i file, --input=file     input truetype font file"
  print " -o file, --output=file    output xgridfit file"
  print " -v , --only-vertical      add only instructions for vertical placement"

try:
  opts, args = getopt.getopt(sys.argv[1:], "hvi:o:", ["help", "only-vertical", "input=", "output="])
except getopt.GetoptError, err:
  print "unrecognized option"
  usage()
  sys.exit(2)
outfile = None
font_name = None
only_vertical = 0
for (o, a) in opts:
  if o in ("-i", "--input"):
    font_name = a
  elif o in ("-h", "--help"):
    usage()
    sys.exit()
  elif o in ("-o", "--output"):
    outfile = a
  elif o in ("-v", "--only-vertical"):
    only_vertical = 1
#font_name = sys.argv[1]
font = fontforge.open(font_name)
f = open(outfile, 'w')
font.selection.all()
#font.selection.select("aacute,edieresis,uni1E69,afii10110,uni04F3")
f.write("<?xml version=\"1.0\"?>\n<xgridfit xmlns=\"http://xgridfit.sourceforge.net/Xgridfit2\">\n<!-- GENERATED FILE, DO NOT EDIT -->\n")
for glyf in font.selection:
  if glyf.isWorthOutputting and not(len(glyf.ttinstrs)):
    #print glyf.glyphname
    refs = glyf.references
    #print len(refs), refs, len(glyf.foreground)
    subref = 0
    cont_num = 0
    point_num = 0
    basedata = ()
    accdata = ()
    for ref in refs:
      shift_x = ref[1][4]
      shift_y = ref[1][5]
      ref_cont = len(font[ref[0]].foreground)
      uni_index = fontforge.unicodeFromName(strip_suff.split(ref[0])[0])
      #print uni_index,
      if ref[0] == "cyrbreve" or ref[0] == "cyrBreve":
	ref_type = 'Mn'
      elif uni_index >= 0:
	ref_type = unicodedata.category(unichr(fontforge.unicodeFromName(strip_suff.split(ref[0])[0])))
      else:
        break
      #print ref_type
      if ref_cont > 0:
        subref = 0
	ref_data(ref, ref_cont, ref[0])
      elif len(font[ref[0]].references) >= 1:
        subref = 1
	point_bot = (0.0, 32768.0, 0)
	point_top = (0.0, -32768.0, 0)
	point_left = (32768.0, 0.0, 0)
	point_right = (-32768.0, 0.0, 0)
        cont_num_prev = cont_num
        dig_subrefs(font[ref[0]].references, ref[0])
	if ref_type == 'Ll' or ref_type == 'Lu':
	  basedata += (point_bot, point_left, point_top, point_right, \
	  range(cont_num_prev,cont_num), ref[0])
	elif ref_type == 'Mn' or ref_type == 'Sk' or ref_type == 'Lm':
	  accdata += (point_bot, point_left, point_top, point_right, \
	  range(cont_num_prev,cont_num), ref[0]),
    #print basedata, accdata
    glyph_head_printed = 0
    glyph_head = " <glyph ps-name=\"%s\" init-graphics=\"yes\">\n"
    if basedata and accdata:
      for t in accdata:
	if t[0][1] > basedata[2][1]: # above accent
	  if not(glyph_head_printed):
	    glyph_head_printed = 1
	    f.write(glyph_head % glyf.glyphname)
	  f.write("  <set-vectors axis=\"y\"/>\n")
	  f.write("  <if test=\"(%d -- %d) &lt; 0.6p\">\n" % (basedata[2][2], t[0][2]))
	  f.write("   <shift-absolute pixel-distance=\"1.0p\">\n    <point num=\"%d\"/>\n" % t[0][2])
	  f.write("   </shift-absolute>\n   <shift>\n    <reference>\n     <point num=\"%d\"/>\n    </reference>\n" % t[0][2])
	  for i in t[4]:
	    f.write("    <contour num=\"%d\"/>\n" % i)
	  f.write("   </shift>\n  </if>\n")
	elif t[2][1] < basedata[0][1]: # below accent
	  if not(glyph_head_printed):
	    glyph_head_printed = 1
	    f.write(glyph_head % glyf.glyphname)
	  f.write("  <set-vectors axis=\"y\"/>\n")
	  f.write("  <if test=\"(%d -- %d) &lt; 0.6p\">\n" % (t[2][2], basedata[0][2] ))
	  f.write("   <shift-absolute pixel-distance=\"-1.0p\">\n    <point num=\"%d\"/>\n" % t[2][2])
	  f.write("   </shift-absolute>\n   <shift>\n    <reference>\n     <point num=\"%d\"/>\n    </reference>\n" % t[2][2])
	  for i in t[4]:
	    f.write("    <contour num=\"%d\"/>\n" % i)
	  f.write("   </shift>\n  </if> <!-- -->\n")
	if t[1][0] >= basedata[1][0] and t[3][0] <= basedata[3][0] and not(only_vertical): # shift accent along x
	  if not(glyph_head_printed):
	    glyph_head_printed = 1
	    f.write(glyph_head % glyf.glyphname)
	  f.write("  <set-vectors axis=\"x\"/>\n")
	  f.write("  <call-macro name=\"shift-accent\">\n")
	  f.write("   <with-param name=\"point-base-left\" value=\"%d\"/>\n" % basedata[1][2])
	  f.write("   <with-param name=\"point-base-right\" value=\"%d\"/>\n" % basedata[3][2])
	  f.write("   <with-param name=\"point-acc-left\" value=\"%d\"/>\n" % t[1][2])
	  f.write("   <with-param name=\"point-acc-right\" value=\"%d\"/>\n" % t[3][2])
	  f.write("  </call-macro>\n  <shift>\n   <reference>\n    <point num=\"%d\"/>\n   </reference>\n" % t[1][2])
	  for i in t[4]:
	    f.write("   <contour num=\"%d\"/> <!-- -->\n" % i)
	  f.write("  </shift>\n")
      if glyph_head_printed:
	f.write(" </glyph> \n")
f.write("</xgridfit>")
f.close()

