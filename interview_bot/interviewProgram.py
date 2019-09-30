#!/usr/bin/env python3

import speech_recognition as sr
from os import system
import random
import nltk
import time
from tkinter import *
import tkinter as tk
import sys
from Detect_Topic.naive_bayes_classifer import classify_topic
from Check_Semantic_Similarity.sentence_similarity import find_similarity
from utils import record_convo
import pickle
import spacy


nlp = spacy.load('en_core_web_md')

#load model
with open('./Detect_Topic/nb_classifier.pkl', 'rb') as f:
    clf = pickle.load(f)
with open('./Detect_Topic/count_vect.pkl', 'rb') as f:
    count_vect = pickle.load(f)


introduction = ['Tell me about yourself.',
'Please introduce yourself.',
'Tell me what motivates you about tech.',]

projects = ['can you please brief me about your contribution in {}',
'Please explain what you did in the project named {}',
'Your project seems intersting. Can you please explain about {}',
'If you had to choose one project to explain, which one would it be? And why?',
'Okay, Let us move our focus to your porject named {}',
'I shall now ask you some questions related to your project {} . Can you tell me about it in brief.',
'What did you learn in the course of your project {}'
]

expertise = ['I see you have mentioned {} as your strength. Can you please explain why?',
'How well are you versed in {}',
'Now comes the intersting part. Tell me about your knowledge in {}',
'What have you worked with in {}',
'You have mentioned {} in your strong fields. Why do we use that?']

#list of default questions
defaultQuestions = ['Can you tell me one important project you have done?',
 'I assume you know about basic OOP. What do you think about object oriented programming?',
 'Can you explain how memory is managed inside a modern computer?']



take_input = True


def voice_out(questionData,root):

	global ShowTextFrame
	global QuestionsAsked
	ShowTextFrame = Frame(root,background = 'black')
	ShowTextFrame.grid(row=10 , column=0)
	#cleardata = "                                                                                                                                                                               "

	clear_data = " "*80

	name1 = Label(ShowTextFrame,text=clear_data,background = 'black',fg = 'white')
	name1.grid(row=2,column = 1,padx=100, pady=30)

	name1 = Label(ShowTextFrame,text=questionData,background = 'black',fg = 'white')
	name1.grid(row=2,column = 1,padx=100, pady=30)
	
	system('say %s' % (questionData))

	#ShowTextFrame.grid_forget()
	QuestionsAsked += 1 
	return ShowTextFrame


with open('./Questions/hardware.txt','r') as pyfi:
	hardwarelist = pyfi.readlines()
with open('./Questions/data_science.txt','r') as cfi:
	data_sciencelist = cfi.readlines()
with open('./Questions/web_dev.txt','r') as algofi:
	web_devlist = algofi.readlines()

with open('./Answers/hardware.txt','r') as pyfi:
	ans_hardwarelist = pyfi.readlines()
with open('./Answers/data_science.txt','r') as cfi:
	ans_data_sciencelist = cfi.readlines()
with open('./Answers/web_dev.txt','r') as algofi:
	ans_web_devlist = algofi.readlines()

# 'Hardware' 'Data Science' 'Data Science' 'Web Development'
def ask_topic(topic):
	print (topic)
	
	if topic == 'Hardware':
		ask_id =  random.randint(0,len(hardwarelist)-1)
		question = hardwarelist[ask_id]
		answer = ans_hardwarelist[ask_id]
		hardwarelist.remove(question)
		ans_hardwarelist.remove(answer)
		return (question,answer,1,)


	if topic == 'Data Science':
		ask_id =  random.randint(0,len(data_sciencelist)-1)
		question = data_sciencelist[ask_id]
		answer = ans_data_sciencelist[ask_id]
		data_sciencelist.remove(question)
		ans_data_sciencelist.remove(answer)
		return (question,answer,1,)

	if topic == 'Web Development':
		ask_id =  random.randint(0,len(web_devlist)-1)
		question = web_devlist[ask_id]
		answer = ans_web_devlist[ask_id]
		web_devlist.remove(question)
		ans_web_devlist.remove(answer)
		return (question,answer,1,)

def counter():
    if 'cnt' not in counter.__dict__:
        counter.cnt = 0
    counter.cnt += 1
    return counter.cnt


