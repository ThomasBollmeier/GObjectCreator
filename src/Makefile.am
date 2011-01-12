dist_bin_SCRIPTS = create_gobjects

SUBDIRS = gobject_creator

install-exec-hook:
	cd $(bindir); mv create_gobjects gobject_creator

uninstall-hook:
	cd $(bindir); rm -rf gobject_creator
