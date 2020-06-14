from rasa.nlu.model import Interpreter
import os
from functions import *
import json

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# load rasa nlu model
rasa_trained_model_path = r'models/nlu'
rasa_interpreter = Interpreter.load(rasa_trained_model_path)


# retrieve the nlu output from rasa
def get_rasa_output(msg):
    msg = str(msg).strip().lower()
    return rasa_interpreter.parse(msg)


print("Hello! Welcome to Festo Process Automation Workstation, how can I help you?")
print(" (you can print \"stop\" at any time to terminate)")
user_input = input("Your message:")

# with open('back_up_test.txt', 'r') as text_questions:
#     lines = text_questions.readlines()
#
# for line in lines:
#     if len(line) < 2:
#         print()
#         continue
#     user_input = line
#     print("* {}".format(line))

# Keep get user input
while user_input != "stop":
    print(" - ", end="")
    rasa_output = get_rasa_output(user_input)
    # If want to check the output from rasa
    print(json.dumps(rasa_output, indent=4))

    # If the intent confidence is not high enough, re-ask the question
    if rasa_output["intent"]["confidence"] < 0.95:
        print("Sorry, I didn't understand your question. You may try another question")
        user_input = input("Your message:")
        continue
    intent = rasa_output["intent"]["name"]
    # If different intent is detected
    if "greet" in intent:
        print("Hi there~")
    elif "goodbye" in intent:
        print("Bye~")
    elif "thank" in intent:
        print("You'are welcome, it's my pleasure")
    elif "search_item" in intent:
        if len(rasa_output["entities"]) < 1:
            print("Sorry, I cannot find this item. You may try another question")
            user_input = input("Your message:")
            continue
        item = rasa_output["entities"][0]["value"]
        if find_item(item):
            print("Yes, there is a {}".format(item))
        else:
            print("Sorry, I cannot find {} here".format(item))
    elif "search_action" in intent:
        if len(rasa_output["entities"]) < 2:
            print("Sorry, I cannot find this action. You may try another question")
            user_input = input("Your message:")
            continue
        if "do" in rasa_output["entities"][0]["entity"]:
            do = rasa_output["entities"][0]["value"]
            item = rasa_output["entities"][1]["value"]
        else:
            item = rasa_output["entities"][0]["value"]
            do = rasa_output["entities"][1]["value"]
        response = find_action(do, item)
        if len(find_action(do, item)) > 0:
            print(response)
        else:
            print("Sorry, I cannot find this action")
    elif "relationship_item" in intent:
        if len(rasa_output["entities"]) < 2:
            print("Sorry, I cannot find their relation. You may try another question")
            user_input = input("Your message:")
            continue
        item1 = rasa_output["entities"][0]["value"]
        item2 = rasa_output["entities"][1]["value"]
        if find_relationship_items(item1, item2) or find_relationship_items(item2, item1):
            print("Yes")
        else:
            print("No")
    elif "search_data_type" in intent:
        if len(rasa_output["entities"]) < 1:
            print("Sorry, I cannot find this data type. You may try another question")
            user_input = input("Your message:")
            continue
        data_type = rasa_output["entities"][0]["value"]
        response = find_data_type(data_type)
        if len(response) > 0:
            print(response)
        else:
            print("Sorry, I cannot find this data type.  You may try another question")
    else:
        print("Sorry, I didn't understand your question. You may try to rephrase the question")
    user_input = input("Your message:")
