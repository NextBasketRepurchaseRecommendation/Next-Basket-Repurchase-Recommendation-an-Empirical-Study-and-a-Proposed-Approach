""" Code for preprocessing Instacart's dataset
Usage:
    1. Download Instacart's dataset to ".\raw_data\Instacart\"
    2. exectue .\preprocess_instacart.py
"""
print('---------------------------------------------------------------------------------------')
print('Preprocessing Instacart''s dataset')
##
import pandas as pd
import numpy as np
import os

MIN_BASKETS_PER_USER=10
MIN_PURCHASES_PER_ITEM=20
NUM_SAMPLED_USERS=10_000

## load dataset
dataset_name='instacart'
raw_data_path=os.path.join('raw_data',dataset_name)
orders1_file_path = os.path.join(raw_data_path,"order_products__prior.csv")
orders2_file_path = os.path.join(raw_data_path,"order_products__train.csv")
orders_file_path = os.path.join(raw_data_path,"orders.csv")

df_orders_metadata = pd.read_csv(orders_file_path)
df_baskets1 = pd.read_csv(orders1_file_path)
df_baskets2 = pd.read_csv(orders2_file_path)
df_baskets = pd.concat([df_baskets1,df_baskets2])
df = pd.merge(df_orders_metadata,df_baskets,how='inner')
df = df.rename(columns={'order_id':'basket', 'product_id':'item', 'user_id':'user'})
df=df[['user','basket','order_number','days_since_prior_order','item']]

## removed items that were purchased less than 20 times
items_counter_df=df.groupby(['item']).apply(lambda x: len(x)).sort_values()
items_to_remove=items_counter_df[items_counter_df<MIN_PURCHASES_PER_ITEM]
df=df[~df['item'].isin(items_to_remove.index)]


##  remove users with less than 11 baskets and users with trimmed timestamps, sample 10K of them
valid_users_df=df.groupby(['user']).apply(lambda x: ~((x['days_since_prior_order']==30).any()) & (x['basket'].nunique()>=MIN_BASKETS_PER_USER))
valid_users_df.value_counts()
list_of_valid_users=valid_users_df[valid_users_df].index
list_of_valid_users=np.random.choice(list_of_valid_users,NUM_SAMPLED_USERS)
df=df[df['user'].isin(list_of_valid_users)]

## compute explicit timestamps
def get_explicit_timestamp(x):
    tmp = (x.sort_values('order_number')[['order_number','days_since_prior_order']].set_index('order_number')
           .fillna(0).groupby(level=0).last().cumsum().astype(int).rename(columns={'days_since_prior_order':'day'}))
    return pd.merge(x,tmp,left_on=['order_number'],right_index=True)

df=df.groupby(['user']).apply(lambda x: get_explicit_timestamp(x)).droplevel(0)
df=df[['user','basket','day','item','order_number']]

## partition train/test/validation
last_baskets = df[['user','basket','order_number']].drop_duplicates().groupby('user')\
    .apply(lambda grp: grp.nlargest(1, 'order_number'))['basket'].values

test_baskets=np.random.choice(last_baskets,int(0.5*len(last_baskets)),replace=False)
validation_baskets=[b for b in last_baskets if not(b in test_baskets)]

## save preprocessed dataframes
df=df[['user','basket','day','item']]
test_df=df[df['basket'].isin(test_baskets)]
validation_df=df[df['basket'].isin(np.array(validation_baskets))]
train_df=df[~df['basket'].isin(last_baskets)]

preprocessed_data_path=os.path.join('preprocessed_data',dataset_name)
if not(os.path.exists(preprocessed_data_path)):
    os.makedirs(preprocessed_data_path)

test_df.to_csv(os.path.join(preprocessed_data_path,'test_data.csv'),index=False)
train_df.to_csv(os.path.join(preprocessed_data_path,'train_data.csv'),index=False)
validation_df.to_csv(os.path.join(preprocessed_data_path,'validation_data.csv'),index=False)

print(' Train baskets were written to %s'%os.path.join(os.path.curdir,preprocessed_data_path, 'train_data.csv'))
print(' Validation baskets were written to %s'%os.path.join(os.path.curdir,preprocessed_data_path, 'validation_data.csv'))
print(' Test baskets were written to %s'%os.path.join(os.path.curdir,preprocessed_data_path, 'test_data.csv'))