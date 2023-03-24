from api.api import app
from db import create_tables

# Creates and ingests the data for all the tables
create_tables()

if __name__ == '__main__':
    app.run()
