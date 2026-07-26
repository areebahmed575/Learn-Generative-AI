import psycopg
import hashlib
import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    RemoveMessage,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from langgraph.graph import MessagesState

load_dotenv()

# ---------------- Database Connection ----------------
DB_URI = os.getenv("DATABASE_URL")
if not DB_URI:
    raise ValueError("DATABASE_URL environment variable is required")

# Create global connection pool
pool = ConnectionPool(
    conninfo=DB_URI, max_size=20, kwargs={"autocommit": True, "prepare_threshold": 0}
)


# ---------------- Database Setup ----------------
def init_db():
    """Initialize PostgreSQL database tables"""
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS threads (
                    thread_id TEXT PRIMARY KEY,
                    name TEXT,
                    username TEXT NOT NULL,
                    FOREIGN KEY(username) REFERENCES users(username)
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id SERIAL PRIMARY KEY,
                    thread_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(thread_id) REFERENCES threads(thread_id)
                )
            """
            )
            conn.commit()


# ---------------- User Management ----------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(username: str, password: str):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (username, password)
                VALUES (%s, %s)
                ON CONFLICT (username) DO UPDATE SET password = EXCLUDED.password
            """,
                (username.strip(), hash_password(password.strip())),
            )
            conn.commit()


def validate_user(username: str, password: str) -> bool:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT password FROM users WHERE username=%s", (username.strip(),)
            )
            row = cursor.fetchone()
            return row and row[0] == hash_password(password.strip())


# ---------------- Chatbot Setup ----------------
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


class State(MessagesState):
    summary: str


def chat_node(state: State):
    summary = state.get("summary", "")
    if summary:
        system_message = f"Summary of conversation earlier: {summary}"
        messages = [SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]

    response = llm.invoke(messages)
    return {"messages": [response]}


def summarize_conversation(state: State):
    summary = state.get("summary", "")
    if summary:
        summary_message = f"This is summary of the conversation to date: {summary}\n\nExtend the summary with the new messages:"
    else:
        summary_message = "Create a summary of the conversation above:"

    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = llm.invoke(messages)

    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}


def should_continue(state: State):
    if len(state["messages"]) > 6:
        return "summarize_conversation"
    return END


# ---------------- LangGraph Checkpointer ----------------
_checkpointer = None


def get_checkpointer():
    global _checkpointer
    if _checkpointer is None:
        _checkpointer = PostgresSaver(pool)
        _checkpointer.setup()
    return _checkpointer


def create_chatbot():
    workflow = StateGraph(State)
    workflow.add_node("chat_node", chat_node)
    workflow.add_node("summarize_conversation", summarize_conversation)
    workflow.add_edge(START, "chat_node")
    workflow.add_conditional_edges("chat_node", should_continue)
    workflow.add_edge("summarize_conversation", END)
    return workflow.compile(checkpointer=get_checkpointer())


chatbot = create_chatbot()


# ---------------- Threads Management ----------------
def retrieve_user_threads(username):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT thread_id, name FROM threads WHERE username=%s", (username,)
            )
            rows = cursor.fetchall()
            return [{"thread_id": r[0], "name": r[1]} for r in rows]


def add_thread(thread_id, name, username):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO threads (thread_id, name, username)
                VALUES (%s, %s, %s)
                ON CONFLICT (thread_id) DO UPDATE SET name = EXCLUDED.name
            """,
                (thread_id, name, username),
            )
            conn.commit()


# ---------------- Messages Management ----------------
def save_message_to_db(thread_id, role, content):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO messages (thread_id, role, content)
                VALUES (%s, %s, %s)
            """,
                (thread_id, role, content),
            )
            conn.commit()


def load_conversation(thread_id):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT role, content FROM messages WHERE thread_id=%s ORDER BY id ASC",
                (thread_id,),
            )
            rows = cursor.fetchall()
    return [{"role": r[0], "content": r[1]} for r in rows]


def get_langraph_state(thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    try:
        state_snapshot = chatbot.get_state(config)
        if state_snapshot and hasattr(state_snapshot, "values"):
            return state_snapshot.values
        return {"messages": [], "summary": ""}
    except Exception as e:
        print(f"Error getting LangGraph state: {e}")
        return {"messages": [], "summary": ""}


# ---------------- Cleanup ----------------
def cleanup():
    try:
        if pool and not pool.closed:
            pool.closeall()
    except:
        pass


# ---------------- Init ----------------
try:
    init_db()
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"❌ Database initialization failed: {e}")
