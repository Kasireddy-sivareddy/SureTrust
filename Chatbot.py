from pocketflow import Node, Flow
import google.generativeai as genai

API_KEY = "AQ.Ab8RN6Kvmg0i3Ka58sTKITrKwvIobnHx9uz95Tzk8ardVYY5Ig"  
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def call_llm(messages):

    prompt = ""
    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"
    response = model.generate_content(prompt)

    return response.text
class ChatNode(Node):
    def prep(self, shared):

        if "messages" not in shared:
            shared["messages"] = []

            print("=" * 50)
            print("🤖 Welcome to AI Chatbot")
            print("Type 'exit' to quit.")
            print("=" * 50)

        user_input = input("You: ")

        if user_input.lower() == "exit":
            return None

        shared["messages"].append({
            "role": "user",
            "content": user_input
        })

        return shared["messages"]

    def exec(self, messages):

        if messages is None:
            return None

        answer = call_llm(messages)

        return answer

    def post(self, shared, prep_res, exec_res):

        if prep_res is None:
            print("\nGoodbye! 👋")
            return None

        print("\nAssistant:", exec_res)
        print()

        shared["messages"].append({
            "role": "assistant",
            "content": exec_res
        })

        return "continue"

chat = ChatNode()

chat - "continue" >> chat

flow = Flow(start=chat)
if __name__ == "__main__":

    shared = {}

    flow.run(shared)