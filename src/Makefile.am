dist_bin_SCRIPTS = create_gobjects

SUBDIRS = gobject_creator

install-exec-hook:
	cd $(DESTDIR)$(bindir); mv create_gobjects gobject_creator

uninstall-hook:
	cd $(DESTDIR)$(bindir); rm -rf gobject_creator
