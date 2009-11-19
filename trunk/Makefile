VERSION:=$(shell date +"%Y%m%d")
PKGNAME=heuristica
FAMILY=Heuristica
SFDFILES=$(FAMILY)-Regular.sfd $(FAMILY)-Italic.sfd $(FAMILY)-Bold.sfd $(FAMILY)-BoldItalic.sfd
DOCUMENTS=OFL.txt OFL-FAQ.txt FontLog.txt
OTFFILES=$(FAMILY)-Regular.otf $(FAMILY)-Italic.otf $(FAMILY)-Bold.otf $(FAMILY)-BoldItalic.otf
TTFFILES=$(FAMILY)-Regular.ttf $(FAMILY)-Italic.ttf $(FAMILY)-Bold.ttf $(FAMILY)-BoldItalic.ttf
PFBFILES=$(FAMILY)-Regular.pfb $(FAMILY)-Italic.pfb $(FAMILY)-Bold.pfb $(FAMILY)-BoldItalic.pfb
AFMFILES=$(FAMILY)-Regular.afm $(FAMILY)-Italic.afm $(FAMILY)-Bold.afm $(FAMILY)-BoldItalic.afm
FFSCRIPTS=generate.ff make_dup_vertshift.pe new_glyph.ff add_anchor_ext.ff \
	add_anchor_y.ff add_anchor_med.ff anchors.ff combining.ff make_comb.ff \
	dub_glyph.pe spaces_dashes.ff case_sub.ff add_ipa.ff hflip_glyph.ff \
	make_dup_rot.ff add_accented.ff dub_glyph_ch.ff same_cyrext.ff \
	make_cap_accent.ff make_superscript.ff dub_aligned.ff same_kern.ff \
	make_kern.ff cop_kern_left.ff cop_kern_right.ff cop_kern_acc.ff \
	cop_kern.ff cop_kern_mult.ff copy_anchors_acc.ff liga_sub.ff \
	COPYING.scripts
#DIFFFILES=$(FAMILY)-Regular.gen.xgf.diff # $(FAMILY)-Italic.gen.xgf.diff $(FAMILY)-Bold.gen.xgf.diff $(FAMILY)-BoldItalic.gen.xgf.diff
XGFFILES=$(FAMILY)-Regular.ed.xgf # $(FAMILY)-Italic.ed.xgf $(FAMILY)-Bold.ed.xgf $(FAMILY)-BoldItalic.ed.xgf
COMPRESS=xz -9

all: $(OTFFILES) ttf

$(FAMILY)-Regular.otf: $(FAMILY)-Regular.sfd $(FFSCRIPTS)
	fontforge -lang=ff -script generate.ff $(FAMILY)-Regular UTRG__

$(FAMILY)-Italic.otf: $(FAMILY)-Italic.sfd $(FFSCRIPTS)
	fontforge -lang=ff -script generate.ff $(FAMILY)-Italic UTI___

$(FAMILY)-Bold.otf: $(FAMILY)-Bold.sfd $(FFSCRIPTS)
	fontforge -lang=ff -script generate.ff $(FAMILY)-Bold UTB___

$(FAMILY)-BoldItalic.otf: $(FAMILY)-BoldItalic.sfd $(FFSCRIPTS)
	fontforge -lang=ff -script generate.ff $(FAMILY)-BoldItalic UTBI__

%.pdf: %.otf
	fntsample -f $< -o $@

# We don't want to change anything in autoinstructed following faces:
$(FAMILY)-Italic.ttf: $(FAMILY)-Italic.gen.ttf $(FAMILY)-Italic.otf
	cp -p $(FAMILY)-Italic.gen.ttf $(FAMILY)-Italic.ttf

$(FAMILY)-Bold.ttf: $(FAMILY)-Bold.gen.ttf $(FAMILY)-Bold.otf
	cp -p $(FAMILY)-Bold.gen.ttf $(FAMILY)-Bold.ttf

$(FAMILY)-BoldItalic.ttf: $(FAMILY)-BoldItalic.gen.ttf $(FAMILY)-BoldItalic.otf
	cp -p $(FAMILY)-BoldItalic.gen.ttf $(FAMILY)-BoldItalic.ttf

$(FAMILY)-Regular.gen.ttf: $(FAMILY)-Regular.otf

%.ttf: %.pe %.gen.ttf %.otf
	fontforge -lang=ff -script $*.pe

#%.gen.ttf: %.otf

%.gen.ttx: %.gen.ttf %.otf
	-rm $*.gen.ttx
	ttx $*.gen.ttf

%.gen.xgf: %.gen.ttx
	-rm $*.gen.xgf
	ttx2xgf $*.gen.ttx
#	patch -l --no-backup-if-mismatch < $*.gen.xgf.diff

%.xml: %.gen.xgf %.ed.xgf
	xgfmerge -o $@ $^

%.pe: %.xml
	xgridfit -p 25 -G no -i $*.gen.ttf -o $*.ttf $<

#$(FAMILY)-Regular.ttf: $(FAMILY)-Regular.pe # $(FAMILY)-Regular.gen.ttf
#	fontforge -lang=ff -script $(FAMILY)-Regular.pe

.SECONDARY : *.pe *.xml *.gen.xgf *.gen.ttx

ttf: $(TTFFILES)

dist-src:
	tar -cvf $(PKGNAME)-src-$(VERSION).tar $(SFDFILES) Makefile \
	$(FFSCRIPTS) $(DOCUMENTS) $(XGFFILES) $(DIFFFILES)
	$(COMPRESS) $(PKGNAME)-src-$(VERSION).tar

dist-otf: all
	tar -cvf $(PKGNAME)-otf-$(VERSION).tar \
	$(OTFFILES) $(DOCUMENTS)
	$(COMPRESS) $(PKGNAME)-otf-$(VERSION).tar

dist-ttf: all
	tar -cvf $(PKGNAME)-ttf-$(VERSION).tar \
	$(TTFFILES) $(DOCUMENTS)
	$(COMPRESS) $(PKGNAME)-ttf-$(VERSION).tar

dist-pfb: all
	tar -cvf $(PKGNAME)-pfb-$(VERSION).tar \
	$(PFBFILES) $(AFMFILES) $(DOCUMENTS)
	$(COMPRESS) $(PKGNAME)-pfb-$(VERSION).tar

dist: dist-src dist-otf dist-ttf

update-version:
	sed -e "s/^Version: .*$$/Version: $(VERSION)/" -i $(SFDFILES)

.PHONY : clean
clean :
	rm *.gen.ttx *..gen.xgf

distclean :
	-rm $(OTFFILES) $(TTFFILES) $(PFBFILES) $(AFMFILES) $(FAMILY)-*_.sfd
