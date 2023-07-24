import datetime
import streamlit as st 
import streamlit.components.v1 as components
import sqlite3
from modules.company import Company
from utils.handle_db import insert_company, insert_newsletter, get_companies, get_newsletters_by_company
from PIL import Image


# email emojy in title
st.set_page_config(page_title="Newletter Search", page_icon="📬", layout="centered")     
# page_bg_img = f"""
# <style>
# [data-testid="stAppViewContainer"] > .main {{
# background-image: rgb(231, 222, 205);
# background-size: 100%;
# display: flex;
# background-position: top left;
# background-repeat: no-repeat;
# background-attachment: local;

# }}
# [data-testid="stHeader"] {{
# background: rgb(231, 222, 205);
# }}
# [data-testid="stToolbar"] {{
# right: 2rem;
# }}
# </style>
# """
# st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)


conn = sqlite3.connect("newsletter.db")
c = conn.cursor()

def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )

icon("📬")
st.title("Search Newsletters")

c.execute("select count(*) from companies")
db_size = c.fetchone()[0] 

companies = get_companies(conn, c)
companies_dict = {}
for company in companies:
    companies_dict[company.name] = company

description_text = "Spark your newsletter design journey with a wealth of inspiration from leading company newsletters. Uncover innovative ideas and trends that will help you craft captivating and irresistible newsletters of your own."
description = st.empty()
description.write(description_text.format("all"))

st.markdown("#####")  
if db_size>0:
    col1, col2 = st.columns([3,1])          
    option = col1.selectbox(label='Explore newsletters by selecting a company', options=list(companies_dict.keys()))
    if option:
        # try to open the logo from local storage under logos/*company_name*
        # if it doesn't exist, show from the url
        try:
            image = Image.open(f"logos/{option.lower()}.png")
            col2.image(image, width=200)
            print(f"Logo found for {option}")
        except FileNotFoundError:
            print(f"Logo not found for {option}")
            col2.image(companies_dict[option].logo_url, width=200)
        except Exception as e:
            print(f"Error: {e}")
            col2.image(companies_dict[option].logo_url, width=200)
        newsletters = get_newsletters_by_company(conn, c, companies_dict[option].email)
        min_date = min([newsletter.date for newsletter in newsletters])
        days_ago = (datetime.datetime.now().astimezone() - min_date).days
        avg_days = days_ago // len(newsletters)
        # in col two show how many newsletters in total and how many days on average between newsletters
        st.markdown(f"{companies_dict[option].bio} On average, they send out a newsletter every **{avg_days}** days.")
        # sort newsletters by date
        newsletters = sorted(newsletters, key=lambda x: x.date, reverse=True)
        current_month = None
        for newsletter in newsletters:    
            st.markdown('##')
            # show month if different from previous newsletter
            if current_month != newsletter.date.month:
                current_month = newsletter.date.month
                st.markdown(f"#### {newsletter.date.strftime('%B - %Y')}")
            readable_date = str(newsletter.date.strftime('%A, %d %B %Y'))
            with st.expander(f"{readable_date} - **{newsletter.subject}**"):
                components.html(newsletter.html, height=600, scrolling=True)
else:
    st.info('Database is Empty.', icon="ℹ️")