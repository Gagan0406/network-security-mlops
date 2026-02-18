import sys

from app.components.data_ingestion import DataIngestion
from app.components.data_validation import DataValidation
from app.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
)
from app.exception.exception import NetworkSecurityException
from app.logging.logger import get_logger


logger = get_logger(__name__)


def run_data_validation_test():
    try:
        training_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        ingestion_artifact = data_ingestion.initiate_data_ingestion()

        data_validation_config = DataValidationConfig(training_config)
        data_validation = DataValidation(
            data_ingestion_artifact=ingestion_artifact,
            data_validation_config=data_validation_config,
        )
        validation_artifact = data_validation.initiate_data_validation()

        logger.info("Data validation completed successfully")
        logger.info("Validation status: %s", validation_artifact.validation_status)
        logger.info(
            "Drift report path: %s", validation_artifact.drift_report_file_path
        )
    except NetworkSecurityException as e:
        logger.error("NetworkSecurityException during data validation: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error during data validation: %s", e)
        raise


if __name__ == "__main__":
    run_data_validation_test()
