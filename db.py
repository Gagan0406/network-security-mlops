import os
import sys
import json
from typing import List, Dict, Any

from dotenv import load_dotenv
import certifi
import pandas as pd
import pymongo

from app.exception.exception import NetworkSecurityException
from app.logging.logger import get_logger

logger = get_logger(__name__)
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
ca = certifi.where()


class NetworkDataExtract:


    def __init__(self) -> None:
        try:
            if not MONGODB_URI:
                raise ValueError("MONGODB_URI environment variable is not set")
            self._client = pymongo.MongoClient(MONGODB_URI, tlsCAFile=ca)
            logger.info("Database is connected")
        except Exception as e:
            logger.error("Failed to initialize MongoDB client", exc_info=True)
            raise NetworkSecurityException(str(e), sys.exc_info())

    def csv_to_json(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = json.loads(df.to_json(orient="records"))
            logger.info("Converted CSV to JSON records from %s", file_path)
            return records
        except Exception as e:
            logger.error("Failed to convert CSV to JSON from %s", file_path, exc_info=True)
            raise NetworkSecurityException(str(e), sys.exc_info())

    def insert_data_to_mongodb(
        self, database: str, collection_name: str, data: List[Dict[str, Any]]
    ) -> int:
        try:
            db = self._client[database]
            collection = db[collection_name]
            result = collection.insert_many(data)
            inserted_count = len(result.inserted_ids)
            logger.info(
                "Inserted %d records into %s.%s",
                inserted_count,
                database,
                collection_name,
            )
            return inserted_count
        except Exception as e:
            logger.error(
                "Failed to insert data into %s.%s", database, collection_name, exc_info=True
            )
            raise NetworkSecurityException(str(e), sys.exc_info())

if __name__=="__main__":
    FILE_PATH = "data\\phisingData.csv"
    DATABASE="db"
    Collection="NetworkData"
    networkObj=NetworkDataExtract()
    data = networkObj.csv_to_json(file_path=FILE_PATH)
    count = networkObj.insert_data_to_mongodb(DATABASE, Collection, data)
    print(count)