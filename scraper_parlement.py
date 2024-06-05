import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from docx import Document
import PyPDF2
import io
import zipfile
import xml.etree.ElementTree as ET
import re
import pandas as pd
import docx2txt

    
def scrape_file_links(url):
    # get all links drom the page that are files
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    pdf_links = soup.find_all("a", string="Download pdf")
    return [urljoin(url, link["href"]) for link in pdf_links]


def scrape_verslag_links(url):
    # get all links drom the page that are web pages
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a", string="Bekijk het verslag")
    return [urljoin(url, link["href"]) for link in links]



def extract_text_from_pdf(pdf_content):
    # obtain text from pdf file
    pdf_content = io.BytesIO(pdf_content)
    reader = PyPDF2.PdfReader(pdf_content)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text


def download_verslag(page_url, download_dir):
    # Extract the ID from the URL
    verslag_id = page_url.split("/")[-1] 
    
    # scrape web page
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Extract and print the text from each <p> tag
    text = ""
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        text += p.get_text() + "\n"

    # write file
    text_filename = os.path.join(download_dir, f"{verslag_id}.txt")
    with open(text_filename, "w", encoding="utf-8") as text_file:
        text_file.write(text)
        

def download_and_convert_file(pdf_url, download_dir):
    # Extract the ID from the URL
    pdf_id = pdf_url.split("=")[-1]
    
    # Download the file
    pdf_response = requests.get(pdf_url)
    pdf_content = pdf_response.content
    
    # define pdf with content type & EOF markers
    contentType = pdf_response.headers['content-type']
    eof_marker = pdf_content[-4:]
    is_pdf = b'EOF\n' in eof_marker
    
    # Extract text from  content
    # file is actually a pdf
    if contentType == 'application/pdf': 
        if is_pdf:
            text = extract_text_from_pdf(pdf_content)
        else: 
            text = ""
    # file is actually a msword file
    elif contentType == 'application/msword': 
        docx = BytesIO(requests.get(url).content)
        text = docx2txt.process(docx)
    # file is actually a excel file
    elif contentType == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(pdf_url)
        print(df)
        text = df.to_string()
    # file is actually a word doc
    else:
        doc = Document(io.BytesIO(pdf_response.content))
        text = "\n".join([para.text for para in doc.paragraphs])
    
    # write as txt file
    text_filename = os.path.join(download_dir, f"{pdf_id}.txt")
    with open(text_filename, "w", encoding="utf-8") as text_file:
            text_file.write(text)
    
    return pdf_id, text

            
def iterate_scraper_over_pages(base_url, query_params):
    # Directory to save the downloaded files
    download_dir = "documents"
    os.makedirs(download_dir, exist_ok=True)

    # Iterate over pages and scrape links
    page_num = query_params["page"]
    while True:
        query_params["page"] = page_num
        url = base_url + "?" + "&".join([f"{k}={v}" for k, v in query_params.items()])
        print(url)
        # obtain the links of files and webpages respectively for the current page
        pdf_links = scrape_pdf_links(url)
        verslag_links = scrape_verslag_links(url)
        # link directs to web page
        if verslag_links: 
            for link in verslag_links:
                print(link)
                download_verslag(link, download_dir)
        # link directs to download pdf file: however sometimes it is not a pdf: exceptions are written
        if pdf_links: 
            for pdf_link in pdf_links:
                print(pdf_link)
                download_and_convert_file(pdf_link, download_dir)

        page_num += 1


# url 
base_url = "https://www.vlaamsparlement.be/nl/parlementaire-documenten"
# filter parameters
query_params = {
    "page": 0,
    "period": "custom",
    "start_period": "2019-06-01",
    "end_period": "2024-05-30",
    "aggregaat[]": "Vraag of interpellatie"
}


iterate_scraper_over_pages(base_url, query_params)
    