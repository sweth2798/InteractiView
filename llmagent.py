import openai

openai.api_key = "<OPENAI_KEY>"


def generateSqlQuery(input):
    prompt = '''For the following input query, generate SQL query on the table 'Transaction', 'TransactionAttribute' 
    and 'TransactionLog'. 'Transaction' table has the following columns 'TransactionID', 'DocTypeID', 'DocTypeName', 
    'SenderID', 'SenderName', 'ReceiverID', 'ReceiverName', 'NativeID', 'TransactionTimestamp', 'ProcessingStatus', 
    'GroupID', 'ConversationID', 'UserStatus'. 'TransactionID' is the unique identifier of a transaction. 
    'ProcessingStatus' column can have any of the following values - 'ABORTED', 'ACCEPTED', 'ACCEPTED W/ ERRORS', 
    'DONE', 'DONE W/ ERRORS', 'NEW', 'NOT DELIVERED', 'NOT ROUTED', 'POLLABLE', 'QUEUED', 'REPROCESSED', 'REPROCESSED 
    AND ABORTED', 'REPROCESSED W/ ERROR', 'REPROCESSING', 'RESUBMITTED', 'RESUBMITTED AND ABORTED', 'RESUBMITTED W/ 
    ERROR', 'RESUBMITTING'. 'TransactionAttribute' table has the following columns 'TransactionID','AttributeID', 
    'AttributeName', 'AttributeType', 'StringAttributeValue', 'NumberAttributeValue', 'DateAttributeValue'. 
    'TransactionLog' table has the following columns 'LogID', 'TransactionID', 'LogTimestamp', 'LogStatus', 'LogClass', 
    'Message', 'DetailedMessage', 'B2BUser', 'SenderName', 'ReceiverName'. 'LogStatus' column can have any of the following values - "ERROR", 
    "WARNING", "INFO". 'TransactionLog' table records progress of transactions. Write only the SQL query for this 
    Natural Language. Nothing else should be included in the output except the SQL query. Here is the input query - 
    ''' + input
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=0.1
    )
    sqlQuery = response.choices[0].message["content"]
    print("LLM Generated SQL Query: " + sqlQuery)
    return sqlQuery


def generateResponse(input, sqlQuery, resultSet):
    prompt = """
                For the following query, this is the resultset: """ + resultSet.__str__() + ''',
                
                If the query requires drawing a table, reply as follows:
                {"table": {"columns": ["column1", "column2", ...], "data": [[A, B, ...], [D, C, ...], ...]}}

                If the query requires creating a bar chart, reply as follows:
                {"bar": {"x-axis": ["A", "B", "C", ...], "y-axis": [25, 24, 10, ...]}}

                If the query requires creating a line chart, reply as follows:
                {"line": {"x-axis": ["A", "B", "C", ...], "y-axis": [25, 24, 10, ...]}}
                
                If the query requires creating a pie chart, reply as follows:
                {"pie": {"x-axis": ["A", "B", "C", ...], "y-axis": [25, 24, 10, ...]}}
                
                If the query requires creating a wordcloud, reply as follows:
                {"wordcloud": {"x-axis": ["A", "B", "C", ...], "y-axis": [25, 24, 10, ...]}}

                There can only be 4 types of chart, "bar", "line", "pie" and "wordcloud".

                If it is just asking a question that requires neither, reply as follows:
                {"answer": "answer"}
                Example:
                {"answer": "The title with the highest rating is 'Gilead'"}

                If you do not know the answer, reply as follows:
                {"answer": "I do not know."}

                Return all output as a string.

                All strings in "columns" list and data list, should be in double quotes,

                For example: {"columns": ["title", "ratings_count"], "data": [["Gilead", 361], ["Spider's Web", 5164]]}

                Lets think step by step.

                Below is the query.
                Query: 
                ''' + input + '''

                SQLQuery:
                ''' + sqlQuery

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=0.1
    )
    response = response.choices[0].message["content"]
    print("LLM Generated Response: " + response)
    return response
