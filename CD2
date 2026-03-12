import streamlit as st
import random

# 設定網頁標題與圖示
st.set_page_config(page_title="元素挑戰賽", page_icon="🧪")

# 元素資料 (可以自行擴充)
if 'elements' not in st.session_state:
    st.session_state.elements = [
        {"s": "H", "n": "氫"}, {"s": "He", "n": "氦"}, {"s": "Li", "n": "鋰"},
        {"s": "Be", "n": "鈹"}, {"s": "B", "n": "硼"}, {"s": "C", "n": "碳"},
        {"s": "N", "n": "氮"}, {"s": "O", "n": "氧"}, {"s": "F", "n": "氟"},
        {"s": "Ne", "n": "氖"}, {"s": "Na", "n": "鈉"}, {"s": "Mg", "n": "鎂"}
    ]

# 初始化遊戲狀態
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.hearts = 3
    st.session_state.current_ques = random.choice(st.session_state.elements)
    st.session_state.mode = random.choice(['s2n', 'n2s']) # 符號猜名稱 或 名稱猜符號

def next_question():
    st.session_state.current_ques = random.choice(st.session_state.elements)
    st.session_state.mode = random.choice(['s2n', 'n2s'])

# 網頁介面
st.title("🧪 元素週期表：多鄰國挑戰版")
st.write(f"### 剩餘生命: {'❤️' * st.session_state.hearts}")
st.write(f"### 目前得分: {st.session_state.score}")

if st.session_state.hearts > 0:
    q = st.session_state.current_ques
    if st.session_state.mode == 's2n':
        st.subheader(f"請問符號「 {q['s']} 」的中文名稱是？")
        ans = q['n']
    else:
        st.subheader(f"請問「 {q['n']} 」的元素符號是？")
        ans = q['s']

    user_ans = st.text_input("在這裡輸入答案...", key="input").strip()

    if st.button("提交答案"):
        if user_ans.lower() == ans.lower():
            st.success("✅ 太棒了！答對了！")
            st.session_state.score += 10
            next_question()
            st.rerun()
        else:
            st.error(f"❌ 答錯囉！正確答案是：{ans}")
            st.session_state.hearts -= 1
            if st.session_state.hearts > 0:
                next_question()
                st.rerun()
else:
    st.error("💀 挑戰結束！愛心用完囉。")
    if st.button("重新開始"):
        st.session_state.score = 0
        st.session_state.hearts = 3
        next_question()
        st.rerun()
