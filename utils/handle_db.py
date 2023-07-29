import datetime
import sqlite3
from modules.company import Company
from modules.newsletter import Newsletter


def insert_company(conn, c, company: Company):
    with conn:
        c.execute("insert into companies values (:id, :name, :url, :email, :logo_url, :bio)", 
                  {'id': company.id, 'name': company.name, 'url': company.url, 'email': company.email, 'logo_url': company.logo_url, 'bio': company.bio})
        
def insert_newsletter(conn, c, newsletter: Newsletter):
    with conn:
        c.execute("insert into newsletters values (:id, :sender, :subject, :text, :html, :date)",
                    {'id': newsletter.id, 'sender': newsletter.sender, 'subject': newsletter.subject, 'text': newsletter.text, 'html': newsletter.html, 'date': newsletter.date})
        
def get_companies(conn, c):
    with conn:
        c.execute("select * from companies")
        result = c.fetchall()
        # map to Company object
        return list(map(lambda x: Company(x[0], x[1], x[2], x[3], x[4], x[5]), result))
    
def get_newsletters_by_company(conn, c, company_email):
    with conn:
        c.execute("select * from newsletters where sender = :sender", {'sender': company_email})
        result = c.fetchall()
        # map to Newsletter object
        return list(map(lambda x: Newsletter(x[0], x[1], x[2], x[3], x[4], datetime.datetime.fromisoformat(x[5])), result))
    
def get_newsletters_for_stats(conn, c):
    with conn:
        c.execute("select * from newsletters")
        result = c.fetchall()
        # map to Newsletter object
        return list(map(lambda x: Newsletter(x[0], x[1], x[2], x[3], x[4], datetime.datetime.fromisoformat(x[5])), result))
