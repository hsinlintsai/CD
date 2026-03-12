import streamlit as st
import random
import time
import pandas as pd
import os

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="元素週期表時速賽", page_icon="⚡", layout="centered")

# --- 2. 排行榜資料庫功能 ---
DB_FILE = "leaderboard.csv"

def save_score(name, score):
    new_data = pd.DataFrame([[name, score, time.strftime("%Y-%m-%d %H:%M")]], 
                            columns=["姓名", "分數", "時間"])
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_csv(DB_FILE, index=False)

def get_leaderboard(limit=10):
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        return df.sort_values(by="分數", ascending=False).head(limit)
    return None

def clear_leaderboard():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

# --- 3. CSS 樣式 ---
st.markdown("""
    <style>
    button[kind="secondary"] p { font-size: 40px !important; font-weight: 900 !important; }
    button[kind="secondary"] { height: 70px !important; border-radius: 12px !important; margin-bottom: 10px !important; border: 2px solid #D3D3D3 !important; background-color: #F8F9FA !important; }
    button[kind="primary"] { height: 80px !important; width: 100% !important; background-color: #FF4B4B !important; border: none !important; }
    button[kind="primary"] p { font-size: 30px !important; font-weight: bold !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 遊戲資料與邏輯 ---
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
    return {"text": f"「 {target['s']} 」是什麼？" if mode == 's2n' else f"「 {target['n']} 」的符號？",
            "correct": correct, "options": options, "start_time": time.time(), "info": f"{target['n']} ({target['s']})"}

def play_sound(url):
    st.components.v1.html(f"""<audio autoplay><source src="{url}" type="audio/mpeg"></audio>""", height=0)

TOTAL_QUESTIONS = 10
if 'step' not in st.session_state:
    st.session_state.step, st.session_state.score = 1, 0
    st.session_state.game_over, st.session_state.feedback = False, False
    st.session_state.q = get_new_q()

# --- 5. 介面佈局 ---
tab_game, tab_rank = st.tabs(["🎮 開始挑戰", "🏆 英雄榜"])

with tab_game:
    st.title("⚡ 元素 10 題速考挑戰")
    if not st.session_state.game_over:
        st.progress(st.session_state.step / TOTAL_QUESTIONS)
        st.write(f"第 {st.session_state.step}/{TOTAL_QUESTIONS} 題 | 總分: **{st.session_state.score}**")
        q = st.session_state.q
        if st.session_state.feedback:
            st.error(f"### ❌ 答錯了！正確是：{q['correct']}")
            if st.button("下一題 ➔", type="primary"):
                st.session_state.feedback = False
                if st.session_state.step < TOTAL_QUESTIONS:
                    st.session_state.step += 1
                    st.session_state.q = get_new_q()
                else: st.session_state.game_over = True
                st.rerun()
        else:
            st.subheader(q['text'])
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
        st.header(f"🏁 完成！總分：{st.session_state.score}")
        name = st.text_input("輸入大名登入英雄榜：", max_chars=10)
        if st.button("提交成績 🚀", type="primary"):
            if name:
                save_score(name, st.session_state.score)
                st.success("已存入英雄榜！")
            else: st.warning("請輸入名字喔！")
        if st.button("再戰一次 🔄"):
            st.session_state.step, st.session_state.score = 1, 0
            st.session_state.game_over, st.session_state.feedback = False, False
            st.session_state.q = get_new_q()
            st.rerun()

# --- 排行榜標籤頁 ---
with tab_rank:
    st.header("🏆 英雄榜 (TOP 10)")
    lb = get_leaderboard(10)
    if lb is not None:
        st.table(lb)
    else:
        st.info("目前尚無紀錄。")
    
    st.divider()
    
    # --- 新增：老師專用管理區 ---
    st.subheader("⚙️ 老師管理區域")
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🔄 刷新榜單"):
            st.rerun()
    with col2:
        confirm = st.checkbox("確認要清空所有紀錄嗎？")
        if st.button("🗑️ 清除排行榜資料", disabled=not confirm):
            clear_leaderboard()
            st.success("排行榜已成功清空！")
            st.rerun()
