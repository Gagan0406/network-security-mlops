import sys

from app.components.data_ingestion import DataIngestion
from app.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from app.exception.exception import NetworkSecurityException
from app.logging.logger import get_logger


logger = get_logger(__name__)


def run_data_ingestion_test():
    try:
        training_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        artifact = data_ingestion.initiate_data_ingestion()
        logger.info("Data ingestion completed successfully")
        logger.info("Train file path: %s", artifact.trained_file_path)
        logger.info("Test file path: %s", artifact.test_file_path)
    except NetworkSecurityException as e:
        logger.error("NetworkSecurityException during data ingestion: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error during data ingestion: %s", e)
        raise


if __name__ == "__main__":
    run_data_ingestion_test()