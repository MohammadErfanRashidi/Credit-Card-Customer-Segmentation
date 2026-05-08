# Customer Segmentation with K-Means Clustering & Streamlit Deployment

A professional end-to-end machine learning project that segments credit card customers based on their transaction behaviour. The pipeline covers data cleaning, exploratory analysis, feature engineering, unsupervised clustering and deployment of an interactive web app that instantly classifies new customers and recommends business strategies.

## Live demo:
[Streamlit webapp](https://credit-card-customer-segmentation-unwywetruzwhz85n82jhcd.streamlit.app/)

## Overview

Understanding customer behaviour is essential for targeted marketing, risk management, and product personalisation. This project applies **K-Means clustering** to group credit card users into five distinct segments using engineered behavioural features such as purchase frequency, cash advance dependency and one‑off purchase patterns. The result is a ready‑to‑use **Streamlit application** that classifies any new customer and presents a clear segment name, a descriptive profile, and a tailored business strategy.

---

## Data Cleaning

The raw dataset was rigorously cleaned to ensure high-quality input for modelling:

- **Missing Values**  
  All rows containing null values were dropped to avoid imputation bias.  
- **Logical Inconsistencies**  
  Contradictory records (e.g., negative transaction amounts, impossible repayment ratios) were identified and removed.  
- **Data Integrity**  
  Final verification confirmed no remaining inconsistencies and a clean, reliable dataset.

---

## Exploratory Data Analysis (EDA)

EDA was performed using both **Python** (pandas, matplotlib, seaborn) and **SQL** to gain a multi-angle understanding of the data:

- Distribution analysis of all numerical features  
- Detection of outliers and extreme values  
- Investigation of relationships between spending behaviour, credit limits and payment habits  
- Initial hypothesis generation about potential customer clusters  

---

## Feature Engineering & Preprocessing

A robust feature set was built from raw transactional and account attributes:

1. **Feature Creation**  
   New, domain-driven features were engineered to capture behaviours such as:
   - `cash_advance_ratio` – share of total spending taken as cash advances  
   - `oneoff_share` – proportion of high‑value, single‑purchase transactions  
   - `purchase_frequency` – how often the customer uses the card  
   - `oneoff_purchase_frequency` – frequency of large, one‑off purchases  

2. **Multicollinearity Reduction**  
   - **Multimodality check**: Features with a multimodality score above 0.05 were removed to avoid biasing the clustering algorithm.  
   - **Correlation grouping**: Pairwise absolute correlations were computed. Groups of features with correlation ≥ 0.7 were identified.  
   - Within each group, the feature with the **higher p‑value** (from a significance test of its relationship with a synthetic target) was discarded. If p‑values tied, the one with **higher skew** was removed.  

3. **Skewness & Outlier Treatment**  
   - Features with absolute skewness > 2 were dropped.  
   - Columns containing a large number of outliers were eliminated.  
   - The final feature set retained: **`purchase_frequency`**, **`oneoff_share`**, **`cash_advance_ratio`**, and **`oneoff_purchase_frequency`** – four interpretable and statistically sound dimensions.

---

## Clustering Approach

### Algorithms Tested

- **K‑Means**  
  - Evaluated using **inertia** (elbow method), **silhouette score**, and **Davies-Bouldin index**.  
  - Optimal cluster count determined to be **5**.

- **DBSCAN**  
  - Tested across multiple combinations of `eps` and `min_samples`.  
  - Consistently produced negative silhouette scores, indicating the data has well‑separated spherical clusters – better suited for K‑Means.

### Final Model

**K‑Means with 5 clusters** was selected and trained on the scaled feature set. The model, the scaler, and the cluster profiles were serialised (`.pkl` and `.json`) for deployment.

### Cluster Interpretation

Principal Component Analysis (PCA) and 3D visualisations were used to explore the separation of clusters. For each segment, mean/median values of the original features were compared against the global average to describe the group's behaviour. Bar plots illustrated the characteristic strengths of each cluster.

---

## Customer Segments & Business Strategies

| Cluster | Segment Name               | Profile                                                                 | Strategy                                                                                     |
|---------|----------------------------|-------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| 0       | Cash‑Advance Dependent     | Rarely buys, cash advances dominate, low credit limit, rarely pays full | Risk containment, financial education, offer personal loans instead of cash advances         |
| 1       | Everyday Super Users       | Frequent small purchases, avoid cash advances, often pay full, high limit | Loyalty rewards, cashback, premium card upgrades, cross‑sell travel & insurance             |
| 2       | Mixed Spenders with Cash Need | High cash advance AND many big purchases, moderate payment behaviour   | Balance transfer offers, instalment plans, monitor for delinquency                            |
| 3       | High‑Volume Balanced Spenders | Extremely active, both small and large purchases, very few cash advances | Premium cards, higher credit lines, concierge services, retention campaigns                  |
| 4       | Big Ticket Spenders        | Infrequent but very large purchases, rarely use cash advances, high limit | Encourage everyday use with bonus points, instalment options for large items                 |

---

## Deployment – Streamlit Web App

An interactive application was built with **Streamlit** to provide instant, business‑ready predictions:

- **Input**: Total Purchases, Total Cash Advances, Tenure (months), One-Off Purchases, Purchases Frequency, One-Off Purchases Frequency.  
- **Processing**:  
  - `cash_advance_ratio` and `oneoff_share` are computed the way we calculated them in feature notebook.  
  - Features are scaled using the saved `scaler.pkl`.  
  - The K‑Means model assigns a cluster.  
- **Output**: The segment name, a detailed description, and the recommended strategy are displayed, pulled from `segment_map.json`.

The app is designed for non‑technical stakeholders, making the machine learning output actionable with zero friction.

---

## Repository Structure

```plaintext
.
├── app.py
├── data
│   ├── app_data.csv
│   ├── credit_card_cleaned.csv
│   ├── credit_card.csv
│   └── credit_card_final.csv
├── LICENSE
├── model
│   ├── kmeans_model.pkl
│   ├── scaler.pkl
│   └── segment_map.json
├── notebooks
│   ├── cleaning.ipynb
│   ├── eda.ipynb
│   ├── feature.ipynb
│   └── modeling.ipynb
├── README.md
├── requirements.txt
└── sql
    └── eda.sql
```

---

## Results & Impact

- **Interpretable Segmentation** – Five stable, business‑meaningful customer groups replace arbitrary heuristics.  
- **Actionable Strategies** – Each segment has a clear, targeted recommendation that can be executed by marketing, risk, or product teams.  
- **Reproducible & Scalable** – The entire feature engineering and modelling pipeline is documented and can be retrained on new data.  
- **Instant Classification** – The Streamlit app eliminates the gap between data science output and day‑to‑day business decisions.

---

## Technologies Used

- **Python** (pandas, NumPy, scikit‑learn, SciPy)  
- **Jupyter Notebook** – Exploratory analysis and modelling  
- **Streamlit** – Web application  
- **SQL** – Initial data exploration  
- **Matplotlib & Seaborn** – Visualisations  
- **PCA** – Dimensionality reduction for visual interpretation  

---
