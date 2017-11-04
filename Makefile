# Python settings
ifndef TRAVIS
	PYTHON_MAJOR := 3
	PYTHON_MINOR := 6
endif

# Project settings
PROJECT := thrive-refugee
PACKAGE := thrive_refugee refugee_manager employment_manager esl_manager donors
SOURCES := Makefile requirements.txt

# System paths
PLATFORM := $(shell python -c 'import sys; print(sys.platform)')
ifneq ($(findstring win32, $(PLATFORM)), )
	SYS_PYTHON := python
	SYS_VIRTUALENV := virtualenv
	# https://bugs.launchpad.net/virtualenv/+bug/449537
#	export TCL_LIBRARY=$(SYS_PYTHON_DIR)\\tcl\\tcl8.5
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
PEP8 := $(BIN)/pycodestyle
PEP8RADIUS := $(BIN)/pep8radius
PEP257 := $(BIN)/pep257
PYLINT := $(BIN)/pylint
PYREVERSE := $(BIN)/pyreverse
NOSE := $(BIN)/nosetests
PYTEST := $(BIN)/py.test
COVERAGE := $(BIN)/coverage

# Flags for PHONY targets
INSTALLED :=$(ENV)/.installed
DEPENDS_CI := $(ENV)/.depends-ci
DEPENDS_DEV := $(ENV)/.depends-dev
ALL := $(ENV)/.all

# Main Targets ###############################################################

.PHONY: all
all: depends $(ALL)
$(ALL): $(SOURCES)
	$(MAKE) pycodestyle pylint
	touch $(ALL)  # flag to indicate all setup steps were successful

.PHONY: ci
ci: env db pycodestyle pylint test
# TODO: gradually add these steps back in as they start passing
# ci: pep257

# Development Installation ###################################################

.PHONY: env
env: .virtualenv $(INSTALLED) thrive_refugee/local_settings.py
$(INSTALLED): requirements.txt
	# TODO: the following line is required to install patched bootstrap-admin
	- $(PIP) uninstall bootstrap-admin --yes
	VIRTUAL_ENV=$(ENV) $(PIP) install -r requirements.txt
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
	$(PIP) install --upgrade pycodestyle pep257 coverage
	touch $(DEPENDS_CI)  # flag to indicate dependencies are installed

.PHONY: .depends-dev
.depends-dev: env Makefile $(DEPENDS_DEV)
$(DEPENDS_DEV): Makefile
	$(PIP) install --upgrade pep8radius pylint
	touch $(DEPENDS_DEV)  # flag to indicate dependencies are installed

# Static Analysis ############################################################

.PHONY: check
check: pycodestyle pep257 pylint

.PHONY: pycodestyle
pep8: pycodestyle

.PHONY: pycodestyle
pycodestyle: .depends-ci
	$(PEP8) $(PACKAGE) --ignore=E402,E501

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
	$(COVERAGE) run --source='.' manage.py test --verbosity=2
	$(COVERAGE) report --fail-under=52

# Cleanup ####################################################################

.PHONY: clean
clean: .clean-dist .clean-test .clean-doc .clean-build clean-db
	rm -rf $(ALL)

.PHONY: clean-env
clean-env: clean
	rm -rf $(ENV)

.PHONY: clean-all
clean-all: clean clean-env .clean-workspace

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

.PHONY: .clean-workspace
.clean-workspace:
	rm -rf *.sublime-workspace
	rm -rf .settings

# Server ####################################################################

MANAGE := $(PYTHON) manage.py
LOADDATA := $(MANAGE) loaddata
DUMPDATA := $(MANAGE) dumpdata --indent=2
DB := thrive.db