def process_input(user_input):
	counter()
	if (counter.cnt < 2):
		choosevaal = [1,2]
		cho = random.choice(choosevaal)
		if cho == 1 and len(ProgrammingLanguages) != 0:
			sent = random.choice(expertise)
			expertise.remove(sent)
			opt = random.choice(ProgrammingLanguages)
			return (sent.format(opt),"",0,)
		elif len(knowledgeStack) != 0:
			sent = random.choice(projects)
			projects.remove(sent)
			opt = random.choice(knowledgeStack)
			return (sent.format(opt),"",0,)
	else:
		topics = (classify_topic(user_input,count_vect,clf))
		return (ask_topic(topics[0]))
		
#Get small quantum packets of input which we will treat as small sentences
def getQuantumInput():
	r = sr.Recognizer()
	r.pause_threshold = 0.2
	r.phrase_threshold = 0.1
	r.non_speaking_duration = 0.1
	with sr.Microphone() as source:
		try:
			audio = r.listen(source, timeout = 4)
			return audio
		except sr.WaitTimeoutError:
			print("Timed out")
			return None


# get audio from the microphone
def get_input(questionData,ShowTextFrame):
	r = sr.Recognizer()
	InputList = []
	print(questionData)
	ShowTextFrame =  voice_out(questionData,ShowTextFrame)
	while(True):
		quantumInput = getQuantumInput() #call this for getting small sentences
		if (quantumInput == None): #if more than 5 sec pause in candidate answer then end answer
			print("Processing...")
			ShowTextFrame.grid_forget()
			return InputList
		InputList.append(quantumInput)



def getTextInput(questionData,ShowTextFrame):
	
	# r = sr.Recognizer()
	# TextList = []
	# AudioList = []
	# AudioList = get_input(questionData,ShowTextFrame)
	# #print("Got all audio inputs")
	# print(AudioList)
	# for recordedAudio in AudioList:
	# 	TextSnippet = r.recognize_google(recordedAudio)
	# 	print("-" , TextSnippet)
	# 	TextList.append(TextSnippet)
	# #print(TextList)
	# return TextList

	ShowTextFrame =  voice_out(questionData,ShowTextFrame)
	text_ip = sys.stdin.readline() 
	TextList = nltk.sent_tokenize(text_ip)
	return TextList



####################
#### MAIN MODULE ###
####################


QuestionsAsked = 0
def startInterview(ShowTextFrame,name,cpi,project1,project2,project3,programmingLanguages,POR1,POR2,POR3): 
	proposedQuestion = "I am Sid, your virtual questioner. " + random.choice(introduction)

	
	global QuestionsAsked
	global knowledgeStack
	knowledgeStack = []

	global Name, Number_of_Questions ,Project1, Project2, Project3
	global ProgrammingLanguages

	ProgrammingLanguages = []

	Name = name
	Number_of_Questions = cpi
	Project1 = project1
	Project2 = project2
	Project3 = project3

	print ("Number of Questions: ",Number_of_Questions)
	knowledgeStack.append(project1)
	knowledgeStack.append(project2)

	for i in programmingLanguages.split(','):
		#knowledgeStack.append(i)
		ProgrammingLanguages.append(i)

	print(knowledgeStack)

	user_input = ["Hello"]

	if Number_of_Questions.lower() == 'easy':
		number_of_Quest = 6
	elif Number_of_Questions.lower() == 'medium':
		number_of_Quest = 8
	elif Number_of_Questions.lower() == 'tough':
		number_of_Quest = 10
	else:
		number_of_Quest = 5



	questionData = proposedQuestion
	sampleAnswer = ""
	answer_avail_flag = 0
	while(QuestionsAsked < number_of_Quest):
		try:
			questionData = proposedQuestion
			user_input =  getTextInput(questionData,ShowTextFrame)
			score = 0
			if(answer_avail_flag):
				score = find_similarity(sampleAnswer,user_input,nlp)
				print("#"*30)
				print("Answer matching index: ",score)
				print("#"*30)
			record_convo(questionData,user_input[0], sampleAnswer, score)
			proposedQuestion, sampleAnswer, answer_avail_flag = process_input(user_input)
			#system(user_input)
    		#user_input = r.recognize_google(audio)
    		#process_input(user_input)

		except sr.UnknownValueError:
			print("Could not understand audio")
			if len(user_input) != 0:
				proposedQuestion = process_input(user_input)

		except sr.RequestError as e:
			print("Could not request results; {0}".format(e))
		try:
			ShowTextFrame.grid_forget()
		except Exception as e:
			pass

	final = "Well Thank You "+ name +". Your interview has concluded." 
	voice_out(final,ShowTextFrame)
	return

