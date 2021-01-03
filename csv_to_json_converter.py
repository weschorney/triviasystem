# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 17:22:23 2021

@author: wes_c
"""

import pandas as pd
import json

def csv_to_json(row):
    question = dict()
    question['question_text'] = row['question_text']
    answers = []
    for letter in ['A', 'B', 'C', 'D']:
        answers.append(letter + ': ' + row[letter] + '\n')
    question['answers'] = answers
    question['correct_answer'] = row['correct_answer']
    question['tier'] = row['tier']
    question['is_asked'] = row['is_asked']
    return question

def question_csv_to_json(csv_path, output_path='setup.json'):
    df = pd.read_csv(csv_path)
    assert all(ele in df.columns for ele in ['question_text', 'A', 'B',\
                                             'C', 'D', 'correct_answer',
                                             'tier', 'is_asked']),\
    "CSV file has incorrect columns."
    questions = []
    for _, row in df.iterrows():
        questions.append(csv_to_json(row))
    json_dict = dict()
    json_dict['participants'] = []
    json_dict['questions'] = questions
    with open(output_path, 'w') as f:
        json.dump(json_dict, f)
    return
