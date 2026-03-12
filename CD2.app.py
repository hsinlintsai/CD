import streamlit as st
import random

# 設定網頁標題
st.set_page_config(page_title="元素挑戰", page_icon="🧪")

# --- CSS 調整：按鈕變窄，文字變得更大更顯眼 ---
st.markdown("""
    <style>
    /* 針對按鈕文字：字體調大至 40px */
    div.stButton > button p {
        font-size: 40px !important; 
        font-weight: 900 !important;
        color: #1E1E1E !important;
    }
    /* 針對按鈕外框：高度減半 (約 60px)，邊框細化 */
    div.stButton > button {
        height: 65px !important;   
        border-radius: 12px !important;
        border: 2px solid #D3D3D3 !important;
        background-color: #F8F9FA !important;
        margin-bottom: 10px !important;
    }
    /* 答錯回饋按鈕：保持醒目 */
    div.stButton > button:contains("下一題") p {
        font-size: 28px !important;
        color: white !important;
    }
    div.stButton > button:contains("下一題") {
        background-color: #FF4B4B !important;
        border: none !important;
        height: 70px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. 元素資料庫
if 'elements_db' not in st.session_state:
    st.session_state.elements_db = [
        {"s": "H", "n": "氫"}, {"s": "He", "n": "氦"}, {"s": "Li", "n": "鋰"}, {"s": "Be", "n": "鈹"},
        {"s": "B", "n": "硼"}, {"s": "C", "n": "碳"}, {"s": "N", "n": "氮"}, {"s": "O", "n": "氧"},
        {"s": "F", "n": "氟"}, {"s": "Ne", "n": "氖"}, {"s": "Na", "n": "鈉"}, {"s": "Mg", "n": "鎂"},
        {"s": "Al", "n": "鋁"}, {"s": "Si", "n": "矽"}, {"s": "P", "n": "磷"}, {"s": "S", "n": "硫"},
        {"s": "Cl", "n": "氯"}, {"s": "Ar", "n": "氬"}, {"s": "K", "n": "鉀"}, {"s": "Ca", "n": "鈣"},
        {"s": "Fe", "n": "鐵"}, {"s": "Cu", "n": "銅"}, {"s": "Zn", "n": "鋅"}, {"s": "Ag", "n": "銀"},
        {"s": "Au", "n": "金"}, {"s": "Hg", "n": "汞"}, {"s": "I", "n": "碘"}, {"s": "Ba", "n": "鋇"}
    ]

# 2. 隨機出題邏輯
def get_new_question():
    target = random.choice(st.session_state.elements_db)
    mode = random.choice(['s2n', 'n2s'])
    correct_ans = target['n'] if mode == 's2n' else target['s']
    
    all_vals = list(set([el['n'] if mode == 's2n' else el['s'] for el in st.session_state.elements_db]))
    all_vals.remove(correct_ans)
    options = random.sample(all_vals, 3) + [correct_ans]
    random.shuffle(options)
    
    return {
        "text": f"符號「 {target['s']} 」是什麼？" if mode == 's2n' else f"元素「 {target['n']} 」的符號？",
        "correct": correct_ans,
        "options": options,
        "full_info": f"{target['n']} 的符號是 {target['s']}"
    }

# 初始化
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.show_feedback = False
    st.session_state.q = get_new_question()

# --- 介面 ---
st.title("🧪 元素 20 題速考")

if not st.session_state.game_over:
    st.progress(st.session_state.current_step / 20)
    st.write(f"進度: {st.session_state.current_step}/20 | 分數: {st.session_state.score}")
    
    q = st.session_state.q

    if st.session_state.show_feedback:
        st.error(f"### ❌ 答錯了！")
        st.info(f"正確答案是：**{q['correct']}**")
        st.write(f"💡 {q['full_info']}")
        
        if st.button("我記住了，下一題 ➔", use_container_width=True):
            st.session_state.show_feedback = False
            if st.session_state.current_step < 20:
                st.session_state.current_step += 1
                st.session_state.q = get_new_question()
            else:
                st.session_state.game_over = True
            st.rerun()

    else:
        st.subheader(q['text'])
        # 四選一按鈕
        for i, option in enumerate(q['options']):
            if st.button(option, key=f"btn_{i}", use_container_width=True):
                if option == q['correct']:
                    st.toast("正確！", icon="✅")
                    st.session_state.score += 5
                    if st.session_state.current_step < 20:
                        st.session_state.current_step += 1
                        st.session_state.q = get_new_question()
                        st.rerun()
                    else:
                        st.session_state.game_over = True
                        st.rerun()
                else:
                    st.session_state.show_feedback = True
                    st.rerun()
else:
    st.balloons()
    st.success(f"🏆 完成挑戰！得分：{st.session_state.score}")
    if st.button("重新開始", use_container_width=True):
        st.session_state.current_step = 1
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.show_feedback = False
        st.session_state.q = get_new_question()
        st.rerun()
