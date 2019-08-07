========================
HBP Validation Framework
========================

This repository contains code related to the Human Brain Project Validation Framework,
part of the Brain Simulation Platform.

All code is copyright 2016-2017 CNRS unless otherwise indicated.


USE:

source activate dev
cd ~/work/hbp-validation-framework/
cd validation_service
sh env_local.sh
python manage.py check
# python manage.py kg_migration
