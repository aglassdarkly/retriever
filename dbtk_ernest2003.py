# Database Toolkit for Ernest 2003 Ecological Archives
# Mammalian Life History Database

# Usage: python /file/path/to/dbtk_ernest2003.py

# TO DO: Replace -999 with Null
# TO DO: Eventually pull get_database_info into a separate module

import urllib
import MySQLdb as dbapi
import sys
sys.path.append("/home/ethan/Dropbox/Ecoinformatics/Database Toolkits/Code")
import dbtk_tools

# Create the Database
databaseinfo = dbtk_tools.get_database_info()
connection = dbapi.connect(host = databaseinfo[2],
                           port = databaseinfo[3],
                           user = databaseinfo[0],
                           passwd = databaseinfo[1])
cursor = connection.cursor()
cursor.execute("DROP DATABASE IF EXISTS MammalLifeHistory")
cursor.execute("CREATE DATABASE MammalLifeHistory")
cursor.execute("USE MammalLifeHistory")
cursor.execute("""
    CREATE TABLE species(
          species_id INT(5) NOT NULL AUTO_INCREMENT,
          sporder CHAR(20),
          family CHAR(20),
          genus CHAR(20),
          species CHAR(20),
          mass DECIMAL(11,2),
          gestation_period DECIMAL(5,2),
          newborn_mass DECIMAL(9,2),
          wean_age DECIMAL(5,2),
          wean_mass DECIMAL(10,2),
          afr DECIMAL(5,2),
          max_lifespan DECIMAL(6,2),
          litter_size DECIMAL(5,2),
          litters_peryear DECIMAL(5,2),
          refs CHAR(30),
          PRIMARY KEY (species_id));
    """)

url = "http://www.esapubs.org/archive/ecol/E084/093/Mammal_lifehistories_v2.txt"
main_table = urllib.urlopen(url)

# Skip over the header line by reading it before processing
line = main_table.readline()

species_id = 0
for line in main_table:
    line = line.strip()
    if line:
        (sporder, family, genus, species, mass, gestation_period,
         newborn_mass, wean_age, wean_mass, afr, max_lifespan, litter_size,
         litters_peryear, refs) = line.split()
        species_id += 1
        cursor.execute("""
            INSERT INTO species VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s)
            """,(species_id, sporder, family, genus, species, float(mass),
                 float(gestation_period), float(newborn_mass), float(wean_age),
                 float(wean_mass), float(afr), float(max_lifespan),
                 float(litter_size), float(litters_peryear), refs))
main_table.close()