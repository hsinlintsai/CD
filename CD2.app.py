import streamlit as st
import random
import time

# 設定網頁標題
st.set_page_config(page_title="元素時速挑戰", page_icon="⚡")

# --- 1. 音效功能 ---
def play_sound(sound_url):
    sound_html = f"""<audio autoplay><source src="{sound_url}" type="audio/mpeg"></audio>"""
    st.markdown(sound_html, unsafe_allow_html=True)

CORRECT_URL = "https://www.soundjay.com/buttons/sounds/button-37.mp3"
WRONG_URL = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

# --- 2. CSS 調整：文字極大化、框框精簡 ---
st.markdown("""
    <style>
    div.stButton > button p {
        font-size: 42px !important; 
        font-weight: 900 !important;
    }
    div.stButton > button {
        height: 70px !important;   
        border-radius: 15px !important;
        margin-bottom: 10px !important;
        background-color: #F0F2F6 !important;
    }
    /* 下一題按鈕樣式 */
    div.stButton > button:contains("下一題") p { font-size: 28px !important; color: white !important; }
    div.stButton > button:contains("下一題") { background-color: #FF4B4B !important; height: 75px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 元素資料庫 ---
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

# --- 4. 遊戲邏輯 ---
def get_new_question():
    target = random.choice(st.session_state.elements_db)
    mode = random.choice(['s2n', 'n2s'])
    correct_ans = target['n'] if mode == 's2n' else target['s']
    all_vals = list(set([el['n'] if mode == 's2n' else el['s'] for el in st.session_state.elements_db]))
    all_vals.remove(correct_ans)
    options = random.sample(all_vals, 3) + [correct_ans]
    random.shuffle(options)
    return {
        "text": f"「 {target['s']} 」是什麼？" if mode == 's2n' else f"「 {target['n']} 」的符號？",
        "correct": correct_ans,
        "options": options,
        "start_time": time.time() # 紀錄出題時間
    }

if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.show_feedback = False
    st.session_state.play_sound = None
    st.session_state.q = get_new_question()

# --- 5. 主畫面 ---
st.title("⚡ 元素時速挑戰賽")

if st.session_state.play_sound:
    play_sound(st.session_state.play_sound)
    st.session_state.play_sound = None

if not st.session_state.game_over:
    st.progress(st.session_state.current_step / 20)
    st.write(f"### 題數: {st.session_state.current_step}/20 | 目前總分: **{st.session_state.score}**")
    
    q = st.session_state.q

    if st.session_state.show_feedback:
        st.error(f"### ❌ 答錯了！")
        st.info(f"正確答案是：**{q['correct']}**")
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
        # 四選一
        for i, option in enumerate(q['options']):
            if st.button(option, key=f"btn_{i}", use_container_width=True):
                # 計算時間得分
                elapsed = time.time() - q['start_time']
                # 基礎10分，每秒扣1分，最低1分
                points = max(1, 10 - int(elapsed))
                
                if option == q['correct']:
                    st.session_state.play_sound = CORRECT_URL
                    st.session_state.score += points
