## Travel Recommendation Chatbot Frontend
- This is the frontend for the Travel Recommendation Chatbot, which provides personalized travel advice based on user preferences. The frontend is built using React and communicates with the backend to fetch travel recommendations.

## Features
   - **User-Friendly Interface:** A simple and intuitive interface for easy interaction with the chatbot.
   - **Model Selection:** Allows users to select different language models for enhanced conversational capabilities.
   - **Multilingual Support:** Supports multiple languages for a broader audience.
   - **Real-Time Chat:** Provides real-time chat functionality with the chatbot.
   - **Export Chat History:** Allows users to export their chat history.

## Installation
- To set up the frontend locally, follow these steps:

 1. Clone the repository:
```sh
    git clone https://github.com/mutemip/travel-recommendation-chatbot.git
    cd swamauri/frontend
```
 2. Install dependencies:
 ```sh
    npm install
 ```
 3. Start development server
 ```sh
 npm start
 ```

 - This will run the app in development mode. Open <http://localhost:3000> to view it in your browser.

## Components
- `App.js:` The main component that sets up the application layout and handles state management.
- `Chatbot.js:` The component that renders the chat interface and handles message display.
- `ChatInterface.jsx:` The component that provides the chat interface with input and message display.
- `InputBox.js:` The component that provides the input box for users to type messages.
- `Message.js:` The component that renders individual messages in the chat.
- `Sidebar.js:` The component that provides settings for model and language selection.

## Configuration
#### Environment Variables
- The frontend communicates with the backend at <http://localhost:8000> by default. Ensure that the backend server is running and accessible at this URL.

#### Model and Language Selection
- The frontend allows users to select different language models and languages. The available models are fetched from the backend and displayed in a dropdown menu.