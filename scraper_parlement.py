import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import PyPDF2
import io


def scrape_pdf_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    pdf_links = soup.find_all("a", string="Download pdf")
    return [urljoin(url, link["href"]) for link in pdf_links]


def scrape_verslag_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    pdf_links = soup.find_all("a", string="Bekijk het verslag")
    return [urljoin(url, link["href"]) for link in pdf_links]



def extract_text_from_pdf(pdf_content):
    pdf_content = io.BytesIO(pdf_content)

    reader = PyPDF2.PdfReader(pdf_content)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text


def download_verslag(page_url, download_dir):
    # Extract the ID from the URL
    verslag_id = page_url.split("/")[-1] 
     
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract and print the text from each <p> tag
    
    text = ""
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        text += p.get_text() + "\n"

    
    text_filename = os.path.join(download_dir, f"{verslag_id}.txt")
    with open(text_filename, "w", encoding="utf-8") as text_file:
        text_file.write(text)
        

def download_and_convert_pdf(pdf_url, download_dir):
    # Extract the ID from the URL
    pdf_id = pdf_url.split("=")[-1]
    
    # Download the PDF file
    pdf_response = requests.get(pdf_url)
    pdf_content = pdf_response.content
    
    # Extract text from PDF content
    text = extract_text_from_pdf(pdf_content)
    
    text_filename = os.path.join(download_dir, f"{pdf_id}.txt")
    with open(text_filename, "w", encoding="utf-8") as text_file:
        text_file.write(text)
        
    
    return pdf_id, text



base_url = "https://www.vlaamsparlement.be/nl/parlementaire-documenten"
query_params = {
    "page": 0,
    "period": "custom",
    "start_period": "2024-01-01",
    "end_period": "2024-01-15",
    "aggregaat[]": "Vraag of interpellatie"
}



# Directory to save the downloaded PDFs
download_dir = "questions"
os.makedirs(download_dir, exist_ok=True)


# Iterate over pages and scrape PDF links
page_num = 0
while True:
    query_params["page"] = page_num
    url = base_url + "?" + "&".join([f"{k}={v}" for k, v in query_params.items()])
    print(url)
    pdf_links = scrape_pdf_links(url)
    verslag_links = scrape_verslag_links(url)

    if verslag_links: 
        for link in verslag_links:
            print(link)
            download_verslag(link, download_dir)
 
    # if pdf_links: 
    #     for pdf_link in pdf_links:
    #         print(pdf_link)
    #         download_and_convert_pdf(pdf_link, download_dir)
    
    page_num += 1
    
    