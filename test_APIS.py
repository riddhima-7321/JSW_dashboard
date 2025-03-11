import requests
import os
from dotenv import load_dotenv


load_dotenv()


EXA_API_KEY = os.getenv("EXA_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


exa_url = "https://api.exa.ai/v1/search"
exa_headers = {"Authorization": f"Bearer {EXA_API_KEY}"}
exa_params = {"query": "Tata Steel company financials procurement"}
exa_response = requests.get(exa_url, headers=exa_headers, params=exa_params)
print("EXA API Response:", exa_response.status_code, exa_response.text)


perplexity_url = "https://api.perplexity.ai/search"
perplexity_headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}"}
perplexity_params = {"query": "Elon Musk Twitter LinkedIn news"}
perplexity_response = requests.get(perplexity_url, headers=perplexity_headers, params=perplexity_params)
print("Perplexity API Response:", perplexity_response.status_code, perplexity_response.text)


serper_url = "https://serper-api.com/v1/search"
serper_headers = {"Authorization": f"Bearer {SERPER_API_KEY}"}
serper_params = {"q": "JSW Steel procurement market position"}
serper_response = requests.get(serper_url, headers=serper_headers, params=serper_params)
print("Serper API Response:", serper_response.status_code, serper_response.text)


