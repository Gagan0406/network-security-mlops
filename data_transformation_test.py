import sys

from app.components.data_ingestion import DataIngestion
from app.components.data_validation import DataValidation
from app.components.data_transformation import DataTransformation
from app.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
)
from app.exception.exception import NetworkSecurityException
from app.logging.logger import get_logger

logger = get_logger(__name__)


def run_data_transformation_test():
    try:
        # set up pipeline configs
        training_config = TrainingPipelineConfig()

        # ingest raw data so we have files to validate & transform
        data_ingestion_config = DataIngestionConfig(training_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        ingestion_artifact = data_ingestion.initiate_data_ingestion()

        # validate the ingested data
        data_validation_config = DataValidationConfig(training_config)
        data_validation = DataValidation(
            data_ingestion_artifact=ingestion_artifact,
            data_validation_config=data_validation_config,
        )
        validation_artifact = data_validation.initiate_data_validation()

        # perform transformation
        data_transformation_config = DataTransformationConfig(training_config)
        data_transformation = DataTransformation(
            data_validation_artifact=validation_artifact,
            data_transformation_config=data_transformation_config,
        )
        transformation_artifact = data_transformation.initiate_data_transformation()

        logger.info("Data transformation completed successfully")
        logger.info("Transformed object path: %s", transformation_artifact.transformed_object_file_path)
        logger.info("Transformed train array path: %s", transformation_artifact.transformed_train_file_path)
        logger.info("Transformed test array path: %s", transformation_artifact.transformed_test_file_path)

    except NetworkSecurityException as e:
        logger.error("NetworkSecurityException during data transformation: %s", e)
        raise
    except Exception as e:
        logger.error("Unexpected error during data transformation: %s", e)
        raise


if __name__ == "__main__":
    run_data_transformation_test()
