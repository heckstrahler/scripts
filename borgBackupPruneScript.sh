#!/bin/bash

indir=$1
#indir="/run/user/1001/gvfs/smb-share:server=192.168.178.111,share=nas/BACKUP/BorgBackup/"

var=$(date)
var=${var//" "/"_"}

echo "Start incremental backup"
borg create --stats -C lz4 $indir::$var ~/.config ~/Sync/
echo "Finished backing up data"
echo "Start pruning existing backups"
borg prune -v --list --keep-hourly=24 --keep-daily=7 --keep-weekly=4 --keep-monthly=12 --keep-yearly=10 $indir
echo "Finised pruning existing backups"
