import os
import sys

_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from app.exception.exception import NetworkSecurityException
from app.entity.config_entity import DataIngestionConfig
from app.entity.artifact_entity import DataIngestionArtifact
from app.logging.logger import get_logger
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

logger = get_logger(__name__)
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(str(e))
        
    def export_collection_as_dataframe(self):
        """
        Read data from mongodb
        """
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGODB_URI)
            collection=self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"])

            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(str(e))
        
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(str(e))
        
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logger.info("Performed train test split on the dataframe")
            logger.info("Exited split_data_as_train_test method of DataIngestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logger.info("Exporting train and test file path")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logger.info("Exported train and test file path")
        except Exception as e:
            raise NetworkSecurityException(str(e))
        
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path,
            )
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(str(e))