from langgraph.graph import START,END,StateGraph
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
from typing import TypedDict, Annotated

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


#checkpointer
checkpointer=InMemorySaver()

# create the graph
graph=StateGraph(ChatState)

# add node
graph.add_node('chat_node',chat_node)

# add edges
graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot=graph.compile(checkpointer=checkpointer)
