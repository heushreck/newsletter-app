import sqlite3
from modules.company import Company
from utils.handle_db import get_companies, insert_company
def main(table: str):
    conn = sqlite3.connect("newsletter.db")
    c = conn.cursor()
    # create company table
    c.execute(f"DROP TABLE {table};")



# main takes command line arguemnt of table
if __name__ == "__main__":
    import sys
    main(sys.argv[1])
