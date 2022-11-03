import json
import pickle
from src import read_params, logger

# Creating an object of the class Logger.
logger_obj = logger.Logger(
    logger_name=__name__, file_name=__file__, streamLogs=True)
lgr = logger_obj.get_logger()


def Predict(predictors, cfile_path="params.yaml"):
    try:
        config = read_params.read_params(cfile_path)
        scaler_path = config["transformation_dir"]["scaler_object"]
        model_path = config["model_dir"]["object"]
        scores_path = config["reports"]["scores"]

        # Setting Machine Failure (machine_f) to 1 if even any single of the other failures is True
        if predictors['machine_f'] != '1':
            if '1' in [predictors["twf"], predictors["hdf"], predictors["pwf"], predictors["osf"], predictors["rnf"]]:
                predictors['machine_f'] = '1'
        lgr.info(predictors)

        # Predictors (into list format)
        # Values of predictors fecthed from the webpage are in string format,
        # converting them into float
        preds = [list(map(float, predictors.values()))]
        lgr.info(f"predictors(list format)): {preds}")

        # STANDARDIZATION of Predictors
        # Loading the scaler object
        scaler = pickle.load(open(scaler_path, 'rb'))
        lgr.info("scaling the predictors to the normal scale..")
        preds_scaled = scaler.transform(preds)
        lgr.info(f"scaled predictors: {preds_scaled} ")

        # PREDICTION
        # Loading the model
        mod = pickle.load(open(model_path, 'rb'))
        prediction = mod.predict(preds_scaled)

        # Accuracy of the model
        with open(scores_path) as f:
            scores = json.load(f)
        score = float(scores["Test Accuracies"]["Adjusted R-squared"])
        accuracy = round(score*100, 3)
        lgr.info(f"Accuracy of the Model: {accuracy}%")

        return round(prediction[0][0], 3), accuracy

    except Exception as e:
        lgr.exception(e)