#!/bin/bash

source /mnt/.env
# Set environment variables
export PGPASSWORD=$PG_PASSWORD

# Backup directory and file name
BACKUP_DIR=' /mnt/db_backups'
BACKUP_FILE="$BACKUP_DIR/backup_$(date +"%Y%m%d%H%M%S")_$PG_NAME.sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Perform the backup
pg_dump -U $PG_USER -h $PG_HOST -p $PG_PORT $PG_NAME > $BACKUP_FILE

# Unset the password variable for security
unset PGPASSWORD
