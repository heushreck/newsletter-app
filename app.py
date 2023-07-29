import datetime
import pandas as pd
import streamlit as st 
import streamlit.components.v1 as components
import sqlite3
from modules.company import Company
from utils.handle_db import get_newsletters_for_stats, insert_company, insert_newsletter, get_companies, get_newsletters_by_company
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns

rcParams['font.family'] = 'sans-serif'
# email emojy in title
st.set_page_config(page_title="Search Newsletters", page_icon="📬", layout="centered")     
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

# access database and get all companies
c.execute("select count(*) from companies")
db_size = c.fetchone()[0] 

companies = get_companies(conn, c)
companies = sorted(companies, key=lambda x: x.name, reverse=False)
companies_dict = {}
for company in companies:
    companies_dict[company.name] = company


# create tabs for search and stats
search_tab, stats_tab = st.tabs(["🔬 Search ", "📋 Stats"])


### TAB 1 - SEARCH NEWSLETTERS ###

search_tab.title("Search Newsletters")
description_text = "Spark your newsletter design journey with a wealth of inspiration from leading company newsletters. Uncover innovative ideas and trends that will help you craft captivating and irresistible newsletters of your own."
description = search_tab.empty()
description.write(description_text.format("all"))
search_tab.markdown("#####")  
if db_size>0:
    col1, col2 = search_tab.columns([3,1])          
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
        if len(newsletters) == 0:
            st.info(f"No newsletters found for {option}", icon="ℹ️")
            st.stop()
        min_date = min([newsletter.date for newsletter in newsletters])
        days_ago = (datetime.datetime.now().astimezone() - min_date).days
        avg_days = days_ago // len(newsletters)
        search_tab.markdown(f"{companies_dict[option].bio} On average, they send out a newsletter every **{avg_days}** days.")
        search_tab.markdown(f"Email: {companies_dict[option].email} - Website: {companies_dict[option].url}")
        
        # sort newsletters by date
        newsletters = sorted(newsletters, key=lambda x: x.date, reverse=True)
        current_month = None
        for newsletter in newsletters:    
            search_tab.markdown('##')
            # show month if different from previous newsletter
            if current_month != newsletter.date.month:
                current_month = newsletter.date.month
                search_tab.markdown(f"#### {newsletter.date.strftime('%B - %Y')}")
            readable_date = str(newsletter.date.strftime('%A, %d %B %Y'))
            with search_tab.expander(f"{readable_date} - **{newsletter.subject}**"):
                components.html(newsletter.html, height=600, scrolling=True)
else:
    st.info('Database is Empty.', icon="ℹ️")


### TAB 2 - STATS ###

stats_tab.title("Some Statistics")
description_text = "This website monitors the newsletters of several companies, here are some fun statistics we found interesting."
description = stats_tab.empty()
description.write(description_text.format("all"))
stats_tab.markdown("#####")
if db_size>0:
    # get all newsletters
    newsletters = get_newsletters_for_stats(conn, c)
    col1, col2, col3 = stats_tab.columns([1,1,1], gap="large")
    # in column 1 show how many companies we monitor, with a big number and a small text
    col1.markdown(f"### {db_size}")
    col1.markdown("Companies monitored")
    # in column 2 show how many newsletters we have in total, with a big number and a small text
    col2.markdown(f"### {len(newsletters)}")
    col2.markdown("Newsletters in total")
    # in column 3 show how many newsletters we get per day, with a big number and a small text
    days_ago = (datetime.datetime.now().astimezone() - min([newsletter.date for newsletter in newsletters])).days
    avg_newsletters = len(newsletters) // days_ago
    col3.markdown(f"### {avg_newsletters}")
    col3.markdown("Newsletters per day")

    # Graph with newsletters per company
    stats_tab.markdown("### Newsletters per company")
    companies_dict = {company.email: {"count": 0,"name": company.name} for k,company in companies_dict.items()}
    for newsletter in newsletters:
        try:
            companies_dict[newsletter.sender]["count"] += 1
        except KeyError:
            print(f"KeyError: No company in DB with email: {newsletter.sender}")
    df = pd.DataFrame.from_dict(companies_dict, orient='index')
    # only top 10
    df = df.set_index('name')
    df = df.sort_values(by=['count'], ascending=False)
    df = df.head(10)
    # make plotly background #E7DECD
    # make plotly bars #2C1A1D


    fig = plt.figure(figsize=(10, 5), facecolor="#E7DECD", edgecolor="#2C1A1D")
    sns.barplot(x=df.index, y=df['count'], color="#D7C8AC", edgecolor="#2C1A1D", alpha=1)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("")
    plt.ylabel("Newsletter Count")
    stats_tab.pyplot(fig)

    # Graph with how many newsletters on weekdays
    stats_tab.markdown("### Newsletters per weekday")
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekdays_dict = {weekday: 0 for weekday in weekdays}
    for newsletter in newsletters:
        weekdays_dict[weekdays[newsletter.date.weekday()]] += 1
    df = pd.DataFrame.from_dict(weekdays_dict, orient='index')
    df = df.rename(columns={0: "count"})

    fig = plt.figure(figsize=(10, 5), facecolor="#E7DECD", edgecolor="#2C1A1D")
    sns.barplot(x=df.index, y=df['count'], color="#D7C8AC", edgecolor="#2C1A1D", alpha=1)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("")
    plt.ylabel("Newsletter Count")
    stats_tab.pyplot(fig)

    # Wordcloud of subject lines
    stats_tab.markdown("### Wordcloud of subject lines")
    from wordcloud import WordCloud, STOPWORDS
    stopwords = set(STOPWORDS)
    stopwords.update(["bist","du","deine","Willkommen", "bei", "Welcome", "to", "the", "Newsletter", "Newsletter", "Quiksilver", "Burton", "Roxy", "DC", "Vans", "Billabong", "Rip", "Curl", "O'Neill", "Volcom", "Element", "Nixon", "Dakine", "Oakley", "Patagonia", "Volkom"])
    text = " ".join([newsletter.subject for newsletter in newsletters])
    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        return "#2C1A1D"
    wordcloud = WordCloud(stopwords=stopwords, background_color="#E7DECD", width=800, height=400, color_func=color_func).generate(text)
    fig = plt.figure(figsize=(10, 5), facecolor="#E7DECD", edgecolor="#2C1A1D")
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    stats_tab.pyplot(fig)
    
