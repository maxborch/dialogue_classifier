from django.shortcuts import render
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from django.conf import settings


# from sklearn import datasets
# from django.conf import settings
# from rest_framework import views
# from rest_framework import status
# from rest_framework.response import Response


# from sklearn.ensemble import RandomForestClassifier


# class Train(views.APIView):
#     def post(self, request):
#         dataset = pd.read_csv(
#             '/Users/maxvonborch/Documents/Master_Thesis/Django/dialogue_classifier/ml_model/files/clean_labelled_features.csv')
#
#         x = dataset.drop(["Label"], axis=1)
#         y = dataset["Label"]
#         #x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
#         lg = LogisticRegression(solver="liblinear", max_iter=10000, C=10)
#         lg.fit(x, y)
#         model_name = "lg"
#         path = os.path.join((settings.MODEL_ROOT, model_name))
#         with open(path, 'wb') as file:
#             pickle.dump(lg, file)
#         return Response(status=status.HTTP_200_OK)
#
#
# class Predict(views.APIView):
#     def post(self, request):
#         predictions = []
#         for entry in request.data:
#             model_name = entry.pop('model_name')
#             path = os.path.join(settings.MODEL_ROOT, model_name)
#             with open(path, 'rb')

def train_logistic_regression():
    dataset = pd.read_csv(
        '/Users/maxvonborch/Documents/Master_Thesis/Django/test_data/test.csv')
    dataset = dataset.drop(["Words", "Duration", "Number of Speakers", "Conversation"], axis=1)
    x = dataset.drop(["Label"], axis=1)
    y = dataset["Label"]
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    lg = LogisticRegression(solver="liblinear", max_iter=10000, C=10)
    lg.fit(x, y)
    model_name = "lg1"
    path = f'/Users/maxvonborch/Documents/Master_Thesis/Django/dialogue_classifier/models/{model_name}'
    with open(path, 'wb') as file:
        pickle.dump(lg, file)


def train_voting_ensemble():
    dataset = pd.read_csv(
        '/Users/maxvonborch/Documents/Master_Thesis/Django/test_data/test.csv')
    dataset = dataset.drop(["Words", "Duration", "Number of Speakers", "Conversation"], axis=1)
    x = dataset.drop(["Label"], axis=1)
    y = dataset["Label"]
    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    clf1 = LogisticRegression(solver="liblinear", max_iter=10000, C=10)
    clf2 = tree.DecisionTreeClassifier(random_state=42, max_depth=4, min_samples_split=0.6, min_samples_leaf=0.1,
                                       max_features=3)
    clf3 = RandomForestClassifier(n_jobs=-1, random_state=42, n_estimators=200, max_depth=15, min_samples_split=0.1,
                                  min_samples_leaf=0.1, max_features=3)
    clf4 = SVC(gamma='auto', kernel="linear", C=10, random_state=42, probability=True)

    ve = VotingClassifier(estimators=[("lr", clf1), ("dt", clf2), ("rf", clf3), ("svm", clf4)], voting="soft")
    ve.fit(x, y)

    model_name = "votingensemble1"
    path = f'/Users/maxvonborch/Documents/Master_Thesis/Django/dialogue_classifier/models/{model_name}'
    with open(path, 'wb') as file:
        pickle.dump(ve, file)


train_voting_ensemble()
