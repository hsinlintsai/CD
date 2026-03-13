import streamlit as st
import random
import time
import pandas as pd
import os

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="元素時速挑戰賽", page_icon="⚡", layout="centered")

# --- 2. 排行榜與資料庫邏輯 ---
DB_FILE = "leaderboard_v2.csv"

def save_score(name, score, level):
    new_data = pd.DataFrame([[name, score, level, time.strftime("%Y-%m-%d %H:%M")]], 
                            columns=["姓名", "分數", "關卡", "時間"])
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

# --- 3. 遊戲資料庫設定 ---
LV1_DB = [
    {"s": "H", "n": "氫"}, {"s": "He", "n": "氦"}, {"s": "Li", "n": "鋰"}, {"s": "Be", "n": "鈹"}, {"s": "B", "n": "硼"},
    {"s": "C", "n": "碳"}, {"s": "N", "n": "氮"}, {"s": "O", "n": "氧"}, {"s": "F", "n": "氟"}, {"s": "Ne", "n": "氖"},
    {"s": "Na", "n": "鈉"}, {"s": "Mg", "n": "鎂"}, {"s": "Al", "n": "鋁"}, {"s": "Si", "n": "矽"}, {"s": "P", "n": "磷"},
    {"s": "S", "n": "硫"}, {"s": "Cl", "n": "氯"}, {"s": "Ar", "n": "氬"}, {"s": "K", "n": "鉀"}, {"s": "Ca", "n": "鈣"},
    {"s": "Sc", "n": "鈧"}, {"s": "Ti", "n": "鈦"}, {"s": "V", "n": "釩"}, {"s": "Cr", "n": "鉻"}, {"s": "Mn", "n": "錳"},
    {"s": "Fe", "n": "鐵"}, {"s": "Co", "n": "鈷"}, {"s": "Ni", "n": "鎳"}, {"s": "Cu", "n": "銅"}, {"s": "Zn", "n": "鋅"}
]

LV2_DB = [
    {"s": "H", "n": "氫"}, {"s": "Li", "n": "鋰"}, {"s": "Na", "n": "鈉"}, {"s": "K", "n": "鉀"}, {"s": "Rb", "n": "銣"}, {"s": "Cs", "n": "銫"},
    {"s": "Be", "n": "鈹"}, {"s": "Mg", "n": "鎂"}, {"s": "Ca", "n": "鈣"}, {"s": "Sr", "n": "鍶"}, {"s": "Ba", "n": "鋇"},
    {"s": "B", "n": "硼"}, {"s": "Al", "n": "鋁"}, {"s": "Ga", "n": "鎵"}, {"s": "In", "n": "銦"},
    {"s": "C", "n": "碳"}, {"s": "Si", "n": "矽"}, {"s": "Ge", "n": "鍺"}, {"s": "Sn", "n": "錫"}, {"s": "Pb", "n": "鉛"},
    {"s": "N", "n": "氮"}, {"s": "P", "n": "磷"}, {"s": "As", "n": "砷"}, {"s": "Sb", "n": "銻"}, {"s": "Bi", "n": "鉍"},
    {"s": "O", "n": "氧"}, {"s": "S", "n": "硫"}, {"s": "Se", "n": "硒"}, {"s": "Te", "n": "碲"},
    {"s": "F", "n": "氟"}, {"s": "Cl", "n": "氯"}, {"s": "Br", "n": "溴"}, {"s": "I", "n": "碘"},
    {"s": "He", "n": "氦"}, {"s": "Ne", "n": "氖"}, {"s": "Ar", "n": "氬"}, {"s": "Kr", "n": "氪"}, {"s": "Xe", "n": "氙"}
]

LV3_DB = [
    {"s": "H2O", "n": "水"}, {"s": "CO2", "n": "二氧化碳"}, {"s": "NaCl", "n": "氯化鈉"}, {"s": "HCl", "n": "鹽酸"},
    {"s": "H2SO4", "n": "硫酸"}, {"s": "HNO3", "n": "硝酸"}, {"s": "NaOH", "n": "氫氧化鈉"}, {"s": "CaCO3", "n": "碳酸鈣"},
    {"s": "NaHCO3", "n": "小蘇打"}, {"s": "Na2CO3", "n": "蘇打粉"}, {"s": "NH3", "n": "氨氣"},
    {"s": "CH4", "n": "甲烷"}, {"s": "C6H12O6", "n": "葡萄糖"}, {"s": "C2H5OH", "n": "酒精"}, {"s": "CH3COOH", "n": "醋酸"},
    {"s": "CaO", "n": "生石灰"}, {"s": "Ca(OH)2", "n": "熟石灰"}, {"s": "H2O2", "n": "雙氧水"}
]

