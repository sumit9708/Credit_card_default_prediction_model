from flask import Flask, request
import sys

import pip
from default_prediction.util.util import read_yaml_file, write_yaml_file
#from matplotlib.style import context
from default_prediction.logger import logging
from default_prediction.exception import ExceptionHandler
import os, sys
import json
from default_prediction.config.configuration import Configuration
from default_prediction.constant import CONFIG_DIR, get_current_time_stamp
from default_prediction.pipeline.pipeline import Pipeline
from default_prediction.entity.defaulter_predictor import DefaulterPredictor, DefaulterData
from flask import send_file, abort, render_template

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "default_prediction"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


from default_prediction.logger import get_log_dataframe

DEFAULTER_DATA_KEY = "defaulter_data"
POTENTIALY_DEFAULTER_KEY = "SeriousDlqin2yrs"

app = Flask(__name__)


@app.route('/artifact', defaults={'req_path': 'default_prediction'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("default_prediction", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=Configuration())
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    context = {
        DEFAULTER_DATA_KEY: None,
        POTENTIALY_DEFAULTER_KEY: None
    }

    if request.method == 'POST':
        CustomerID = int(request.form['CustomerID'])
        RevolvingUtilizationOfUnsecuredLines = float(request.form['RevolvingUtilizationOfUnsecuredLines'])
        age = int(request.form['age'])
        NumberOfTime30_to_59DaysPastDueNotWorse = int(request.form['NumberOfTime30_to_59DaysPastDueNotWorse'])
        DebtRatio = float(request.form['DebtRatio'])
        MonthlyIncome = float(request.form['MonthlyIncome'])
        NumberOfOpenCreditLinesAndLoans = int(request.form['NumberOfOpenCreditLinesAndLoans'])
        NumberOfTimes90DaysLate = int(request.form['NumberOfTimes90DaysLate'])
        NumberRealEstateLoansOrLines = int(request.form['NumberRealEstateLoansOrLines'])
        NumberOfTime60_to_89DaysPastDueNotWorse= int(request.form['NumberOfTime60_to_89DaysPastDueNotWorse'])
        NumberOfDependents = float(request.form['NumberOfDependents'])

        defaulter_data = DefaulterData(CustomerID=CustomerID,
                                   RevolvingUtilizationOfUnsecuredLines=RevolvingUtilizationOfUnsecuredLines,
                                   age=age,
                                   NumberOfTime30_to_59DaysPastDueNotWorse=NumberOfTime30_to_59DaysPastDueNotWorse,
                                   DebtRatio=DebtRatio,
                                   MonthlyIncome=MonthlyIncome,
                                   NumberOfOpenCreditLinesAndLoans=NumberOfOpenCreditLinesAndLoans,
                                   NumberOfTimes90DaysLate=NumberOfTimes90DaysLate,
                                   NumberRealEstateLoansOrLines=NumberRealEstateLoansOrLines,
                                   NumberOfTime60_to_89DaysPastDueNotWorse=NumberOfTime60_to_89DaysPastDueNotWorse,
                                   NumberOfDependents=NumberOfDependents
                                   )
        defaulter_df = defaulter_data.get_defaulter_input_data_frame()
        defaulter_predictor = DefaulterPredictor(model_dir=MODEL_DIR)
        SeriousDlqin2yrs = defaulter_predictor.predict(X=defaulter_df)
        context = {
            DEFAULTER_DATA_KEY: defaulter_data.get_defaulter_data_as_dict(),
            POTENTIALY_DEFAULTER_KEY: SeriousDlqin2yrs
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)


@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)


@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)


@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run()