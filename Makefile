DEST := $(HOME)/.gnome2/epiphany/extensions/
FILES := deliciouspost.ephy-extension deliciouspost.py delicious16.png delicious22.png delicious24.png delicious32.png

install:
	mkdir --parents $(DEST)
	cp $(FILES) $(DEST)
