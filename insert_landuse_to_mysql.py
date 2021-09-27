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

# Creation of table 'landuse' in the database
"""
CREATE TABLE landuse(   id VARCHAR(256)  PRIMARY KEY,
                       parcel_number VARCHAR(128),
                       building_sqft DOUBLE,
                       year_built INT,
                       landuse VARCHAR(300) );
"""



# SQL statement to insert values into 'landuse'
sql = "INSERT INTO landuse (id, parcel_number, building_sqft, year_built, landuse) VALUES (%s, %s, %s, %s, %s)"

# Formating data fetched from open data source API
def format_land_data(record):
    d = {}
    d['id'] = record.get(':id')
    d['updated_at'] = record.get(':updated_at')
    d['created_at'] = record.get(':created_at')
    d['doc_type'] = 'LANDUSE'
    d['building_sqft'] = float(record.get('bldgsqft'))
    d['parcel_number'] = record.get('blklot')
    d['year_built'] = int(record.get('yrbuilt'))
    d['landuse'] = record.get('landuse')


    return {"doc": d}

total_results = 155468
num_records = 2000
wait_time = 5
parcel_offset=0

#Creating a loop to fetch and insert 2000 records in one iteration
for i in range(parcel_offset,total_results,num_records):
    results = client.get("acdm-wktn",exclude_system_fields=False, limit=num_records, offset=i)
    payload = []
    for rec in results:
        payload.append(format_parcel_data(rec))

    for doc in results:
        val = (str(uuid.uuid4()), doc['parcel_number'], float(doc.get('building_sqft', 0)), int(doc.get('year_built', 0)), doc.get('landuse', '-'))
        mycursor.execute(sql, val)
    mydb.commit()

    print ('Sleeping for %i seconds' % wait_time)
    time.sleep(wait_time)
