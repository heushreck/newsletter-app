from imap_tools import MailBox, AND
from dotenv import load_dotenv
import os

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

# Fetch all unseen emails containing "xyz.com" in the from field
# Don't mark them as seen
# Set bulk=True to read them all into memory in one fetch
# (as opposed to in streaming which is slower but uses less memory)
messages = mb.fetch(criteria=AND(seen=False, from_="deutschlandcard.de"),
                        mark_seen=False,
                        bulk=True)

files = []
for msg in messages:
    # Print form and subject
    print(msg.from_, ': ', msg.subject)
    # Print the plain text (if there is one)
    print(msg.text)
    # Add attachments
    # files += [att.payload for att in msg.attachments if att.filename.endswith('.pdf')]
    html = msg.html
    # save html to file
    with open("email.html", "w") as file:
        file.write(html)
        print("html saved to file")
