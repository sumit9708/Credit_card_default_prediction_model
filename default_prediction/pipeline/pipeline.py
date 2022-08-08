from tkinter import E
from default_prediction.config.configuration import Configuration
from default_prediction.constant import *
from default_prediction.exception import ExceptionHandler
import os,sys
from default_prediction.logger import logging

from default_prediction.entity.config_artifact import DataIngestionArtifact
from default_prediction.entity.config_entity import DataIngestionConfig
from default_prediction.component.data_ingestion import DataIngestion

class Pipeline:
    def __init__(self,config: Configuration = Configuration())->None:
        try:
            self.config = config

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def start_data_transformation(self):
        pass

    def start_model_trainer(self):
        pass

    def start_model_evaluation(self):
        pass

    def start_model_pusher(self):
        pass


    def run_pipeline(self):
        try:
            # Data Ingestion
            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:
            raise ExceptionHandler(e,sys) from e