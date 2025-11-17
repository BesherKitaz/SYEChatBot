from bs4 import BeautifulSoup
import os

scraped_folder = './scraped_pages'
preprocessed_out = './preprocessed_text'
files = []


for file in os.listdir(scraped_folder):
    with open(scraped_folder + '/' + file, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines() if len(line.strip()) > 40]
    cleaned_text = "\n".join(lines)
    files.append({"filename": file, "text": cleaned_text})

for file in files: 
    with open(preprocessed_out + '/' + file['filename'], 'w') as f: 
        f.write(file['text']) 

