import streamlit as st
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI
from exa_py import Exa

load_dotenv(dotenv_path=".env", override=True)

EXA_API_KEY = os.getenv("EXA_API_KEY").strip()
SERPER_API_KEY = os.getenv("SERPER_API_KEY").strip()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY").strip()


XA_API_KEY = "your_api_key_here" 

def fetch_company_data(company_name):
    if not EXA_API_KEY:
        return {"error": "Missing API key for Exa.ai"}

    exa = Exa(EXA_API_KEY)
    query = f"{company_name} company financials procurement"

    try:
        response = exa.search_and_contents(query, text=True)

       
        formatted_results = {
            "query": query,
            "search_type": getattr(response, "resolved_search_type", "N/A"),
            "cost": getattr(response, "cost_dollars", {}).total if hasattr(response, "cost_dollars") else "N/A",
            "results": []
        }

       
        if hasattr(response, "results") and response.results:
            for result in response.results:
                formatted_results["results"].append({
                    "title": getattr(result, "title", "No Title"),
                    "url": getattr(result, "url", "No URL"),
                    "summary": getattr(result, "text", "No Description")
                })

        return formatted_results  

    except Exception as e:
        return {"error": f"Failed to fetch company details: {str(e)}"}


def fetch_social_media(contact_name):
    

    client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
    messages = [
        {
            "role": "system",
            "content": (
                "You are a research assistant. Fetch the latest LinkedIn and Twitter insights "
                "about the given person, focusing on industry news and professional activities."
            ),
        },
        {
            "role": "user",
            "content": f"Find recent LinkedIn and Twitter updates for {contact_name}.",
        },
    ]

    try:
        response = client.chat.completions.create(
            model="sonar-small",  
            messages=messages,
        )
        
        return response  

    except Exception as e:
        return {"error": str(e)}

def fetch_google_search(company_name):
    

    if not SERPER_API_KEY:
        return {"error": "Missing API key for Serper API"}

    url = "https://google.serper.dev/search"  
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "q": f"{company_name} procurement steel vendors market position"
    }

    try:
        response = requests.post(url, headers=headers, json=data) 
        response.raise_for_status() 

        return response.json()  

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch Google search data: {str(e)}"}





#Streamlit application
st.title(" JSW Company Dashboard")
company_name = st.text_input("Enter Company Name")
project_name = st.text_input("Enter Project Name (Optional)")
contact_name = st.text_input("Enter Key Contact Name & Role")

if st.button("Fetch Intelligence"):
    with st.spinner("Fetching data..."):
        company_data = fetch_company_data(company_name)
        social_data = fetch_social_media(contact_name)
        search_data = fetch_google_search(company_name)
    
    st.subheader(" Company Overview")
    st.write(company_data)

    st.subheader(" Social Media Insights (Perplexity AI)")
    st.write(social_data)

    st.subheader("Google Search Results")
    st.write(search_data)