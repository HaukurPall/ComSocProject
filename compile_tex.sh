#!/usr/bin/env bash
FILENAME=project
pdflatex ${FILENAME}.tex </dev/null
bibtex ${FILENAME}.aux </dev/null
pdflatex ${FILENAME}.tex </dev/null
pdflatex ${FILENAME}.tex </dev/null