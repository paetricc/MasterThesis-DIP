#####################################                                                                                                                                                                          
# Autor: Tomas Bartu                #
# Email: xbartu11@stud.fit.vutbr.cz #
# Datum: 2025-04-27                 #
##################################### 

SHELL=/bin/bash
NAME=poster
SUBDIRS:=paper poster
ZIPFILE:=xbartu11_Kvantově\ inspirované\ optimalizační\ algoritmy_2.zip
ZIPFILES:=nahled.png paper/abstrakt.pdf poster/poster.pdf


.PHONY: all clean $(SUBDIRS)

all: $(SUBDIRS)

$(SUBDIRS):
	$(MAKE) -C $@

zip: $(ZIPFILES)
	zip -j $(ZIPFILE) $(ZIPFILES)

clean:
	for dir in $(SUBDIRS); do \
		$(MAKE) -C $$dir clean; \
	done
	rm -f $(ZIPFILE)
