from langgraph.graph import START,END,StateGraph
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
from typing import TypedDict, Annotated
import sqlite3

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=api_key,
    temperature=0
)

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def chat_node(state:ChatState):
    messages=state['messages']
    response=llm.invoke(messages)

    return {'messages':[response]}

conn=sqlite3.connect(database='chatbot.db',check_same_thread=False)
#checkpointer
checkpointer=SqliteSaver(conn=conn)

# create the graph
graph=StateGraph(ChatState)

# add node
graph.add_node('chat_node',chat_node)

# add edges
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():

    all_threads = set()

    for checkpoint in checkpointer.list(None):
        thread_id = checkpoint.config['configurable']['thread_id']
        all_threads.add(thread_id)

    return list(all_threads)