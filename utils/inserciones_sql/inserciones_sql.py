#!/usr/bin/python3

import os
import csv
import re

from tkinter.ttk import Progressbar
from tkinter import filedialog as fd
from tkinter import messagebox as msg

file_types = (
	('CSV', '*.csv'),
)


home_dir = os.path.expanduser('~')
current_directory = os.path.curdir
decimal_pattern = r'^[+-]?[\d]+[.]{1}[\d]+$'
timestamp_pattern = r'([\d]{4}-{1}[\d]{2}-{1}[\d]{2}T{1}[\d]{2}:[\d]{2}:[\d]{2}[.+]?([\d]{3}Z|[\d]{2}:[\d]{2}))'


# ruta del archivo csv a tratar
file = fd.askopenfilename(
    title='Seleccione el csv', 
    initialdir=home_dir, 
    filetypes=file_types,
)

file_name = file.split(os.sep)[-1]

# ruta donde se guardara el archivo sql
sql_file = fd.asksaveasfile(
    initialfile=file_name.split('.')[0],
    title='Guardar archivo',
    defaultextension='.sql',
    filetypes=(('SQL files', '*.sql'), ),
)

# Aqui recorro el csv
with open(file) as csv_file:


    csv_reader = csv.DictReader(csv_file)
    headers = csv_reader.fieldnames

    insert = ''

    # concatena los encabezados para incluirlos en la instruccion INSERT
    for i in range(len(headers)):
        if i == len(headers) - 1:
            insert += f'{headers[i]}'
        else:
            insert += f'{headers[i]}, '
    
    # nombre de la tabla en PostgreSQL
    table_name = file_name.title() + 's' if not file_name.endswith('s') else file_name.title()
    sql_file.write(f"INSERT INTO {table_name}({insert})\n")
    sql_file.write("VALUES\n")

    float_check = True
    float_headers = [False for _ in headers]
    # escribe cada uno de los VALUES en una nueva fila
    for row in csv_reader:
        # solo checo en la primera fila que columnas almacenan floats
        if float_check:
            if headers[i] not in ['SECTOR', 'bissioCode']:
                # checar si cumple con el formato de número decimal
                if re.search(decimal_pattern, row[headers[i]]) is not None:
                    float_headers[i] = True
            float_check = False # para que ya no se ejecute en posteriores columnas
        data = ''
        for i in range(len(headers)):
            # si esta vacio pero esa columna es un decimal ponlo a 0
            if row[headers[i]] == '' and float_headers[i]:
                if i == len(headers) - 1:
                        data += '0'
                else:
                    data += '0, '
                continue
            # los que están bajo este header pueden tratarse como string
            if headers[i] not in ['SECTOR', 'bissioCode']:
                # checar si cumple con el formato de número decimal
                if re.search(decimal_pattern, row[headers[i]]) is not None:
                    # ponerlo sin comillas
                    if i == len(headers) - 1:
                        data += f'{row[headers[i]]}'
                    else:
                        data += f'{row[headers[i]]}, '
                    continue

            result = re.search(timestamp_pattern, row[headers[i]])

            if result is not None:
                if i == len(headers) - 1:
                    data += f"TO_TIMESTAMP('{row[headers[i]]}', 'YYYY-MM-DD HH24:MI:SSTZH')"
                else:
                    data += f"TO_TIMESTAMP('{row[headers[i]]}', 'YYYY-MM-DD HH24:MI:SSTZH'), "
                continue

            if i == len(headers) - 1:
                data += f'\'{row[headers[i]]}\''
            else:
                data += f'\'{row[headers[i]]}\', '
        sql_file.write(f'({data}),\n')

sql_file.close()

msg.showinfo(
    title='Exito',
    message='¡Archivo generado exitosamente!'
)
