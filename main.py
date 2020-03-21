import os
from tkinter import * 
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
import re
from nltk.stem import PorterStemmer
import time

def creatinvertedindex():
    stemming=PorterStemmer()
    dict={}
    path = os.getcwd()
    files=os.listdir(path+"\Trump Speechs")
    qq=re.compile('\W+')
    y=re.compile("\d+")
    global filelist
    filelist=[]
    for f in files:
        fname=path+"\Trump Speechs\\"
        fname+=f
        lines=open(fname,"r")
        next(lines)
        wordslist=lines.read()
        x=qq.split(wordslist)
        name=y.findall(f)
        name=int(name[0])
        for i in x:
            i=stemming.stem(i)
            if i not in dict:
                dict[i]=[]
                dict[i].append(name)
            else:
                if name not in dict[i]:
                    dict[i].append(name)
        lines.close()
        filelist.append(name)
        fname=""
        
    fo=open("StopwordList.txt")
    x=fo.read()
    listt=x.split()
    for i in listt:
        if i in dict:
            del dict[i]

    wordfile=open("invertedindex.txt","w")
    for x,y in dict.items():
        wordfile.write(str(x)+" "+str(y)+'\n')
    wordfile.close()
    return dict
    
def booleanquery(queryy,dict):
    stemming=PorterStemmer()
    dict=dict
    query=queryy
    x=query.split()
    q=[]
    for i in x:
        if i!="AND" and i!="OR" and i!="NOT":
            q.append(stemming.stem(i))
        else:
            q.append(i)
            
    result=[]
    def operation():
        global result
        operator=operatorstack.pop()
        if operator=="AND":
            x=operandstack.pop()
            y=operandstack.pop()
            r=(list(set(x) & set(y)))
            operandstack.append(r)

        elif operator=="OR":
            x=operandstack.pop()
            y=operandstack.pop()
            r=(list(set(x) | set(y)))
            operandstack.append(r)
            
        elif operator=="NOT":
            x=operandstack.pop()
            r=(list(set(filelist) - set(x)))
            operandstack.append(r)

        return
    
    operatorstack=[]
    operandstack=[]
    flag=0
    while q:
        x=q.pop(0)
        if x=="AND":
            if operatorstack:
                while operatorstack[-1] > x:
                    operation()
            operatorstack.append(x)
        elif x=="OR":
            if operatorstack:
                while operatorstack[-1] > x:
                    operation()
            operatorstack.append(x)
        elif x=="NOT":
            operatorstack.append(x)
        elif x=="(":
            operatorstack.append(x)
        elif x==")":
            while operatorstack[-1]!="(":
                operation()
            operatorstack.pop()
        elif x!="AND" and x!="OR" and x!="NOT"  and x!="(" and x!=")":
            if x in dict:
                operandstack.append(dict[x])
            elif x not in dict:
                blanklist=[]
                operandstack.append(blanklist)
    while operatorstack:
        operation()
            
    return operandstack[0]

def createpositionalindex():
    stemming=PorterStemmer()
    dict={}
    path = os.getcwd()
    files=os.listdir(path +"\Trump Speechs")
    qq=re.compile('\W+')
    y=re.compile("\d+")
    for f in files:
        fname=path+"\Trump Speechs\\"
        fname+=f
        lines=open(fname,"r")
        next(lines)
        wordslist=lines.read()
        x=qq.split(wordslist)
        name=y.findall(f)
        name=int(name[0])
        j=0
        for i in x:
            i=stemming.stem(i)
            if i not in dict:
                dict[i]={}
                dict[i][name]=[]
                dict[i][name].append(j)
            else:
                if name not in dict[i]:
                    dict[i][name]=[]
                    dict[i][name].append(j)
                elif name in dict[i]:
                    dict[i][name].append(j)
            j+=1
        lines.close()
        fname=""
        
    fo=open("StopwordList.txt")
    x=fo.read()
    listt=x.split()
    for i in listt:
        if i in dict:
            del dict[i]

    wordfile=open("positionalindexfile.txt","w")
    for x,y in dict.items():
        wordfile.write(str(x)+" "+str(y)+'\n')
    wordfile.close()
    return dict

