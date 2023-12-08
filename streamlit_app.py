import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

import pandas as pd
import numpy as np
import plotly.express as px
import streamlet as st
import matplotlib.pyplot as plt


df = pd.read_csv('indicator.csv', header=0, index_col='no')
df2 = pd.read_csv('SurveyResultWeights.csv', index_col = 0)
adf = pd.read_csv('AdaptiveIndicators.csv', header=0,index_col = 'no')
cdf = pd.read_csv('CopingIndicators.csv', header=0, index_col = 'no')


#idx = pd.Index(range(1, 33, 1))
#df.reindex(idx)
#df.set_index('no',inplace=True)
st.title('Drought Resilience DSS')

Sindicators = []

Cindicators = []

Aindicators = []

for (columnName, columnData) in df.iterrows():
    if columnData["type"] == 's':
        Sindicators.append(columnData["body"])
    if columnData["type"] == 'c':
        Cindicators.append(columnData["body"])
    if columnData["type"] == 'a':
        Aindicators.append(columnData["body"])

susceptability = 0
s1 = 0
s2 = 0
Schoice = st.multiselect('Which susceptibility indicators would you like to use?', (Sindicators))
for item in Schoice:
    for (index, columnData) in df.iterrows():
        if columnData['body'] == item:
            if columnData['display'] == 'slider':
                a = st.slider(columnData['body'], 0, columnData['range'])
                df.amount[index] = a
                df.standard[index] = a/columnData['range']
                s1 += df.loc[index, "standard"]*df.loc[index, "weights"]*df.loc[index, "direction"]
                s2 += df.loc[index, "weights"]
            if columnData['display'] == 'radio':
                a = st.radio(columnData['body'], ['Yes','No'])
                df.amount[index] = a
                df.standard[index] = a
                if df.loc[index, "standard"] == ("Yes"):
                    placeholder=1
                else: 
                    placeholder =0
                s1 += placeholder*df.loc[index, "weights"]*df.loc[index, "direction"]
                s2 += df.loc[index, "weights"]
if s1>0 and s2>0:
    susceptability = s1/s2
    st.write(susceptability)

coping = 0
c1=0
c2=0
Cchoice = st.multiselect('Which coping capacity indicators would you like to use?',  (Cindicators))
for item in Cchoice:
    for (index, columnData) in df.iterrows():
        if columnData['body'] == item:
            if columnData['display'] == 'slider':
                a = st.slider(columnData['body'], 0, columnData['range'])
                df.amount[index] = a
                df.standard[index] = a/columnData['range']
                c1 += df.loc[index, "standard"]*df.loc[index, "weights"]*df.loc[index, "direction"]
                c2 += df.loc[index, "weights"]
            if columnData['display'] == 'radio':
                a = st.radio(columnData['body'], ['Yes','No'])
                if a == 'Yes': 
                    df.amount[index] = 1
                    df.standard[index] = 1
                elif a == 'No':
                    df.amount[index] = 0
                    df.standard[index] = 0
                if df.loc[index, "standard"] == ("Yes"):
                    placeholder=1
                else: 
                    placeholder =0
                c1 += placeholder*df.loc[index, "weights"]*df.loc[index, "direction"]
                c2 += df.loc[index, "weights"]
if c1>0 and c2>0:
    coping = c1/c2
    st.write(coping)

adaptive = 0
a1=0
a2=0
Achoice = st.multiselect('Which adaptive capacity indicators would you like to use?',  (Aindicators))
for item in Achoice:
    for (index, columnData) in df.iterrows():
        if columnData['body'] == item:
            if columnData['display'] == 'slider':
                a = st.slider(columnData['body'], 0, columnData['range'])
                df.amount[index] = a
                df.standard[index] = a/columnData['range']
                a1 += df.loc[index, "standard"]*df.loc[index, "weights"]*df.loc[index, "direction"]
                a2 += df.loc[index, "weights"]
            if columnData['display'] == 'radio':
                a = st.radio(columnData['body'], ['Yes','No'])
                if a == 'Yes': 
                    df.amount[index] = 1
                    df.standard[index] = 1
                elif a == 'No':
                    df.amount[index] = 0
                    df.standard[index] = 0
                a1 += df.loc[index, "amount"]*df.loc[index, "weights"]*df.loc[index, "direction"]
                a2 += df.loc[index, "weights"]
if a2 > 0 and a1 > 0:
    adaptive = a1/a2



col1, col2, col3 = st.columns(3)
#drawing the graph
scircle = plt.Circle(xy =(0,0), radius = 0.75, facecolor = 'white')

labels = ['Resiliense Score', 'other']
values = [susceptability, 1-susceptability]
fig = px.pie(labels, values = values, hole = 0.5,
              names = labels, color = labels,
              title = 'Susceptability Score',
              color_discrete_map = {'score':'blue', 'other': 'black'
             })
fig.update_traces(
                   title_font = dict(size=25,family='Verdana', 
                                     color='darkred'),
                   hoverinfo='label+percent',
                   textinfo='percent', textfont_size=15)
st.plotly_chart(fig)
plt.gca().add_artist(scircle)



ccircle = plt.Circle(xy =(0,0), radius = 0.75, facecolor = 'white')

labels = ['Resiliense Score', 'other']
values = [coping, 1-coping]
fig = px.pie(labels, values = values, hole = 0.5,
              names = labels, color = labels,
              title = 'Coping Capacity Score',
              color_discrete_map = {'score':'blue', 'other': 'black'
             })
fig.update_traces(
                   title_font = dict(size=25,family='Verdana', 
                                     color='darkred'),
                   hoverinfo='label+percent',
                   textinfo='percent', textfont_size=15)
st.plotly_chart(fig)
plt.gca().add_artist(ccircle)

acircle = plt.Circle(xy =(0,0), radius = 0.75, facecolor = 'white')

labels = ['Resiliense Score', 'other']
values = [adaptive, 1-adaptive]
fig = px.pie(labels, values = values, hole = 0.5,
              names = labels, color = labels,
              title = 'Adaptive Capacity Score',
              color_discrete_map = {'score':'blue', 'other': 'black'
             })
fig.update_traces(
                   title_font = dict(size=25,family='Verdana', 
                                     color='darkred'),
                   hoverinfo='label+percent',
                   textinfo='percent', textfont_size=15)
st.plotly_chart(fig)
plt.gca().add_artist(acircle)
