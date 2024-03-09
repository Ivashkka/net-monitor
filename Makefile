DIST_DIR := /usr/local/bin/net-monitor
CONF_DIR := /etc/net-monitor
SYSD_DIR := /etc/systemd/system
VENV_DIR := $(DIST_DIR)/net-monitor-venv

CONF_FILES := ./conf.yaml
SYSD_FILES := ./net-monitor.service
SIDE_FILES := $(DIST_DIR)/Makefile $(DIST_DIR)/LICENSE $(DIST_DIR)/.gitignore $(DIST_DIR)/README.md $(DIST_DIR)/conf.yaml
REQ_FILE := $(DIST_DIR)/requirements.txt

CLEAN_LAST := $(SYSD_DIR)/net-monitor.service

PYTHON_VERSION := $(shell python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')

all: install

install:
	apt install python$(PYTHON_VERSION)-venv
	mkdir $(DIST_DIR)
	cp -r . $(DIST_DIR)
	rm $(SIDE_FILES)
	mkdir $(CONF_DIR)
	cp $(CONF_FILES) $(CONF_DIR)
	cp $(SYSD_FILES) $(SYSD_DIR)
	python3 -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip3 install -r $(REQ_FILE)
	systemctl daemon-reload

clean:
	systemctl stop net-monitor.service
	rm -r $(DIST_DIR)
	rm -r $(CONF_DIR)
	rm $(CLEAN_LAST)
	systemctl daemon-reload
