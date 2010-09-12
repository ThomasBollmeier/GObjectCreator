#!/bin/bash

# ====== Pythondateien durchsuchen: 

py_files=""
for fname in `find $1 -name '*.py' -type f`; do 
    py_files="$py_files $fname"
done
xgettext -o $2 $py_files

# ====== Glade-Dateien durchsuchen: 

ui_files=""
for fname in `find $1 -name '*.ui' -type f`; do 
    ui_files="$ui_files $fname"
done
xgettext -L Glade --join-existing -o $2 $ui_files


