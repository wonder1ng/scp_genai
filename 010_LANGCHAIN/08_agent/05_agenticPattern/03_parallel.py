import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel
from pydantic import BaseModel, Field
from openai import OpenAI

load_dotenv()

def full_path(path):
    return os.path.join(os.path.dirname(__file__), path)

client = OpenAI()

parser = StrOutputParser()

def transcribe_audio(file, lang="ko"):
    with open(file, "rb") as af:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=af,
            response_format="text",
            language=lang
        )
    return transcript

parallel_translate = RunnableParallel(
    origin = RunnableLambda(lambda x: transcribe_audio(full_path(x), "en")),
    translation = RunnableLambda(lambda x: transcribe_audio(full_path(x)))
)

class EvlauateTranslation(BaseModel):
    """번역 품질 평가 결과"""
    evaluate: str = Field(description="품질 평가 내용")
    score: int = Field(description="1~5 점수")
    origin: str = Field(description="번역 전 원문")
    translation: str = Field(description="개선된 번역")

final_parser = PydanticOutputParser(pydantic_object=EvlauateTranslation)

vote_prompt = ChatPromptTemplate.from_template(
    """
    당신은 번역 품질 평가자입니다. 다음 번역의 품질을 평가해주세요.
    원문(영어): {origin}
    번역(한국어): {translation}

    평가점수: 1~5점
    {format_instructions}
    """
)

llm1 = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
llm2 = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)
llm3 = ChatOpenAI(model="gpt-4o-mini", temperature=1.0)

voter1 = vote_prompt.partial(format_instructions=final_parser.get_format_instructions()) | llm1 | final_parser
voter2 = vote_prompt.partial(format_instructions=final_parser.get_format_instructions()) | llm2 | final_parser
voter3 = vote_prompt.partial(format_instructions=final_parser.get_format_instructions()) | llm3 | final_parser

parallel_vote = RunnableParallel(
    voter1 = voter1,
    voter2 = voter2,
    voter3 = voter3
)

chain = parallel_translate | parallel_vote

result = chain.invoke("harvard.wav")

final = {}
for k, v in result.items():
    print("첫 번역")
    print(k)
    print(v)
    print()
    second_result = parallel_vote.invoke({"origin": v.origin, "translation": v.translation})
    final.update({k: 0})
    for k2, v2 in second_result.items():
        print("개선된 번역")
        print(v2.score)
        print(v2.evaluate)
        final[k] += v2.score
    final[k] = (final[k], v.translation)
    print()

final = dict(sorted(final.items(), key=lambda i: i[1][0], reverse=True))
print("final")
for k, v in final.items():
    print("최종")
    print(k)
    print(v)
    print()