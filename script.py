from src.components.data_ingestion import DataIngestionConfig
from src.components.data_ingestion import DataIngestion

from src.components.data_extraction import DataExtractionConfig
from src.components.data_extraction import DataExtraction




if __name__ == "__main__":
    obj = DataIngestion()
    raw_data = obj.initiate_data_ingestion()

    data_extraction = DataExtraction()
    data_extraction.initiate_data_extraction(raw_data)