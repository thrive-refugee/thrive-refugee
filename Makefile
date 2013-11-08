WD := $(shell pwd)
VENV := $(WD)/venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MANAGE := $(WD)/manage.py
DEV := $(WD)/dev
DB := $(DEV)/thrive.db


# Install and Setup
.PHONY: install
install: reset_venv

.PHONY: create_venv
create_venv:
	virtualenv -p python2.7 $(VENV)

.PHONY: setup_venv
setup_venv:
	$(PIP) install -r requirements.txt

.PHONY: clean_venv
clean_venv:
	rm -rf $(VENV)

.PHONY: reset_venv
reset_venv: clean_venv create_venv setup_venv


# Database
.PHONY: delete_db
delete_db:
	rm -f $(DB)

.PHONY: syncdb
syncdb:
	$(MANAGE) syncdb --noinput

.PHONY: dump_data
dump_data:
	$(MANAGE) dumpdata auth > thrive_refugee/fixtures/auth.json
	$(MANAGE) dumpdata esl_manager.ESLStudent > esl_manager/fixtures/eslstudent.json
	$(MANAGE) dumpdata esl_manager.Attended > esl_manager/fixtures/attended.json
	$(MANAGE) dumpdata esl_manager.Assesment > esl_manager/fixtures/assesment.json
	$(MANAGE) dumpdata refugee_manager.Volunteer > refugee_manager/fixtures/volunteer.json
	$(MANAGE) dumpdata refugee_manager.Case > refugee_manager/fixtures/case.json
	$(MANAGE) dumpdata refugee_manager.Individual > refugee_manager/fixtures/individual.json
	$(MANAGE) dumpdata refugee_manager.CaseDetail > refugee_manager/fixtures/casedetail.json
	$(MANAGE) dumpdata refugee_manager.ActivityNote > refugee_manager/fixtures/activitynote.json
	$(MANAGE) dumpdata refugee_manager.Event > refugee_manager/fixtures/event.json
	$(MANAGE) dumpdata refugee_manager.Assessment > refugee_manager/fixtures/assessment.json

.PHONY: load_data
load_data:
	$(MANAGE) loaddata thrive_refugee/fixtures/auth.json
	$(MANAGE) loaddata esl_manager/fixtures/eslstudent.json
	$(MANAGE) loaddata esl_manager/fixtures/attended.json
	$(MANAGE) loaddata esl_manager/fixtures/assesment.json
	$(MANAGE) loaddata refugee_manager/fixtures/volunteer.json
	$(MANAGE) loaddata refugee_manager/fixtures/case.json
	$(MANAGE) loaddata refugee_manager/fixtures/individual.json
	$(MANAGE) loaddata refugee_manager/fixtures/casedetail.json
	$(MANAGE) loaddata refugee_manager/fixtures/activitynote.json
	$(MANAGE) loaddata refugee_manager/fixtures/event.json
	$(MANAGE) loaddata refugee_manager/fixtures/assessment.json

.PHONY: reset_db
reset_db: delete_db syncdb load_data


# Other
.PHONY: reset_all
reset_all: reset_db reset_venv


# Run
.PHONY: run
run:
	$(MANAGE) runserver
