import os 
import streamlit as st 
from dotenv import load_dotenv
import requests
import json
from bs4 import BeautifulSoup
from openai import OpenAI

#---------------------------------------------------
#for steamlit deployment only 
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"] #Comment both key when runing on vs code 
#---------------------------------------------------

#load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
MODEL="gpt-4o-mini"
openai=OpenAI()

## Round 1 Process of calling LLM:

# Headers for requests
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/117.0.0.0 Safari/537.36"}


#class for website web scraping
class Website:
    def __init__(self,url):
        self.url=url
        response=requests.get(url, headers=headers)
        self.body=response.content
        soup=BeautifulSoup(self.body,"html.parser")
        self.title=soup.title.string if soup.title else "No Title Found"

        #clean the text extraction
        if soup.body:
            for irrelevant in soup.body(["script","style","img","input"]):
                irrelevant.decompose()
            self.text=soup.body.get_text(separator="\n",strip=True)
        else:
            self.text=""

        #Extract links
        self.links=[link.get("href") for link in soup.find_all("a") if link.get("href")]

    def get_contents(self):
        # Return formatted webpage title and content
        return f"Webpage Title:\n{self.title}\nWebpage Content:\n{self.text}\n\n"
    
#LLM Prompt [one shot prompting]
link_system_prompt="""
You are a funny assistant analyzing a company website. Your mission: find the juiciest, most brochure-worthy links!
Forget boring legal stuff – we're looking for About Us, Careers, or anything that screams 'we're awesome!'
Respond in JSON:
{
    "links": [
        {"type": "about page", "url": "https://company.com/about"},
        {"type": "careers page", "url": "https://company.com/careers"}
    ]
}
"""

def get_links(url):
    website=Website(url)

    #instantiate the model
    response=openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system","content":link_system_prompt},
            {"role":"user","content":f"Here are some links from {url}:\n" + "\n".join(website.links)},
        ],
        response_format={"type":"json_object"}
    )
    return json.loads(response.choices[0].message.content)

## Round 2 Process of calling LLM:

# Funny Brochure Prompt
system_prompt = """
You are the world’s funniest marketing assistant! Your job is to turn boring corporate jargon into a hilarious, entertaining, and slightly ridiculous company brochure.
Mention company culture, customers, jobs, and anything weirdly fun about them. Respond in markdown format!
"""

#pulling combined data of links and contents
def get_all_details(url):
    result = "Landing Page:\n"  # Start with a label for the main page content
    result += Website(url).get_contents()  # Get and append the main page content 

    #call the function above that call LLM
    links=get_links(url)
    return result, links

def get_brochure_user_prompt(company_name,url):
    user_prompt= f"You are looking at a company called {company_name}\n"
    user_prompt+= f"Here are the contents of its landing page and other relevant pages; Use this information to build a short brochure of the company in markdown.\n"
    
    #call the function "get_all_details" for all info extraction
    all_details, _ = get_all_details(url)
    user_prompt += all_details

    #put at threshold on number of chracters
    user_prompt=user_prompt[:5000]

    return user_prompt

def create_brochure(company_name,url):

    response=openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":get_brochure_user_prompt(company_name,url)}
        ],
    )
    return response.choices[0].message.content

###---------------### STREAMLIT APP DESIGN ###---------------###

st.set_page_config(page_title="MakeMyBrochure")

## Display the image and title
col1, col2 = st.columns([1, 8])
with col1:
    st.image("openai.webp", width=100)  # Adjust the width as needed
with col2:
    st.title("OpenAI-MyFunBrochurePal")    

# Get User Input
url = st.text_input("Enter Company Website URL:")

if url:
    with st.spinner("Mission Extraction..."):
        all_details,links=get_all_details(url)

    if links["links"]:
        st.subheader("🔗 Your Shortlisted Useful Website Webpages")
        for link in links["links"]:
            st.markdown(f"-**{link['type'].title()}**: [Visit]({link['url']})")
    else:
        st.warning("⚠️ No relevant links found. Please try another website.")

    if st.button("I approve these Webpages"):
        with st.spinner("📝 AI is crafting your masterpiece..."):
            brochure=create_brochure("A Cool Company", url)
            st.markdown(brochure)

            st.download_button(
                label="Download Brochure",
                data=brochure,
                file_name="funny_{company_name}_brochure.md",
                mime="text/markdown"
            )
