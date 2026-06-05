# 금융 도우미 에이전트 챗봇

# 1. 네이버 뉴스 가져오기
# 2. 구글 검색으로 기업 개요/최근 정보 조회
# 3. 환율 조회
# 4. 주가 조회
from ast import literal_eval
import math
from typing import Literal
from flask import jsonify
import requests, os
from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
import yfinance as yf
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from pydantic import BaseModel, Field

@tool
def get_news(text: str, display: int = 20, sort: Literal["sim", "date"] = "date") -> list:
    """
    네이버 뉴스에서 키워드로 최신 기사 html을 list로 가져온다.
    params:
        text: 검색 키워드
        display: 가져올 기사 개수. 기본 20
        sort: 정렬 기준. sim: 관련도, date: 최신순
    """
    NAVER_API_URL = "https://openapi.naver.com/v1/search/news.json"

    NAVER_API_HEADERS = {
        "X-Naver-Client-Id": os.getenv("NAVER_API_ID"),
        "X-Naver-Client-Secret": os.getenv("NAVER_API_SECRET")
    }

    params = {
        "query": text,
        "display": 20,
        "sort": sort    # "sim", "date"
    }
    response = requests.get(NAVER_API_URL, headers=NAVER_API_HEADERS, params=params)
    data = response.json()
    news = [WebBaseLoader(e.get("originallink")).load() for e in data["items"]]
    
    return news

@tool
def get_company_info(company: str) -> dict:
    """
    구글에서 기업 정보를 검색해서 개요와 최근 소식을 요약해서 반혼
    params:
        company: 검색할 기업명
    """
    class CompanyInfo(BaseModel):
        overview: str = Field(
            description="기업의 기본 개요, 설립 목적, 주요 사업 등을 요약한 내용"
        )
        recent_infomation: str = Field(
            description="기업의 최근 주가 움직임, 최신 동향, 최근 성과, 향후 추이 등을 요약한 내용"
        )

    web_search = TavilySearch(max_results=10)
    company_llm = ChatOpenAI(model="gpt-4o-mini")
    company_agent = create_agent(company_llm, [web_search], response_format=CompanyInfo)
    result = company_agent.invoke({
        "messages": 
        [("system", 
          f"당신은 {company} 기업의 25년차 IR 전문가입니다. 주어진 구조에 맞춰 답변하세요."), 
          ("user", 
           f"{company} 기업의 개요와 최근 정보를 검색해서 알려줘")]})
    return literal_eval(result["messages"][-1].content)

@tool
def get_exchange_rate() -> dict:
    """KRW 1원 기준으로 모든 외화 환율 반환"""
    response = requests.get(f"https://open.er-api.com/v6/latest/KRW")
    data = response.json()
    # data["rates"]["KRW"]
    return data["rates"]
    # response = requests.get(f"https://open.er-api.com/v6/latest/{currency}")
    # data = response.json()
    # data["rates"]["KRW"]
    # return data["rates"]["KRW"]

@tool
def get_stock_price(ticker):
    """yfinance로 다양한 기업의 주가를 가져온다. 예) 애플("AAPL")과 삼성전자("005930.KS)"""
    try:
        data = yf.Ticker(ticker).history(period="1d")
        print("data")
        print(data)
        return data
    except Exception as e:
        print("error!!!!!!!!!!")
        print(e)
        return e

@tool
def send_payment(recipient: str, amount: int) -> str:
    """수신자에게 지정 금액을 송금"""
    return f"{recipient}에게 {amount}원 송금 완료"

@tool
def exchange(amount: float, from_currency: str, to_currency: str, to: bool = False) -> dict:
    """통화 환전
        params:
            amount: 환전할 금액
            from_currency: 환전할 통화.
            to_currency: 환전 받을 통화.
            to: amount의 기준 통화. False면 from_currency 기준, True면 to_currency 기준
        예:
            amount=1000, from_currency="KRW", to_currency="USD", to=True
            USD 1000을 KRW로 구매.
            amount=1000, from_currency="KRW", to_currency="JPY", to=False
            KRW 1000로 JPY를 구매.
    """
    if to:
        response = requests.get(f"https://open.er-api.com/v6/latest/{to_currency}")
        rate = response.json()["rates"][from_currency]
        return jsonify({from_currency: math.ceil(amount * rate), to_currency: amount})
    response = requests.get(f"https://open.er-api.com/v6/latest/{from_currency}")
    rate = response.json()["rates"][to_currency]
    return jsonify({from_currency: amount, to_currency: math.floor(amount * rate)})

TOOLS = [get_news, get_company_info, get_exchange_rate, get_stock_price, exchange]