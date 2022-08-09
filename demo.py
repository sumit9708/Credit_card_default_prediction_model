from default_prediction.exception import ExceptionHandler
from default_prediction.pipeline.pipeline import Pipeline
from default_prediction.logger import logging
from default_prediction.config.configuration import Configuration

def main():
    try:

        pipeline = Pipeline()
        pipeline.run_pipeline()
        #config = Configuration()

        #return config.get_data_validation_config()
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()