#!/usr/bin/env bash
FILENAME=Proofs
rm -rf *.aux *.bbl *.blg *.log
pdflatex ${FILENAME}.tex </dev/null
bibtex ${FILENAME}.aux </dev/null
pdflatex ${FILENAME}.tex </dev/null
pdflatex ${FILENAME}.tex </dev/null