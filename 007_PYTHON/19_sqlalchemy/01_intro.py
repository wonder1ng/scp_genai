from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from sqlalchemy import Column, Integer, String

basePath = "\\".join(__file__.split("\\")[:-1])
# create_engine:
# - SQLAlchemy의 "DB 연결 엔진" 생성 함수
# - 실제로 DB와 통신하는 핵심 객체
engine = create_engine(f"sqlite:///{basePath}\\example.db")
# declarative_base():
# - ORM 모델(User 같은 클래스)들이 상속받는 기본 클래스 생성
# - 이 Base를 통해 SQLAlchemy가 클래스들을 "테이블 정의"로 인식
Base = declarative_base()

# 모델(테이블) 정의
class User(Base):
    # 테이블 이름 지정
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# Base.metadata:
# - 지금까지 선언된 모든 ORM 클래스(User 등)의
#   테이블 메타정보를 가지고 있음
# create_all(engine):
# - engine(DB 연결 대상)을 기준으로
# - 정의된 테이블이 DB에 없으면 생성
# - 이미 있으면 생성하지 않음
Base.metadata.create_all(engine)

# sessionmaker:
# - DB 작업을 수행할 "세션 클래스"를 생성
# - session = DB 작업 단위 (INSERT/SELECT/UPDATE/DELETE)
# bind=engine:
# - 이 세션이 어떤 DB에 연결될지 지정
Session = sessionmaker(bind=engine)
session = Session()

new_user = User(name="홍길동", age=25)
session.add(new_user)
new_user = User(name="고길동", age=35)
session.add(new_user)
session.commit()

print('-' * 30)
users = session.query(User).all()
for user in users:
    print(user.name, user.age)
print('-' * 30)
