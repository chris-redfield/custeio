import streamlit as st
from neuralprophet import NeuralProphet
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#### utility functions

@st.cache
def load_data():
  df = pd.read_csv('../data/analise-custeio-v11-3-2019-2016.csv', encoding='iso8859-1')
  df2 = pd.read_csv('../data/analise-custeio-v11-3-2015-2012.csv', encoding='iso8859-1')
  df = pd.concat([df,df2])
  return df

def get_prediction(df):
    df = df.copy()
    df['data'] = df['ID_DIA'].astype(str) + "/" + df['ID_MES'].astype(str) + "/" + df['ID_ANO'].astype(str)
    df_category = pd.DataFrame(df['DESPESAS_PAGAS'].groupby(df['data']).sum())

    df_category.shape

    df_category.index = pd.to_datetime(df_category.index, format="%d/%m/%Y")
    df_category = df_category.sort_index()
    df_category[df_category['DESPESAS_PAGAS'] < 0] = 0
    df_category['DESPESAS_PAGAS'] = df_category['DESPESAS_PAGAS'].rolling(window=15).mean()

    
    df_category = df_category.dropna()
    #df_category2 = df_category[:-300] ## dataframe fica vazio se for menor que isso
    df_category2 = df_category[:'2018-12-31']
    df_category2['ds'] = df_category2.index.copy()
    df_category2['y'] = df_category2.DESPESAS_PAGAS
    df_category2 = df_category2.drop(columns=['DESPESAS_PAGAS'])
    df_category2 = df_category2.reset_index()
    df_category2 = df_category2.drop(columns=['data'])
    
    m = NeuralProphet()
    metrics = m.fit(df_category2, freq="D")
    future = m.make_future_dataframe(df_category2, periods=500)
    forecast = m.predict(future)
    df_category['ds'] = df_category.index.copy()
    df_category['y'] = df_category.DESPESAS_PAGAS
    df_category = df_category.drop(columns=['DESPESAS_PAGAS'])
    df_category = df_category.reset_index()
    df_category = df_category.drop(columns=['data'])
    df_predictions = df_category.merge(forecast[['ds','yhat1']], on='ds', how='left')
    
    return df_predictions

#### utility functions

## Title
st.title('Análise de custeio')

## Loads data
df = load_data()

## Treemap
fig = px.treemap(df, path=['NO_ORGAO', 'NO_NATUREZA_DESPESA_DETA'], values='DESPESAS_PAGAS')
st.plotly_chart(fig)

## Selects
option = st.sidebar.selectbox(
    'Órgão',
     df['NO_ORGAO'].value_counts().index)

'Órgão: ', option

df = df[df['NO_ORGAO'] == option]

option_nd = st.sidebar.selectbox(
    'Despesa',
     df['NO_NATUREZA_DESPESA_DETA'].value_counts().index)

'Despesa: ', option_nd

df = df[df['NO_NATUREZA_DESPESA_DETA'] == option_nd]

## Plots df
df 

## Predicts
predictions = get_prediction(df)
predictions.index = predictions['ds']
predictions = predictions.drop(columns=['ds'])

## Plot predicts
predictions = predictions.rename(columns={"y": "Valor executado", "yhat1": "Valor previsto"})

st.line_chart(predictions)


## Docs
expander = st.beta_expander("Sobre este estudo")
expander.write("Lorem Ipsum...")

