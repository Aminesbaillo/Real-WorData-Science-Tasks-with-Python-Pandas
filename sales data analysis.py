#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os


# 1- Merge the 12 months of sales into a single CSV file 

# In[3]:


files = [file for file in os.listdir("C:\\Users\\DELL\\OneDrive\\Bureau\\selfeducations\\projects\\sales project DS\\data sales")]
all_months_data = pd.DataFrame()
for file in files : 
    df = pd.read_csv("C:\\Users\\DELL\\OneDrive\\Bureau\\selfeducations\\projects\\sales project DS\\data sales\\"+file)
    all_months_data = pd.concat([all_months_data,df])
all_months_data.to_csv("all_data.csv",index = False )


# In[4]:


all_data = pd.read_csv("C:\\Users\\DELL\\OneDrive\\Bureau\\selfeducations\\projects\\sales project DS\\data sales\\all_data.csv")
all_data.head()


# In[5]:


all_data.shape


# we gonna make a copie of data in case we do any error : 
# 

# In[6]:


all_data_copie01 = all_data  


# 2- Augmente data with columns : 
# 

#     2-1 : add month columns : 

# In[7]:


all_data["Month"] = all_data['Order Date'].str[0:2]
all_data.head()


#     2-2 drop row with NaN : 

# In[8]:


all_data = all_data.dropna(axis = 0)


# In[9]:


len(all_data.index)


# In[10]:


len(all_data_copie01.index)


#     3-3 add sales columns : 

# ** make it the 2 columns quantity ordered and price each float : 
# 

# In[11]:


all_data.loc[515:520]


# In[12]:


all_data = all_data[all_data["Order Date"].str[0:2]!='Or']
 


# In[13]:


all_data["Quantity Ordered"] = pd.to_numeric(all_data["Quantity Ordered"])
all_data["Price Each"] = pd.to_numeric(all_data["Price Each"])


# In[14]:


all_data["Sales"] = all_data["Quantity Ordered"]*all_data["Price Each"]


# In[30]:


all_data.head()


#     3-4 add city column : 

# In[19]:


def get_city(adresse):
    return adresse.split(',')[1]
def get_state(adresse):
    return adresse.split(',')[2].split(' ')[1]

all_data["City"] = all_data["Purchase Address"].apply(lambda x: f"{get_city(x)} ({get_state(x)})")
all_data.head()


# 4- best months sales : 
#     

# In[20]:


results = all_data.groupby('Month').sum()
results


# In[21]:


import matplotlib.pyplot as plt 


# In[22]:


Months = range(1,13)
plt.bar(Months,results['Sales'])
plt.xticks(Months)
plt.ylabel('Sales in usd ($)')
plt.xlabel('months number ')
plt.show()


# 5- what city had the highest number of sales ? 

# In[23]:


result_city = all_data.groupby('City').sum()
result_city


# In[24]:


cities = [city for city,df in all_data.groupby('City')]
plt.bar(cities,result_city['Sales'])
plt.xticks(cities,rotation = 'vertical', size = 8)
plt.ylabel("Sales in usd ($)")
plt.xlabel("city name ")
plt.show()
cities


# 6- what time should we display advertisements likelihood of customer's buying product ?

# In[25]:


all_data.head()


# In[29]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])


# In[30]:


all_data.head()


# In[35]:


all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data['count'] = 1
all_data.head()


# In[43]:


hours = [hour for hour,df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of orders')
plt.grid()
plt.show()


# In[39]:


result = all_data.groupby('Hour').sum()
result


# 7-what product are most often sold togethor ? 

# In[65]:


DF = all_data[all_data['Order ID'].duplicated(keep= False )]
DF['grouped']= DF.groupby('Order ID')['Product'].transform(lambda x :','.join(x))
DF = DF[['Order ID','grouped']].drop_duplicates()
DF.head()


# In[47]:





# In[71]:


from itertools import combinations 
from collections import Counter 
count = Counter()
for row in DF['grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list,2)))
for key,value in count.most_common(10) : 
    print(key,value)
        


# In[73]:


product_group = all_data.groupby('Product')
product_group.sum()


# In[61]:





# In[74]:


Quantity_ordered = product_group.sum()['Quantity Ordered']
products = [product for product,df in product_group]
plt.bar(products, Quantity_ordered)
plt.xticks('Product')
plt.xlabel('Quantity_ordered')
plt.ylabel('Number of orders')
plt.xticks(products,rotation = 'vertical',size = 8)
plt.show()


# In[75]:


prices = all_data.groupby('Product').mean()['Price Each']
print(prices)


# In[80]:


fig,ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.bar(products,Quantity_ordered,color = 'g')
ax2.plot(products,prices,'b-')

ax1.set_xlabel('Product name ')
ax2.set_ylabel('Quantuty ordered',color = 'g')
ax2.set_ylabel('Prices ($)',color = 'b')
ax1.set_xticklabels(products,rotation = 'vertical',size = 8)
plt.show()


# In[ ]:




