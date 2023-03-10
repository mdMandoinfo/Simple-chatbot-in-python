import json
import re
from Tkinter import *

# create a context variable
context = ""

# Function to get the bot's response for a given user input
def get_bot_response(user_input):
    global context
    # Get dataset from intents.json file
    with open("intents.json", "r") as json_file:
        data = json.load(json_file)

    intents = data["intents"]
    for intent in intents:
        # check if the intent has the current context
        if context in intent["context"]:
            patterns = intent["patterns"]
            for pattern in patterns:
                match = re.search(pattern.lower(), user_input.lower())
                if match:
                    context = intent["tag"]
                    return intent["responses"][0]
    # set context to none if there is no match
    context = ""
    return "I am sorry, I do not understand what you are saying."
    
# Function to handle sending a message
def send_message(event=None):
    user_input = user_input_field.get()
    conversation_history.config(state=NORMAL)
    conversation_history.insert(INSERT, "You: " + user_input + "\n")
    conversation_history.config(state=DISABLED)
    conversation_history.see(END) 
    if user_input.lower() == "quit":
        bot_response = "Goodbye, have a nice day!"
    else:
        bot_response = get_bot_response(user_input)
    conversation_history.config(state=NORMAL)
    conversation_history.insert(INSERT, "Chatbot: " + bot_response + "\n")
    conversation_history.config(state=DISABLED)
    conversation_history.see(END) 
    user_input_field.delete(0, END)
    
# Function to clear the conversation history
def clear_history():
    conversation_history.config(state=NORMAL)
    conversation_history.delete(1.0, END)
    conversation_history.config(state=DISABLED)

# Function to clear the user input field
def clear_input():
    user_input_field.delete(0, END)
root = Tk()
root.title("Chatbot")
root.geometry("700x750")

conversation_history = Text(root, bg='white')
conversation_history.config(state=DISABLED)
conversation_history.pack()

user_input_frame = Frame(root)
user_input_frame.pack()

user_input_field = Entry(user_input_frame)
user_input_field.bind("<Return>", send_message)
user_input_field.pack(side=LEFT)

send_button = Button(user_input_frame, text="Send", command=send_message)
send_button.pack(side=LEFT)

clear_history_button = Button(user_input_frame, text="Clear History", command=clear_history)
clear_history_button.pack(side=LEFT)

clear_input_button = Button(user_input_frame, text="Clear Input", command=clear_input)
clear_input_button.pack(side=LEFT)

print("Chatbot: Hello, How can I help you today?")
conversation_history.config(state=NORMAL)
conversation_history.insert(INSERT, "Chatbot: Hello, How can I help you today?\n")
conversation_history.config(state=DISABLED)
root.mainloop()
