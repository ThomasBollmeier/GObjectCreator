#! /bin/sh

py3=`which python3`
PYTHONPATH=src; $py3 -c "import gobject_creator; print(gobject_creator.VERSION)"

