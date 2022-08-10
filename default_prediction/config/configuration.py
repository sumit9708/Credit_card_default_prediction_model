import os,sys
from collections import namedtuple
from default_prediction.entity.config_entity import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelTrainerConfig, TrainingPipelineConfig
from default_prediction.exception import ExceptionHandler
from default_prediction.constant import *
from default_prediction.util.util import read_yaml_file
from default_prediction.logger import logging


class Configuration:
    def __init__(self):
        try:
            self.config_info = read_yaml_file(file_path=CONFIG_FILE_PATH)
            self.training_pipeline_config =  self.get_training_pipeline_config()
            self.time_stamp = get_current_time_stamp()
            
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(
                artifact_dir,
                DATA_INGESTION_ARTIFACT_DIR,
                self.time_stamp
            )
            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_info[DATA_INGESTION_DOWNLOAD_URL_KEY]

            csv_download_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_CSV_DOWNLOAD_DIR_KEY]
            )
            
            raw_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY],
            )

            schema_file_path = os.path.join(ROOT_DIR,
            SCHEMA_DIR_KEY,SCHEMA_FILE_NAME)

            ingested_data_dir = os.path.join(data_ingestion_artifact_dir,
            data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
            )
            ingested_train_dir = os.path.join(ingested_data_dir,
            data_ingestion_info[DATA_INGESTION_TRAIN_DIR_KEY]
            )
            ingested_test_dir = os.path.join(ingested_data_dir,
            data_ingestion_info[DATA_INGESTION_TEST_DIR_KEY]
            )

            data_ingestion_config = DataIngestionConfig(
                dataset_download_url,
                csv_download_dir,
                raw_data_dir,
                schema_file_path,
                ingested_train_dir, 
                ingested_test_dir,
            )
            logging.info(f"data_ingestion_config is : [{data_ingestion_config}]")

            print(data_ingestion_config)

            return data_ingestion_config
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_data_validation_config(self):

        try:

            logging.info("-----------data validation config log started-----------------")
            artifact_dir = self.training_pipeline_config.artifact_dir

            time_stamp = self.time_stamp

            self.data_validation_config = self.config_info[DATA_VALIDATION_CONFIG_KEY]

            data_validation_artifact_dir = os.path.join(artifact_dir,
            DATA_VALIDATION_ARTIFACT_DIR_NAME,
            time_stamp
            )

            schema_file_path = os.path.join(ROOT_DIR,
            self.data_validation_config[DATA_VALIDATION_SCHEMA_DIR_KEY],
            self.data_validation_config[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
            )

            report_file_path = os.path.join(data_validation_artifact_dir,
            self.data_validation_config[DATA_VALIDATION_REPORT_FILE_NAME_KEY]
            )

            report_page_file_path = os.path.join(data_validation_artifact_dir,
            self.data_validation_config[DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY]
            )

            data_validation_config = DataValidationConfig(
                schema_file_path, 
                report_file_path, 
                report_page_file_path
                )

            logging.info(f"data_validation_config : [{data_validation_config}]")

            return data_validation_config

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_data_transformation_config(self):
        try:
            logging.info("------------------data transformation config log started-----------------")
            artifact_dir = self.training_pipeline_config.artifact_dir

            time_stamp = self.time_stamp

            data_transformation_artifact_dir = os.path.join(artifact_dir,
            DATA_TRANSFORMATION_ARTIFACT_DIR_NAME,
            time_stamp
            )

            logging.info(f"data_transformation_artifact_dir : [{data_transformation_artifact_dir}]")

            self.data_transformation_config = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            transformed_train_dir = os.path.join(data_transformation_artifact_dir,
            self.data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
            self.data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY]
            )

            logging.info(f"transformed_train_dir : [{transformed_train_dir}]")

            transform_test_dir = os.path.join(data_transformation_artifact_dir,
            self.data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY],
            self.data_transformation_config[DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY]
            )

            logging.info(f"transformed_test_dir : [{transform_test_dir}]")

            preprocessed_object_file_path = os.path.join(data_transformation_artifact_dir,
            self.data_transformation_config[DATA_TRANSFORMATION_PREPROCESSED_DIR_KEY],
            self.data_transformation_config[DATA_TRANSFORMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY]
            )

            logging.info(f"preprocessed_object_file_path : [{preprocessed_object_file_path}]")

            data_transformation_config = DataTransformationConfig(transformed_train_dir, 
                                                                transform_test_dir, 
                                                                preprocessed_object_file_path
                                                                )
            logging.info(f"data_transformation_config: [{data_transformation_config}]")
            return data_transformation_config
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_model_trainer_config(self):
        try:

            logging.info("---------------model trainer config log started-------------------")
            artifact_dir = self.training_pipeline_config.artifact_dir

            time_stamp = self.time_stamp

            artifact_dir = self.training_pipeline_config.artifact_dir

            model_trainer_artifact_dir=os.path.join(
                artifact_dir,
                MODEL_TRAINER_ARTIFACT_DIR_NAME,
                time_stamp
            )
            model_trainer_config_info = self.config_info[MODEL_TRAINER_CONFIG_KEY]

            trained_model_file_path = os.path.join(model_trainer_artifact_dir,
            model_trainer_config_info[MODEL_TRAINER_TRAINED_MODEL_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_MODEL_FILE_NAME_KEY]
            )

            model_config_file_path = os.path.join(ROOT_DIR ,
            model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_DIR_KEY],
            model_trainer_config_info[MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY]
            )

            base_accuracy = model_trainer_config_info[MODEL_TRAINER_BESE_ACCURACY_KEY]

            model_trainer_config = ModelTrainerConfig(
                trained_model_file_path=trained_model_file_path,
                base_accuracy=base_accuracy,
                model_config_file_path=model_config_file_path
            )
            logging.info(f"Model trainer config: {model_trainer_config}")
            return model_trainer_config

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_model_evaluation_config(self):
        try:
            pass
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_model_pusher_config(self):
        pass

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
            logging.info("get_training_pipeline_config log Started")
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipeline config:{training_pipeline_config}")

            logging.info(f"training_pipeline_config is : [{training_pipeline_config}]")
        
            return training_pipeline_config
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    print("data_ingestion_log_completed")

    def new_method(self):
        training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
        return training_pipeline_config