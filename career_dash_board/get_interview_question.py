# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 17:03:03 2022

@author: watercross
"""
import pandas as pd
from datetime import datetime
import warnings

def get_interview_question(selected_company_name, selected_year):
    google_df = pd.read_csv('./data_source/google.csv')
    amazon_df = pd.read_csv('./data_source/amazon.csv')
    meta_df = pd.read_csv('./data_source/meta.csv')
    microsoft_df = pd.read_csv('./data_source/microsoft.csv')

    interview_merge = google_df.append(amazon_df)

    interview_merge = interview_merge.append(meta_df)

    interview_merge = interview_merge.append(microsoft_df)

    interview_merge['d'] = pd.to_datetime(interview_merge['date'])
    interview_merge['y'] = interview_merge['d'].dt.year
    # print(interview_merge['y'])
    include = interview_merge[interview_merge['y'] == int(selected_year)]

    if len(include.index) > 0:
        i = 0
        for q in include['question']:
            print(str(i) + ". " + q + '\n')
            i += 1
    else:
        print("There are no records in the database.")