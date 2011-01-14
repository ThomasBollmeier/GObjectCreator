AUTOMAKE_OPTIONS = dist-bzip2

SUBDIRS = src data doc examples

rpmspec:
	@echo -n "Creating RPM spec file $(PACKAGE)-$(PACKAGE_VERSION).spec ..."
	@sh create_rpmspec.sh $(bindir) $(pkgpythondir) $(datarootdir)
	@echo "done"

clean-local:
	rm -rf *.spec

distclean-local:
	rm -rf create_rpmspec.sh

