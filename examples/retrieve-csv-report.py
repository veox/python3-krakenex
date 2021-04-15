#!/usr/bin/env python3
#
# Responses can be binary ZIP streams instead of the expected JSON,
# based on query parameters. A prime example is 'RetrieveReport':
#
# https://www.kraken.com/features/api#get-history-export
#
# This script shows how to "unpack" such a response. 
#
# Run unbuffered to see output as in happens:
# python -u export-csv-export.py

###################################
##       Library imports         ##
###################################

from json import JSONDecodeError
from pprint import pprint
from time import sleep

import krakenex

###################################
##          Key setup            ##
###################################

kraken = krakenex.API()
# NOTE: key must have the "Export data" permission.
kraken.load_key('/path/to/export-data.key')
  
###################################
##           Report              ##
###################################

# Request report.
response = kraken.query_private(
    'AddExport',
    {
        'description': 'reporting',
        'report': 'ledgers',
        'format': 'CSV',
    },
)
report_id = response['result']['id']

# "Wait" for the report to be created.
print('Waiting for export to be ready...', end='')
while True:
    sleep(10)
    response = kraken.query_private('ExportStatus', {'report': 'ledgers'})
    if len(response['error']) > 0 and response['error'][0] == 'EExport:Not ready':
        print('.', end='')
    else:
        print('')
        break

# Expecting streamed binary response when query successful.
try:
    response = kraken.query_private('RetrieveExport', {'id': report_id})
except JSONDecodeError:
    export_bytes = kraken.response.content
    with open('ledgers.csv.zip', 'wb') as fd:
        fd.write(export_bytes)
    print('Done! Written as: ledgers.csv.zip')
else:
    pprint(response)
