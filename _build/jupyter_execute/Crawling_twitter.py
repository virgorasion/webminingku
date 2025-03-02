#!/usr/bin/env python
# coding: utf-8

# # Crawling Twitter Using Twint
# Twint adalah library python yang difungsikan untuk crawling data timeline di twitter dengan cara yang sangat mudah dan simpel.
# 
# Karena kodingan ini dibuat di colab oleh karena itu kita sambungkan terlebih dahulu ke google drive kita.

# Hubungkan colab ke google drive

# In[1]:


from google.colab import drive
drive.mount('/content/drive')


# In[2]:


get_ipython().run_line_magic('cd', 'drive/MyDrive/webmining/TugasWebmining/')


# instalasi twint. lebih jelasnya dapat dilihat di link yang akan di cloning

# In[3]:


get_ipython().system('git clone --depth=1 https://github.com/twintproject/twint.git')
get_ipython().run_line_magic('cd', 'twint')
get_ipython().system('pip3 install . -r requirements.txt')
get_ipython().system('pip install twint')
get_ipython().system('pip install aiohttp==3.7.0')
get_ipython().system('pip install nest_asyncio')
import twint
import nest_asyncio
nest_asyncio.apply()


# cek, apakah kita sudah berada di direktori yang diinginkan

# In[4]:


get_ipython().system('pwd')


# Konfigurasi crawling dengan twint

# In[8]:


# c = twint.Config()
# c.Search = '#percumalaporpolisi'
# c.Pandas = True
# c.Limit = 60
# c.Store_csv = True
# c.Custom["tweet"] = ["tweet"]
# c.Output = "dataset.csv"
# twint.run.Search(c)


# ## Penjelasan Pandas
# Pandas adalah sebuah library di Python yang berlisensi BSD dan open source yang menyediakan struktur data dan analisis data yang mudah digunakan. Pandas biasa digunakan untuk membuat tabel, mengubah dimensi data, mengecek data, dan lain sebagainya. Struktur data dasar pada Pandas dinamakan DataFrame, yang memudahkan kita untuk membaca sebuah file dengan banyak jenis format seperti file .txt, .csv, dan .tsv. Fitur ini akan menjadikannya table dan juga dapat mengolah suatu data dengan menggunakan operasi seperti join, distinct, group by, agregasi, dan teknik lainnya yang terdapat pada SQL

# In[11]:


import pandas as pd


# In[16]:


import random
read_file = pd.read_csv ('dataset.csv')
# label = ['positif','netral','negatif']
# data = []
# for i in range(read_file.size):
#   rand = random.randint(0,2)
#   data.append(label[rand])
# read_file.insert(1,"label",data, True)
# pd.DataFrame(read_file).to_csv('dataset.csv')
print(read_file)


# In[19]:


data = pd.read_excel('dataset.xlsx')
data


# ## Penjelasan NTLK dan Sastrawi
# - Naural Language Toolkit (NLTK) adalah sebuah platform yang digunakan untuk membangun program analisis teks. Platform ini awalnya dirilis oleh Steven Bird dan Edward Loper dalam kaitannya dengan mata kuliah komputasi linguistik di Universitas Pennsylvania pada tahun 2001. Ada sebuah buku pegangan untuk platform tersebut dengan judul Natural Language Processing dengan Python.
# 
# - Python Sastrawi adalah pengembangan dari proyek PHP Sastrawi. Python Sastrawi merupakan library sederhana yang dapat mengubah kata berimbuhan bahasa Indonesia menjadi bentuk dasarnya.

# In[35]:


get_ipython().system('pip install nltk')
get_ipython().system('pip install Sastrawi')


# ## Penjelasan RE
# Re atau Regular Expression module Python menyediakan seperangkat fungsi yang memungkinkan kita untuk mencari sebuah string untuk match (match).

# In[36]:


import pandas as pd
import re
import numpy as np

import nltk
nltk.download('punkt')
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


# Proses stopword untuk menghilangkan kata-kata yang tidak perlu

# In[37]:


