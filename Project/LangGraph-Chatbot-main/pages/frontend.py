import streamlit as st
import sys
import os
from backend.core import cleanup


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.core import (
    chatbot,
    save_message_to_db,
    load_conversation,
    retrieve_user_threads,
    add_thread,
    get_langraph_state,
    cleanup,
)
from langchain_core.messages import HumanMessage, AIMessage
import uuid

st.set_page_config(page_title="My Chatbot", page_icon="🤖", layout="wide")


# ---------------- Helpers ----------------
def generate_thread_id():
    return str(uuid.uuid4())


def convert_to_langchain_messages(message_history):
    """Convert message history to LangChain message format"""
    messages = []
    for msg in message_history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    return messages


# ---------------- Session Initialization ----------------
for key in [
    "authenticated",
    "username",
    "thread_id",
    "message_history",
    "new_chat",
    "chat_threads",
]:
    if key not in st.session_state:
        if key == "thread_id":
            st.session_state[key] = generate_thread_id()
        elif key == "message_history":
            st.session_state[key] = []
        elif key == "new_chat":
            st.session_state[key] = True
        elif key == "chat_threads":
            st.session_state[key] = {}
        else:
            st.session_state[key] = False if key == "authenticated" else ""

# ---------------- LOGIN CHECK ----------------
if not st.session_state.get("authenticated", False):
    st.error("🔒 Please login first")
    if st.button("Go to Login"):
        st.switch_page("Login.py")
    st.stop()

try:
    threads = retrieve_user_threads(st.session_state["username"])
    # print("threads", threads)
    # print("before st.session_state['chat_threads']", st.session_state['chat_threads'])
    st.session_state["chat_threads"] = (
        {t["thread_id"]: t["name"] for t in threads} if threads else {}
    )
    # print("after st.session_state['chat_threads']", st.session_state['chat_threads'])
except Exception as e:
    st.error(f"Failed to load conversations: {str(e)}")
    st.session_state["chat_threads"] = {}

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title(f"👤 {st.session_state['username']}")

    try:
        test_threads = retrieve_user_threads(st.session_state["username"])
        # print("test_threads", test_threads)
        st.success("🟢 Connected to Database")
    except Exception as e:
        st.error("🔴 Database Connection Error")
        st.caption(f"Error: {str(e)[:50]}...")

    st.markdown("---")

    if st.session_state.get("thread_id"):
        langraph_state = get_langraph_state(st.session_state["thread_id"])
        # print("langraph_state.......:",langraph_state)
        if langraph_state.get("summary"):
            with st.expander("📝 Conversation Summary"):
                st.write(langraph_state["summary"])

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("Login.py")

    if st.button("💬 New Chat", use_container_width=True):
        new_id = generate_thread_id()
        st.session_state["thread_id"] = new_id
        st.session_state["message_history"] = []
        st.session_state["new_chat"] = True
        st.rerun()

    st.header("📚 My Conversations")

    if st.session_state["chat_threads"]:
        # print("st.session_state['chat_threads']...", st.session_state['chat_threads'])
        # print("reversed(list(st.session_state['chat_threads'].items())", reversed(list(st.session_state['chat_threads'].items())))
        for thread_id, name in reversed(list(st.session_state["chat_threads"].items())):
            display_name = name if name else "Untitled Chat"
            if len(display_name) > 25:
                display_name = display_name[:22] + "..."

            if st.button(
                f"💬 {display_name}",
                key=f"btn_thread_{thread_id}",
                use_container_width=True,
            ):
                try:
                    # print("thread_id", thread_id)
                    st.session_state["thread_id"] = thread_id
                    # print("load_conversation", load_conversation(thread_id))
                    # print("before st.session_state['message_history']", st.session_state['message_history'])
                    st.session_state["message_history"] = load_conversation(thread_id)
                    # print("after st.session_state['message_history']", st.session_state['message_history'])
                    st.session_state["new_chat"] = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load conversation: {str(e)}")
    else:
        st.caption("No conversations yet. Start a new chat!")

    st.markdown("---")
    st.caption("💾 PostgreSQL (Neon)")
    st.caption("🔒 Secure cloud storage")
    st.caption("📝 Auto-summarization enabled")

# ---------------- MAIN CHAT AREA ----------------
st.markdown(
    "<h1 style='text-align: center;'>LangGraph Chatbot with Persistent Memory & Summarization</h1>",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.session_state.get("thread_id"):
        langraph_state = get_langraph_state(st.session_state["thread_id"])
        # print("langraph_state:",langraph_state)
        message_count = len(langraph_state.get("messages", []))
        # print("message_count",message_count)

        if langraph_state.get("summary"):
            st.info(f"📝 Conversation summarized • {message_count} active messages")
        elif message_count > 4:
            st.warning(f"⚡ {message_count}/6 messages (summarization at 6+)")
        else:
            st.success(f"💬 {message_count}/6 messages")


# print("st.session_state['message_history']", st.session_state['message_history'])
for message in st.session_state["message_history"]:
    # print("Display chat history message", message)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Type your message here...")
if user_input:
    try:

        if st.session_state["new_chat"]:
            thread_name = user_input[:30]
            try:
                add_thread(
                    st.session_state["thread_id"],
                    thread_name,
                    st.session_state["username"],
                )
                st.session_state["chat_threads"][
                    st.session_state["thread_id"]
                ] = thread_name
                st.session_state["new_chat"] = False
            except Exception as e:
                st.error(f"Failed to create thread: {type(e).__name__}: {str(e)}")
                print(f"Full error: {e}")
                import traceback

                traceback.print_exc()

        st.session_state["message_history"].append(
            {"role": "user", "content": user_input}
        )

        save_message_to_db(st.session_state["thread_id"], "user", user_input)

        with st.chat_message("user"):
            st.markdown(user_input)

        user_message = HumanMessage(content=user_input)

        response_text = ""
        with st.chat_message("assistant"):
            response_box = st.empty()
            CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}

            try:

                for message_chunk, metadata in chatbot.stream(
                    {"messages": [user_message]}, config=CONFIG, stream_mode="messages"
                ):

                    if (
                        hasattr(message_chunk, "content")
                        and isinstance(message_chunk, AIMessage)
                        and metadata.get("langgraph_node") == "chat_node"
                    ):
                        response_text += message_chunk.content
                        response_box.markdown(response_text)

                if response_text:
                    st.session_state["message_history"].append(
                        {"role": "assistant", "content": response_text}
                    )
                    save_message_to_db(
                        st.session_state["thread_id"], "assistant", response_text
                    )

                langraph_state = get_langraph_state(st.session_state["thread_id"])
                if langraph_state.get("summary"):
                    st.success(
                        "📝 Conversation has been summarized to maintain efficiency!"
                    )

            except Exception as e:
                error_msg = f"❌ Error generating response: {str(e)}"
                response_box.markdown(error_msg)
                st.session_state["message_history"].append(
                    {"role": "assistant", "content": error_msg}
                )
                print(f"Error details: {e}")
                import traceback

                traceback.print_exc()

    except Exception as e:
        st.error(f"❌ Error processing message: {str(e)}")

        with st.chat_message("user"):
            st.markdown(user_input)
        print(f"Outer error details: {e}")
        import traceback

        traceback.print_exc()
