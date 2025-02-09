#!/bin/bash

echo "Aguardando MySQL iniciar..."
while ! nc -z db 3306; do
    echo "Esperando o Banco seguro"
    sleep 2
done
echo "Banco seguro pronto para uso"

while ! nc -z db_vulnerable 3306; do
    echo "Esperando o Banco vulnerável"
    sleep 2
done
echo "Banco vulnerável pronto para uso"

python init_db.py
python init_db_vulnerable.py

exec "$@"