# parcel_browse

A Python based web application used to load pacel data and land use data fetched from the open data source [DataSF](https://datasf.org/opendata/) 
## Getting Started

Required: [Python 3.8](https://www.python.org/downloads/) and [MySQL](https://dev.mysql.com/downloads/mysql/) installed to run this application.  
Clone the repo and follow these steps to run the application.   

### Setting up the database

Use [this link](https://dev.mysql.com/downloads/mysql/) to install MySQL Server.<br/>After installation, launch MySQL using the follwoing command
```
$ mysql -u root -p;
```
Create a user for this application.
```
mysql> CREATE USER '<your-user-name>'@'localhost' IDENTIFIED BY '<your-password>';
```

Grant the user the privileges to access the database.

```
mysql> GRANT ALL PRIVILEGES ON *.* TO '<your-user-name>'@'localhost' WITH GRANT OPTION;

mysql> FLUSH PRIVILEGES;
```
Create a new database 'browse_parcels' using the following command

```
mysql> CREATE DATABASE browse_parcels;
```
To start using the database, use the following command.

```
mysql> USE browse_parcels;
```
Create two tables 'parcel' and 'landuse' using the following statements

```

mysql> CREATE TABLE parcel(   id VARCHAR(256)  PRIMARY KEY,
                       parcel_number VARCHAR(128),
                       address VARCHAR(500),
                       zoning VARCHAR(300) );

mysql> CREATE TABLE landuse(   id VARCHAR(256)  PRIMARY KEY,
                       parcel_number VARCHAR(128),
                       building_sqft DOUBLE,
                       year_built INT,
                       landuse VARCHAR(300) );
```
Create a new table 'parcels_data' based on the 'parcel' and 'landuse' tables using the following statementS.
```
mysql> CREATE TABLE parcels_data(   id INT AUTO_INCREMENT PRIMARY KEY,
                       parcel_number VARCHAR(128),
                       address VARCHAR(500),
                       zoning VARCHAR(300),
                       building_sqft DOUBLE,
                       year_built INT,
                       landuse VARCHAR(300 );

mysql> INSERT INTO 
parcels_data (id,parcel_number, address, zoning,building_sqft, year_built,landuse)
SELECT p.parcel_number, p.address, p.zoning, l.building_sqft, l.year_built, l.landuse
FROM parcel p, landuse l
WHERE p.parcel_number = l.parcel_number;
```
### Fetching the data from the data source
Get an API token from [DataSF](https://datasf.org/opendata/).
Install [Sodapy](https://github.com/xmunoz/sodapy) to fetch the data records via API.
Run the 'fetch_and_insert' python files, after editing the files with your:
```
API TOKEN, <username>, <password>
```

### Installing Required Python Modules
Create a virtual environment using virtualenv 
```
$ virtualenv <name-of-your-virtual-environment>
```
Activate the virtual environment using 
```
$ source <name-of-your-virtual-environment>/bin/activate
```
To deactivate, run
```
$ deactivate
```
Here run the following command in your virtual environment and in your working directory to install all the dependencies.
```
(name-of-your-virtual-environment) your/working/directory$ pip install -r requirements.txt
```
Before running the application edit the username and the password for your MySQL database in the app.py file.

## Running the application
Run the application from parcel_browse folder using
```
(name-of-your-virtual-environment)$ flask run
```
## Output [Log]


## Built With

* [Flask](https://pypi.org/project/Flask/) - The web application framework
* [MySQL](https://www.mysql.com/) - Database

## References

* [Head First Python](https://www.oreilly.com/library/view/head-first-python/9781491919521/)
* [DataTables](https://datatables.net/)
* [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)
* [MySQL Documentation](https://dev.mysql.com/doc/)

## Caution
The requirements.txt file does not contain the libraries used in insert_*_to_mysql.py files.