# --- 4. CSS 樣式修正：加入字體自適應 (Clamp) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; }
    
    /* 所有按鈕通用：強制單行與圓角 */
    button {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }

    /* 首頁與選項按鈕 */
    button[kind="secondary"] {
        height: 9vh !important; 
        min-height: 50px !important;
        border-radius: 12px !important;
        margin-bottom: 8px !important;
        border: 2px solid #4A90E2 !important;
        background-color: #FFFFFF !important;
        width: 100% !important;
    }

    /* 關鍵修正：字體根據螢幕寬度縮放，最小 18px，最大 32px */
    button[kind="secondary"] p {
        font-size: clamp(18px, 5vw, 32px) !important;
        font-weight: 800 !important;
        color: #1A1A1A !important;
    }
    
    /* 作答時的「元素符號」文字要再大一點，維持 6vh */
    .game-font button[kind="secondary"] p {
        font-size: clamp(24px, 7vh, 50px) !important;
    }

    /* 提交/下一題紅色大按鈕 */
    button[kind="primary"] {
        height: 10vh !important;
        background-color: #FF4B4B !important;
    }
    button[kind="primary"] p {
        font-size: clamp(20px, 4vh, 32px) !important;
        color: #FFFFFF !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 5. 遊戲邏輯 ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = "HOME"
    st.session_state.current_db = []
    st.session_state.level_name = ""

def get_new_q(db):
    target = random.choice(db)
    mode = random.choice(['s2n', 'n2s'])
    correct = target['n'] if mode == 's2n' else target['s']
    pool = list(set([el['n'] if mode == 's2n' else el['s'] for el in db]))
    pool.remove(correct)
    options = random.sample(pool, 3) + [correct]
    random.shuffle(options)
    return {"text": f"「{target['s']}」是什麼？" if mode == 's2n' else f"「{target['n']}」的符號？",
            "correct": correct, "options": options, "start_time": time.time()}

def play_sound(url):
    st.components.v1.html(f"""<audio autoplay><source src="{url}" type="audio/mpeg"></audio>""", height=0)

# --- 6. 介面介面 ---
tab_game, tab_rank = st.tabs(["🎮 挑戰", "🏆 榜單"])

with tab_game:
    if st.session_state.game_state == "HOME":
        st.title("⚡ 元素時速挑戰")
        st.write("選擇難度開始練習：")
        
        # 這裡會應用 clamp 字體，自動縮小不破框
        if st.button("🟢 L1：原子序 1-30", use_container_width=True):
            st.session_state.current_db = LV1_DB
            st.session_state.level_name = "1-30序號"
            st.session_state.game_state = "START_CLICK"
            st.rerun()
            
        if st.button("🔵 L2：主族元素 1A-8A", use_container_width=True):
            st.session_state.current_db = LV2_DB
            st.session_state.level_name = "主族元素"
            st.session_state.game_state = "START_CLICK"
            st.rerun()
            
        if st.button("🔴 L3：國中必考化合物", use_container_width=True):
            st.session_state.current_db = LV3_DB
            st.session_state.level_name = "必考化合物"
            st.session_state.game_state = "START_CLICK"
            st.rerun()

    elif st.session_state.game_state == "START_CLICK":
        st.subheader(f"目標關卡：{st.session_state.level_name}")
        st.write("📏 規則：10題，1.5秒後每秒扣10分。")
        if st.button("我準備好了，開始！", type="primary", use_container_width=True):
            st.session_state.step, st.session_state.score = 1, 0
            st.session_state.feedback = False
            st.session_state.q = get_new_q(st.session_state.current_db)
            st.session_state.game_state = "PLAYING"
            st.rerun()

    elif st.session_state.game_state == "PLAYING":
        st.write(f"第 {st.session_state.step}/10 題 | 分數: {st.session_state.score}")
        
        q = st.session_state.q
        
        if st.session_state.feedback:
            st.error(f"❌ 答錯！正確是：{q['correct']}")
            if st.button("下一題 ➔", type="primary", use_container_width=True):
                st.session_state.feedback = False
                if st.session_state.step < 10:
                    st.session_state.step += 1
                    st.session_state.q = get_new_q(st.session_state.current_db)
                else: st.session_state.game_state = "FINISHED"
                st.rerun()
        else:
            st.markdown(f"### {q['text']}")
            # 加入 game-font 類別讓作答按鈕文字更大
            st.markdown('<div class="game-font">', unsafe_allow_html=True)
            for idx, opt in enumerate(q['options']):
                if st.button(opt, key=f"opt_{idx}", use_container_width=True):
                    elapsed = time.time() - q['start_time']
                    if opt == q['correct']:
                        pts = 100 if elapsed <= 1.5 else max(0, int(100 - (elapsed - 1.5) * 10))
                        st.session_state.score += pts
                        play_sound("https://www.soundjay.com/buttons/sounds/button-37.mp3")
                        if st.session_state.step < 10:
                            st.session_state.step += 1
                            st.session_state.q = get_new_q(st.session_state.current_db)
                            st.rerun()
                        else: st.session_state.game_over = True; st.session_state.game_state = "FINISHED"; st.rerun()
                    else:
                        play_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                        st.session_state.feedback = True; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.game_state == "FINISHED":
        st.balloons()
        st.header(f"🏁 得分：{st.session_state.score}")
        name = st.text_input("輸入名字登錄英雄榜：", max_chars=8)
        if st.button("提交成績 🚀", type="primary", use_container_width=True):
            if name: save_score(name, st.session_state.score, st.session_state.level_name)
        if st.button("回首頁 🏠", use_container_width=True):
            st.session_state.game_state = "HOME"; st.rerun()

with tab_rank:
    st.write("🏆 TOP 10 榜單")
    lb = get_leaderboard(10)
    if lb is not None: st.table(lb)
    if st.button("🔄 刷新"): st.rerun()
    confirm = st.checkbox("清除紀錄模式")
    if st.button("🗑️ 執行清空", disabled=not confirm):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.rerun()
