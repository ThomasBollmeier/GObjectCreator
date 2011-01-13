# Templates:

goctemplatedir = $(datarootdir)/$(PACKAGE)/templates

valatemplatedir = $(goctemplatedir)/vala
csharptemplatedir = $(goctemplatedir)/csharp
gobjecttemplatedir = $(goctemplatedir)/gobject

dist_valatemplate_DATA = \
templates/vala/class.tmpl \
templates/vala/intf.tmpl

dist_csharptemplate_DATA = \
templates/csharp/class.tmpl \
templates/csharp/intf.tmpl

dist_gobjecttemplate_DATA = \
templates/gobject/class_source.tmpl \
templates/gobject/intf_source.tmpl \
templates/gobject/enum_class_header.tmpl \
templates/gobject/class_header.tmpl \
templates/gobject/error_domain_source.tmpl \
templates/gobject/enum_class_source.tmpl \
templates/gobject/flags.tmpl \
templates/gobject/intf_header.tmpl \
templates/gobject/class_header_protected.tmpl \
templates/gobject/error_domain_header.tmpl

# Icons:

icondir = $(datarootdir)/$(PACKAGE)/icons
dist_icon_DATA = \
icons/GObjectCreator.xpm

uninstall-hook:
	rm -rf $(DESTDIR)$(datadir)/$(PACKAGE)
