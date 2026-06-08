import uuid
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

graph = StateGraph(state_schema=MessagesState)
memory = MemorySaver()

def call_model(state):
    """LLM 메시지 전달 및 응답"""
    messages = state["messages"]
    system_message = SystemMessage(content="당신은 친절한 AI비서입니다.")
    all_messages = [system_message] + messages

    print("모델 호출 함수 실행중. 메시지 수:", len(messages))
    response = llm.invoke(all_messages)
    print("모델 응답 생성 완료:", response.content[:50])
    
    return {"messages": response}

graph.add_node("model", call_model)
graph.add_edge(START, "model")
graph.add_edge("model", END)

app = graph.compile(checkpointer=memory)

thread_id = str(uuid.uuid4())
config = {"configurable": {"thread_id": thread_id}}

user_input = "내 이름은 김철수야. 안녕."
result = app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
user_input = "내 이름이 뭐라고?"
result2 = app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)

print(config)
print(f"AI 응답: {result2["messages"][-1].content}")
print("=============")

for i, message in enumerate(result2["messages"]):
    print(f"메세지 {i}: {message.type} - {message.content}")
print("=============")

thread_id2 = str(uuid.uuid4())
config2 = {"configurable": {"thread_id": thread_id2}}

user_input = "내 이름은 홍길동. 안녕."
result3 = app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config2)
user_input = "내 이름이 뭐라고?"
result4 = app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config2)

user_input = "내 직업은 프로그래머."
result5 = app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config2)
user_input = "내 이름과 직업이 뭐라고?"
result6 = app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config2)

print(config2)
print(f"AI 응답: {result6["messages"][-1].content}")
print("=============")
result7 = app.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)
print(config)
print(f"AI 응답: {result7["messages"][-1].content}")
print("=============")
