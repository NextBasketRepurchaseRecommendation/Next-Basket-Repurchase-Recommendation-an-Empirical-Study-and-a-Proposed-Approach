# Pre-processing and Partitioning Datasets for ''Next Basket Repurchase Recommendation - an Empirical Study and a Proposed Approach"

This repository contains code for pre-processing and partitioning the datasets used 
in the Paper ''Next Basket Repurchase Recommendation - an Empirical Study and a Proposed Approach".


## Datasets
We consider the following datasets:

1. [Instacart](https://www.kaggle.com/c/instacart-market-basket-analysis/data):  The dataset consists of transactional data and items’ metadata. The items’ metadata was used for the
analysis in Section 2, and the transactional data was used for the experimental evaluation in Section 5. The transactional data
in Instacart contains 30M transactions collected over a year from Instacart’s grocery service. These transactions are associated with 3M baskets corresponding to 206K users.

2. [Dunnhumby](https://www.dunnhumby.com/source-files/): This dataset is based on two years of household transactions associated with 2.5K frequent shoppers. The dataset comprises 2M transactions associated with 270K baskets.

3. [ValuedShopper](https://www.kaggle.com/competitions/acquire-valued-shoppers-challenge/data) : This dataset contains 350M transactions collected over a year from an online grocery
service. These transactions are associated with 30M baskets corresponding to 300K users

## Pre-processing

For all the datasets:
1. Items that were purchased less than 20 times were removed.
2. Users with less than 11 baskets were discarded.

In addition, the following procedures were carried for pre-processing Instacart's and ValuedShopper's datasets:
1. The timestamps in the Instacart dataset are given in a differential manner. Allegedly, the real timestamps can be computed using an
accumulative sum. However, we noticed that the maximal difference between two consecutive baskets is trimmed by
the maximal value of 30 days, making it irreversible to compute the original timestamps. Hence, we discarded users that did not place any order for more than 30 days.
2.  Unlike the rest of the datasets, ValuedShopper's dataset does not contain unique product ids. In order to mitigate this, we created unique product ids by hashing the concatenation of the
product’s brand id, company id, and category id, which are all available in the dataset.
3.  Users sampling - In order to face the large amounts of transactional data in the ValuedShopper dataset, we followed the same procedure from [here](https://dl.acm.org/doi/10.1145/3397271.3401066) and randomly sampled 10K users. 

## Partitioning
We followed the the following convention: the training data for each user consists of all baskets except for the last one. 
The remaining baskets are randomly split into test (50%) and validation (50%).

## Usage
To pre-process and partition the datasets, follow these steps:
1. Clone this repository to your local machine.


2. Install the requirements: ```pip install -r requirements.txt```.


3. Download the datasets to  ```.\raw_data\ ``` (the links can be found on the **Datasets** section above).

4. Run ```preprocess_all_datasets.bat``` for Windows OS and ```preprocess_all_datasets.sh``` for Linux OS.


5. The pre-processed files will be written to  ```.\preprocessed_data\ ```.


## License
This project is licensed under the MIT License - see the LICENSE file for details.