def remove_stopwords(text):
    with open('/content/drive/MyDrive/webmining/stopword.txt') as f:
        stopwords = f.readlines()
        stopwords = [x.strip() for x in stopwords]
    
    text = nltk.word_tokenize(text)
    text = [word for word in text if word not in stopwords]
                     
    return text


# Stemming untuk proses perubahan kata berimbuhan menjadi kata dasar

# In[38]:


def stemming(text):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    
    result = [stemmer.stem(word) for word in text]
    
    return result


# In[39]:


def preprocessing(text):
    #case folding
    text = text.lower()

    #remove non ASCII (emoticon, chinese word, .etc)
    text = text.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\'," ").replace('\\f'," ").replace('\\r'," ")

    # remove non ASCII (emoticon, chinese word, .etc)
    text = text.encode('ascii', 'replace').decode('ascii')

    # remove mention, link, hashtag
    text = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", text).split())

    #replace weird characters
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    text = text.replace('-', ' ')

    #tokenization and remove stopwords
    text = remove_stopwords(text)

    #remove punctuation    
    text = [''.join(c for c in s if c not in string.punctuation) for s in text]  

    #stemming
    text = stemming(text)

    #remove empty string
    text = list(filter(None, text))
    return text


# In[40]:


data['tweet'].apply(preprocessing).to_csv('preprocessing.csv')


# In[41]:


pd.read_csv('preprocessing.csv')


# Tokenizing adalah proses pemisahan teks menjadi potongan-potongan yang disebut sebagai token untuk kemudian di analisa. Kata, angka, simbol, tanda baca dan entitas penting lainnya dapat dianggap sebagai token.

# In[42]:


from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
dataTextPre = pd.read_csv('/content/drive/MyDrive/webmining/TugasWebmining/twint/preprocessing.csv')
vectorizer = CountVectorizer(min_df=1)
bag = vectorizer.fit_transform(dataTextPre['tweet'])
dataTextPre


# In[43]:


matrik_vsm=bag.toarray()
matrik_vsm.shape


# In[44]:


matrik_vsm[0]


# In[45]:


a=vectorizer.get_feature_names_out()


# In[46]:


dataTF =pd.DataFrame(data=matrik_vsm,index=list(range(1, len(matrik_vsm[:,1])+1, )),columns=[a])
dataTF


# In[47]:


label = pd.read_excel('/content/drive/MyDrive/webmining/TugasWebmining/twint/dataset.xlsx')
dj = pd.concat([dataTF.reset_index(), label["label"]], axis=1)
dj


# In[48]:


dj['label'].unique()


# ## Penjelasan Scikit Learn
# Scikit Learn atau sklearn merupakan sebuah module dari bahasa pemrograman Python yang dibangun berdasarkan NumPy,SciPy,dan Matplotlib. Fungsi dari module ini adalah untuk membantu melakukan processing data atau pun melakukan training data untuk kebutuhan machine learning atau data science.

# In[49]:


get_ipython().system('pip install -U scikit-learn')


# ## Penjelasan Information Gain
# Information Gain merupakan teknik seleksi fitur yang memakai metode scoring untuk nominal
# ataupun pembobotan atribut kontinue yang didiskretkan menggunakan maksimal entropy. Suatu entropy
# digunakan untuk mendefinisikan nilai Information Gain. Entropy menggambarkan banyaknya informasi
# yang dibutuhkan untuk mengkodekan suatu kelas. Information Gain (IG) dari suatu term diukur
# dengan menghitung jumlah bit informasi yang diambil dari prediksi kategori dengan ada atau tidaknya
# term dalam suatu dokumen.
# 
# 
# $$
# Entropy \ (S) \equiv \sum ^{c}_{i}P_{i}\log _{2}p_{i}
# $$
# 
# c : jumlah nilai yang ada pada atribut target (jumlah kelas klasifikasi).
# 
# Pi : porsi sampel untuk kelas i.
# 
# 
# $$
# Gain \ (S,A) \equiv Entropy(S) - \sum _{\nu \varepsilon \ values } \dfrac{\left| S_{i}\right| }{\left| S\right|} Entropy(S_{v})
# $$
# 
# A : atribut
# 
# V : menyatakan suatu nilai yang mungkin untuk atribut A
# 
# Values (A) : himpunan nilai-nilai yang mungkin untuk atribut A
# 
# |Sv| : jumlah Sampel untuk nilai v
# 
# |S| : jumlah seluruh sample data Entropy 
# 
# (Sv) : entropy untuk sampel sampel yang memiliki nilai v
# 

