from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import os
from application_logger import logger
from predict_via_model import Predict

# Creating an object of the class Logger.
logger_obj = logger.Logger(
    logger_name=__name__, file_name=__file__, streamLogs=True)
lgr = logger_obj.get_logger()


app = Flask(__name__, template_folder=os.path.join('webapp', 'templates'))


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        lgr.exception(e)


@app.route('/prediction+results', methods=['POST', 'GET'])
@cross_origin()
def main():
    if request.method == 'POST':
        try:
            # fetching the predictors
            lgr.info("fetching the predictors..")
            if request.form:
                predictors = dict(request.form)
                lgr.info(predictors)
                lgr.info("predictors values fetched!")
                prediction, accuracy = Predict(predictors)

                return render_template('results.html', prediction=prediction, accuracy=accuracy)

            elif request.json:
                lgr.info('fetching the predictors from the API..')
                predictors = request.json
                print(predictors)
                lgr.info(predictors)
                lgr.info('predictors fetched!')
                prediction = Predict(predictors)[0]

                return {"Air temperature [K]": prediction}

        except Exception as e:
            lgr.exception(e)
            error_m1 = "It's either that you have rendered some inputs empty or its values are out of the range."
            error_m2 = "Please try again with apt values!"
            
            return render_template('404.html', error_m1=error_m1, error_m2=error_m2)


@app.route('/analytics', methods=['GET'])
@cross_origin()
def analytics_report():
    try:
        return render_template("eda_report.html")
    except Exception as e:
        lgr.exception(e)
        error_m1 = "There's some error loading the Analytics Report."
        error_m2 = "Kindly try again after some time!"
        return render_template('404.html', error_m1=error_m1, error_m2=error_m2)


if __name__ == "__main__":
    app.run(debug=True)
