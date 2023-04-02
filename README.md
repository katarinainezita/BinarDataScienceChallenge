
# Binar Data Science Challenge

Kriteria dalam challenge yang diterapkan dalam program ini adalah :


#### Membuat sebuah API yang dapat menerima input user berupa teks dan file dengan 2 endpoint dan membuat server API dengan Flask dan Swagger UI. API ini bisa menghasilkan output berupa teks yang sudah di cleansing.

Dalam program dibuat sebuah file dengan nama apps.py yang berisikan serangkaian kode untuk dapat membuat API 

Langkah - Langkah :

a. Impor modul yang diperlukan

```
from flask import Flask, request, jsonify
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from
import re
import pandas as pd
import sqlite3
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
```

b. Konfigurasi dasar dari Flask

```
app = Flask(__name__)
app.config["DEBUG"] = True

UPLOAD_FOLDER = 'static/uploadFile'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
```

c. Konfigurasi Swagger 

```
app.json_encoder = LazyJSONEncoder
swagger_template = dict(
info = {
    'title': LazyString(lambda: 'Data Cleansing'),
    'version' : LazyString(lambda: '1.0.0'),
    'description' : LazyString(lambda: 'Dokumentasi untuk Data Cleansing')
    },
    host = LazyString(lambda: request.host)    
)


swagger_config = {
    "headers":[],
    "specs": [
        {
            "endpoint" : 'docs',
            "route" : '/docs.json',
        }
    ],
    "static_url_path" : "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/" 
}
swagger = Swagger(app=app, config = swagger_config, template = swagger_template)

```

d. Fungsi untuk mengunggah file ke server dan membaca data dari file csv yang diunggah

```
@swag_from("docs/1.yml", methods = ['POST'])
@app.route('/uploadFile', methods = ['POST'])
def uploadFile():
    upload_file = request.files['file']

    if upload_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], upload_file.filename)
        upload_file.save(file_path)
        df = pd.read_csv(file_path, encoding = 'latin-1')
    return str(df)
```

e. Fungsi untuk memproses teks yang diunggah ke server.

```
@swag_from("docs/2.yml", methods = ['POST'])
@app.route('/textProcessing', methods = ['POST'])

def textProcessing():

    connection = sqlite3.connect('data/kamusalay.db')
    kamus_alay_df = pd.read_sql('''SELECT * FROM kamusalay;''', connection)
    connection.close()

    abusive = pd.read_csv('data/abusive.csv')

    text = request.form.get('text')

    clean_text = re.sub(r'[\W_0-9]', ' ', text.lower())
    stemmed_text = ' '.join([ps.stem(word) for word in clean_text.split() if not word in stop_words])

    json_response = {
        'status_code' : 200,
        'description' : 'Original Text',
        'data': stemmed_text
    }

    response_data = jsonify(json_response)
    return response_data
```

f. Menjalankan aplikasi Flask di port 2003

```
if __name__ == "__main__":
    app.run(debug=True, port=2003)
```

#### Menyimpan data dalam SQLite menggunakan modul SQLite3

Untuk melakukan penyimpanan data dapat dilakukan dengan membuat sebuah file dengan nama createDatabase.py

Langkah - Langkah :

a. Impor modul yang diperlukan

```
import sqlite3
import pandas as pd
```

b. Membuka koneksi ke database sqlite3

```
connection = sqlite3.connect('data/kamusalay.db')
```

c. Membuat sebuah tabel 

```
try:
    connection.execute("""CREATE TABLE kamusalay (alay VARCHAR(256), baku VARCHAR(256)); """)
    print("table created!")
except:
    print("table already exists!")
```

d. Membaca file csv dan memasukkannya ke dalam suatu DataFrame

```
kamusDF = pd.read_csv('data/new_kamusalay.csv', names=['Alay', 'Baku'], encoding='Latin-1')
```

e. Menyimpan DataFrame ke dalam tabel

```
kamusDF.to_sql(name='kamusalay', con=connection, if_exists='replace', index=False)
```

f. Menyimpan perubahan

```
connection.commit()
```

g. Menutup koneksi ke database

```
connection.close()
```

#### Report Hasil Analisis Data

Analisis dilakukan dengan membuat sebuah file Challenge_DataScience_Binar.ipynb di google collab

Langkah - Langkah :

a. Membuat koneksi dengan google drive

```
from google.colab import drive 
drive.mount('/content/drive')
```

b. Import modul yang diperlukan

```
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
```

c. Membaca sebuah file CSV dan disimpan dalam variable df

```
df = pd.read_csv("/content/drive/MyDrive/Binar-Data-Science/data.csv", encoding='latin-1')
```

d. Menampilkan 5 data teratas

```
df.head()
```

e. Menampilkan 5 data terbawah

```
df.tail()
```

f. Menampilkan dimensi atau ukuran dari DataFrame

```
df.shape
```

g. Menghitung jumlah baris duplikat dalam DataFrame dan Menghapus file yang duplikat

```
df.duplicated().sum()
df = df.drop_duplicates()
```

h. Mengecek apakah ada missing value

```
df.isna()
```

i. Menghitung persentase (missing value) dalam setiap kolom dari DataFrame

```
df.isna().sum()/df.shape[0]
```

j. Membersihkan teks pada kolom 'Tweet' dalam DataFrame

```
df['Tweet'] = df['Tweet'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x).lower().strip()))
```

g. Menghapus kata-kata yang tidak berguna atau stop words dari teks pada kolom 'Tweet' dalam DataFrame

```
stop_words = set(stopwords.words('indonesian'))
stop_words -= {'mau', 'maka', 'akan', 'yang', 'untuk', 'dan', 'juga', 'dari', 'di', 'kan'}


def remove_stopwords(teks):
    words = teks.split()
    filtered_words = [word for word in words if word.lower() not in stop_words and word.isalpha()]
    return ' '.join(filtered_words)

df['Tweet'] = df['Tweet'].apply(remove_stopwords)
```

