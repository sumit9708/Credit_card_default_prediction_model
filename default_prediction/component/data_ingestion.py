import os,sys
from default_prediction.config.configuration import Configuration
from default_prediction.logger import logging
from default_prediction.exception import ExceptionHandler
from default_prediction.util.util import read_yaml_file
from six.moves import urllib
from  default_prediction.entity.config_artifact import DataIngestionArtifact
from default_prediction.entity.config_entity import DataIngestionConfig
import shutil
import pandas as pd
import numpy as np
from default_prediction.util.util import read_yaml_file
from default_prediction.constant import *

print("reached in data_ingestion inside component")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_dowloaded_data(self,)->str:
        try:
            logging.info("--------------data ingestion log inside component started----------------")
            download_url = self.data_ingestion_config.data_download_url

            logging.info(f"download_url is [{download_url}]")

            csv_download_dir = self.data_ingestion_config.csv_download_dir

            if os.path.exists(csv_download_dir):
                os.remove(csv_download_dir)

            os.makedirs(csv_download_dir,exist_ok=True)

            csv_file_name = os.path.basename(download_url)

            csv_file_path = os.path.join(csv_download_dir,csv_file_name)

            logging.info(f"csv_file_path is : [{csv_file_path}]")

            urllib.request.urlretrieve(download_url,csv_file_path)

            return csv_file_path

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def get_raw_csv_data(self):
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)
            os.makedirs(raw_data_dir,exist_ok=True)

            csv_download_dir = self.data_ingestion_config.csv_download_dir
 
            csv_file_path = self.get_dowloaded_data()

            file_name = os.listdir(csv_download_dir)[0]

            file_path = os.path.join(raw_data_dir,file_name)

            shutil.copy(csv_file_path,raw_data_dir)

            raw_data_dir_file = os.listdir(raw_data_dir)[0]

            logging.info(f"raw_data_dir_file is :[{raw_data_dir_file}]")

            return file_path

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def split_into_train_and_test_data(self):
        try:
            
            file_path = self.get_raw_csv_data()

            raw_data_dir = self.data_ingestion_config.raw_data_dir

            logging.info(f"raw_data_dir : [{raw_data_dir}]")

            file_name = os.listdir(raw_data_dir)[0]

            file_path = os.path.join(raw_data_dir,file_name)

            logging.info(f"file_path is :[{file_path}]")

            schema_file_path = self.data_ingestion_config.schema_file_path

            schema = read_yaml_file(file_path=schema_file_path)

            default_prediction_dataframe = pd.read_csv(file_path)

            default_prediction_dataframe.columns = schema[COLUMNS_KEY]

            train_set = default_prediction_dataframe[:120000]

            test_set = default_prediction_dataframe[120000:]

            return train_set,test_set

        except Exception as e:
            raise ExceptionHandler(e,sys) from e

    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            
            train_set,test_set = self.split_into_train_and_test_data()

            ingested_test_dir = self.data_ingestion_config.ingested_test_dir

            logging.info(f"ingested_test_dir is :[{ingested_test_dir}]")
            ingested_train_dir = self.data_ingestion_config.ingested_train_dir
            logging.info(f"ingested_train_dir is :[{ingested_train_dir}]")

            #raw_data_dir = self.get_raw_csv_data()

            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.listdir(raw_data_dir)[0]
            logging.info(f"file_name is :[{file_name}]")
            train_file_path = os.path.join(ingested_train_dir,file_name)

            logging.info(f"train_file_path is :[{train_file_path}]")

            os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
            
            test_file_path = os.path.join(ingested_test_dir,file_name)
            logging.info(f"test_file_path is :[{test_file_path}]")

            os.makedirs(self.data_ingestion_config.ingested_test_dir,exist_ok=True)
            
            logging.info(f"Exporting Training Dataset To file:[{train_file_path}]")

            train_set.to_csv(train_file_path,index=False)

            test_set.to_csv(test_file_path,index=False)

            is_ingested = True

            message = "Data Ingestion Completed Successfuly"

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path, 
                test_file_path, 
                is_ingested, 
                message
            )

            logging.info(f"data_ingestion_artifact is : [{data_ingestion_artifact}]")

            return data_ingestion_artifact
        except Exception as e:
            raise ExceptionHandler(e,sys) from e
    print("log after data_ingestion")

    def __del__(self):
        logging.info(f"{'='*20}Data Ingestion log completed.{'='*20} \n\n")