# In[50]:


from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(dj.drop(labels=['label'], axis=1),
    dj['label'],
    test_size=0.3,
    random_state=0)


# In[51]:


y_train


# In[52]:


X_train


# Penjelasan mutual_info_classif mengukur ketergantungan antara variabel. Itu sama dengan nol jika dan hanya jika dua variabel acak independen, dan nilai yang lebih tinggi berarti ketergantungan yang lebih tinggi.

# In[53]:


from sklearn.feature_selection import mutual_info_classif
mutual_info = mutual_info_classif(X_train, y_train)
mutual_info


# In[54]:


mutual_info = pd.Series(mutual_info)
mutual_info.index = X_train.columns
mutual_info.sort_values(ascending=False)


# In[55]:


mutual_info.sort_values(ascending=False).plot.bar(figsize=(50, 20))


# Import SelectKbest untuk memilih fitur tertinggi

# In[56]:


from sklearn.feature_selection import SelectKBest
sel_five_cols = SelectKBest(mutual_info_classif, k=100)
sel_five_cols.fit(X_train, y_train)
X_train.columns[sel_five_cols.get_support()]


# In[57]:


X_train=X_train.values
y_train=y_train.values
X_test=X_test.values
y_test=y_test.values


# ## Penjelasan Naive Bayes
# Naive Bayes adalah algoritma machine learning yang digunakan untuk keperluan klasifikasi atau pengelompokan suatu data. Algoritma ini didasarkan pada teorema probabilitas yang dikenalkan oleh ilmuwan Inggris Thomas Bayes. Naive Bayes berfungsi memprediksi probabilitas di masa depan berdasarkan pengalaman sebelumnya, sehingga dapat digunakan untuk pengambilan keputusan.

# In[58]:


from sklearn.naive_bayes import GaussianNB
gauss = GaussianNB()
gauss.fit(X_train, y_train)


# In[60]:


from sklearn.metrics import make_scorer, accuracy_score,precision_score
testing = gauss.predict(X_test) 
accuracy_gauss=round(accuracy_score(y_test,testing)* 100, 2)
accuracy_gauss


# ##Penjelasan Matplotlib
# Matplotlib adalah library Python yang fokus pada visualisasi data seperti membuat plot grafik. Matplotlib pertama kali diciptakan oleh John D. Hunter dan sekarang telah dikelola oleh tim developer yang besar. Awalnya matplotlib dirancang untuk menghasilkan plot grafik yang sesuai pada publikasi jurnal atau artikel ilmiah. Matplotlib dapat digunakan dalam skrip Python, Python dan IPython shell, server aplikasi web, dan beberapa toolkit graphical user interface (GUI) lainnya.

# In[62]:


import matplotlib.pyplot as plt
from sklearn import metrics


# ##Penjelasan Confusion Matrix
# Confusion matrix juga sering disebut error matrix. Pada dasarnya confusion matrix memberikan informasi perbandingan hasil klasifikasi yang dilakukan oleh sistem (model) dengan hasil klasifikasi sebenarnya. Confusion matrix berbentuk tabel matriks yang menggambarkan kinerja model klasifikasi pada serangkaian data uji yang nilai sebenarnya diketahui.
# 
# membuat Confusion Matrix dengan column vertical (negatif,netral dan positif) dan column horizontal (negatif,netral dan positif)

# In[63]:


conf_matrix =metrics.confusion_matrix(y_true=y_test, y_pred=testing)
cm_display = metrics.ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = ['negatif', 'netral','positif'])
cm_display.plot()
plt.show()


