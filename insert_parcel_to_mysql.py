import mysql.connector
import uuid
import requests
import pandas as pd
from sodapy import Socrata
import json
import time

# Data API
client = Socrata("data.sfgov.org",
                 "API TOKEN",
                 username="USERNAME",
                 password="PASSWORD")

# MySQL Database instance
mydb = mysql.connector.connect(
  host="localhost",
  user="USER",
  password="PASSWORD",
  database="browse_parcels"
)

mycursor = mydb.cursor()

# Creation of table 'parcel' in the database
"""
CREATE TABLE parcel(   id VARCHAR(256)  PRIMARY KEY,
                       parcel_number VARCHAR(128),
                       address VARCHAR(500),
                       zoning VARCHAR(300) );
"""

# SQL statement to insert values into 'parcel'
sql = "INSERT INTO parcel (id, parcel_number, address, zoning) VALUES (%s, %s, %s, %s)"

# Formating data fetched from open data source API
def format_parcel_data(record):
    d = {}
    d['id'] = record.get(':id')
    d['updated_at'] = record.get(':updated_at')
    d['created_at'] = record.get(':created_at')
    d['doc_type'] = 'PARCEL'
    d['address'] = record.get('to_address_num', 'Unknown') \
                    +" "+record.get('street_name', 'Unknown')+" "+\
                    record.get('street_type', 'Unknown')
    d['parcel_number'] = record.get('blklot')
    d['zoning'] = record.get('zoning_code', None)

    return {"doc": d}

total_results = 233722
num_records = 2000
wait_time = 5
parcel_offset=0

#Creating a loop to fetch and insert 2000 records in one iteration
for i in range(parcel_offset,total_results,num_records):
    results = client.get("acdm-wktn",exclude_system_fields=False, limit=num_records, offset=i)
    payload = []
    for rec in results:
        payload.append(format_parcel_data(rec))

    for doc in payload:
        val = (str(uuid.uuid4()), doc['parcel_number'], doc.get('address', '-'), doc.get('zoning', '-'))
        mycursor.execute(sql, val)
    mydb.commit()

    print ('Sleeping for %i seconds' % wait_time)
    time.sleep(wait_time)
