import datetime
import streamlit as st 
import streamlit.components.v1 as components
import sqlite3
from modules.company import Company
from utils.handle_db import insert_company, insert_newsletter, get_companies, get_newsletters_by_company


# email emojy in title
st.set_page_config(page_title="Newletter Search", page_icon="📧" )     
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


conn = sqlite3.connect("newsletter.db")
c = conn.cursor()

st.title("Search Newsletters")

c.execute("select count(*) from companies")
db_size = c.fetchone()[0] 

companies = get_companies(conn, c)
print(companies)

# make a dict out of companies with name as key and email as value
companies_dict = {}
for company in companies:
    companies_dict[company.name] = company


st.markdown("#####")  
if db_size>0:                   
    option = st.selectbox(label='Select Company', options=list(companies_dict.keys()))
    if option:
        newsletters = get_newsletters_by_company(conn, c, companies_dict[option].email)
        col1, col2 = st.columns([2,1])
        col1.image(companies_dict[option].logo_url, width=400)
        print(newsletters[0].date)
        min_date = min([datetime.datetime.fromisoformat(newsletter.date) for newsletter in newsletters])
        days_ago = (datetime.datetime.now().astimezone() - min_date).days
        avg_days = days_ago // len(newsletters)
        # in col two show how many newsletters in total and how many days on average between newsletters
        col2.markdown(f"**{len(newsletters)}** newsletters sent in the last **{days_ago}** days. On average **{avg_days}** days between newsletters.")
        for newsletter in newsletters:     
            st.markdown('##')
            readable_date = newsletter.date.split(" ")[0]
            with st.expander(f"{readable_date} - {newsletter.subject}"):
                components.html(newsletter.html, height=500, scrolling=True)
else:
    st.info('Database is Empty.', icon="ℹ️")