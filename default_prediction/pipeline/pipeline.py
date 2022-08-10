from tkinter import E
from default_prediction.component.data_transformation import DataTransformation
from default_prediction.component.data_validation import DataValidation
from default_prediction.component.model_training import ModelTrainer
from default_prediction.config.configuration import Configuration
from default_prediction.constant import *
from default_prediction.exception import ExceptionHandler
import os,sys
from default_prediction.logger import logging

from default_prediction.entity.config_artifact import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact
from default_prediction.entity.config_entity import DataIngestionConfig,DataValidationConfig
from default_prediction.component.data_ingestion import DataIngestion

class Pipeline:
    def __init__(self,config: Configuration = Configuration())->None:
        try:
            self.config = config

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def start_data_ingestion(self,)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            data_ingestion_artifact = data_ingestion_artifact

            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.config.get_data_validation_config())
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(data_transformation_config=self.config.get_data_transformation_config(),
            data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact
            )
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            model_training = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),data_transformation_artifact=data_transformation_artifact)
            return model_training.initiate_model_trainer()
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass


    def run_pipeline(self):
        try:
            
            # Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                            data_validation_artifact=data_validation_artifact
            )

            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return data_ingestion_artifact,data_validation_artifact,data_transformation_artifact,model_trainer_artifact

        except Exception as e:
            raise ExceptionHandler(e,sys) from e