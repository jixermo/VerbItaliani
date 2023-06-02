# -*- coding: utf-8 -*-
"""
Created on Jun 21 08:30:20 2022

@author: jixermo
"""

import requests
from bs4 import BeautifulSoup, element
from random import randrange

def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)


def open_html(path):
    with open(path, 'rb') as f:
        return f.read()      


def compare(x,y):
    n=0
    x=x.replace(" ", "")
    y=y.replace(" ", "")
   #Function to compare the inserted and correct verbs        
    if(y==x):
        n=1
    elif(y.find('\'/')!=-1):
        p=y.find('\'/')
        y1=y[:p+1]
        y2=y[p+2:]
        if(y1==x or y2==x):
            n=1
    return n


sel=["Presente","Passato Prossimo","Imperfetto","Trapassato Prossimo",\
     "Passato Remoto","Trapassato remoto","Futuro Semplice","Futuro Anteriore",\
     "Condizionale Presente","Condizionale Passato",\
     "Congiuntivo Presente","Congiuntivo Passato","Congiuntivo Imperfetto",\
     "Congiuntivo Trapassato","Imperativo","A Casaccio"]

#Infinte Loop
while (1==1):
	
	#User input the desired verb
	print('Inserisci il verbo desiderato:')
	InputVerbi = input()    
	
	#Loop to obtain a verb that can be found in the database:
	ErrorPage=True
	while (ErrorPage==True):
	    #Request desired verb webpage
	    url='https://www.coniugazione.it/verbo/'+InputVerbi+'.php'
	    r = requests.get(url)
	    save_html(r.content, 'temp')
	    html = open_html('temp')
	    #print(r.content[:100])
	        
	    #Parse html, and check if input is existent in database
	    soup = BeautifulSoup(r.content, 'html.parser')
	    ErrorPage=bool(soup.find(text='Errore : 404    '))
	    if(ErrorPage==True):
	        print('Verbi non trovato, inserisci un verbi di nuovo:')
	        InputVerbi = input()    
	
	#Extract Table using divs tempscorps class tag: 
	divs = soup.findAll("div", {"class": "tempscorps"})
	
	
	#Extract VerbForms from divs:
	VerbForms=[]
	for i in range(len(divs)):
	    temp = list(divs[i].children)
	    VerbForms.append(temp)
	
	for i in range(len(VerbForms)):
	    for j in range(len(VerbForms[i])):
	        if(isinstance(VerbForms[i][j], element.Tag)==True):
	            VerbForms[i][j]=VerbForms[i][j].text
	
	#ONCE DATA OF VERB FORMS OBTAINED, CONTINUE WITH OTHER INPUTS:
	    
	#User input desired verb form
	Selection=0
	print('\nSeleziona la forma del verbo:')
	while (Selection<1 or Selection>16):
	    for i in range(len(sel)):
	        print(str(i+1)+'. '+ sel[i])
	    Selection = input()
	    Selection=int(Selection)
	    if(Selection>0 and Selection<16):
	        print('Hai selezionato il '+sel[Selection-1])
	    elif(Selection==16):
	        Selection=randrange(1,15)
	        print('È stato selezionato il '+sel[Selection-1])
	    else:
	        print("Non hai selezionato un numero adatto, inserisci di nuovo (1-16):")
	
	#User inputs verb forms:
	if(Selection>=11 and Selection<=14): #For congiuntivo
	    print('che io:')
	    io="che io "+input()
	    print('che tu:')
	    tu='che tu '+input()
	    print('che lui:')
	    lui='che lui '+input()
	    print('che noi:')
	    noi='che noi '+input()
	    print('che voi:')
	    voi='che voi '+input()
	    print('che loro:')
	    loro='che loro '+input()
	elif(Selection==15): #For Imperativo
	    io='-'
	    print('tu:')
	    tu=input()
	    print('lui:')
	    lui=input()
	    print('noi:')
	    noi=input()
	    print('voi:')
	    voi=input()
	    print('loro:')
	    loro=input()
	else:
	    print('io:')
	    io='io '+input()
	    print('tu:')
	    tu='tu '+input()
	    print('lui:')
	    lui='lui '+input()
	    print('noi:')
	    noi='noi '+input()
	    print('voi:')
	    voi='voi '+input()
	    print('loro:')
	    loro='loro '+input()
	    
	n=0
	#InputForms list of coniugazione
	InputForms=[io,tu,lui,noi,voi,loro]
	
	#Obtain correct verb forms:
	CorrectVerbs=['Null']*6
	if(Selection!=15):
	    n=Selection-1
	    for i in range(6):
	        CorrectVerbs[i]=VerbForms[n][0+3*i]+VerbForms[n][1+3*i]
	elif(Selection==15):
	    n=Selection-1
	    #If imperativo table length is more than 12, combine the rows to correct the table
	    #If not, then proceed as usual
	    if(len(VerbForms[n])>12):
	        temp=[]
	        for k in range(5):
	            join="".join(VerbForms[n][2+3*k:4+3*k])
	            temp.append(join)
	            CorrectVerbs=VerbForms[n][:1]+temp
	    else:
	        for i in range(6):
	            CorrectVerbs[i]=VerbForms[n][0+2*i]
	        
	#print(CorrectVerbs)
	            
	# Creates a list containing 5 lists, each of 8 items, all set to 0
	w, h = 3, 6
	Result = [["-1" for x in range(w)] for y in range(h)] 
	#Compare the values
	s=[-1]*6
	for j in range(6):        
	    s[j]=compare(InputForms[j],CorrectVerbs[j])
	    Result[j][0]=InputForms[j]
	    Result[j][1]=CorrectVerbs[j]
	    if(s[j]==0):
	        Result[j][2]='X'
	    elif(s[j]==1):
	        Result[j][2]=' '
	        
	#Print/tabulate
	formatted_row = '{:<20} {:<20} {:>6}'
	print(formatted_row.format("Risposte", "Soluzioni", "Sbagli"))
	
	for Row in Result:
	    print(formatted_row.format(*Row))
