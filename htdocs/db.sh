#!/bin/bash

BTICK='`'
EXPECTED_ARGS=3
E_BADARGS=65
MYSQL=`which mysql`

Q0="DROP DATABASE IF EXISTS $1;"
Q1="CREATE DATABASE IF NOT EXISTS $1 DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"
Q2="GRANT ALL ON ${BTICK}$1${BTICK}.* TO '$2'@'localhost' IDENTIFIED BY '$3';"
Q3="FLUSH PRIVILEGES;"
SQL="${Q0}${Q1}${Q2}${Q3}"

if [ $# -ne $EXPECTED_ARGS ]
then
    echo "Usage: $0 dbname dbuser dbpass"
    #exit $E_BADARGS
    return
fi

echo "Executing: $MYSQL -uroot -p -e '$SQL'"
$MYSQL -uroot -p -e "$SQL"

sleep 0.2
python manage.py makemigrations
echo "Finished making migrations"

sleep 0.2
python manage.py migrate
echo "Finished migrating"

sleep 0.5
echo "loading 0_auth_user"
python manage.py loaddata eproweb/fixtures/0_auth_user.json

echo "loading user"
python manage.py loaddata eproweb/fixtures/1_userprofile.json

echo "loading units"
python manage.py loaddata epro/fixtures/units.json

echo "loading status"
python manage.py loaddata epro/fixtures/status.json

echo "loading offices"
python manage.py loaddata epro/fixtures/offices.json

echo "loading currency"
python manage.py loaddata epro/fixtures/currency.json

echo "loading fundcodes"
python manage.py loaddata epro/fixtures/fundcodes.json

echo "loading deptcodes"
python manage.py loaddata epro/fixtures/deptcodes.json