h. Melakukan stemming pada teks yang ada pada kolom 'Tweet' pada DataFrame

```
stemmer = PorterStemmer()

def stem_text(text):
    words = text.split()
    stemmed_words = [stemmer.stem(word) for word in words]
    return ' '.join(stemmed_words)

df['Tweet'] = df['Tweet'].apply(stem_text)
```

i. Melakukan tokenisasi pada setiap teks pada kolom 'Tweet' dari DataFrame

```
def tokenize(text):
    tokens = nltk.word_tokenize(text)
    return tokens

df['Tweet'] = df['Tweet'].apply(tokenize)
```

j. Menghapus tanda baca

```
def remove_punctuation(text):
    # mengubah daftar kata menjadi string tunggal
    text = ' '.join(text)
    # membuat translation table yang berisi mapping untuk menghapus punctuation
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

df['Tweet'] = df['Tweet'].apply(remove_punctuation)
```

k. Mengganti setiap kata alay menjadi kata baku

```
# membaca teks dari file
with open('/content/drive/MyDrive/Binar-Data-Science/data.csv', 'r', encoding="Latin-1") as file:
    teks = file.read()

# membaca daftar akronim dari file
with open('/content/drive/MyDrive/Binar-Data-Science/new_kamusalay.csv', 'r', encoding='Latin-1') as file:
    lines = file.readlines()

# menghapus karakter newline pada setiap akronim
daftar_akronim = [akronim.strip() for akronim in lines]

# mengganti setiap akronim dengan definisinya
daftar_akronim_dict = {}
for line in lines:
    parts = line.strip().split(',')
    if len(parts) == 2:
        daftar_akronim_dict[parts[0]] = parts[1]

for akronim in daftar_akronim_dict:
    teks = teks.replace(akronim, daftar_akronim_dict[akronim])
```

l. Membuat dataframe baru yang hanya memuat kolom Tweet dan HS_Individual dengan kondisi kolom HS_Individual yang sama dengan 1.

```
new_df = df.loc[df['HS_Individual'] == 1, ['Tweet', 'HS_Individual']]
```

m. Penghitungan jumlah karakter dan jumlah kata pada setiap tweet pada kolom Tweet

```
new_df['total_char'] = new_df['Tweet'].apply(len)
new_df['total_word'] = new_df['Tweet'].apply(lambda sent: len(sent.split()))
```

n. Menghitung nilai rata-rata

```
new_df.mean()
```

didapatkan hasil :

```
total_char       98.248671
total_word       15.276084
```

o. Mencari nilai median

```
new_df.median()
```

didapatkan hasil :

```
total_char       89.0
total_word       14.0
```

p. Mencari nilai mode

```
new_df['total_char'].mode()
new_df['total_word'].mode()
```

didapatkan hasil :

```
0    78
0    10
```

q. Menghitung range

```
range_total_word = new_df.total_word.max() - new_df.total_word.min()
range_total_char = new_df.total_char.max() - new_df.total_char.min() 
```

didapatkan hasil :

```
48
226
```

r. Mengambil nilai terendah dan nilai tertinggi 

```
p0 = new_df.total_char.min()
p100 = new_df.total_char.max()
```

didapatkan hasil :

```
6
278
```

s. Menghitung batas bawah dan batas atas

```
q1 = new_df.total_char.quantile(0.25)
q2 = new_df.total_char.quantile(0.5)
q3 = new_df.total_char.quantile(0.75)
iqr = q3 - q1
lower_limit = q1 - 1.5*iqr
upper_limit = q3 + 1.5*iqr

print("Batas Bawah 'total char' : ", lower_limit)
print("Nilai minimum", p0)

if lower_limit < p0 :
  print("Tidak ada outlier dari sisi batas bawah")
else :
  print("Ada outlier dari sisi batas bawah")

print()
print("Batas Atas 'total_char' : ", upper_limit)
print("Nilai maksimum", p100)

if upper_limit > p100 :
  print("Tidak ada outlier dari sisi batas atas")
else :
  print("Ada outlier dari sisi batas atas")
```

didapatkan hasil :

```
Batas Bawah 'total char' :  -61.0
Nilai minimum 6
Tidak ada outlier dari sisi batas bawah

Batas Atas 'total_char' :  243.0
Nilai maksimum 278
Ada outlier dari sisi batas atas
```

t. Mencari variance

```
new_df.var()
```

didapatkan hasil :

```
total_char       3372.640719
total_word         79.623533
```

u. Mencari standar deviasi

```
new_df.std()
```

didapatkan hasil :

```
total_char       58.074441
total_word        8.923202
```

v. Menghitung skewness

```
new_df.skew()
```

didapatkan hasil

```
total_char       0.891788
total_word       1.039487
```

w. Menghitung kurtosis

```
new_df.kurtosis()
```

didapatkan hasil :

```
total_char       0.753535
total_word       1.430769
```

x. Membuat histogtam untuk total karakter dan total kata

```
new_df.total_char.hist()
new_df.total_word.hist()
```

didapatkan hasil : 

ss total_word
ss total_char

y. Mencari kata yang sering muncul

```
from wordcloud import WordCloud

text = ' '.join(new_df['Tweet'])
wordcloud = WordCloud().generate(text)

plt.imshow(wordcloud)
plt.axis("off")
plt.show()
```

didapatkan hasil :

ss word_cloud

z. Mencari korelasi antara total karakter dan total kata

```
new_df.plot(x='total_word', y='total_char', kind='scatter')
```

didapatkan hasil :

ss scatter