""" Code for preprocessing Valuedshopper's dataset
Usage:
    1. Download Valuedshopper's dataset to ".\raw_data\ValuedShopper\"
    2. exectue .\preprocess_valuedshopper.py
"""
print('---------------------------------------------------------------------------------------')
print('Preprocessing ValuedShopper''s dataset')
##
import pandas as pd
import numpy as np
import os

MIN_BASKETS_PER_USER=10
MIN_PURCHASES_PER_ITEM=20
NUM_SAMPLED_USERS=10_000

## load dataset
dataset_name='valuedshopper'
raw_data_path=os.path.join('raw_data',dataset_name)
path_to_raw_data=os.path.join(raw_data_path,"transactions.csv")

df = pd.read_csv(path_to_raw_data,nrows=5_000_000)
df['day']=pd.to_datetime(df['date'],format='%Y-%m-%d')
df['day']=(df['day'] -df['day'].min()).dt.days
df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d').dt.strftime('%Y%m%d').astype(int)
df['basket'] = df['date'].astype(str)+'_'+df['id'].astype(str)
df['item'] = df['dept'].astype(str)+'_'+df['category'].astype(str)+"_"+df['brand'].astype(str)+'_'+df['company'].astype(str)
df['user'] = df['id'].astype(str)
df=df[['user','basket','day','item']]

## removed items that were purchased less than 20 times
items_counter_df=df.groupby(['item']).apply(lambda x: len(x)).sort_values()
items_to_remove=items_counter_df[items_counter_df<MIN_PURCHASES_PER_ITEM]
df=df[~df['item'].isin(items_to_remove.index)]

##  remove users with less than 11 baskets, sample 10K of them
users_baskets_counter_df=df.groupby(['user']).apply(lambda x: x['basket'].nunique()).sort_values()
users_to_remove=users_baskets_counter_df[users_baskets_counter_df<MIN_BASKETS_PER_USER]
df=df[~df['user'].isin(users_to_remove.index)]
all_users_list=df['user'].values
sampled_users=np.random.choice(all_users_list,NUM_SAMPLED_USERS,replace=False)
df=df[df['user'].isin(sampled_users)]

## partition train/test/validation
last_baskets = df[['user','basket','day']].drop_duplicates().groupby('user')\
    .apply(lambda grp: grp.nlargest(1, 'day'))['basket'].values

test_baskets=np.random.choice(last_baskets,int(0.5*len(last_baskets)),replace=False)
validation_baskets=[b for b in last_baskets if not(b in test_baskets)]

len(test_baskets)
len(validation_baskets)

## save preprocessed dataframes
test_df=df[df['basket'].isin(test_baskets)]
validation_df=df[df['basket'].isin(np.array(validation_baskets))]
train_df=df[~df['basket'].isin(last_baskets)]

preprocessed_data_path =os.path.join('preprocessed_data',dataset_name)
if not(os.path.exists(preprocessed_data_path)):
    os.makedirs(preprocessed_data_path)
test_df.to_csv(os.path.join(preprocessed_data_path, 'test_data.csv'),index=False)
train_df.to_csv(os.path.join(preprocessed_data_path, 'train_data.csv'),index=False)
validation_df.to_csv(os.path.join(preprocessed_data_path, 'validation_data.csv'),index=False)

print(' Train baskets were written to %s'%os.path.join(os.path.curdir,preprocessed_data_path, 'train_data.csv'))
print(' Validation baskets were written to %s'%os.path.join(os.path.curdir,preprocessed_data_path, 'validation_data.csv'))
print(' Test baskets were written to %s'%os.path.join(os.path.curdir,preprocessed_data_path, 'test_data.csv'))