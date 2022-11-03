import json
import pickle
from src import read_params, logger

# Creating an object of the class Logger.
logger_obj = logger.Logger(
    logger_name=__name__, file_name=__file__, streamLogs=True)
lgr = logger_obj.get_logger()


def Predict(predictors, cfile_path="params.yaml"):
    """Does the prediction for the predictors fetched form the webapp or the API. 

    Args:
        predictors (dict): Predictors attributes fetched from the webapp or the API.
        cfile_path (str, optional): Configuration file's path that contains all the params and paths.
        Defaults to "params.yaml".

    Returns:
        float: Prediction.
    """
    try:
        config = read_params.read_params(cfile_path)
        scaler_path = config["transformation_dir"]["scaler_object"]
        model_path = config["model_dir"]["object"]
        scores_path = config["reports"]["scores"]

        # First and foremost, transform all the values of predictors in the float dtype
        # since values of predictors fetched from the webpage are in string format
        predictors = {key: float(value) for (key, value) in zip(
            predictors.keys(), predictors.values())}

        # Setting Machine Failure (machine_f) to 1 if even any single of the other failures is True
        # (this is the dataset condition)
        if predictors['machine_f'] != 1:
            if 1 in [predictors["twf"], predictors["hdf"], predictors["pwf"], predictors["osf"], predictors["rnf"]]:
                predictors['machine_f'] = 1
        lgr.info(predictors)

        # Predictors (into list format)
        preds = [list(predictors.values())]
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
        lgr.info(f"prediction: {prediction}")

        # Accuracy of the model
        with open(scores_path) as f:
            scores = json.load(f)
        score = float(scores["Test Accuracies"]["Adjusted R-squared"])
        accuracy = round(score*100, 3)
        lgr.info(f"Accuracy of the Model: {accuracy}%")

        return round(prediction[0][0], 3), accuracy

    except Exception as e:
        lgr.exception(e)
