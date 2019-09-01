#!/usr/bin/env python
# coding: utf-8

# In[4]:


def get_all(s, beg_tag, end_tag):
    out_list=[]
    while s.find(beg_tag)!=-1:
        beg=s.find(beg_tag)
        end=s.find(end_tag,beg+len(beg_tag))
        text=s[beg+len(beg_tag):end]
        out_list.append(text)
        s = s[end+1:]
        
    return out_list


# In[5]:


def remove_between(s, beg_tag, end_tag):
    while s.find(beg_tag)!=-1:
        beg=s.find(beg_tag)
        end=s.find(end_tag,beg+len(beg_tag))
        s = s[:beg]+s[end+1:]
        
    return s


# In[6]:


import requests
 
rubric_list={"Россия":"/russia/society",
             "Мир":"/world/politic",
             "Экономика":"/economics/companies",
             "Силовые структуры":"/forces/violation",
             "Наука и техника":"/science/science",
             "Культура":"/culture/kino",
             "Спорт":"/sport/football",
             "Интернет и СМИ":"/media/internet",
             "Путешествия":"/travel/world"}
rubric_common="https://lenta.ru/rubrics"
base_address="https://lenta.ru"

rubric_freq_20={}

for rubric in rubric_list.keys() :
    r = requests.get(rubric_common+rubric_list[rubric])
    links=[]
    dates=[31,30,29,28]
    for d in dates:
        s = r.text
        beg_tag=str(d)+" августа</div><h4><a href=\""
#        beg_tag="</div><h4><a href=\""
        end_tag="\""

        links+=get_all(s,beg_tag,end_tag)

    articles=[]
    for l in links:
        r_link = requests.get(base_address+l)
        article_text_list = get_all(r_link.text,"<p>","</p>")
        article_text = ""
        for s in article_text_list:
            article_text += s

        article_text_clean = remove_between(article_text,"<",">")
        article_text_clean = article_text_clean.replace(","," ")
        article_text_clean = article_text_clean.replace("."," ")

        articles.append(article_text_clean)

    total_text=[]
    for a in articles:
        a_words = [s for s in a.split(" ")]
        total_text+=a_words

    freq_dict={}
    for w in total_text:
        if w in freq_dict.keys():
            freq_dict[w]+=1
        elif (len(w)>3):
            freq_dict[w]=1
            
    freqs=[]
    for w in freq_dict.keys():
        if freq_dict[w] not in freqs:
            freqs.append(freq_dict[w])
    freqs.sort(reverse=True)

    freq_words={}
    for w in freq_dict.keys():
        if freq_dict[w] in freq_words:
            freq_words[freq_dict[w]].append(w)
        else:
            freq_words[freq_dict[w]]=[w]

    out_list=[]
    for f in freqs:
        for w in freq_words[f]:
            out_list.append([w,f])

    out_list_20 = out_list[0:20]
    rubric_freq_20[rubric]=out_list_20
    
print(rubric_freq_20)


# In[7]:


import csv
import os

for rubric_name in rubric_freq_20.keys():
    path = os.path.join("C:\\Alex\\Lenta",rubric_name+".csv")
    print(path)
    with open(path, mode='w') as csv_file:
        fieldnames = ['word', 'frequency']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for l in rubric_freq_20[rubric_name]:
            writer.writerow({'word': l[0], 'frequency': l[1]})


# In[ ]:




