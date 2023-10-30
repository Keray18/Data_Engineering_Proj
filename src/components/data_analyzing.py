import os 
import sys  
from src.logger import logging
from src.exception import CustomException

import re
import nltk
import pandas as pd  
from dataclasses import dataclass

from src.utils import get_sentiment_scores, empty_sentences, calculate_scores

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')


@dataclass
class DataAnalysisConfig:
    output_data_path: str=os.path.join('artifact', "output.csv")



class DataAnalysis:
    def __init__(self):
        self.data_analysis_config = DataAnalysisConfig()

    def initiate_data_analysis(self, new_data_path):
        try:
            df = pd.read_csv(new_data_path)
            logging.info('Analyzing the sentences has been started.....')
            
            pol_scores = []
            get_sentiment_scores(dataframe=df, pol_scores=pol_scores)
            logging.info("Polarity Scores have been calculated")

            df['polarity_score'] = pol_scores
            df['positive_score'] = [score['pos'] for score in pol_scores]
            df['negative_score'] = [score['neg'] for score in pol_scores]
            df['subjective_score'] = [score['compound'] for score in pol_scores]
            logging.info("Positive, Negative and Subjective scores have been recorded")

            empty_articles = df['Articles'].apply(empty_sentences)
            if empty_articles.any():
                df = df[~empty_articles]
                logging.info("Removing the empty articles")
            

            final_df = calculate_scores(df)  
            final_df.to_csv(self.data_analysis_config.output_data_path, index=False, header=True)
            logging.info("Analysis of text is completed successfully.")

            return(
                self.data_analysis_config.output_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
