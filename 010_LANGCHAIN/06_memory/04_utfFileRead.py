import json, os

with open(os.path.join(os.path.dirname(__file__), "history.json"), "r", encoding="utf_8") as f:
    messages = json.load(f)

ROLE = {"human": "사용자", "ai": "챗봇", "system": "시스템"}

print(f"=== {len(messages)} 메시지 ===")

for i, m in enumerate(messages, 1):
    role = ROLE.get(m.get("type"), "기타")
    content = m.get("data", {}).get("content", "")
    print(f"{i:02d}. {role:<8} {content}")