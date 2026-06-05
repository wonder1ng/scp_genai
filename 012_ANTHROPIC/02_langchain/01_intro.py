from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

load_dotenv()

llm = ChatAnthropic(model="claude-sonnet-4-6")

response = llm.invoke("인공지능에 대해 설명해")
print(response.content)