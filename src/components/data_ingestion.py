import os 
import sys  
from src.logger import logging
from src.exception import CustomException

import pandas as pd  
from dataclasses import dataclass


@dataclass 
class DataIngestionConfig:
    raw_data_path: str=os.path.join('artifact', "raw.csv")



class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Initiating Data Ingestion")
        try:
            df = pd.read_excel('notebook/data/Input.xlsx')
            logging.info("Read the dataset as dataframe")

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Ingestion Completed! Data saved as mentioned.")

            return(
                self.ingestion_config.raw_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)


    