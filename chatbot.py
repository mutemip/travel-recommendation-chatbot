from dotenv import load_dotenv
import sys
import os
import gradio as gr
from swarmauri.standard.llms.concrete.GroqModel import GroqModel
from swarmauri.standard.messages.concrete.SystemMessage import SystemMessage
from swarmauri.standard.agents.concrete.SimpleConversationAgent import SimpleConversationAgent
from swarmauri.standard.conversations.concrete.MaxSystemContextConversation import MaxSystemContextConversation
import gradio as gr
import csv

# Load environment variables from .env file
load_dotenv()

# Fetch the API key from environment variables
API_KEY = os.getenv("API_KEY")


# Initialize the GroqModel with the API key
llm = GroqModel(api_key=API_KEY)

# Get the available models from the llm instance
allowed_models = llm.allowed_models

# Initialize a MaxSystemContextConversation instance
conversation = MaxSystemContextConversation()

# Define a function to dynamically change the model based on dropdown input
def load_model(selected_model):
    return GroqModel(api_key=API_KEY, name=selected_model)

def converse(input_text, history, system_context, model_name):
    print(f"system_context: {system_context}")
    print(f"Selected model: {model_name}")

    # Initialize the model dynamically based on user selection
    llm = load_model(model_name)

    # Initialize the agent with the new model
    agent = SimpleConversationAgent(llm=llm, conversation=conversation)

    # Set the system context for travel recommendations
    agent.conversation.system_context = SystemMessage(content=system_context)

    # Ensure input text is a string
    input_text = str(input_text)
    print(conversation.history)

    # Execute the input command with the agent
    result = agent.exec(input_text)
    print(result, type(result))

    return str(result)

# Define the system context for travel recommendations
system_context = """
You are a travel recommendation chatbot. 
Provide personalized travel advice based on the user's preferences and needs. 
Consider factors like destination, budget, activities, and any special requests. 
Always be friendly and helpful.
"""

# Set up the Gradio ChatInterface with a dropdown for model selection
demo = gr.ChatInterface(
    fn=converse,
    additional_inputs=[
        gr.Textbox(label="User Preferences (e.g., destination, budget, activities)"),
        gr.Dropdown(label="Model Name", choices=allowed_models, value=allowed_models[0])
    ],
    title="Travel Recommendation Chatbot",
    description="Get personalized travel recommendations based on your preferences."
)

if __name__ == "__main__":
    demo.launch()
