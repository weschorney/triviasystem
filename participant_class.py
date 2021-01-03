# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 13:27:05 2021

@author: wes_c
"""

class Participant:
    def __init__(self, name, n_tiers, start_tier=2):
        self.name = name
        self.n_tiers = n_tiers
        self.question_record = [0] * n_tiers
        self.correct_record = [0] * n_tiers
        self.tier = start_tier

    def answer_question(self, question, answer):
        #tiers are 1--n, so offset by 1
        self.question_record[question['tier'] - 1] += 1
        if answer.lower() == question['correct_answer'].lower():
            print("\nCorrect!\n")
            self.correct_record[question['tier'] - 1] += 1
            if self.tier < self.n_tiers:
                #increase the tier
                self.tier += 1
        else:
            #decrease the tier
            print("\nIncorrect. The correct",
                  f"answer was {question['correct_answer']}.\n")
            if self.tier > 1:
                self.tier -= 1
        return
