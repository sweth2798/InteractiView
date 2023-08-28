from flask import Flask, request, jsonify

from llmagentv2 import generateResponse, generateSqlQuery
from datastore import MySql, Dremio
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


app = Flask(__name__)

@app.route('/interactiview', methods=['POST'])
def getResponseFromLLM():
    try:
        data = request.get_json()
        datastore = data['datastore']
        input = data['query']

        sqlQuery = generateSqlQuery(input)
        logging.info("LLM Generated SQL Query: " + sqlQuery)

        db = None
        if datastore == 'MySQL':
            db = MySql('root', 'manage', 'wmb2b-db', '3306', 'b2bswag')
        elif datastore == 'Dremio':
            db = Dremio('b2bdremio', 'Dremio@123', 'dremio-oss', '31010', 'knockout',
                        'dremio-jdbc-driver.jar')

        resultSet = db.executeQuery(db.getConnection(), sqlQuery)

        print("SQL Query Result: " + resultSet.__str__())
        logging.info("SQL Query Result: " + resultSet.__str__())

        response = generateResponse(input, sqlQuery, resultSet)
        logging.info("LLM Generated Response: " + response)

        return json.loads(response)  # Convert the response to JSON format

    except Exception as e:
        logging.error("Error: "+ e.__str__())
        return jsonify({'error': 'There was some issue while processing the query. Please refine your query or narrow '
                                 'down your search criteria' + e.__str__()}), 400  # Bad Request

if __name__ == '__main__':
    app.run(debug=True, port=9097)

