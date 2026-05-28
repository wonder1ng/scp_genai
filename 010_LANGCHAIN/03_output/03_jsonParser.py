from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")
parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ("system", "답변은 항상 JSON으로만 하시오. 설명 금지"),
    ("user", "{question}\n\n{format_instructions}")
]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser

result = chain.invoke