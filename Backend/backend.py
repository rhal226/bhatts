'''
CS 498 Project
~~~~~~~~~~~~~~~~
Implementing the backend of the 498 project with a command line interace
while the API is still under construction

Usage:
    backend.py symptom <symptom>...
    backend.py disease <disease>...

'''


from flask import Flask, request
import docopt
import functools
import pandas as pd
import numpy as np
import json


app = Flask(__name__)


def fixOrder():
    df = pd.read_csv("../data/disease_precautions.csv")
    print(df)
    df = df.sort_values("Disease").reset_index(drop=True)
    print(df)
    df.to_csv("../data/disease_precautions.csv", index=False)


def searchSymp(symptoms):
    print(symptoms)
    df  = pd.read_csv("../data/disease_symptoms.csv")
    # test = df[df.isin([symptoms[0]]).any(axis=1)]
    # print(test)

    mask = functools.reduce(np.logical_or, [df[f"Symptom_{i}"].str.contains(symptoms[0], case=False) for i in range(1, 18)]).fillna(False)
    result = df[mask]

    return result.to_json


def searchDisease(disease):
    df = pd.read_csv("../data/disease_description.csv")
    print(df["Disease"])
    mask = functools.reduce(np.logical_or, [df["Disease"].str.contains(disease[0], case=False)])

    result = df[mask]
    # result = df[df["Disease"].str.contains(disease[0], case=False)]
    print(result)

    return result.to_json


@app.route('/SearchDatabase/<string:arg>', methods=["GET"])
def searchDB(arg):
    arg = json.loads(arg)
    descDF = pd.read_csv("../data/disease_description.csv")
    sympDF = pd.read_csv("../data/disease_symptoms.csv")
    precDF = pd.read_csv("../data/disease_precautions.csv")
    mask = None

    if arg["symptom"]:
        mask = functools.reduce(np.logical_or, [sympDF[f"Symptom_{i}"].str.contains(arg["<symptom>"][0], case=False) for i in
                                                range(1, 18)]).fillna(False)
    elif arg["disease"]:
        mask = functools.reduce(np.logical_or, [descDF["Disease"].str.contains(arg["<disease>"][0], case=False)])

    descDF = descDF[mask]
    sympDF = sympDF[mask].dropna(axis=1)
    precDF = precDF[mask].dropna(axis=1)

    print(descDF)
    print(sympDF)
    print(precDF)

    return [descDF, sympDF, precDF]






if __name__ == '__main__':
    # args = docopt.docopt(__doc__)
    # print(args)
    # if args["symptom"]:
    #     searchSymp(args["<symptom>"])
    # elif args["disease"]:
    #     searchDisease(args["<disease>"])
    # fixOrder()
    # searchDB(args)
    app.run(debug=True)