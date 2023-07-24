from imap_tools import MailBox, AND
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import sqlite3
from modules.newsletter import Newsletter
from utils.handle_db import insert_newsletter


conn = sqlite3.connect("newsletter.db")
c = conn.cursor()

# create newsletter table
c.execute("""CREATE TABLE if not exists newsletters (id integer,
                        sender varchar(100) not null,
                        subject varchar(255) not null,
                        text varchar(255) not null,
                        html varchar(255) not null,
                        date varchar(100) not null
                    );""")

my_env_file='credentials.env'
env_path=os.path.join('', my_env_file)
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    raise FileNotFoundError("File {} not found".format(env_path))

SERVER = os.getenv('EMAIL_SERVER')
USER = os.getenv('EMAIL_USER')
PASSWORD = os.getenv('EMAIL_PASSWORD')

# Server is the address of the IMAP server
mb = MailBox(SERVER).login(USER, PASSWORD)

def email_to_newsletter(email):
    return Newsletter(email.uid, email.from_, email.subject, email.text, email.html, email.date)

def get_emails(date):
    result = []
    # Fetch all email from a specific date
    for msg in mb.fetch(criteria=AND(date=date), bulk=True):
        result.append(msg)

    result = list(map(email_to_newsletter, result))
    return result

def save_files(emails):
    for email in emails:
        with open(f'data/emails/{email.id}.html', 'w') as f:
            f.write(email.html)
        with open(f'data/emails/{email.id}.txt', 'w') as f:
            f.write(email.text)

def write_to_database(emails):
    for email in emails:
        insert_newsletter(conn, c, email)

def edit_html(emails):
    # edit the html my replacing the email: neues.brief@outlook.com with example@email.com
    for email in emails:
        email.html = email.html.replace(USER, "example@email.com")
        # delete all hrefs links
        email.html = email.html.replace("href", "href_")
    return emails

def main():
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    # convert datetime to date
    yesterday = yesterday.date()
    new_emails = get_emails(yesterday)
    # save_files(new_emails)
    new_email = edit_html(new_emails)
    write_to_database(new_emails)
    print(f"{len(new_emails)} new emails saved to database")


if __name__ == "__main__":
    main()