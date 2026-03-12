import streamlit as st
import random
import time

# 設定網頁標題
st.set_page_config(page_title="元素時速挑戰", page_icon="⚡")

# --- 1. CSS 修正：確保文字放大且按鈕精簡 ---
st.markdown("""
    <style>
    /* 放大按鈕文字 */
    button[kind="secondary"] p {
        font-size: 40px !important;
        font-weight: 900 !important;
    }
    /* 按鈕高度與樣式 */
    button[kind="secondary"] {
        height: 70px !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
        border: 2px solid #E0E0E0 !important;
    }
    /* 下一題按鈕專屬樣式 */
    .next-btn button {
        background-color: #FF4B4B !important;
        color: white !important;
        height: 80px !important;
    }
    .next-btn button p {
        font-size: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 元素資料庫 ---
if 'db' not in st.session_state:
    st.session_state.db = [
        {"s": "H", "n": "氫"}, {"s": "He", "n": "氦"}, {"s": "Li", "n": "鋰"}, {"s": "Be", "n": "鈹"},
        {"s": "B", "n": "硼"}, {"s": "C", "n": "碳"}, {"s": "N", "n": "氮"}, {"s": "O", "n": "氧"},
        {"s": "F", "n": "氟"}, {"s": "Ne", "n": "氖"}, {"s": "Na", "n": "鈉"}, {"s": "Mg", "n": "鎂"},
        {"s": "Al", "n": "鋁"}, {"s": "Si", "n": "矽"}, {"s": "P", "n": "磷"}, {"s": "S", "n": "硫"},
        {"s": "Cl", "n": "氯"}, {"s": "Ar", "n": "氬"}, {"s": "K", "n": "鉀"}, {"s": "Ca", "n": "鈣"},
        {"s": "Fe", "n": "鐵"}, {"s": "Cu", "n": "銅"}, {"s": "Zn", "n": "鋅"}, {"s": "Ag", "n": "銀"},
        {"s": "Au", "n": "金"}, {"s": "Hg", "n": "汞"}, {"s": "I", "n": "碘"}, {"s": "Ba", "n": "鋇"}
    ]

# --- 3. 核心函數 ---
def get_new_q():
    target = random.choice(st.session_state.db)
    mode = random.choice(['s2n', 'n2s'])
    correct = target['n'] if mode == 's2n' else target['s']
    
    # 抽取干擾項
    pool = [el['n'] if mode == 's2n' else el['s'] for el in st.session_state.db]
    pool = list(set(pool))
    pool.remove(correct)
    options = random.sample(pool, 3) + [correct]
    random.shuffle(options)
    
    return {
        "text": f"「 {target['s']} 」是什麼？" if mode == 's2n' else f"「 {target['n']} 」的符號？",
        "correct": correct,
        "options": options,
        "start_time": time.time()
    }

# 初始化狀態
if 'step' not in st.session_state:
    st.session_state.step = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.feedback = False
    st.session_state.q = get_new_q()

# 音效播放器
def play(url):
    st.components.v1.html(f"""<audio autoplay><source src="{url}" type="audio/mpeg"></audio>""", height=0)

# --- 4. 介面渲染 ---
st.title("⚡ 元素時速挑戰賽")

if not st.session_state.game_over:
    st.progress(st.session_state.step / 20)
    st.write(f"第 {st.session_state.step}/20 題 | 總分: **{st.session_state.score}**")

    q = st.session_state.q

    if st.session_state.feedback:
        st.error(f"### ❌ 答錯了！")
        st.info(f"正確答案是：**{q['correct']}**")
        st.markdown('<div class="next-btn">', unsafe_allow_html=True)
        if st.button("我記住了，下一題 ➔", use_container_width=True):
            st.session_state.feedback = False
            if st.session_state.step < 20:
                st.session_state.step += 1
                st.session_state.q = get_new_q()
                st.rerun()
            else:
                st.session_state.game_over = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.subheader(q['text'])
        # 四選一按鈕
        for idx, opt in enumerate(q['options']):
            if st.button(opt, key=f"opt_{idx}", use_container_width=True):
                duration = time.time() - q['start_time']
                if opt == q['correct']:
                    # 答對：基礎 10 分，每秒扣 1.5 分，最低 1 分
                    pts = max(1, int(10 - (duration * 1.5)))
                    st.session_state.score += pts
                    play("https://www.soundjay.com/buttons/sounds/button-37.mp3")
                    st.toast(f"✅ 秒回！得 {pts} 分", icon="🔥")
                    
                    if st.session_state.step < 20:
                        st.session_state.step += 1
                        st.session_state.q = get_new_q()
                        st.rerun()
                    else:
                        st.session_state.game_over = True
                        st.rerun()
                else:
                    play("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                    st.session_state.feedback = True
                    st.rerun()
else:
    st.balloons()
    st.success(f"🏆 挑戰結束！最終得分：{st.session_state.score}")
    if st.button("重新開始", use_container_width=True):
        st.session_state.step = 1
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.feedback = False
        st.session_state.q = get_new_q()
        st.rerun()
