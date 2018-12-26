#/***************************************************************************
# SocleMos
#
# Outil de génération et de croisement de modes d'occupation du sol
#							 -------------------
#		begin				: 2018-11-08
#		git sha				: $Format:%H$
#		copyright			: (C) 2018 by Corentin Falcon (SIRS)
#		email				: corentin.falcone@sirs-fr.com
# ***************************************************************************/
#
#/***************************************************************************
# *																		 *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or	 *
# *   (at your option) any later version.								   *
# *																		 *
# ***************************************************************************/

#################################################
# Edit the following to match your sources lists
#################################################


#Add iso code for any locales you want to support here (space separated)
# default is no locales
# LOCALES = af
LOCALES =

# If locales are enabled, set the name of the lrelease binary on your system. If
# you have trouble compiling the translations, you may have to specify the full path to
# lrelease
#LRELEASE = lrelease
#LRELEASE = lrelease-qt4


# translation
SOURCES = \
	__init__.py \
	create_socle.py repair_socle.py socle_mos_plugin.py

PLUGINNAME = soclemos

PY_FILES = \
	__init__.py \
	create_socle.py repair_socle.py socle_mos_plugin.py

UI_FILES = interface_repair.py interface_socle.py

EXTRAS = metadata.txt icon.png

EXTRA_DIRS =

RESOURCE_FILES = resources.py



PEP8EXCLUDE=pydev,resources.py,conf.py,third_party,ui


default: compile

compile: $(UI_FILES) $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<

# The deploy  target only works on unix like operating system where
# the Python plugin directory is located at:
# $HOME/.qgis/python/plugins
deploy: compile
	mkdir -p $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(UI_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(RESOURCE_FILES) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)
	cp -vf $(EXTRAS) $(HOME)/.qgis/python/plugins/$(PLUGINNAME)

clean:
	@echo
	@echo "------------------------------------"
	@echo "Removing uic and rcc generated files"
	@echo "------------------------------------"
	rm $(COMPILED_UI_FILES) $(COMPILED_RESOURCE_FILES)
