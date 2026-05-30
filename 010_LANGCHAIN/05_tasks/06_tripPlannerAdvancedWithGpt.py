from ast import literal_eval
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

# 목적 - 여행 계획을 작성한다.
# 도시 입력 -> 음식 추천 
#          -> 관광지 추천
#          -> 호텔 추천
# 사용자 입력의 OO을 보고, 시간표/동선/교통수단 vs 음식/관광지/호텔
# RunnableParallel, RunnableBranch

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate(
    [("system",
      """
      다음의 여행 관련 질문을 보고 반드시 아래 형식의 dict만 반환해.

      {{'result': True, 'city': 'seoul', "text": str}}

      규칙:
      1. result는 여행 계획이 도시의 음식이나 관광지, 숙소 등을 정하는 등 어느 정도 구체적이면 True
      2. 여행 계획이 너무 추상적이면 False
      3. city는 반드시 문자열이어야 함
      4. city는 절대 빈 문자열('', null, None)로 반환하면 안 됨
      5. 질문에 도시가 없으면 가장 적절한 여행 도시를 하나 추천해서 넣어
      6. 반환은 dict 하나만 하고 다른 설명은 절대 추가하지 마
      7. text는 사용자 질문을 그대로 반환해
      8. result와 city, text는 항상 포함해야 함
      """),
     ("human", "{text}")])

configs = {
    True: {
        "prompt": ChatPromptTemplate(
            [("system", "당신은 {city}의 30년차 관광 현지 가이드. 관광객에게 {city}의 관광 시 추천할 {obj}에 대해 간략히 작성하시오. 빈 개행(\\n\\n)은 하지 마시오."),
             ("human", "{text}")]),
        "items": {
            "timeTable": "시간표",
            "route": "동선",
            "transport": "교통수단",
        },
    },
    False: {
        "prompt": ChatPromptTemplate(
            [("system", "당신은 {city}의 30년차 현지인. 관광객에게 {city}의 {obj}에 대해 간략히 추천하시오. 다른 여행지는 언급말고 {city}에 대해서만 기술하시오. 빈 개행(\\n\\n)은 하지 마시오."),
             ("human", "{text}")]),
        "items": {
            "food": "음식",
            "attraction": "관광지",
            "hotel": "호텔",
        },
    },
}

make_chain = lambda conf: RunnableParallel(
    {k: (conf["prompt"].partial(obj=v)| llm| StrOutputParser())
    for k, v in 
    conf["items"].items()})

branch = (prompt 
          | llm 
          | RunnableLambda(lambda x: print("\n\n- start", x, sep="\n\n") or literal_eval(x.content)) 
          | (lambda x: make_chain(configs[x["result"]])))

questions = [
    {"text": "한국에서 2박3일로 갔다오기 좋은 해외 여행지. 여유롭게 쉬다 오고 싶어"},
    {"text": "피렌체에서 티본 스테이크와 트러플 파스타를 먹고 성당, 미술관, 박물관, 광장을 관람할 거야"}
]

for q in questions:
    print("질문:", q)
    result = branch.invoke({"text": q})
    print("답변:")
    [print(k + "\n" + result[k] + "\n") for k in result.keys()]
    print("="*30)

# 질문: {'text': '한국에서 2박3일로 갔다오기 좋은 해외 여행지. 여유롭게 쉬다 오고 싶어'}

# - start
# content="{'result': False, 'city': 'paris', 'text': '한국에서 2박3일로 갔다오기 좋은 해외 여행지. 여유롭게 쉬다 오고 싶어'}" additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 42, 'prompt_tokens': 231, 'total_tokens': 273, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_da89e836d0', 'id': 'chatcmpl-DkUFxXoSmYNaJlb4HpvOx3yOpfhqM', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019e6e95-a116-7de1-acd2-903006945a07-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 231, 'output_tokens': 42, 'total_tokens': 273, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# 음식
# 관광지
# 호텔
# 답변:

# food
# 파리에서의 여행은 어느 단기간에도 독특한 매력을 제공합니다. 2박 3일의 일정으로 여유롭게 쉬면서 즐길 수 있는 몇 가지 추천 음식을 소개할게요.
# 1. **크로아상 (Croissant)**: 아침을 시작할 때는 신선하게 구운 크로아상 한 장과 함께 커피를 즐기는 것이 좋습니다. 바삭하고 부드러운 식감이 환상적입니다.
# 2. **포크 바게트 (Baguette)**: 바게트와 다양한 치즈, 햄을 곁들여 간편한 점심으로 즐겨보세요. 특히 파리의 유명한 베이커리에서 구입한 바게트는 훌륭합니다.
# 3. **오뗄레트 (Omelette)**: 너무 복잡한 요리 대신, 간단하면서도 맛있는 오뗄레트를 점심이나 저녁으로 추천합니다. 파리의 브라세리에서 현지 느낌을 느껴보세요.
# 4. **부야베스 (Bouillabaisse)**: 제안하는 저녁 메뉴로는 신선한 해산물로 만든 부야베스가 있습니다. 파리에서도 지중해의 맛을 즐길 수 있는 좋은 선택입니다.
# 5. **마카롱 (Macaron)**: 디저트는 파리의 유명한 마카롱을 놓칠 수 없습니다. 다양한 색상과 맛이 있어 선물용으로도 좋습니다.
# 6. **와인 (Wine)**: 식사와 함께 좋은 프랑스 와인 한 잔은 필수입니다. 파리의 여러 와인 바나 레스토랑에서 현지 와인을 체험해 보세요.
# 이처럼 파리에서는 간단한 음식에서부터 고급 요리에 이르기까지 다양하게 즐길 수 있으니, 여유롭게 도시의 분위기를 만끽하며 맛있는 시간을 보내시길 바랍니다.

# attraction
# 파리에서 즐길 수 있는 관광지를 몇 가지 추천해 드리겠습니다. 
# 1. **에펠탑**: 파리의 상징인 에펠탑은 필수 방문지입니다. 낮에는 주변 공원에서 피크닉을 즐기거나, 저녁에는 탑의 조명이 켜지는 모습을 감상하세요.
# 2. **루브르 박물관**: 세계에서 가장 유명한 미술관 중 하나인 루브르 박물관은 모나리자, 비너스 드 밀로 등 많은 걸작을 소장하고 있습니다. 관람 후에는 박물관 근처의 튈르리 정원에서 여유를 즐길 수 있습니다.
# 3. **몽마르트르**: 이곳은 아티스트들이 많이 모였던 곳으로, 사크레 쾨르 대성당의 아름다운 전경을 감상할 수 있습니다. 아트 갤러리와 아늑한 카페들이 가득해 산책하기에 좋은 곳입니다.
# 4. **세느강 크루즈**: 세느강에서의 크루즈는 파리의 주요 명소들을 다른 시각에서 감상할 수 있는 멋진 경험입니다. 특히 저녁에 해가 지고 조명이 켜질 때가 가장 아름답습니다.
# 5. **오르세 미술관**: 인상파 미술의 거장들이 많이 전시된 오르세 미술관은 건물 자체도 훌륭한 볼거리입니다. 보다 여유롭게 작품을 감상해 보세요.
# 6. **마레 지구**: 이곳은 예쁜 카페와 부티크, 상점들이 많아 걷기 좋은 동네입니다. 작은 골목길을 탐방하며 독특한 매력을 느껴보세요.
# 7. **아크 드 트리옹프**: 샹젤리제 거리 끝에 위치한 아크 드 트리옹프에서 파리의 전경을 바라보는 것도 좋은 선택입니다.
# 2박 3일 일정에 맞춰 여유롭게 각지를 돌아보시길 추천드립니다! 파리의 매력을 한껏 느끼시길 바랍니다.

