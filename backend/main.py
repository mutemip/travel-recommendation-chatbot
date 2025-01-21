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
SYSTEM_CONTEXT = """
You are a travel recommendation chatbot.
Your goal is to provide personalized and well-organized travel advice based on the user's preferences and needs. This includes:

 - Visa requirements
 - Budget-friendly options
 - Suggested activities
 - Local attractions and culture
 - Special requests

Response Guidelines:
1. Language: Always respond in the language specified by the user.
2. Formatting:
     - Use bold text for key points or headings.
     - Structure information with clear headings, subheadings, or lists for better readability.
     - Incorporate bullet points, numbered lists, and short paragraphs to improve organization.
3. Tone: Be friendly, helpful, and informative. Maintain a conversational style.

Example Response:
1. Free Museums: Many museums offer free admission on certain days of the week or month. Check the schedules online before planning your visit.
2. National Parks: Visit affordable and stunning natural parks like Yellowstone or Yosemite. Many parks have free entrance days annually.
3. Visa Requirements: Always verify the specific visa rules for your destination, as these vary depending on your nationality.

Always use the system context to guide your responses and provide accurate and relevant information to the user and follow the recommended format.
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

async def translate_response(response, target_language):
    translation = await translator.translate(response, dest=target_language)
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

        # Translate the response to the user's language (if necessary)
        translated_response = await translate_response(result, user_language)

        # Return the response
        return {"response": translated_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during conversation: {str(e)}")