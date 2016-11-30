#!/bin/bash

timestamp=$(date +%s)

abs_dir=/home/daw2035/microbe_db/submissions_automation
backup_dir=$abs_dir/backups/$timestamp/
mkdir $backup_dir

rsync $abs_dir/submitters.xlsx $backup_dir
rsync $abs_dir/annotations_master.xlsx $backup_dir