# ##Penjelasan K-Means
# K-Means Clustering merupakan algoritma yang efektif untuk menentukan cluster dalam sekumpulan data, di mana pada algortima tersebut dilakukan analisis kelompok yang mengacu pada pemartisian N objek ke dalam K kelompok (Cluster) berdasarkan nilai rata-rata (means) terdekat. Adapun persamaan yang sering digunakan dalam pemecahan masalah dalam menentukan jarak terdekat adalah persamaan Euclidean berikut :
# 
# $$
# d(p,q) = \sqrt{(p_{1}-q_{1})^2+(p_{2}-q_{2})^2+(p_{3}-q_{3})^2}
# $$
# 
# 
# d = jarak obyek
# 
# p = data 
# 
# q = centroid
# 
# TruncatedSVD adalah Teknik pengurangan dimensi menggunakan SVD terpotong

# Prediksi Dengan Clustering

# In[64]:


from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD


# In[65]:


# Latih Kmeans dengan n cluster terbaik
modelKm = KMeans(n_clusters=3, random_state=12)
modelKm.fit(dataTF.values)
prediksi = modelKm.predict(dataTF.values)

# Pengurangan dimensi digunakan untuk memplot dalam representasi 2d
pc=TruncatedSVD(n_components=2)
X_new=pc.fit_transform(dataTF.values)
centroids=pc.transform(modelKm.cluster_centers_)
print(centroids)
plt.scatter(X_new[:,0],X_new[:,1],c=prediksi, cmap='viridis')
plt.scatter(centroids[:,0] , centroids[:,1] , s = 50, color = 'red')


# #Perangkingan Kalimat Berita Dengan PageRank
# ##Penjelasan Scrapy
# Scrapy adalah web crawling dan web scraping framework tingkat tinggi yang cepat, digunakan untuk merayapi situs web dan mengekstrak data terstruktur dari halaman mereka. Ini dapat digunakan untuk berbagai tujuan, mulai dari penambangan data hingga pemantauan dan pengujian otomatis.

# In[66]:


get_ipython().system('pip install scrapy')
get_ipython().system('pip install crochet')


# In[67]:


import scrapy


# In[71]:


import scrapy
from scrapy.crawler import CrawlerRunner
import re
from crochet import setup, wait_for
setup()

