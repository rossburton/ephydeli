DEST := $(HOME)/.gnome2/epiphany/extensions/
FILES := deliciouspost.ephy-extension deliciouspost.py delicious.png
DIST_FILES := $(FILES) README COPYING Makefile

install:
	mkdir --parents $(DEST)
	cp $(FILES) $(DEST)

dist:
	mkdir ephydeli
	cp $(DIST_FILES) ephydeli
	tar zcvf ephydeli.tar.gz ephydeli
	rm -rf ephydeli
