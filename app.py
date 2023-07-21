import streamlit as st 
import streamlit.components.v1 as components
import sqlite3
from modules.company import Company
from utils.handle_db import insert_company, insert_newsletter, get_companies, get_newsletters_by_company


# email emojy in title
st.set_page_config(page_title="Newletter Search", page_icon="📧" )     
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("Image-of-your-choice");
background-size: 100%;
display: flex;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


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
    option = st.selectbox('Select Company 📱', list(companies_dict.keys()))
    newsletters = get_newsletters_by_company(conn, c, companies_dict[option].email)
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"### {option}")
    # image of company logo
    col2.image(companies_dict[option].logo_url, width=100)
    col3.markdown(f"### {len(newsletters)} Newsletters\n in total")
    for newsletter in newsletters:     
        st.markdown('##')
        readable_date = newsletter.date.split(" ")[0]
        with st.expander(f"{readable_date} - {newsletter.subject}"):
            components.html(newsletter.html, height=500, scrolling=True)
else:
    st.info('Database is Empty.', icon="ℹ️")