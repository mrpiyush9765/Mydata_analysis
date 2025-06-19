#import all labraily
from itertools import count

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit import columns

st.set_page_config(
    page_title='Consolefare Analytics Portal',
    page_icon='📊'
)
#title
st.title(':rainbow[Data Analusis Portal]',)
st.subheader(':red[Explore data like ease.]',divider='rainbow')

file=st.file_uploader('Drop csv or xlsx file',type=['csv','xlsx'] )
if(file !=None):
    if(file.name.endswith('csv')):
        data=pd.read_csv(file)
    else:
        data=pd.read_excel(file)

    st.dataframe(data)
    st.info("File is Successfully Uploded",icon='✅')

    st.subheader(':rainbow[Basic information of the dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4=st.tabs(['Summary','Top and bottom Rows','Data Types','Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in dataset')
        st.subheader(':gray[Statistical summary of the dataset]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows=st.slider('Nunmar of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))

        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('Nunmar of rows you want', 1, data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))

    with tab3:
        st.subheader(':gray[Data types of column]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader('Column Names in Dataset')
        st.write(list(data.columns))

    st.subheader(':rainbow[Column Valuse to Count]', divider='rainbow')
    with st.expander('Value Count'):
        col1,col2=st.columns(2)
        with col1:
            column=st.selectbox('Choose Column Name',options=list(data.columns))
        with col2:
            toprows=st.number_input('Top rows',min_value=1,step=1)

        count=st.button('Count')
        if (count==True):
            result= data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='gray')
            fig=px.bar(data_frame=result,x=column,y='count',text='count')
            st.plotly_chart(fig)
            fig=px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result, names=column, values='count')
            st.plotly_chart(fig)

    st.subheader(':rainbow[Groupby : Simplify your data analysis]', divider='rainbow')
    st.write('The groupby lets you summarize data by specific categories and groups')

    with st.expander('Group By your columns'):
        col1, col2, col3 = st.columns(3)

        with col1:
            groupby_cols = st.multiselect('Choose your column to groupby', options=list(data.columns))

        with col2:
            operation_col = st.selectbox('Choose column for operation', options=list(data.columns))

        with col3:
            operation = st.selectbox('Choose operation', options=['sum', 'max', 'min', 'mean', 'median', 'count'])
        if(groupby_cols):
            result=data.groupby(groupby_cols).agg(
                newcol=(operation_col,operation)
            ).reset_index()
            st.dataframe(result)


#Data visulization Part
            st.subheader(':gray[Data Visulization]',divider='gray')
            graps=st.selectbox('Choose your graphs',options=['line','bar','scatter','pie','sunburst'])
            if(graps=='line'):
                x_axis = st.selectbox('Choose X axis', options=(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=(result.columns))
                color=st.selectbox('Colar Information',options=[None]+list(result.columns))
                fig=px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)
            elif(graps=='bar'):
                x_axis = st.selectbox('Choose X axis', options=(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=(result.columns))
                color = st.selectbox('Colar Information', options=[None] + list(result.columns))
                facet_col=st.selectbox('Column Information',options=[None] + list(result.columns))
                fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)

            elif(graps=='scatter'):
                x_axis = st.selectbox('Choose X axis', options=(result.columns))
                y_axis = st.selectbox('Choose Y axis', options=(result.columns))
                color = st.selectbox('Colar Information', options=[None] + list(result.columns))
                size=st.selectbox('Size Column',options=[None]+list(result.columns))
                fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color,size=size)
                st.plotly_chart(fig)

            elif(graps=='pie'):
                values=st.selectbox('Choose Numerical Values',options=list(result.columns))
                names = st.selectbox('Choose labels', options=list(result.columns))
                fig=px.pie(data_frame=result,values=values,names=names)
                st.plotly_chart(fig)

            elif(graps=='sunburst'):
                path=st.multiselect('Choose Your Path',options=(result.columns))
                fig=px.sunburst(data_frame=result,path=path,values='newcol')
                st.plotly_chart(fig)








