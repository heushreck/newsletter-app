import sqlite3

from modules.company import Company
from utils.handle_db import insert_company


def main():
    conn = sqlite3.connect("newsletter.db")
    c = conn.cursor()

    # create company table
    c.execute("""CREATE TABLE if not exists companies (id integer,
                            name varchar(50) not null,
                            url varchar(255) not null,
                            email varchar(100) not null,
                            logo_url varchar(255) not null
                        );""")
    

    name = "Deutschlandcard"
    url = "https://www.deutschlandcard.de"
    email = "info@reply.deutschlandcard.de"
    logo_url = "https://upload.wikimedia.org/wikipedia/de/thumb/6/6d/DeutschlandCard_logo.svg/2560px-DeutschlandCard_logo.svg.png"
    id = hash(email)
    
    company = Company(id, name, url, email, logo_url)
    insert_company(conn, c, company)
    print("Company inserted successfully")

if __name__ == "__main__":
    main()