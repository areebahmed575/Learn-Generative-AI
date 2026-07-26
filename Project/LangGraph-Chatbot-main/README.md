# 🧠 LangGraph AI Assistant with Persistent Memory & Summarization

A sophisticated AI chatbot application built with **Streamlit**, **LangGraph**, and **PostgreSQL** featuring intelligent conversation management, real-time streaming, and automatic summarization.

## ✨ Features

### 🤖 **Lanchain and Langgraph Capabilities**
- **Memory-Enabled Conversations**: AI remembers context across messages
- **Real-Time Streaming**: Instant response generation with live typing indicators
- **Intelligent Summarization**: Automatic conversation summarization when reaching message limits
- **Persistent Chat History**: All conversations saved and retrievable

### 🔐 **Security & Authentication**
- **Secure User Authentication**: Password-protected user accounts
- **Session Management**: Secure session handling
- **Data Privacy**: User data isolation and protection
- **Cloud Database**: Secure PostgreSQL (Neon) integration

### 💾 **Data Management**
- **Thread-Based Conversations**: Organized chat management
- **Auto-Save**: Real-time message saving
- **Conversation History**: Access all past conversations
- **Cloud Storage**: Data persistence across sessions

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database (Neon Cloud recommended)
- OpenAI API key or compatible LLM provider

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/langgraph-ai-assistant.git
   cd langgraph-ai-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Database Configuration
   DATABASE_URL=your_postgresql_connection_string
   
   # AI Model Configuration
   GOOGLE_API_KEY=your_google_api_key
   MODEL_NAME=gemini-2.0-flash  # or your preferred model
   ```

4. **Run the application**
   ```bash
   streamlit run Login.py
   ```

## 🛠️ Configuration

### Database Setup (Neon PostgreSQL)

1. **Create a Neon account** 
2. **Create a new project** and database
3. **Copy the connection string** to your `.env` file
4. **Run the initialization script** to create tables

### AI Model Configuration
Update your `.env` file with the appropriate API keys and model names.


## 📋 Requirements

### Python Dependencies
```txt
streamlit
langgraph
langgraph-checkpoint-postgres
langchain-google-genai
langchain-core
psycopg-binary
psycopg-pool
python-dotenv
```


