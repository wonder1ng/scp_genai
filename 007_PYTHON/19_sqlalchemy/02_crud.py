from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.session import Session as TypeSession

from sqlalchemy import Column, Integer, String

base_path = "\\".join(__file__.split("\\")[:-1])
# create_engine:
# - SQLAlchemy의 "DB 연결 엔진" 생성 함수
# - 실제로 DB와 통신하는 핵심 객체
engine = create_engine(f"sqlite:///{base_path}\\example.db")
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

# db 실행
Base.metadata.create_all(engine)

# CRUD
def create_user(session: TypeSession, name, age):
    new_user = User(name=name, age=age)
    session.add(new_user)
    session.commit()
    return new_user

def list_users(session: TypeSession):
    users = session.query(User).all()
    return users

def get_user_by_id(session: TypeSession, user_id):
    # 구식 코드
    # user = session.query(User).filter_by(user_id).first()
    # return user
    return session.get(User, user_id)

def update_user_age(session: TypeSession, user_id, new_age):
    user = session.get(User, user_id)
    if not user:
        return False
    user.age = new_age
    session.commit()
    return True

def delete_user_age(session: TypeSession, user_id):
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True

def delete_user_by_name(session: TypeSession, name):
    users = session.query(User).filter_by(name=name).all()
    if not users:
        return 0
    for user in users:
        session.delete(user)
        session.commit()
    return users.__len__()

if __name__ == "__main__":
    Session = sessionmaker(bind=engine)
    with Session() as session:
        hong = create_user(session, "홍길동", 22)
        kim = create_user(session, "김길동", 33)
        print(f"추가된 사용자들: {hong,id}, {kim.id}")

        user = get_user_by_id(session, hong.id)
        print(f"조회한 사람은: {hong.id}, {hong.name}")

        deleted_user_count = delete_user_by_name(session, "홍길동")
        print(f"삭제된 사용자 수는: {deleted_user_count}")

        users = list_users(session)
        print("전체 사용자 조회")
        for u in users:
            print(f" - {u.id}: {u.name}, {u.age}")