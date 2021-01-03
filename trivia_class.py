# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 14:37:08 2021

@author: wes_c
"""

import random
import json
from participant_class import Participant

class Trivia:
    def __init__(self, setup_file, start_tier=2):
        self.setup = json.load(open(setup_file))
        self.participants = []
        self.questions = []
        self.n_tiers = None
        self.start_tier = start_tier
        self.kill_signal = False

    @staticmethod
    def random_list_ele(lst):
        idx = random.sample(list(range(len(lst))), 1)
        return lst[idx[0]]

    def get_questions(self):
        self.questions = self.setup['questions']
        self.n_tiers = max(question['tier'] for question in self.questions)
        print(f"Successfully added {len(self.questions)} questions.")
        print(f"Max question tier is {self.n_tiers}.")
        return

    def get_participants(self):
        if self.n_tiers is None:
            print("Must use get_questions method first to get n_tiers")
            return
        else:
            for participant in self.setup['participants']:
                self.participants.append(Participant(participant, self.n_tiers,
                                                start_tier=self.start_tier))
            print(f"Successfully added {len(self.participants)} participants.")
            return

    def answer_question(self, question, answer, participant):
        if answer == 'finish':
            self.kill_signal = True
            return
        else:
            participant.answer_question(question, answer)
            question['is_asked'] = True
        return

    @staticmethod
    def ask_question(question, participant):
        print(f"The next question is for {participant.name}.\n")
        print(question['question_text'], '\n')
        for answer in question['answers']:
            print(answer)
        return

    def get_question(self, participant):
        p_tier = participant.tier
        tier_questions = [question for question in self.questions\
                          if question['tier'] == p_tier and\
                          question['is_asked'] == False]
        if not tier_questions:
            next_best_questions = []
            offset = 1
            while not next_best_questions and offset <= self.n_tiers:
                up_tier = p_tier + offset
                down_tier = p_tier - offset
                next_best_questions = [question for question in self.questions\
                                       if (question['tier'] == up_tier\
                                       or question['tier'] == down_tier)\
                                       and question['is_asked'] == False]
                offset += 1
            if not next_best_questions:
                #no questions left in game
                print("Exhausted questions. Ending Trivia.\n")
                self.kill_signal = True
            else:
                question = self.random_list_ele(next_best_questions)
                return question
        else:
            question = self.random_list_ele(tier_questions)
            return question

    def print_results(self):
        for participant in self.participants:
            print(f"======={participant.name}=======\n")
            for i in range(self.n_tiers):
                print(f"Tier {i} questions asked: ", 
                      f"{participant.correct_record[i]} /",
                      f"{participant.question_record[i]}\n")
        overall = [(participant.name, sum(participant.correct_record))\
                   for participant in self.participants]
        overall.sort(key=lambda x: x[1], reverse=True)
        print("Overall Rankings:")
        for idx, score in enumerate(overall):
            print(f"{idx + 1}. {score[0]}: {score[1]} correct answers.")
        return

    def play_turn(self, turn):
        turn = turn % len(self.participants)
        participant = self.participants[turn]
        question = self.get_question(participant)
        if self.kill_signal == True:
            return
        else:
            self.ask_question(question, participant)
            answer = input("Your answer: ")
            while answer.lower() not in ['a', 'b', 'c', 'd', 'finish']:
                input_str = ''.join(["Whoops, try again. Answer must be A,",
                                     " B, C, D, or finish. "])
                answer = input(input_str)
            answer = answer.lower()
            self.answer_question(question, answer, participant)
            return

    def host_game(self):
        turn = 0
        print("Welcome to Trivia Night!\n")
        self.get_questions()
        self.get_participants()
        print("You can end the trivia at any time by typing 'finish'")
        print("Let's begin.\n")
        print("========================================\n")
        while not self.kill_signal:
            print(f"Turn {turn + 1}\n")
            self.play_turn(turn)
            turn += 1
            print("========================================\n")
        print("Thanks for playing! Here are the results:\n")
        self.print_results()
        input("Press any key to exit.")
        return

if __name__ == '__main__':
    Trivia('setup.json').host_game()