.PHONY: db
db: env $(DB)
$(DB): */fixtures/*.json
	$(MAKE) migrate loaddata

.PHONY: clean-db
clean-db: env
	rm -f $(DB)
	rm -f thrive_refugee/local_settings.py

.PHONY: migrate
migrate: env
	$(MANAGE) migrate --noinput

.PHONY: loaddata
loaddata: env */fixtures/*.json
	$(LOADDATA) thrive_refugee/fixtures/auth.json
	$(LOADDATA) esl_manager/fixtures/eslstudent.json
	$(LOADDATA) esl_manager/fixtures/attended.json
	$(LOADDATA) esl_manager/fixtures/assesment.json
	$(LOADDATA) refugee_manager/fixtures/volunteer.json
	$(LOADDATA) refugee_manager/fixtures/case.json
	$(LOADDATA) refugee_manager/fixtures/casefile.json
	$(LOADDATA) refugee_manager/fixtures/individual.json
	$(LOADDATA) refugee_manager/fixtures/casedetail.json
	$(LOADDATA) refugee_manager/fixtures/activitynote.json
	$(LOADDATA) refugee_manager/fixtures/assessment.json
	$(LOADDATA) thrive_refugee/fixtures/eventtype.json
	$(LOADDATA) thrive_refugee/fixtures/event.json
	$(LOADDATA) employment_manager/fixtures/employmentclient.json
	$(LOADDATA) employment_manager/fixtures/job.json
	$(LOADDATA) employment_manager/fixtures/skill.json
	$(LOADDATA) employment_manager/fixtures/assesment.json
	$(LOADDATA) employment_manager/fixtures/language.json
	$(LOADDATA) donors/fixtures/donors.json
	$(LOADDATA) donors/fixtures/donations.json

.PHONY: dumpdata
dumpdata: env
	$(DUMPDATA) auth > thrive_refugee/fixtures/auth.json
	$(DUMPDATA) esl_manager.ESLStudent > esl_manager/fixtures/eslstudent.json
	$(DUMPDATA) esl_manager.Attended > esl_manager/fixtures/attended.json
	$(DUMPDATA) esl_manager.Assesment > esl_manager/fixtures/assesment.json
	$(DUMPDATA) refugee_manager.Volunteer > refugee_manager/fixtures/volunteer.json
	$(DUMPDATA) refugee_manager.Case > refugee_manager/fixtures/case.json
	$(DUMPDATA) refugee_manager.CaseFile > refugee_manager/fixtures/casefile.json
	$(DUMPDATA) refugee_manager.Individual > refugee_manager/fixtures/individual.json
	$(DUMPDATA) refugee_manager.CaseDetail > refugee_manager/fixtures/casedetail.json
	$(DUMPDATA) refugee_manager.ActivityNote > refugee_manager/fixtures/activitynote.json
	$(DUMPDATA) refugee_manager.Assessment > refugee_manager/fixtures/assessment.json
	$(DUMPDATA) swingtime.EventType > thrive_refugee/fixtures/eventtype.json
	$(DUMPDATA) swingtime.Event > thrive_refugee/fixtures/event.json
	$(DUMPDATA) employment_manager.EmploymentClient > employment_manager/fixtures/employmentclient.json
	$(DUMPDATA) employment_manager.Job > employment_manager/fixtures/job.json
	$(DUMPDATA) employment_manager.Skill > employment_manager/fixtures/skill.json
	$(DUMPDATA) employment_manager.Assesment > employment_manager/fixtures/assesment.json
	$(DUMPDATA) employment_manager.Language > employment_manager/fixtures/language.json
	$(DUMPDATA) donors.Donor > donors/fixtures/donors.json
	$(DUMPDATA) donors.Donation > donors/fixtures/donations.json

.PHONY: run
run: env $(DB) migrate
	$(MANAGE) runserver

.PHONY: launch
launch: env $(DB) migrate
	eval "sleep 1; $(OPEN) http://127.0.0.1:8000" &
	$(MAKE) run

.PHONY: run-private
run-private: run

.PHONY: launch-private
launch-private: launch

.PHONY: run-public
run-public: env $(DB) migrate
	$(MANAGE) runserver 0.0.0.0:8000

.PHONY: launch-public
launch-public: env $(DB) migrate
	eval "sleep 1; $(OPEN) http://localhost:8000" &
	$(MAKE) run-public
