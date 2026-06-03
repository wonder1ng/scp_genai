from dotenv import load_dotenv
from langchain_community.agent_toolkits.load_tools import get_all_tool_names

load_dotenv()
print("--- load_tools를 통해 가져올 수 있는 모든 도구")
names = sorted(get_all_tool_names())

for name in names:
    print(f" - {name}")

print(f"\n총 {len(names)}개가 현재 사용 가능")