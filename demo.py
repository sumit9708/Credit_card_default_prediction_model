from default_prediction.exception import ExceptionHandler
from default_prediction.pipeline.pipeline import Pipeline
from default_prediction.logger import logging

def main():
    try:

        pipeline = Pipeline()
        pipeline.run_pipeline()
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()