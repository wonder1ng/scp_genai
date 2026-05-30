from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 챗봇입니다."),
    ("user", "{input}")
])

chain = prompt | llm | StrOutputParser()
print(chain.invoke({"input": "안녕하세요, 나는 홍길동입니다."}))
print(chain.invoke({"input": "내가 누구야?"}))
print(chain.invoke({"input": "아니! 내가 방금 말했잖아!! 왜 그것도 몰라?"}))

print("=" * 30)

prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 챗봇입니다."),
    MessagesPlaceholder("history"),
    ("user", "{input}")
])

chain2 = prompt_with_history | llm | StrOutputParser()

history_example = [
    HumanMessage(content="안녕하세요, 저는 홍길동입니다."),
    AIMessage(content="네, 홍길동님 반갑습니다.")
]

answer = chain2.invoke({
    "history": history_example,
    "input": "제 이름이 뭐였죠?"
})

print(answer)