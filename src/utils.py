import pandas as pd
import os 
import sys
import requests
from bs4 import BeautifulSoup

from src.exception import CustomException
from src.logger import logging



def get_articles(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        element_classes = ['td-post-content tagdiv-type', 'tdb-block-inner td-fix-index']

        articles = []

        for class_name in element_classes:
            element_class = soup.find_all(attrs={'class': class_name})

            for element in element_class:
                paragraphs = element.find_all('p')

                for paragraph in paragraphs:
                    para = paragraph.get_text()
                    articles.append(para)
        return articles
        
    except Exception as e:
        raise CustomException(e,sys)


def format_paragraphs(paragraphs):
    try:
        formatted_text = '\n'.join(paragraphs)
        return formatted_text
    
    except Exception as e:
        raise CustomException(e,sys)



def save_articles(row, folder_name):
    try:
        filename = os.path.join(folder_name, f"{row['URL_ID']}.txt")
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as file:
                article_text = row['Articles']
                file.write(article_text)
        else:
            logging.info(f"File {filename} already exists.")
            
    except Exception as e:
        raise CustomException(e, sys)
