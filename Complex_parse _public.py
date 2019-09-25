import praw
import random
import socket
import sys
from praw.models import MoreComments
import multiprocessing
from multiprocessing import Process
import time
import os


def parse_context(text):
    import spacy
    spacy.prefer_gpu()
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    return_out = []
    for token in doc:
        context = []
        context.append(token.text)
        context.append(token.lemma_)
        context.append(token.tag_)
        context.append(token.pos_)
        context.append(token.dep_)
        return_out.append(context)

    return return_out

    
def parse_sentence(text):
    import spacy
    import re
    spacy.prefer_gpu()
    nlp = spacy.load('en')
    boundary = re.compile('^[0-9]$')

    def custom_seg(doc):
        prev = doc[0].text
        length = len(doc)
        for index, token in enumerate(doc):
            if (token.text == '.' and boundary.match(prev) and index!=(length - 1)):
                doc[index+1].sent_start = False
            prev = token.text
        return doc

    nlp.add_pipe(custom_seg, before='parser')

    doc = nlp(text)

    return_out = [] 

    for sentence in doc.sents:
        return_part = []
        return_part.append(sentence.text)
        return_part.append(parse_context(sentence.text))
        
        return_out.append(return_part)

    return return_out

def recursive_call(input_array):
    return_out = []
    return_out.append(parse_sentence(input_array[0]))
    if len(input_array) > 1:
        for i in range(len(input_array[1])):
            return_out.append(recursive_call(input_array[1][i]))
        return return_out
    else:
        return return_out


def thread_1(input_array, position, return_out):
    return_out[position] = recursive_call(input_array)

def Reverse(lst):
    lst.reverse()
    return lst

def multi_parse(input_array):
    
    parsed_out = []
    a_number = len(input_array) 

    print("for :", a_number)

    if a_number%4 == 0:

        for i in range(0, a_number, 4):

            if __name__=='__main__':
                manager = multiprocessing.Manager()
                return_dict = manager.dict()
                jobs = []
                for j in range(0, 4):
                    
                    sub_sec = input_array[i+j]
                    p = multiprocessing.Process(target=thread_1, args=(sub_sec, i+j, return_dict))
                    
                    jobs.append(p)
                    p.start()
                
                for proc in jobs:
                    proc.join()
                
                final_out = return_dict.values()
                parsed_out.append(Reverse(final_out))
                




    elif a_number < 4:

        for i in range(0, a_number):
            if __name__=='__main__':
                manager = multiprocessing.Manager()
                return_dict = manager.dict()
                jobs = []
                for j in range(0, a_number):
                    
                    sub_sec = input_array[i+j]
                    p = multiprocessing.Process(target=thread_1, args=(sub_sec, i+j, return_dict))
                    
                    jobs.append(p)
                    p.start()
                
                for proc in jobs:
                    proc.join()
                
                final_out = return_dict.values()
                parsed_out.append(Reverse(final_out))

    else:
        
        sub_range = a_number - a_number%4 
    
        for i in range(0, sub_range, 4):

            if __name__=='__main__':
                manager = multiprocessing.Manager()
                return_dict = manager.dict()
                jobs = []
                for j in range(0, 4):
                    
                    sub_sec = input_array[i+j]
                    p = multiprocessing.Process(target=thread_1, args=(sub_sec, i+j, return_dict))
                    
                    jobs.append(p)
                    p.start()
                
                for proc in jobs:
                    proc.join()
                
                final_out = return_dict.values()
                parsed_out.append(Reverse(final_out))
        
        for i in range(sub_range, a_number):
            if __name__=='__main__':
                manager = multiprocessing.Manager()
                return_dict = manager.dict()
                jobs = []
                for j in range(0, a_number%4):
                    
                    sub_sec = input_array[i+j]
                    p = multiprocessing.Process(target=thread_1, args=(sub_sec, i+j, return_dict))
                    
                    jobs.append(p)
                    p.start()
                
                for proc in jobs:
                    proc.join()
                
                final_out = return_dict.values()
                parsed_out.append(Reverse(final_out))


    print(parsed_out)
    return parsed_out




print(reddit.user.me())
subreddit = reddit.subreddit('Gundam')
top_subreddit = subreddit.top()


def telescope_comments(this_level):
    return_out = []
    out_children = []
    return_out.append(this_level.body)
    for next_level in this_level.replies:
        out_children.append(telescope_comments(next_level))
    return_out.append(out_children)
    return return_out


super_array = []

for submission in subreddit.top(limit=1):
    print(submission.title)
    print("--------------")
    print(submission.id)
    print("--------------")
    #print(submission.selftext)

    submission.comments.replace_more(limit=None)
    for top_level_comment in submission.comments:
        super_array.append(telescope_comments(top_level_comment))

    multi_parse(super_array)



