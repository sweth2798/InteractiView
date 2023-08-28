import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from llmagent import generateResponse, generateSqlQuery
from datastore import MySql, Dremio


def decode_response(response: str) -> dict:
    return json.loads(response)


def write_response(response_dict: dict):
    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("x-axis", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("x-axis", inplace=True)
        st.line_chart(df)

    # Check if the response is a pie chart
    if "pie" in response_dict:
        data = response_dict["pie"]
        plt.pie(data['y-axis'], labels=data['x-axis'], startangle=90)
        st.pyplot()

    if "wordcloud" in response_dict:
        data = response_dict["wordcloud"]
        label_count_dict = {label: count for label, count in zip(data['x-axis'], data['y-axis'])}
        wordcloud = WordCloud(width=800, height=800, background_color='white').generate_from_frequencies(
            label_count_dict)
        plt.figure(figsize=(8, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot()

    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)


st.title("InteractiView")

datastore = st.selectbox(
    'Datastore to query',
    ('MySQL', 'Dremio'))

input = st.text_area("Insert your query")

st.set_option('deprecation.showPyplotGlobalUse', False)

if st.button("Submit Query", type="primary"):
    try:
        sqlQuery = generateSqlQuery(input)

        db = None

        if datastore == 'MySQL':
            db = MySql('root', 'manage', 'localhost', '5306', 'b2bswag')
        elif datastore == 'Dremio':
            db = Dremio('b2bdremio', 'Dremio@123', 'localhost', '31010', 'knockout',
                        'C:/Learning/Code/Python/PycharmProjects/pythonProject/streamlit/dremio-jdbc-driver.jar')

        resultSet = db.executeQuery(db.getConnection(), sqlQuery)
        print("SQL Query Result: " + resultSet.__str__())

        response = generateResponse(input, sqlQuery, resultSet)
        # Decode the response.
        decoded_response = decode_response(response)

        # Write the response to the Streamlit app.
        write_response(decoded_response)
    except Exception as e:
        st.write("There was some issue while processing the query. Please refine your query or narrow down your search criteria")



