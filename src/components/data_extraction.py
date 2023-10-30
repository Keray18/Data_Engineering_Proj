import os 
import sys  
from src.logger import logging
from src.exception import CustomException

import pandas as pd  
from dataclasses import dataclass

from src.utils import get_articles, format_paragraphs, save_articles

@dataclass
class DataExtractionConfig:
    new_data_path: str=os.path.join('artifact', "new.csv")



class DataExtraction:
    def __init__(self):
        self.data_extraction_config = DataExtractionConfig()

    def initiate_data_extraction(self, raw_data_path):
        try:
            df = pd.read_csv(raw_data_path)
            logging.info("RAW data have been read and extraction begins....")

            df['Articles'] = df['URL'].apply(get_articles)
            df['Articles'] = df['Articles'].apply(format_paragraphs)
            logging.info("Articles are extracted and in a readabled format")

            
            folder_name = 'articles_folder'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            df.apply(save_articles, axis=1, folder_name=folder_name)    
            logging.info("Texts Have been Created")

            df.to_csv(self.data_extraction_config.new_data_path, index=False, header=True)
            logging.info("Extraction of data is Completed.")

            return(
                self.data_extraction_config.new_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
