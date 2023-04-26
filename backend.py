'''
CS 498 Project
~~~~~~~~~~~~~~~~
Implementing the backend of the 498 project with a command line interace
while the API is still under construction

Usage:
    backend.py symptom <symptom>...
    backend.py disease <disease>...

'''

from flask import Flask, request, render_template, jsonify
import functools
import pandas as pd
import numpy as np
import json

app = Flask(__name__, template_folder="templates", static_folder="static", )


#
# def fixOrder():
#     df = pd.read_csv("../data/disease_precautions.csv")
#     print(df)
#     df = df.sort_values("Disease").reset_index(drop=True)
#     print(df)
#     df.to_csv("../data/disease_precautions.csv", index=False)
#
#
# def searchSymp(symptoms):
#     print(symptoms)
#     df  = pd.read_csv("../data/disease_symptoms.csv")
#     # test = df[df.isin([symptoms[0]]).any(axis=1)]
#     # print(test)
#
#     mask = functools.reduce(np.logical_or, [df[f"Symptom_{i}"].str.contains(symptoms[0], case=False) for i in range(1, 18)]).fillna(False)
#     result = df[mask]
#
#     return result.to_json
#
#
# def searchDisease(disease):
#     df = pd.read_csv("../data/disease_description.csv")
#     print(df["Disease"])
#     mask = functools.reduce(np.logical_or, [df["Disease"].str.contains(disease[0], case=False)])
#
#     result = df[mask]
#     # result = df[df["Disease"].str.contains(disease[0], case=False)]
#     print(result)
#
#     return result.to_json

@app.route("/user")
def user():
    return render_template('user.html')


@app.route("/new")
def newUser():
    return render_template('new.html')


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/sympCheck")
def sympCheck():
    return render_template('symptomChecker.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/contact")
def contact():
    return render_template('contactUs.html')

@app.route("/searchDB<string:args>", methods=["GET"])
def searchDB(args):
    arg = json.loads(args)

    descDF = pd.read_csv("data/disease_description.csv")
    sympDF = pd.read_csv("data/disease_symptoms.csv")
    precDF = pd.read_csv("data/disease_precautions.csv")
    mask = None

    if arg[1] == "searchSymptom":
        searches = arg[0].split(", ")
        mask = functools.reduce(np.logical_or, [sympDF[f"Symptom_{i}"].str.contains('|'.join(searches), case=False) for i in
                                                range(1, 18)]).fillna(False)
    elif arg[1] == "searchDisease":
        mask = functools.reduce(np.logical_or, [descDF["Disease"].str.contains(arg[0], case=False)])

    descDF = descDF[mask]
    sympDF = sympDF[mask].dropna(axis=1)
    precDF = precDF[mask].dropna(axis=1)

    # print(descDF)

    return jsonify([descDF.to_json(), sympDF.to_json(), precDF.to_json()])


if __name__ == '__main__':
    # args = docopt.docopt(__doc__)
    # print(args)
    # if args["symptom"]:
    #     searchSymp(args["<symptom>"])
    # elif args["disease"]:
    #     searchDisease(args["<disease>"])
    # fixOrder()
    # searchDB(args)
    app.run()
