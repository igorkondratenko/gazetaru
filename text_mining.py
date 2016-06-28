import urllib.request as urllib
import datetime
from bs4 import BeautifulSoup as bs
import mysql.connector as sql
import re
import os
import pymorphy2
from stop_words import get_stop_words
from gensim.models.word2vec import Word2Vec


#connection to database
connection = sql.connect(user='root',host='127.0.0.1',database='text_mining')
cursor = connection.cursor()
query_insert_word = "INSERT INTO stats (Word,id_artilce) VALUES (%s,%s)"
query_insert_article = "INSERT INTO articles (name,date_article,processed) VALUES (%s, %s, %s)"
query_change_state_article = "UPDATE articles SET processed = TRUE where name = %s"
query_select_article = "SELECT * FROM articles WHERE name=%s"

#create files
page = "http://www.gazeta.ru/politics/"
for i in range(1,3):
    #break
    print(i)
    links_page = urllib.urlopen(page).read()
    main_soup = bs(links_page,"lxml")
    links = main_soup.findAll("a",href=re.compile('/politics/2016.*html$'))
    string_links = []
    for link in links:
        string_links.append(link['href'])
    string_links = set(string_links)
    for link in string_links:
        page_article = urllib.urlopen("http://www.gazeta.ru"+link).read()
        soup = bs(page_article,"lxml")
        date_time = re.sub(":",".",soup.find("span",{"class":"ml20 date_time"}).text)
        
        header = soup.find("h2",{"class":"h_1 mt5 mb10"})
        file = open("C:/Users/User/Desktop/articles/"+ date_time+" "+header.text+".txt",'w+',encoding='utf-8')
        articles = soup.findAll("p")
        #print("1: "+str(header))
        for article in articles:
            str_artilce = re.sub(r'[^\w\s\.,-]',"",article.text);
            if 'class' in article.attrs:
                if article.attrs["class"][0] not in ["intro","d_2","pb10"]:
                    file.write(str_artilce+"\n")
            else:
                if 'class' in article.parent.attrs:
                    if article.parent.attrs['class'][0] != "bottom_info":
                        file.write(str_artilce+"\n")
        #print ("2: "+str(header))
    #следующая страница
    page = "http://www.gazeta.ru"+main_soup.find("a", {"id": "other_clickA"})['href']

dir = "C:/Users/User/Desktop/articles"
files = os.listdir(dir)

n_files=0
for file in files:
    name_file = re.sub(r'\d{2}\.\d{2}\.\d{4}, \d{2}\.\d{2} ',"",file);
    cursor.execute(query_select_article,(re.sub(".txt","",name_file),))

    flag = False
    for row in cursor:
        flag = True
    
    if not flag:
        data = re.match(r'\d{2}\.\d{2}\.\d{4}, \d{2}\.\d{2}',file);
        d_obj = datetime.datetime.strptime(data.group(0),"%d.%m.%Y, %H.%M")
        cursor.execute(query_insert_article,(re.sub(".txt","",name_file),d_obj,False))
        connection.commit()
        
        cursor.execute(query_select_article,(re.sub(".txt","",name_file),))
        id_article = 0;
        for row in cursor:
            if row[3]==0:
                id_article = row[0]
                open_file = open("C:/Users/User/Desktop/articles/"+file, encoding="utf8")
                try:
                    str_file = open_file.read()
                except Exception:
                    print (file)
                list_words = re.sub("[\.,]","",str_file).split()
                g = 0;
                for word in list_words:
                    morph = pymorphy2.MorphAnalyzer()
                    try:
                        cursor.execute(query_insert_word,(morph.parse(word)[0].normal_form,id_article))
                        connection.commit()
                    except Exception:
                        print(file)                    
                        continue
                    g = g+1;
                    print ("Article "+str(n_files)+": "+str(g)+" из "+str(len(list_words)))
   
    n_files = n_files + 1
    print("Обработано: "+str(n_files)+" из "+str(len(files)))


model = Word2Vec.load('ruwiki.word2vec.model')
country_list = [item[0] for item in model.most_similar('швеция')]

stop_words = get_stop_words('ru')
cursor.execute("SELECT word,count(*) as c FROM stats GROUP BY word ORDER BY c desc LIMIT 100")
for row in cursor:
    if (row[0] not in stop_words) and (re.compile('\d+').match(row[0])==None):
        if (row[0] in country_list):
            #print (row[0]+": "+ str(row[1]))
            president = model.most_similar(positive=[row[0], 'путин'], negative=['россия'], topn=1)
            print (row[0]+": "+president[0])
    #break
    
cursor.close()
connection.close()

#print(model.most_similar(positive=['россия', 'украина'], negative=['путин'], topn=5))
