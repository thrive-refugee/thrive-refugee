# Python settings
ifndef TRAVIS
	PYTHON_MAJOR := 2
	PYTHON_MINOR := 7
endif

# Project settings
PROJECT := thrive-refugee
PACKAGE := thrive_refugee refugee_manager employment_manager swingtime esl_manager donors
SOURCES := Makefile requirements.txt

# System paths
PLATFORM := $(shell python -c 'import sys; print(sys.platform)')
ifneq ($(findstring win32, $(PLATFORM)), )
	SYS_PYTHON_DIR := C:\\Python$(PYTHON_MAJOR)$(PYTHON_MINOR)
	SYS_PYTHON := $(SYS_PYTHON_DIR)\\python.exe
	SYS_VIRTUALENV := $(SYS_PYTHON_DIR)\\Scripts\\virtualenv.exe
	# https://bugs.launchpad.net/virtualenv/+bug/449537
	export TCL_LIBRARY=$(SYS_PYTHON_DIR)\\tcl\\tcl8.5
else
	SYS_PYTHON := python$(PYTHON_MAJOR)
	ifdef PYTHON_MINOR
		SYS_PYTHON := $(SYS_PYTHON).$(PYTHON_MINOR)
	endif
	SYS_VIRTUALENV := virtualenv
endif

# virtualenv paths
ENV := env
ifneq ($(findstring win32, $(PLATFORM)), )
	BIN := $(ENV)/Scripts
	OPEN := cmd /c start
else
	BIN := $(ENV)/bin
	ifneq ($(findstring cygwin, $(PLATFORM)), )
		OPEN := cygstart
	else
		OPEN := open
	endif
endif

# virtualenv executables
PYTHON := $(BIN)/python
PIP := $(BIN)/pip
EASY_INSTALL := $(BIN)/easy_install
RST2HTML := $(PYTHON) $(BIN)/rst2html.py
PDOC := $(PYTHON) $(BIN)/pdoc
PEP8 := $(BIN)/pep8
PEP8RADIUS := $(BIN)/pep8radius
PEP257 := $(BIN)/pep257
PYLINT := $(BIN)/pylint
PYREVERSE := $(BIN)/pyreverse
NOSE := $(BIN)/nosetests
PYTEST := $(BIN)/py.test
COVERAGE := $(BIN)/coverage

# Remove if you don't want pip to cache downloads
PIP_CACHE_DIR := .cache
PIP_CACHE := --download-cache $(PIP_CACHE_DIR)

# Flags for PHONY targets
INSTALLED :=$(ENV)/.installed
DEPENDS_CI := $(ENV)/.depends-ci
DEPENDS_DEV := $(ENV)/.depends-dev
ALL := $(ENV)/.all

# Main Targets ###############################################################

.PHONY: all
all: depends $(ALL)
$(ALL): $(SOURCES)
	$(MAKE) pep8
	# TODO: gradually add these steps back in as they start passing
	# ci: pep257 pylint
	touch $(ALL)  # flag to indicate all setup steps were successful

.PHONY: ci
ci: env db pep8 test
# TODO: gradually add these steps back in as they start passing
# ci: pep257 pylint

# Development Installation ###################################################

.PHONY: env
env: .virtualenv $(INSTALLED) thrive_refugee/local_settings.py
$(INSTALLED): requirements.txt
	VIRTUAL_ENV=$(ENV) $(PIP) install -r requirements.txt $(PIP_CACHE)
	touch $(INSTALLED)  # flag to indicate project is installed

.PHONY: .virtualenv
.virtualenv: $(PIP)
$(PIP):
	$(SYS_VIRTUALENV) --python $(SYS_PYTHON) $(ENV)

thrive_refugee/local_settings.py:
	cp thrive_refugee/local_settings.default thrive_refugee/local_settings.py

.PHONY: depends
depends: .depends-ci .depends-dev

.PHONY: .depends-ci
.depends-ci: env Makefile $(DEPENDS_CI)
$(DEPENDS_CI): Makefile
	$(PIP) install $(PIP_CACHE) --upgrade pep8 pep257 coverage
	touch $(DEPENDS_CI)  # flag to indicate dependencies are installed

.PHONY: .depends-dev
.depends-dev: env Makefile $(DEPENDS_DEV)
$(DEPENDS_DEV): Makefile
	$(PIP) install $(PIP_CACHE) --upgrade pep8radius pylint
	touch $(DEPENDS_DEV)  # flag to indicate dependencies are installed

# Static Analysis ############################################################

.PHONY: check
check: pep8 pep257 pylint

.PHONY: pep8
pep8: .depends-ci
	$(PEP8) $(PACKAGE) --ignore=E501

.PHONY: pep257
pep257: .depends-ci
	$(PEP257) $(PACKAGE)

.PHONY: pylint
pylint: .depends-dev
	$(PYLINT) $(PACKAGE) --rcfile=.pylintrc

.PHONY: fix
fix: .depends-dev
	$(PEP8RADIUS) --docformatter --in-place

# Testing ####################################################################

.PHONY: test
test: .depends-ci
	$(COVERAGE) erase
	$(COVERAGE) run --source='.' manage.py test
	$(COVERAGE) report --fail-under=45

# Cleanup ####################################################################

.PHONY: clean
clean: .clean-dist .clean-test .clean-doc .clean-build clean-db
	rm -rf $(ALL)

.PHONY: clean-env
clean-env: clean
	rm -rf $(ENV)

.PHONY: clean-all
clean-all: clean clean-env .clean-workspace .clean-cache

.PHONY: .clean-build
.clean-build:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf *.egg-info

.PHONY: .clean-doc
.clean-doc:
	rm -rf README.rst apidocs docs/*.html docs/*.png

.PHONY: .clean-test
.clean-test:
	rm -rf .coverage

.PHONY: .clean-dist
.clean-dist:
	rm -rf dist build

.PHONY: .clean-cache
.clean-cache:
	rm -rf $(PIP_CACHE_DIR)

.PHONY: .clean-workspace
.clean-workspace:
	rm -rf *.sublime-workspace
	rm -rf .settings

# Server ####################################################################

MANAGE := $(PYTHON) manage.py
DB := thrive.db

.PHONY: db
db: env $(DB)
$(DB): */fixtures/*.json
	$(MAKE) syncdb loaddata

.PHONY: clean-db
clean-db: env
	rm -f $(DB)
	rm -f thrive_refugee/local_settings.py

.PHONY: syncdb
syncdb: env
	$(MANAGE) syncdb --noinput

.PHONY: loaddata
loaddata: env */fixtures/*.json
	$(MANAGE) loaddata thrive_refugee/fixtures/auth.json
	$(MANAGE) loaddata esl_manager/fixtures/eslstudent.json
	$(MANAGE) loaddata esl_manager/fixtures/attended.json
	$(MANAGE) loaddata esl_manager/fixtures/assesment.json
	$(MANAGE) loaddata refugee_manager/fixtures/volunteer.json
	$(MANAGE) loaddata refugee_manager/fixtures/case.json
	$(MANAGE) loaddata refugee_manager/fixtures/individual.json
	$(MANAGE) loaddata refugee_manager/fixtures/casedetail.json
	$(MANAGE) loaddata refugee_manager/fixtures/activitynote.json
	$(MANAGE) loaddata refugee_manager/fixtures/assessment.json
	$(MANAGE) loaddata swingtime/fixtures/eventtype.json
	$(MANAGE) loaddata swingtime/fixtures/event.json
	$(MANAGE) loaddata employment_manager/fixtures/employmentclient.json
	$(MANAGE) loaddata employment_manager/fixtures/job.json
	$(MANAGE) loaddata employment_manager/fixtures/skill.json
	$(MANAGE) loaddata employment_manager/fixtures/assesment.json
	$(MANAGE) loaddata employment_manager/fixtures/language.json
	$(MANAGE) loaddata donors/fixtures/donors.json
	$(MANAGE) loaddata donors/fixtures/donations.json

.PHONY: dumpdata
dumpdata: env
	$(MANAGE) dumpdata auth > thrive_refugee/fixtures/auth.json
	$(MANAGE) dumpdata esl_manager.ESLStudent > esl_manager/fixtures/eslstudent.json
	$(MANAGE) dumpdata esl_manager.Attended > esl_manager/fixtures/attended.json
	$(MANAGE) dumpdata esl_manager.Assesment > esl_manager/fixtures/assesment.json
	$(MANAGE) dumpdata refugee_manager.Volunteer > refugee_manager/fixtures/volunteer.json
	$(MANAGE) dumpdata refugee_manager.Case > refugee_manager/fixtures/case.json
	$(MANAGE) dumpdata refugee_manager.Individual > refugee_manager/fixtures/individual.json
	$(MANAGE) dumpdata refugee_manager.CaseDetail > refugee_manager/fixtures/casedetail.json
	$(MANAGE) dumpdata refugee_manager.ActivityNote > refugee_manager/fixtures/activitynote.json
	$(MANAGE) dumpdata refugee_manager.Assessment > refugee_manager/fixtures/assessment.json
	$(MANAGE) dumpdata swingtime.EventType > swingtime/fixtures/eventtype.json
	$(MANAGE) dumpdata swingtime.Event > swingtime/fixtures/event.json
	$(MANAGE) dumpdata employment_manager.EmploymentClient > employment_manager/fixtures/employmentclient.json
	$(MANAGE) dumpdata employment_manager.Job > employment_manager/fixtures/job.json
	$(MANAGE) dumpdata employment_manager.Skill > employment_manager/fixtures/skill.json
	$(MANAGE) dumpdata employment_manager.Assesment > employment_manager/fixtures/assesment.json
	$(MANAGE) dumpdata employment_manager.Language > employment_manager/fixtures/language.json
	$(MANAGE) dumpdata donors.Donor > donors/fixtures/donors.json
	$(MANAGE) dumpdata donors.Donation > donors/fixtures/donations.json

.PHONY: run
run: env $(DB) syncdb
	$(MANAGE) runserver

.PHONY: launch
launch: env $(DB) syncdb
	eval "sleep 1; $(OPEN) http://127.0.0.1:8000" &
	$(MAKE) run

.PHONY: run-private
run-private: run

.PHONY: launch-private
launch-private: launch

.PHONY: run-public
run-public: env $(DB) syncdb
	$(MANAGE) runserver 0.0.0.0:8000

.PHONY: launch-public
launch-public: env $(DB) syncdb
	eval "sleep 1; $(OPEN) http://localhost:8000" &
	$(MAKE) run-public
