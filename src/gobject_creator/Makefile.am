gocdir = $(pkgpythondir)

goc_PYTHON = \
__init__.py

codegendir = $(gocdir)/code_generation

codegen_PYTHON = \
code_generation/bool_parser.py \
code_generation/generation_inout.py \
code_generation/parser.py \
code_generation/__init__.py \
code_generation/components.py \
code_generation/scope.py \
code_generation/translator.py \
code_generation/usercode.py

valagendir = $(codegendir)/vala

valagen_PYTHON = \
code_generation/vala/__init__.py \
code_generation/vala/generator_vala.py

csharpgendir = $(codegendir)/csharp

csharpgen_PYTHON = \
code_generation/csharp/__init__.py \
code_generation/csharp/generator_csharp.py

gobjectgendir = $(codegendir)/gobject

gobjectgen_PYTHON = \
code_generation/gobject/gobject_marshaller_generator.py \
code_generation/gobject/__init__.py \
code_generation/gobject/gobject_introspection_support.py \
code_generation/gobject/generator_gobject.py

metadir = $(gocdir)/metamodel

meta_PYTHON = \
metamodel/visitor.py \
metamodel/meta_objects.py \
metamodel/__init__.py \
metamodel/introspection_info.py \
metamodel/introspection_decorators.py \
metamodel/object_catalog.py

iodir = $(gocdir)/io

io_PYTHON = \
io/__init__.py \
io/py_input.py \
io/include_handling.py

install-data-local:
	chmod +x create_config_module.sh
	./create_config_module.sh $(datarootdir)
	mkdir -p $(gocdir)
	mv config.py $(gocdir)

uninstall-hook:
	rm -rf $(pkgpythondir)
