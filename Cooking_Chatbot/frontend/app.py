from flask import Flask, request, jsonify, render_template
import dotenv 
from google.cloud import dialogflow_v2beta1 as dialogflow
from google.protobuf.json_format import MessageToJson
import json
import pickle
from nltk.corpus import wordnet as wn


config = dotenv.dotenv_values("../.env")
PROJECT_ID = config['PROJECT_ID']


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# NLP function that grabs the food items from the user data queries
# Outputs all previously searched food items from user
def find_food_items(user_queries):
    food = wn.synset('food.n.02')
    food_base = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))

    food_list = list()
    for food in food_base:
        for text in user_queries:
            if text.lower() == food.lower():
                food_list.append(text)
    return food_list


# Run Flask app
if __name__ == "__main__":
    app.run()


# This function will only fire once the webhook is called.
# A webhook is called when a fulfillment is added onto an intent
# This means that webhooks are driven by intent
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    user_query = data['queryResult']['queryText']
    
    # Loading the user models from the pickle file
    user_data = load_user_info()
    
    # A returning user response from the chatbot
    if user_query in user_data:
        user_food_list = find_food_items(user_data[user_query]['queries'])
        user_name = user_data[user_query]['name']
        fulfillment_text = f"Welcome back {user_name}! Here is a list of some ingredients you have searched for previously: {user_food_list}. What other food do you want to search for?"
        webhook_response = {
            "fulfillmentText": fulfillment_text,
            "outputContexts": [
                {
                    "name": "projects/chatbot-project-382920/agent/sessions/unique/contexts/start_recipe_convo-custom-followup"
                }
            ]
        }
        return jsonify(webhook_response)

    # If the user likes curry, return a curry recipe
    if user_query == 'yes':
        fulfillment_text = detect_intent_knowledge(project_id=PROJECT_ID, session_id="unique", knowledge_base_id='projects/chatbot-project-382920/knowledgeBases/MTk5Mzc5OTk1OTk4MzQyMzQ4OA', text='Keema Curry recipe', language_code='en')
        fulfillment_text = "Here is a " + fulfillment_text 
        reply = {
            "fulfillmentText": fulfillment_text,
            "outputContexts": [
                {
                    "name": "projects/chatbot-project-382920/agent/sessions/unique/contexts/start_recipe_convo-custom-followup"
                }
            ]
        }
        return jsonify(reply)
    
    # If user does not like curry, ask for another recipe to search for
    elif user_query == 'no':
        reply = {
            "fulfillmentText": "Thats okay! What other food or ingredient do you like?",
            "outputContexts": [
                {
                    "name": "projects/chatbot-project-382920/agent/sessions/unique/contexts/start_recipe_convo-custom-followup"
                }
            ]
        }
        return jsonify(reply)
    

# API function that sends a message from user to chatbot
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = PROJECT_ID
    
    response = detect_intent_texts(project_id, "unique", message, 'en')
    json_response = MessageToJson(response._pb)
    json_response = json.loads(json_response)

    do_all_user(json_response, message)

    response_text = { "message":  response.query_result.fulfillment_text}
    return jsonify(response_text)


def do_all_user(json_response, message):
    user_data = load_user_info()

    possible_user_name = find_user_name(json_response)

    possible_user_name_alterate_query = find_user_name_alternate_query(json_response)

    user_name = ''
    if possible_user_name != '':
        user_name = possible_user_name
    elif possible_user_name_alterate_query != '':
        user_name = possible_user_name_alterate_query
    
    # Changes .env file dynamically for CURRENT_USER
    if user_name != '':
        dotenv.set_key("../.env", "CURRENT_USER", user_name)
    config = dotenv.dotenv_values("../.env")
    current_user = config['CURRENT_USER']

    # Either create unique user model entry or update user model
    age = find_age(json_response)
    if current_user not in user_data:
        new_user = {
            "name": current_user,
            "age": age,
            "queries": [],
        }
        user_data[current_user] = new_user
        save_user_info(user_data)
    elif current_user in user_data:
        if age:
            user_data[current_user]['age'] = age
        user_data[current_user]['queries'].append(message)
        save_user_info(user_data)
        

# Function to find the name of the user
def find_user_name(json_response):
    user_name = ''
    try:
        user_name = json_response['queryResult']['outputContexts'][-1]['parameters']['person.original']
    except Exception as error:
        print('error: ', error)
    finally:
        return user_name


# Function to find a previous name entered by the user(???)
def find_user_name_alternate_query(json_response):
    user_name = ''
    try:
        user_name = json_response['alternativeQueryResults'][0]['outputContexts'][0]['parameters']['person.original']
    except Exception as error:
        pass
    finally:
        return user_name


# Function to find the age of the user
def find_age(json_response):
    age = ''
    try:
        age = json_response['queryResult']['outputContexts'][-1]['parameters']['age.original']
    except Exception as error:
        pass
    finally:
        return age


# Function to find intents from the chatbot
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response
    

# Function to save a user model into the pickle file
def save_user_info(dict_data):
    try:
        with open('user_data.pickle', 'wb') as file:
            pickle.dump(dict_data, file)
    except Exception as error:
        pass


# Function to load user models from pickle file
def load_user_info():
    data = dict()
    try:
        with open('user_data.pickle', 'rb') as file:
            data = pickle.load(file)
    except Exception as error:
        pass
    finally:
        return data


def detect_intent_knowledge(
    project_id, session_id, language_code, knowledge_base_id, text
):
    """Returns the result of detect intent with querying Knowledge Connector.

    Args:
    project_id: The GCP project linked with the agent you are going to query.
    session_id: Id of the session, using the same `session_id` between requests
              allows continuation of the conversation.
    language_code: Language of the queries.
    knowledge_base_id: The Knowledge base's id to query against.
    texts: A list of text queries to send.
    """
    session_client = dialogflow.SessionsClient()
    session_path = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    knowledge_base_path = knowledge_base_id
    query_params = dialogflow.QueryParameters(
        knowledge_base_names=[knowledge_base_path]
    )

    request = dialogflow.DetectIntentRequest(
        session=session_path, query_input=query_input, query_params=query_params
    )
    response = session_client.detect_intent(request=request)
    return response.query_result.fulfillment_text