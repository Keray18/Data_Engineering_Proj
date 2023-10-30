from src.components.data_ingestion import DataIngestionConfig
from src.components.data_ingestion import DataIngestion

from src.components.data_extraction import DataExtractionConfig
from src.components.data_extraction import DataExtraction

from src.components.data_analyzing import DataAnalysisConfig
from src.components.data_analyzing import DataAnalysis




if __name__ == "__main__":
    obj = DataIngestion()
    raw_data = obj.initiate_data_ingestion()

    data_extraction = DataExtraction()
    raw_data = data_extraction.initiate_data_extraction(raw_data)

    data_analysis = DataAnalysis()
    data_analysis.initiate_data_analysis(new_data)
    print("output file has been created")