# hotel
# 파리에서의 숙박 장소를 추천해 드릴게요. 파리는 매력적인 호텔들이 많아서 선택이 어렵지만, 편안하게 지낼 수 있는 곳들을 몇 군데 소개하겠습니다.
# 1. **르 메르디앙 에투알 (Le Meridien Etoile)**: 샹젤리제 근처에 위치해 있어 접근성이 뛰어나고, 모던한 분위기를 자랑합니다. 호텔 내에는 다양한 레스토랑과 바도 있어 여유롭게 시간을 보낼 수 있습니다.
# 2. **호텔 드 라 뮈르 (Hôtel de la Mur)**: 마레구역에 위치해 있어 예쁜 카페와 작은 상점들이 가까워 도보로 둘러보기 좋습니다. 아늑하고 세련된 인테리어로 편안한 휴식을 제공합니다.
# 3. **오텔 르 마르소 (Hôtel Le Marceau Bastille)**: 바스티유 근처에 위치해 있어 파리의 대표적인 관광지를 쉽게 방문할 수 있습니다. 현대적이고 세련된 디자인의 객실에서 편안한 숙박이 가능합니다.
# 4. **호텔 루브르 몽테르기 (Hôtel Louvre Montorgueil)**: 루브르 박물관과 가까워 예술과 문화를 즐기기 좋은 위치에 있습니다. 고풍스러운 분위기와 친절한 서비스로 유명합니다. 
# 이 외에도 파리에는 다양한 스타일과 가격대의 호텔들이 많으니, 본인의 취향에 맞는 곳을 선택하면 좋겠어요. 즐거운 여행 되세요!
# ==============================
# 질문: {'text': '피렌체에서 티본 스테이크와 트러플 파스타를 먹고 성당, 미술관, 박물관, 광장을 관람할 거야'}

# - start
# content="{'result': True, 'city': 'florence', 'text': '피렌체에서 티본 스테이크와 트러플 파스타를 먹고 성당, 미술관, 박물관, 광장을 관람할 거야'}" additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 54, 'prompt_tokens': 242, 'total_tokens': 296, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_da89e836d0', 'id': 'chatcmpl-DkUG7AhVk6c72N9hCU4vDZ2JPTyOM', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019e6e95-c95d-78d1-bc39-d5700d7f1181-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 242, 'output_tokens': 54, 'total_tokens': 296, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
# 시간표
# 동선교통수단
# 답변:

# timeTable
# 피렌체에서의 하루 일정을 아래와 같이 추천드립니다. 이 일정은 티본 스테이크와 트러플 파스타를 포함한 맛있는 식사를 즐기고, 주요 관광 명소들을 방문하도록 구성했습니다.
# ### 아침
# - **09:00**: **아침식사** – 근처 카페에서 이탈리안 커피와 페이스트리를 즐기세요.
# - **10:00**: **두오모(Duomo)** – 산타 마리아 델 피오레 대성당의 멋진 외관을 감상하고, 원하시면 내부도 관람해주세요.
# ### 오전
# - **11:00**: **우피치 미술관(Uffizi Gallery)** – 세계적으로 유명한 미술관에서 보티첼리, 다 빈치, 미켈란젤로의 작품을 감상하세요. 사전 예약을 추천합니다.
# ### 점심
# - **13:00**: **점심식사** – 피렌체 지역의 유명한 티본 스테이크가 포함된 레스토랑에서 식사하세요. 'Trattoria Mario'나 'Buca Lapi'를 추천합니다.
# ### 오후
# - **14:30**: **아카데미아 미술관(Galleria dell'Accademia)** – 다비드 상을 포함한 미켈란젤로의 작품을 감상하세요.
# - **16:00**: **피렌체 구시가 광장(Piazza della Signoria)** – 역사적인 광장과 다양한 조각상을 감상하며 여유로운 시간을 가지세요.
# ### 저녁
# - **18:00**: **트러플 파스타 저녁식사** – 'Trattoria da Burde'에서 신선한 트러플 파스타를 즐기세요.
# ### 밤
# - **20:00**: **피렌체의 야경 감상** – 피렌체의 아름다운 야경을 즐기기 위해 미켈란젤로 광장(Piazzale Michelangelo)으로 이동하세요.
# ### 추가 팁
# - 각 미술관, 박물관은 사전 예약을 통해 대기 시간을 줄이는 것이 좋습니다.
# - 피렌체는 도보로 이동하기 좋은 도시에니 적절한 신발을 신고 다니세요.
# 좋은 여행 되시길 바랍니다!

