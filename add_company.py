import sqlite3
from modules.company import Company
from utils.handle_db import get_companies, insert_company
import pandas as pd


def main():
    conn = sqlite3.connect("newsletter.db")
    c = conn.cursor()

    # create company table
    c.execute("""CREATE TABLE if not exists companies (id integer,
                            name varchar(50) not null,
                            url varchar(255) not null,
                            email varchar(100) not null,
                            logo_url varchar(255) not null,
                            bio varchar(255) not null
                        );""")
    

    # read all companies from from db
    existing_companies = get_companies(conn, c)
    
    df = pd.read_csv("companies.csv", sep=";")
    for index, row in df.iterrows():
        email = row["email"]
        if any(company.email == email for company in existing_companies):
            print(f"Company {index} already exists")
            continue
        company = Company(hash(row["email"]), row["name"], row["url"], row["email"], row["logo_url"], row["bio"])
        insert_company(conn, c, company)
        print(f"Company {index} inserted successfully")

if __name__ == "__main__":
    main()