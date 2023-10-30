import pandas as pd
import os 
import sys
import requests
from bs4 import BeautifulSoup

from src.exception import CustomException
from src.logger import logging

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


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



def get_sentiment_scores(dataframe, pol_scores):
    try:
        nltk.download('vader_lexicon')
        sia = SentimentIntensityAnalyzer()

        for article in df['Articles']:
            pol = sia.polarity_scores(article)
            pol_scores.append(pol)

        return pol_scores
    
    except Exception as e:
        raise CustomException(e, sys)


def empty_sentences(text):
    try:
        sentences = nltk.sent_tokenize(text)
        return len(sentences) == 0

    except Exception as e:
        raise CustomException(e, sys)



def calculate_scores(df):
    try:
        for index, row in df.iterrows():
            article = row['Articles']

            sentences = nltk.sent_tokenize(article)
            average_sentence_length = sum(len(nltk.word_tokenize(sentence)) for sentence in sentences) / len(sentences)

            words = nltk.word_tokenize(article)
            tagged = nltk.pos_tag(words)
            complex_words = [word for word in words if len(word) > 2]

            percentage_complex_words = (len(complex_words) / len(words)) * 100
            complex_word_count = len(complex_words)

            fog_index = 0.4 * (average_sentence_length + percentage_complex_words)

            total_word_count = len(words)
            average_words_per_sentence = total_word_count / len(sentences)
            average_word_length = sum(len(word) for word in words) / len(words)

            # total_syllables = sum(count_syllables(word) for word in words)
            # avg_syllables_per_word = total_syllables / total_word_count

            personal_pronouns = [word for word, pos in tagged if pos in ['PRP', 'PRP$', 'WP', 'WP$']]
            personal_pronoun_count = len(personal_pronouns)

            df.at[index, 'avg_sentence_length'] = average_sentence_length
            df.at[index, 'percentage_of_complex_words'] = percentage_complex_words
            df.at[index, 'fog_index'] = fog_index
            df.at[index, 'avg_number_of_words_per_sentence'] = average_words_per_sentence
            df.at[index, 'complex_word_count'] = complex_word_count
            df.at[index, 'word_count'] = total_word_count
            # df.at[index, 'syllable_per_word'] = avg_syllables_per_word
            df.at[index, 'Personal_Pronouns'] = personal_pronoun_count
            df.at[index, 'avg_word_length'] = average_word_length

        return df

    except Exception as e:
        raise CustomException(e,sys)