# route
# 피렌체에서의 하루 관광 동선을 다음과 같이 추천드립니다:
# ### 오전
# 1. **아카데미아 미술관 (Galleria dell'Accademia)**:
#    - 오전 일찍 방문하여 미켈란젤로의 다비드상을 감상하세요. 이른 시간대에 가면 혼잡함을 피할 수 있습니다.
# 2. **두오모 성당 (Cathedral of Santa Maria del Fiore)**:
#    - 아카데미아에서 도보로 이동. 성당의 웅장한 외관과 내부를 둘러본 후, 쿠폴라(돔)에 올라가 피렌체 전경을 감상하세요.
# ### 점심
# 3. **티본 스테이크와 트러플 파스타**:
#    - 추천 레스토랑: "Trattoria Mario" 또는 "Osteria Vini e Vecchi Sapori"에서 현지 음식을 즐기세요.
# ### 오후
# 4. **우피치 미술관 (Galleria degli Uffizi)**:
#    - 식사 후 우피치 미술관으로 이동해 르네상스 예술의 masterpieces를 감상하세요. 사파르로 테마를 정해 감상하는 것도 좋습니다.
# 5. **웨키오 다리 (Ponte Vecchio)**:
#    - 미술관에서 나와 다리로 이동. 이곳에서 독특한 보석 가게들을 구경하며 그림 같은 풍경을 즐겨보세요.
# ### 저녁
# 6. **시뇨리아 광장 (Piazza della Signoria)**:
#    - 하루의 피로를 풀며 광장을 걸어보세요. 거대한 조각상들과 아름다운 건축물들이 있는 이곳에서 사진 찍기에도 좋은 장소입니다.
# 7. **저녁 식사 및 자유 시간**:
#    - 나중에 “Trattoria da Burde”와 같은 곳에서 평판 좋은 저녁을 즐기세요. 저녁 후에는 피렌체의 야경을 즐길 수 있는 좋은 카페나 바에서 휴식을 취하세요.
# 이 동선을 통해 피렌체의 문화와 미식을 모두 경험하시길 바랍니다! 즐거운 여행 되세요!

# transport
# 피렌체에서의 관광은 정말 매력적입니다! 여러 가지 교통수단을 추천해 드릴게요.
# 1. **도보**: 피렌체의 대부분 관광지는 도보로 쉽게 이동할 수 있습니다. 특히, 역사적인 중심지는 좁은 골목과 매력적인 광장이 많아 걷는 것이 가장 좋은 방법입니다. 
# 2. **자전거**: 자전거를 대여해 시내를 둘러보는 것도 좋은 아이디어입니다. 자전거 도로가 잘 마련되어 있어 편리하게 이동할 수 있습니다.
# 3. **트램과 버스**: 피렌체 시내 외곽 지역을 여행할 때는 버스나 트램을 이용하세요. 대중교통이 잘 연결되어 있어, 주요 관광 명소로 쉽게 이동할 수 있습니다.
# 4. **택시 또는 공유 차량 서비스**: 이동 거리가 길거나 수많은 짐을 가지고 있을 때는 택시나 우버 같은 공유 차량 서비스를 이용하는 것이 편리합니다.
# 5. **전통적인 리프트**: 피렌체에서는 몇몇 장소에서 리프트를 사용할 수 있어, 주변 경관을 감상하며 이동하는 재미도 있습니다.
# 성당, 미술관, 박물관, 광장을 관광한 후, 현지 식당에서 티본 스테이크와 트러플 파스타를 맛보는 것은 정말 멋진 경험이 될 것입니다. 즐거운 여행 되세요!
# ==============================