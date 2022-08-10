import os
import sys

from default_prediction.exception import ExceptionHandler
from default_prediction.util.util import load_object

import pandas as pd


class DefaulterData:

    def __init__(self,
                 CustomerID : int,
                 RevolvingUtilizationOfUnsecuredLines : float,
                 age: int,
                 NumberOfTime30_to_59DaysPastDueNotWorse : int,
                 DebtRatio : float,
                 MonthlyIncome : float,
                 NumberOfOpenCreditLinesAndLoans : int,
                 NumberOfTimes90DaysLate : int,
                 NumberRealEstateLoansOrLines : int,
                 NumberOfTime60_to_89DaysPastDueNotWorse : int,
                 NumberOfDependents : float,
                 SeriousDlqin2yrs : int = None
                 ):
        try:
            self.CustomerID = CustomerID
            self.RevolvingUtilizationOfUnsecuredLines = RevolvingUtilizationOfUnsecuredLines
            self.age = age
            self.NumberOfTime30_to_59DaysPastDueNotWorse = NumberOfTime30_to_59DaysPastDueNotWorse
            self.DebtRatio = DebtRatio
            self.MonthlyIncome = MonthlyIncome
            self.NumberOfOpenCreditLinesAndLoans = NumberOfOpenCreditLinesAndLoans
            self.NumberOfTimes90DaysLate = NumberOfTimes90DaysLate
            self.NumberRealEstateLoansOrLines = NumberRealEstateLoansOrLines
            self.NumberOfTime60_to_89DaysPastDueNotWorse = NumberOfTime60_to_89DaysPastDueNotWorse
            self.NumberOfDependents = NumberOfDependents
            self.SeriousDlqin2yrs = SeriousDlqin2yrs
        except Exception as e:
            raise ExceptionHandler(e, sys) from e

    def get_defaulter_input_data_frame(self):

        try:
            defaulter_input_dict = self.get_defaulter_data_as_dict()
            return pd.DataFrame(defaulter_input_dict)
        except Exception as e:
            raise ExceptionHandler(e, sys) from e

    def get_defaulter_data_as_dict(self):
        try:
            input_data = {
                "CustomerID": [self.CustomerID],
                "RevolvingUtilizationOfUnsecuredLines": [self.RevolvingUtilizationOfUnsecuredLines],
                "age": [self.age],
                "NumberOfTime30_to_59DaysPastDueNotWorse": [self.NumberOfTime30_to_59DaysPastDueNotWorse],
                "DebtRatio": [self.DebtRatio],
                "MonthlyIncome": [self.MonthlyIncome],
                "NumberOfOpenCreditLinesAndLoans": [self.NumberOfOpenCreditLinesAndLoans],
                "NumberOfTimes90DaysLate": [self.NumberOfTimes90DaysLate],
                "NumberRealEstateLoansOrLines": [self.NumberRealEstateLoansOrLines],
                "NumberOfTime60_to_89DaysPastDueNotWorse":[self.NumberOfTime60_to_89DaysPastDueNotWorse],
                 "NumberOfDependents":[self.NumberOfDependents]}
            return input_data
        except Exception as e:
            raise ExceptionHandler(e, sys)


class DefaulterPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise ExceptionHandler(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise ExceptionHandler(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            median_house_value = model.predict(X)
            return median_house_value
        except Exception as e:
            raise ExceptionHandler(e, sys) from e