def positionalquery(queryy,dict):
    stemming=PorterStemmer()
    query=queryy
    x=query.split()
    q=[]
    distance=0
    checkquery=0
    # distflag=False
    for i in x:
        checkquery+=1
        if i.startswith("/"):
            dist=re.sub("/","",i)
            try:
                distance=int(dist)
                x.pop()
                # distflag=True
            except:
                print("distance is not given")
                sys.exit()
        else:
            q.append(stemming.stem(i))    
    # if  len(q)!=2:
    #     print("************* Error in query! ***************")
    #     print("Query must be of the form : word1 word2 /distance(in int) ")
    #     sys.exit()
    # elif distflag==False and len(q)!=2:
    #     print("************* Error in query! ***************")
    #     print("Query must be of the form : word1 word2 /distance(in int) ")
    #     sys.exit()

    l1=[]
    l2=[]
    var=0
    list1ofdoc=[]
    for i in q:
        if var==0:
            for x in dict[i]:
                l1.append(x)
        elif var==1:
            for x in dict[i]:
                l2.append(x)
        var=var+1

    list1ofdoc=list(set(l1) & set(l2))
    finallist=[]

    for i in list1ofdoc:
        ll1=dict[q[0]][i].copy()
        ll2=dict[q[1]][i].copy()
        ll1.sort()
        ll2.sort()
        x=0
        y=0
        while ll1 and ll2:
            if ll1[x]>ll2[y]:
                d=ll1[x]-ll2[y]-1
                if d==distance:
                    finallist.append(i)
                    break
                ll2.pop(0)
            elif ll2[y]>ll1[x]:
                d=ll2[y]-ll1[x]-1
                if d==distance:
                    finallist.append(i)
                    break
                ll1.pop(0)
            elif ll1[x]==ll2[y]:
                if distance==0:
                    finallist.append(i)
                    break
                ll2.pop(0)
                ll1.pop(0)

    return finallist

def checktypeofQuery(q):
    x=q.split()
    for i in x:
        if i == "AND" or i=="OR" or i=="NOT":
            return "B"
        if i.startswith("/"):
            return "p"
    if len(x)==1:
        return "B"
    elif len(x)==2:
        return "p"    
    return "error"
    

invertndex=creatinvertedindex()
positionalindex=createpositionalindex()
def searchquery():
    t0=time.time()
    strr=entry.get()
    global answer_value
    answer.delete(1.0,END)
    c=checktypeofQuery(strr)
    if c=="B":
        answer_value=booleanquery(strr,invertndex)
    elif c=="p":
        answer_value=positionalquery(strr,positionalindex)
    elif c=="error":
        messagebox.showerror("QUERY ERROR", "For Positional Query : Query must be of the form : word1 word2 /distance(in int) \n For Boolean Query (AND OR NOT must be in caps, every word must be seperated by a space) :")
    t1=time.time()
    for i in answer_value:
        answer.insert(END,'Speech_')
        answer.insert(END,i)
        answer.insert(END,'\n')
    
    finaltime=t1-t0
    ft="{0:.8f}".format(finaltime)
    r.delete(1.0,END)
    r.insert(END,"About "+str(len(answer_value)) +" result(s)  ("+str(ft)+" seconds)")
    answer.pack()

def showinformation():
    messagebox.showinfo("HELP","For Positional Query : Query must be of the form : word1 word2 /distance(in int) \n For Boolean Query (AND OR NOT must be in caps, every word must be seperated by a space) :")
    
root=tk.Tk() 
root.geometry("900x700")
root.resizable(0,0)
root.title("Retrieve Information")
root.configure(background="steel blue")
canvas=Canvas(root,width=900, height=246)
path = os.getcwd()
image=ImageTk.PhotoImage(Image.open(path+"/bgg.jpg"))
canvas.create_image(0,0,anchor=NW, image=image)
canvas.pack()

topframe=Frame(root, borderwidth=2)
entry=Entry(topframe,justify=CENTER,width=65,bd=10,font=("Arial",12,"bold"))
entry.pack(side=LEFT)
button=Button(topframe,text="SEARCH", command=searchquery,width=10,bd=4, font=("Arial",12,"bold"))
button.pack(side=RIGHT)
img=ImageTk.PhotoImage(Image.open(path+"/info.png"))
info=Button(topframe,image=img, command=showinformation,width=25, bd=3)
info.pack(side=RIGHT)
topframe.pack(side=TOP,pady=20)

bottomframe=Frame(root)
r=Text(bottomframe,width = 100,height=1, font=("Helvetica", 15, "bold", "italic"), bg="steel blue",bd=0,insertborderwidth=0,fg="white")
r.pack( side=TOP )
scroll=Scrollbar(bottomframe)
scroll.pack(side=RIGHT,fill=Y)
answer=Text(bottomframe,yscrollcommand=scroll.set,insertborderwidth=3, bd=5,width = 40, height=4, font=("Helvetica", 15, "bold"))
scroll.config(command=answer.yview)
answer.pack(expand=TRUE, fill=BOTH )
bottomframe.pack(side=BOTTOM, fill=BOTH, expand=TRUE,pady=20, padx=55)
l1=Label()

root.mainloop()