class QuotesToCsv(scrapy.Spider):
    name = "TugasPPW"
    start_urls = [
        'https://nasional.tempo.co/read/1656990/jokowi-dan-pemimpin-g20-gelar-pertemuan-tertutup',
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            '__main__.ExtractFirstLine': 1
        },
        'FEEDS': {
            'news.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        """parse data from urls"""
        for quote in response.css('#isi > p'):
            yield {'news': quote.extract()}


class ExtractFirstLine(object):
    def process_item(self, item, spider):
        """text processing"""
        lines = dict(item)["news"].splitlines()
        first_line = self.__remove_html_tags__(lines[0])

        return {'news': first_line}

    def __remove_html_tags__(self, text):
        """remove html tags from string"""
        html_tags = re.compile('<.*?>')
        return re.sub(html_tags, '', text)

@wait_for(10)
def run_spider():
    crawler = CrawlerRunner()
    d = crawler.crawl(QuotesToCsv)
    return d


# In[70]:


# run_spider()


# In[72]:


dataNews = pd.read_csv('news.csv')
dataNews


# PyPDF2 adalah pustaka PDF python murni gratis dan open-source yang mampu memisahkan, menggabungkan , memotong, dan mengubah halaman file PDF.
# 
# Install PyPDF2

# In[93]:


get_ipython().system('pip install PyPDF2')


# In[94]:


import PyPDF2


# In[95]:


pdfReader = PyPDF2.PdfFileReader('news.pdf')
pageObj = pdfReader.getPage(0)
document = pageObj.extractText()
document


# PunktSentenceTokenizer adalah Sebuah tokenizer kalimat yang menggunakan algoritma tanpa pengawasan untuk membangun model untuk kata-kata singkatan, kolokasi, dan kata-kata yang memulai kalimat dan kemudian menggunakan model itu untuk menemukan batas kalimat.

# In[96]:


from nltk.tokenize.punkt import PunktSentenceTokenizer
def tokenize(document):
    # Kita memecahnya menggunakan  PunktSentenceTokenizer
    doc_tokenizer = PunktSentenceTokenizer()
    # sentences_list adalah daftar masing masing kalimat dari dokumen yang ada.
    sentences_list = doc_tokenizer.tokenize(document)
    return sentences_list
sentences_list = tokenize(document)
sentences_list


# In[97]:


kal=1
for i in sentences_list:
    print('\nKalimat {}'.format(kal))
    kal+=1
    print(i)


# Tokenizing adalah proses pemisahan teks menjadi potongan-potongan yang disebut sebagai token untuk kemudian di analisa. Kata, angka, simbol, tanda baca dan entitas penting lainnya dapat dianggap sebagai token.

# In[99]:


from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
vectorizer = CountVectorizer()
cv_matrix=vectorizer.fit_transform(sentences_list)
print ("Banyaknya kosa kata = ", len((vectorizer.get_feature_names_out())))


# In[100]:


print ("Banyaknya kalimat = ", (len(sentences_list)))


# In[101]:


print ("kosa kata = ", (vectorizer.get_feature_names_out()))


# In[102]:


# mengubah kumpulan dokumen mentah menjadi matriks fitur TF-IDF
normal_matrix = TfidfTransformer().fit_transform(cv_matrix)
print(normal_matrix.toarray())


# In[103]:


normal_matrix.shape


# NetworkX adalah paket Python untuk pembuatan, manipulasi, dan studi tentang struktur, dinamika, dan fungsi jaringan yang kompleks. Ini menyediakan:

# In[104]:


import networkx as nx


# Graph adalah kumpulan dati titik (node) dan garis dimana pasangan – pasangan titik (node) tersebut dihubungkan oleh segmen garis. Node ini biasa disebut simpul (vertex) dan segmen garis disebut ruas (edge)

# In[105]:


res_graph = normal_matrix * normal_matrix.T
print(res_graph)


# In[106]:


nx_graph = nx.from_scipy_sparse_matrix(res_graph)
nx.draw_circular(nx_graph)


# In[107]:


print('Banyaknya sisi {}'.format(nx_graph.number_of_edges()))


# Menkalikan data dengan data Transpose

# In[108]:


res_graph = normal_matrix * normal_matrix.T


# PageRank menghitung peringkat node dalam grafik G berdasarkan struktur tautan masuk. Awalnya dirancang sebagai algoritma untuk menentukan peringkat halaman web.

# In[109]:


ranks=nx.pagerank(nx_graph,)


# In[112]:


arrRank=[]
for i in ranks:
    arrRank.append(ranks[i])
dfRanks = pd.DataFrame(arrRank,columns=['PageRank'])
dfSentence = pd.DataFrame(sentences_list,columns=['News'])
dfJoin = pd.concat([dfSentence,dfRanks], axis=1)
dfJoin


# In[113]:


sortSentence=dfJoin.sort_values(by=['PageRank'],ascending=False)
sortSentence


# In[115]:


sortSentence.head(4)


# ##Latent Semantic Indexing(LSI) Topik Berita
# 

# In[118]:


get_ipython().system('pip install PySastrawi')
get_ipython().system('pip install nltk')
get_ipython().system('pip install Sastrawi')


# In[121]:


import PyPDF2
pdfReader = PyPDF2.PdfFileReader('news.pdf')
pageObj = pdfReader.getPage(0)
document = pageObj.extractText()
print(document)


# In[122]:


import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('stopwords')


# In[123]:


word_tokens = word_tokenize(document)
print(word_tokens)


# In[124]:


stop_words = set(stopwords.words('indonesian'))
word_tokens_no_stopwords = [w for w in word_tokens if not w in stop_words]
print(word_tokens_no_stopwords)


# In[125]:


import os
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


# In[126]:


# Vectorize document using TF-IDF
tfidf = TfidfVectorizer(lowercase=True,
                        ngram_range = (1,1))

# Fit and Transform the documents
train_data = tfidf.fit_transform(word_tokens_no_stopwords)
train_data


# In[127]:


num_components=10

# Create SVD object
lsa = TruncatedSVD(n_components=num_components, n_iter=100, random_state=42)

# Fit SVD model on data
lsa.fit_transform(train_data)

# Get Singular values and Components 
Sigma = lsa.singular_values_ 
V_transpose = lsa.components_.T
V_transpose


# In[128]:


# Print the topics with their terms
terms = tfidf.get_feature_names()

for index, component in enumerate(lsa.components_):
    zipped = zip(terms, component)
    top_terms_key=sorted(zipped, key = lambda t: t[1], reverse=True)[:5]
    top_terms_list=list(dict(top_terms_key).keys())
    print("Topic "+str(index+1)+": ",top_terms_list)


# ##Ensemble BaggingClassifier dengan Metode DecisionTreeClassifier
# 

# In[129]:


from sklearn import model_selection
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

X = X_train
Y = y_train

# seed = 8
# kfold = model_selection.KFold(n_splits = 3,
# 					random_state = seed)

# initialize the base classifier
base_cls = DecisionTreeClassifier()

# no. of base classifier
num_trees = 500

# bagging classifier
model = BaggingClassifier(base_estimator = base_cls,
						n_estimators = num_trees)

results = model_selection.cross_val_score(model, X, Y)
print("accuracy :")
print(results.mean())


# ##Ensemble BaggingClassifier dengan Metode SVC

# In[130]:


from sklearn import model_selection
from sklearn.ensemble import BaggingClassifier
from sklearn.svm import SVC
import pandas as pd

X = X_train
Y = y_train

# seed = 8
# kfold = model_selection.KFold(n_splits = 3,
# 					random_state = seed)

# initialize the base classifier
base_cls = SVC()

# no. of base classifier
num_trees = 500

# bagging classifier
model = BaggingClassifier(base_estimator = base_cls,
						n_estimators = num_trees)

results = model_selection.cross_val_score(model, X, Y)
print("accuracy :")
print(results.mean())


# ##Ensemble RandomForestClassifier dengan GridSearchCV

# In[131]:


from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV
rfc=RandomForestClassifier(random_state=42)
param_grid = { 
    'n_estimators': [50,100,200,500],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth' : [4,5,6,7,8],
    'criterion' :['gini', 'entropy']
}
CV_rfc = GridSearchCV(estimator=rfc, param_grid=param_grid, cv= 5)
CV_rfc.fit(X_train, y_train)


# In[132]:


CV_rfc.best_params_


# In[133]:


rfc1=RandomForestClassifier(random_state=42, max_features='log2', n_estimators= 50, max_depth=6, criterion='gini')
rfc1.fit(X_train, y_train)


# In[136]:


RandomForestClassifier(criterion='gini', max_depth=6, random_state=42)


# In[137]:


pred=rfc1.predict(X_test)
print("Accuracy for Random Forest on CV data: ",accuracy_score(y_test,pred))


# ##Ensemble StackingClassifier

# In[138]:


from sklearn.model_selection import train_test_split
#membagi kumpulan data menjadi data pelatihan dan data pengujian.
X_train,X_test,y_train,y_test=train_test_split(dj.drop(labels=['label'], axis=1),
    dj['label'],
    test_size=0.3,
    random_state=0)


# In[140]:


from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import StackingClassifier
from sklearn.naive_bayes import GaussianNB
estimators = [
    ('rf', RandomForestClassifier(random_state=42,max_features='log2', n_estimators= 50, max_depth=6, criterion='gini')),
    ('rf2', RandomForestClassifier(random_state=42,max_features='log2', n_estimators= 50, max_depth=6, criterion='entropy'))
]
clf = StackingClassifier(
    estimators=estimators, final_estimator=RandomForestClassifier(n_estimators=10, random_state=42)
)
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, stratify=y, random_state=42
# )
clf.fit(X_train.values, y_train.values).score(X_test.values, y_test.values)


# In[ ]:


from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3).fit(dataTF)
prediksi = kmeans.predict(dataTF)
centroids = kmeans.cluster_centers_


# In[ ]:


prediksi


# In[ ]:


pd.DataFrame(prediksi,columns=['Cluster'])

