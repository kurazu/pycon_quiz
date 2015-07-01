#!/bin/bash
for file in ../solutions/official/*.py
do
    echo ${file}
    pygmentize -f html -l python -o "${file}.html" "${file}"
done

python make.py
