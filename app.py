from flask import Flask, render_template, request
import mysql.connector
from flask_paginate import Pagination, get_page_parameter

app = Flask(__name__)

dbconfig = {'host': '127.0.0.1', 'user': 'USER', 
                        'password': 'PASSWORD', 'database': 'browse_parcels', }
         
conn = mysql.connector.connect(**dbconfig)

@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 50
    offset=page*limit-limit
    cur = conn.cursor(dictionary=True, buffered=True)
    # Zoning Values to choose from 
    cur.execute("SELECT DISTINCT zoning FROM  parcels_data")
    zoning = cur.fetchall() 
    # Landuse Values to choose from
    cur.execute("SELECT DISTINCT landuse FROM  parcels_data")
    landuse = cur.fetchall() 
    # Initial retrieval to show on entry
    cur.execute("SELECT * FROM parcels_data ORDER BY id ASC LIMIT %s OFFSET %s",(limit, offset))
    parcels = cur.fetchall() 
    total = 149105
    
    if request.method == "POST":
        
        #Handling queries from the client side.
        query1, query2 = request.form['zoning_select'], request.form['landuse_select']
        
        if query1 == '' and query2 == '':
            cur.execute("SELECT * FROM parcels_data ORDER BY id ASC LIMIT %s OFFSET %s",(limit, offset))
            parcels = cur.fetchall()

        elif query1 and not query2:
            search_text = request.form['zoning_select']
            
            cur.execute("SELECT * FROM parcels_data WHERE zoning IN (%s) ORDER BY id ASC LIMIT %s OFFSET %s", (search_text,limit, offset))
            parcels = cur.fetchall()  
        
        elif query2 and not query1:
            search_text = request.form['landuse_select']
            
            cur.execute("SELECT * FROM parcels_data WHERE landuse IN (%s) ORDER BY id ASC LIMIT %s OFFSET %s", (search_text,limit, offset))
            parcels = cur.fetchall()  
        
        else:
            search_text1 = request.form['zoning_select']
            search_text2 = request.form['landuse_select']
            
            cur.execute("SELECT * FROM parcels_data WHERE zoning IN (%s) and landuse IN (%s) ORDER BY id ASC LIMIT %s OFFSET %s", (search_text1, search_text2, limit, offset))
            parcels = cur.fetchall()  
         
    pagination = Pagination(page=page, per_page=limit, total=total, search=False, css_framework='bootstrap3')
    
    return render_template('base.html', parcels=parcels, zoning=zoning, landuse=landuse, pagination=pagination)
 
if __name__ == "__main__":
    app.run(debug=True)