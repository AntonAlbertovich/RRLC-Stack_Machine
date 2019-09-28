import praw
import random
import socket
import sys
from praw.models import MoreComments
import multiprocessing
from multiprocessing import Process
import time
import os
import pickle

def parse_context(text):
    import spacy
    spacy.prefer_gpu()
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    return_out = [text]
    for token in doc:

        if token.dep_ != "punct":
            
            return_out.append(token.pos_)
    
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
        return_out.append(parse_context(sentence.text))
        

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

def orginize(template, final_out):
    return_out = final_out
    for i in range(len(template)):
        if final_out[i][0][0][0] == template[i][0]:
            continue 
        else:
            for j in range(len(template)):
                if final_out[i][0][0][0] == template[j][0]:
                    return_out[j] = final_out[i]
                    break

                elif len(final_out[i][0][0][0]) < len(template[j][0]):
                    candidate = True
                    for k in range(len(final_out[i][0][0][0])):

                        if final_out[i][0][0][0][k] != template[j][0][k]:
                            candidate = False
                            break
                    if candidate == True:
                        return_out[j] = final_out[i]
                        break
    return return_out           

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
                
                in_sec = []
                
                for j in range(0, 4):
                    
                    sub_sec = input_array[i+j]
                    in_sec.append(sub_sec)
                    p = multiprocessing.Process(target=thread_1, args=(sub_sec, i+j, return_dict))
                    
                    jobs.append(p)
                    p.start()
                
                for proc in jobs:
                    proc.join()
                
                final_out = return_dict.values()
                
                
                parsed_out.append(final_out[0])
                parsed_out.append(final_out[1])
                parsed_out.append(final_out[2])
                parsed_out.append(final_out[3])




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


    
    for i in range(len(super_array)):
        print("0000", len(super_array[i]))
                
        print(super_array[i])

    
    out_data = multi_parse(super_array)
    
    #output_file= open("add_data.bin", "wb")
    #pickle.dump(Tasks, output_file)
    #output_file.close()
    Additions =[]
    print(len(super_array))
    print(len(out_data))
    
   
    for i in range(len(out_data)):
        print(".")

        print(out_data[i])

