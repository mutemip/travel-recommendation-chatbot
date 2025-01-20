from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langdetect import detect
from googletrans import Translator
import os
from swarmauri.standard.llms.concrete.GroqModel import GroqModel
from swarmauri.standard.messages.concrete.SystemMessage import SystemMessage
from swarmauri.standard.agents.concrete.SimpleConversationAgent import SimpleConversationAgent
from swarmauri.standard.conversations.concrete.MaxSystemContextConversation import MaxSystemContextConversation

# Load environment variables
load_dotenv()

# Fetch the API key from the .env file
API_KEY = os.getenv("API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the system context
# SYSTEM_CONTEXT = """
# You are a travel recommendation chatbot. 
# Provide personalized travel advice based on the user's preferences and needs. 
# Consider factors like destination, budget, activities, and any special requests. 
# Always be friendly and helpful.
# """


SYSTEM_CONTEXT = """
You are a travel recommendation chatbot. 
Provide personalized travel advice based on the user's preferences and needs. 
Consider factors like Visa requirements, destination, budget, activities, and any special requests. 
Always be friendly and helpful.

When providing responses:
 - Use bold text to highlight important information.
 - Format headings, lists, and emphasis for better readability.
 - Respond in the language specified by the user.

Example:
1. Free Museums(In Bold): Many museums offer free admission on certain days of the week or month. 
2. National Parks(In Bold): Visit affordable and stunning natural parks like Yellowstone or Yosemite.
"""


# Initialize a shared conversation instance
conversation = MaxSystemContextConversation()

# Define the Pydantic model for request validation
class MessageRequest(BaseModel):
    message: str
    model: str

# Endpoint to get the list of available models
@app.get("/models")
async def get_models():
    """
    Returns the list of allowed models.
    """
    try:
        llm = GroqModel(api_key=API_KEY)
        return {"models": llm.allowed_models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching models: {str(e)}")


translator = Translator()

def translate_response(response, target_language):
    translation = translator.translate(response, dest=target_language)
    return translation.text

# Endpoint to handle conversation
@app.post("/converse")
async def converse(request: MessageRequest):
    """
    Handles user queries and returns responses from the model.
    """
    try:
        # Detect the language of the user's message
        user_language = detect(request.message)
        # Load the selected model
        llm = GroqModel(api_key=API_KEY, name=request.model)

        # Initialize the conversation agent
        agent = SimpleConversationAgent(llm=llm, conversation=conversation)

        # Set the fixed system context
        agent.conversation.system_context = SystemMessage(content=SYSTEM_CONTEXT)

        # Process the user message
        result = agent.exec(request.message)

        # Translate the response to the user's language(if necessary)
        translated_response = translate_response(result, user_language)

        # Return the response
        return {"response": translated_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during conversation: {str(e)}")
