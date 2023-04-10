'''
CS 498 Project
~~~~~~~~~~~~~~~~
Implementing the backend of the 498 project with a command line interace
while the API is still under construction

Usage:
    backend.py symptom <symptom>...
    backend.py disease <disease>...

'''



import docopt
import functools
import pandas as pd
import numpy as np


def searchSymp(symptoms):
    print(symptoms)
    df  = pd.read_csv("../data/disease_symptoms.csv")
    # test = df[df.isin([symptoms[0]]).any(axis=1)]
    # print(test)

    mask = functools.reduce(np.logical_or, [df[f"Symptom_{i}"].str.contains(symptoms[0]) for i in range(1, 18)]).fillna(False)
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


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    # print(args)
    if args["symptom"]:
        searchSymp(args["<symptom>"])
    elif args["disease"]:
        searchDisease(args["<disease>"])
