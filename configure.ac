#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.65])
AC_INIT([gobject_creator], [m4_esyscmd([./get_goc_version.sh | tr -d '\n'])], [TBollmeier@web.de])

AM_INIT_AUTOMAKE

# For RPM spec file creation:

AC_SUBST([GOC_RPM_INSTALL], [/opt/gobject_creator])

GOC_RPM_INSTALL=/opt/gobject_creator

AC_ARG_WITH(
[rpm-install],
[AS_HELP_STRING(
[--with-rpm-install=RPM_INSTALL_DIR], 
[set installation root path in RPM spec file to RPM_INSTALL_DIR @<:@/opt/gobject_creator@:>@]
)], 
[GOC_RPM_INSTALL=${withval}]
)

AC_SUBST([GOC_RPM_INSTALL])

# Checks for programs.
AC_PROG_CC
AC_CHECK_PROG([GLIB_GENMARSHAL], [glib-genmarshal], [yes], [no])
if test $GLIB_GENMARSHAL = "no"; then
	AC_MSG_ERROR([glib-genmarshal is needed by GObjectCreator])
fi
AM_PATH_PYTHON([3.0])

# Checks for libraries.

# Checks for header files.

# Checks for typedefs, structures, and compiler characteristics.

# Checks for library functions.

AC_CONFIG_FILES([
create_rpmspec.sh
Makefile
src/Makefile
src/gobject_creator/Makefile
src/gobject_creator/create_config_module.sh
data/Makefile
doc/Makefile
examples/Makefile
])
AC_OUTPUT
