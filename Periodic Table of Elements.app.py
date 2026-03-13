import streamlit as st
import random
import time
import pandas as pd
import os

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="元素時速賽", page_icon="⚡", layout="centered")

# --- 2. 排行榜功能 ---
DB_FILE = "leaderboard.csv"

def save_score(name, score):
    new_data = pd.DataFrame([[name, score, time.strftime("%Y-%m-%d %H:%M")]], columns=["姓名", "分數", "時間"])
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else: df = new_data
    df.to_csv(DB_FILE, index=False)

def get_leaderboard(limit=10):
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        return df.sort_values(by="分數", ascending=False).head(limit)
    return None

# --- 3. CSS 響應式優化：確保不需捲動 ---
st.markdown("""
    <style>
    /* 移除 Streamlit 預設的上邊距 */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* 題目文字大小自適應 */
    h3 { font-size: 5.5vw !important; margin-bottom: 0.5rem !important; }
    
    /* 選項按鈕：高度改用 vh (螢幕高度百分比) */
    button[kind="secondary"] {
        height: 10vh !important;  /* 固定佔據螢幕高度的 10% */
        min-height: 50px !important;
        border-radius: 10px !important;
        margin-bottom: 5px !important;
        border: 2px solid #4A90E2 !important;
        background-color: #FFFFFF !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 選項文字大小自適應 */
    button[kind="secondary"] p {
        font-size: 6vh !important; /* 字體大小隨螢幕高度縮放 */
        font-weight: 900 !important;
        color: #1A1A1A !important;
    }
    
    /* 提交/下一題按鈕 */
    button[kind="primary"] {
        height: 12vh !important;
        background-color: #FF4B4B !important;
    }
    button[kind="primary"] p { font-size: 4vh !important; color: #FFFFFF !important; }

    /* 隱藏 Streamlit 的裝飾元素以節省空間 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 遊戲資料 ---
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

def get_new_q():
    target = random.choice(st.session_state.db)
    mode = random.choice(['s2n', 'n2s'])
    correct = target['n'] if mode == 's2n' else target['s']
    pool = list(set([el['n'] if mode == 's2n' else el['s'] for el in st.session_state.db]))
    pool.remove(correct)
    options = random.sample(pool, 3) + [correct]
    random.shuffle(options)
    return {"text": f"「{target['s']}」是什麼？" if mode == 's2n' else f"「{target['n']}」的符號？",
            "correct": correct, "options": options, "start_time": time.time(), "info": f"{target['n']}({target['s']})"}

def play_sound(url):
    st.components.v1.html(f"""<audio autoplay><source src="{url}" type="audio/mpeg"></audio>""", height=0)

TOTAL_QUESTIONS = 10
if 'step' not in st.session_state:
    st.session_state.step, st.session_state.score = 1, 0
    st.session_state.game_over, st.session_state.feedback = False, False
    st.session_state.q = get_new_q()

# --- 5. 介面佈局 ---
tab_game, tab_rank = st.tabs(["🎮 挑戰", "🏆 榜單"])

with tab_game:
    if not st.session_state.game_over:
        # 緊湊顯示進度與分數
        st.write(f"第 {st.session_state.step}/10 題 | 總分: {st.session_state.score}")
        st.progress(st.session_state.step / TOTAL_QUESTIONS)
        
        q = st.session_state.q
        
        if st.session_state.feedback:
            st.error(f"❌ 錯了！正確是：{q['correct']}")
            if st.button("下一題 ➔", type="primary", use_container_width=True):
                st.session_state.feedback = False
                if st.session_state.step < TOTAL_QUESTIONS:
                    st.session_state.step += 1
                    st.session_state.q = get_new_q()
                else: st.session_state.game_over = True
                st.rerun()
        else:
            st.subheader(q['text'])
            # 垂直排列四個按鈕，確保手機好點擊
            for idx, opt in enumerate(q['options']):
                if st.button(opt, key=f"opt_{idx}", use_container_width=True):
                    elapsed = time.time() - q['start_time']
                    if opt == q['correct']:
                        pts = max(1, int(15 - (elapsed * 2.5)))
                        st.session_state.score += pts
                        play_sound("https://www.soundjay.com/buttons/sounds/button-37.mp3")
                        if st.session_state.step < TOTAL_QUESTIONS:
                            st.session_state.step += 1
                            st.session_state.q = get_new_q()
                            st.rerun()
                        else: st.session_state.game_over = True; st.rerun()
                    else:
                        play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                        st.session_state.feedback = True; st.rerun()
    else:
        st.balloons()
        st.write(f"🏁 完成！總分：{st.session_state.score}")
        name = st.text_input("輸入名字登錄：", max_chars=8)
        if st.button("提交成績 🚀", type="primary", use_container_width=True):
            if name: save_score(name, st.session_state.score); st.success("已存入！")
        if st.button("再戰一次 🔄", use_container_width=True):
            st.session_state.step, st.session_state.score = 1, 0
            st.session_state.game_over, st.session_state.feedback = False, False
            st.session_state.q = get_new_q(); st.rerun()

with tab_rank:
    st.write("🏆 TOP 10 英雄榜")
    lb = get_leaderboard(10)
    if lb is not None: st.table(lb)
    if st.button("🔄 刷新"): st.rerun()
    confirm = st.checkbox("清除資料")
    if st.button("🗑️ 執行清空", disabled=not confirm):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.rerun()
