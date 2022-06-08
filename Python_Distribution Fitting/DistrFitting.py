#!/usr/bin/env python
# coding: utf-8

# # Distribution Fitting
# 
# Set data, secara umum biasa digali informasi yang terkandung di dalamnya. Misalnya data tersebut terdistribusi menurut distriusi data apa.
# 
# Grafik distribusi data diperoleh dengan cara melihat berapa kali data tersebut muncul (frekuensi) pada tiap nilai data. Sumbu x adalah data, sumbu y adalah frekuensi. 
# 
# Salah satu contoh distrbusi adalah distrbusi normal. Pada distribusi normal, nilai tengah adalah data yang paling banyak, sedangkan nilai ekstrim adalah pencilan (frekuensi sedikit). Grafik distribusi normal berbentuk bel simetris
# 
# ![page-123.jpg](attachment:page-123.jpg)

# Contoh Data Debit (disimpan dalam file bernama : dataDebit.csv)
# 
# ======
# 
# Tahun,hydrData
# 
# 1966,764
# 
# 1965,722
# 
# 1969,706
# 
# 1962,698
# 
# 1974,695
# 
# 1961,679
# 
# 1967,678
# 
# 1963,648
# 
# 1970,643
# 
# 1971,641
# 
# 1959,636
# 
# 1975,634
# 
# 1973,575
# 
# 1967,572
# 
# 1972,536
# 
# 1960,531
# 
# =====

# ## Kode Program untuk Distribution Fitting Data Debit

# In[31]:


#Membaca Data

import read_csv as rd

#read data from file
filename = 'dataDebit.csv' #membaca data dari file 'dataDebit.csv'
rd.read_csv(filename) #column name is variable name : hydrData
print (rd.hydrData)


# In[32]:


#Deskripsi data
import scipy as sc
import numpy as np

desc = sc.stats.describe(rd.hydrData)
nod = desc[0] #banyaknya data
minmax = desc[1]
mean = desc[2]
std = np.sqrt(desc[3])  
cv  = std/mean    
var = desc[3]
skew = desc[4]
kurt = desc[5]

print (desc)


# In[40]:


#Pencocokan Distribusi data
pdf_nod = 5 * nod
x = np.linspace(min(rd.hydrData), max(rd.hydrData), pdf_nod) # x pdf

dist_names = ['norm','lognorm','pearson3', 'expon'] #distribusi yang akan dicoba : normal, log-normal, log pearson3, exponensial
choose_distribution = dist_names[3] #ambil nama jenis distribusi dari variabel dist_names.
#Jika ingin mencoba distribusi normal, dist_names[0], jika lognormal, dist_names[1]

dist = getattr(sc.stats, choose_distribution) #ambil atribut distribusi tertentu (tiap distribusi beda atribut)
param = dist.fit(rd.hydrData)

#fitting/mencocokkan distribusi yang dipilih
pdf_fitted = dist.pdf(x, *param[:-2], loc=param[-2], scale=param[-1])
cdf_fitted = dist.cdf(x, *param[:-2], loc=param[-2], scale=param[-1])
#pdf_fitteds = pdf_fitted
#cdf_fitteds = cdf_fitted

#Applying the Kolmogorov-Smirnov test, uji untuk menentukan distribusi mana yang paling cocok
D, p = sc.stats.kstest(rd.hydrData, choose_distribution, args=param); # D = KS test statistic, p = p value
print (choose_distribution, p, param) #tampilkan : nama distribusi, p value, parameter distribusi
print ('=======================================')


# # Plot Grafik Distribusi

# In[41]:


import matplotlib.pyplot as plt

plt.figure(1)
yhist, xhist, _ = plt.hist(rd.hydrData, alpha=0.5, label='Actual')
pdf_scale = yhist.max() / np.amax(pdf_fitted)
pdf_fitted_scaled = pdf_fitted * pdf_scale
plt.plot(x, pdf_fitted_scaled, 'r-', label= choose_distribution +'(Fitted)')

plt.legend(loc='upper right')
plt.xlabel('Data')
plt.ylabel('Frequency')
plt.title('Fitted Distribution is '+ choose_distribution)
plt.show()


# Silahkan diganti-ganti variabel 'choose_distribution' pada program untuk mendapatkan distibusi lain
# 
# distribusi normal --> choose_distribution = dist_names[0]
# 
# distribusi log normal --> choose_distribution = dist_names[1]
# 
# distribusi log pearson type 3 --> choose_distribution = dist_names[2]
# 
# distribusi exponential --> choose_distribution = dist_names[3]

# ## Data yang diberikan di atas, mana distribusi yang paling cocok? apakah normal, log normal, log pearson type 3, atau exponential???
# 
# Perhatikan nilai p (p value) pada tiap distribusi yang dipilih. Nilai p yang paling besar menunjukkan bahwa data tersebut paling cocok dengan distribusi itu

# In[ ]:




