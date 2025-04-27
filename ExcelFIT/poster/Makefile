#####################################                                                                                                                                                                          
# Autor: Tomas Bartu                #
# Email: xbartu11@stud.fit.vutbr.cz #
# Datum: 2025-04-27                 #
##################################### 

SHELL=/bin/bash
NAME=poster

all: pdflatex

bibtex: $(NAME).aux
	bibtex $(NAME)

pdflatex: $(NAME).tex
	pdflatex -jobname=$(NAME) $^
	pdflatex -jobname=$(NAME) $^
	pdflatex -jobname=$(NAME) $^

clean:
	rm -rf $(NAME).{aux,dvi,log,ps,fls,synctex.gz,fdb_latexmk,out,toc,bbl,blg}
