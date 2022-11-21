
ifeq ($(OS),Windows_NT)
    detected_OS := Windows
    PYTHON = py
else
    detected_OS := $(shell uname)  # same as "uname -s"
    PYTHON = python3
endif


# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY = help install clean_install documentation

# Defines the default target that `make` will to try to make, or in the case of a phony target, execute the specified commands
# This target is executed whenever we just type `make`
.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "to install the project type make install"
	@echo "to create docs run make documentation"
	@echo "------------------------------------"

install:
	${PYTHON} -m pip install .


clean_install:
	${PYTHON} setup.py bdist_wheel clean
	${PYTHON} -m pip install .


documentation:
	${PYTHON} setup.py build_sphinx
