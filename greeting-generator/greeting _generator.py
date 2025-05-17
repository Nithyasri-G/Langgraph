import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langgraph.graph import StateGraph, END
from langchain.schema.runnable import RunnableLambda

# Load environment variables from .env file
load_dotenv()

# Access API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the language model
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# Define state as a dictionary
GreetingState = dict

# Node function to generate greeting message
def generate_greeting_node(state: GreetingState) -> GreetingState:
    occasion = state["occasion"]
    tone = state["tone"]
    name = state["name"]

    prompt = f"""
    Write a {tone} greeting message for {name} on the occasion of {occasion}.
    """

    response = llm([HumanMessage(content=prompt)])
    return {"occasion": occasion, "tone": tone, "name": name, "greeting": response.content}

# Wrap the node function in a RunnableLambda
generate_greeting = RunnableLambda(generate_greeting_node)

# Build the graph
builder = StateGraph(GreetingState)
builder.add_node("GenerateGreeting", generate_greeting)
builder.set_entry_point("GenerateGreeting")
builder.add_edge("GenerateGreeting", END)

graph = builder.compile()

# Run the app
if __name__ == "__main__":
    print("🎉 Greeting Message Generator!")
    occasion = input("Enter the occasion (e.g., birthday, festival): ")
    tone = input("Enter the tone (e.g., formal, casual, funny): ")
    name = input("Enter the recipient's name: ")

    result = graph.invoke({"occasion": occasion, "tone": tone, "name": name})

    print("\n✨ Your generated greeting message:\n")
    print(result["greeting"])
