from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
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
Consider factors like destination, budget, activities, and any special requests. 
Always be friendly and helpful.

When providing responses:
- Use markdown for formatting.
- Format headings, lists, and emphasis using markdown syntax.
- Bold key terms or phrases directly without using `**`. For example, use `**Free Museums**` to render it as bold in markdown.

Example:
1. **Free Museums**: Many museums offer free admission on certain days of the week or month. 
2. **National Parks**: Visit affordable and stunning natural parks like Yellowstone or Yosemite.
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

# Endpoint to handle conversation
@app.post("/converse")
async def converse(request: MessageRequest):
    """
    Handles user queries and returns responses from the model.
    """
    try:
        # Load the selected model
        llm = GroqModel(api_key=API_KEY, name=request.model)

        # Initialize the conversation agent
        agent = SimpleConversationAgent(llm=llm, conversation=conversation)

        # Set the fixed system context
        agent.conversation.system_context = SystemMessage(content=SYSTEM_CONTEXT)

        # Process the user message
        result = agent.exec(request.message)

        # Return the response
        return {"response": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during conversation: {str(e)}")
