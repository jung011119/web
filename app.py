import streamlit as st  #streamlit run app.py
import firebase_admin
from firebase_admin import credentials, firestore

import time

def NotifyAndRerun():
    time.sleep(1)
    st.rerun()

def Calculator():
    
    st.title("계산기 (feat.Jay)")
    col1, col2_1, col2_2, col2_3, col2_4, col3 = st.columns([2,.8,.8,.8,1,2])
    
    num1, num2 = 0,0
    
    with col1:
        num1 = st.number_input("1번째 숫자", None, None, 0.0, 1.0)
    with col2_1:
        plus = st.button("덧셈")
    with col2_2:
        minus = st.button("뺄셈")
    with col2_3:
        dup = st.button("곱셈")
    with col2_4:
        div = st.button("나눗셈")
    with col3:
        num2 = st.number_input("2번째 숫자", None, None, 0.0, 1.0)


    if plus:
        operation = "+"
        result = num1+num2
        st.success(f"{num1} {operation} {num2} = {result}")
        db.collection("calculator").add({"digit1":num1, "digit2":num2, "calc":operation, "result":result, "at":firestore.SERVER_TIMESTAMP})
    elif minus:
        operation = "-"
        result = num1-num2
        st.success(f"{num1} {operation} {num2} = {result}")
        db.collection("calculator").add({"digit1":num1, "digit2":num2, "calc":operation, "result":result, "at":firestore.SERVER_TIMESTAMP})
    elif dup:
        operation = "*"
        result = num1*num2
        st.success(f"{num1} {operation} {num2} = {result}")
        db.collection("calculator").add({"digit1":num1, "digit2":num2, "calc":operation, "result":result, "at":firestore.SERVER_TIMESTAMP})
    elif div:
        operation = "/"
        result = num1/num2
        st.success(f"{num1} {operation} {num2} = {result}")
        db.collection("calculator").add({"digit1":num1, "digit2":num2, "calc":operation, "result":result, "at":firestore.SERVER_TIMESTAMP})
    else:
        st.write("사칙연산 버튼을 눌러주세요.")

cred = credentials.Certificate("key.json")
if not firebase_admin._apps:
   firebase_admin.initialize_app(cred)
db = firestore.client()

if "login" not in st.session_state:
    st.session_state["login"] = False

if "register" not in st.session_state:
    st.session_state["register"] = False

if st.session_state["register"]:
    with st.form("회원가입"):
        title = st.title("회원가입")  
        id = st.text_input("아이디")
        pw = st.text_input("비밀번호", type="password")
        sub = st.form_submit_button("확인")  
    if id and pw and sub:
        db.collection("accounts").add({"id":id, "password":pw})
        st.success("회원가입 완료")
        st.write(f"계정'{id}'추가됨")
        st.session_state["register"] = False
        NotifyAndRerun()


elif st.session_state["login"]:
    st.title("다이어리")
    if st.button("로그아웃"):
        st.session_state["login"] = False
        NotifyAndRerun()

else:
    st.title("확인을 위해선 로그인해야 합니다")
    id = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")

    if st.button("로그인"):
        if not id or not password:
            st.warning("아이디와 비번을 입력하세요.")
            NotifyAndRerun()
        accounts = db.collection("accounts").stream()
        linkedPW = ""
        for account in accounts:
            acc = account.to_dict()
            if id == acc["id"]:
                linkedPW = acc["password"]
                break
            else:
                st.error("아이디 없음")
                NotifyAndRerun()
        if linkedPW == password:
            st.session_state["login"] = True
            NotifyAndRerun()
        else:
            st.error("비밀번호 오류")
            NotifyAndRerun()
    if st.button("회원가입"):
        st.session_state["register"] = True
        NotifyAndRerun()

if st.session_state["login"]:

    Calculator()



    # with st.form("input_form"):
    #     title = st.title("메모장 feat.재희")  
    #     task = st.text_input("해야할 일 작성")
    #     deadLine = st.text_input("마감 시간 작성")
    #     sub = st.form_submit_button("추가")  
    # if sub:
    #     st.write(f"{task}추가됨")

    
    # if sub and task and deadLine:
    #     db.collection("todos").add({"content":task, "deadLine":deadLine, "at":firestore.SERVER_TIMESTAMP})
    #     NotifyAndRerun()

    # docs = db.collection("todos").stream()
    # for doc in docs:
    #     todo = doc.to_dict()
    #     col1, col2, colDel = st.columns([4,4,2])

    #     with col1:
    #         st.info(todo["content"])

    #     with col2:
    #         st.info(todo["deadLine"])

    #     with colDel:
    #         if st.button("삭제", key = doc.id):
    #             st.warning("정말 삭제하시겠습니까?", icon="⚠️")
    #             db.collection("todos").document(doc.id).delete()
    #             st.button("네")

        
