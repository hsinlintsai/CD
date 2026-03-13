import streamlit as st
import random
import time
import pandas as pd
import os

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="元素時速挑戰賽", page_icon="⚡", layout="centered")

# --- 2. 排行榜邏輯 (修正版) ---
DB_FILE = "leaderboard_v4.csv"

def save_score(name, score, level):
    new_row = {"姓名": name, "分數": score, "關卡": level, "時間": time.strftime("%Y-%m-%d %H:%M")}
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        except:
            df = pd.DataFrame([new_row])
    else:
        df = pd.DataFrame([new_row])
    df.to_csv(DB_FILE, index=False)

def get_level_rank(level_name):
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            if "關卡" in df.columns:
                filtered = df[df["關卡"] == level_name]
                return filtered.sort_values(by="分數", ascending=False).head(5)
        except:
            return None
    return None

# --- 3. 遊戲資料庫 (HTML 下標) ---
LV1_DB = [{"s": "H", "n": "氫"}, {"s": "He", "n": "氦"}, {"s": "Li", "n": "鋰"}, {"s": "Be", "n": "鈹"}, {"s": "B", "n": "硼"}, {"s": "C", "n": "碳"}, {"s": "N", "n": "氮"}, {"s": "O", "n": "氧"}, {"s": "F", "n": "氟"}, {"s": "Ne", "n": "氖"}, {"s": "Na", "n": "鈉"}, {"s": "Mg", "n": "鎂"}, {"s": "Al", "n": "鋁"}, {"s": "Si", "n": "矽"}, {"s": "P", "n": "磷"}, {"s": "S", "n": "硫"}, {"s": "Cl", "n": "氯"}, {"s": "Ar", "n": "氬"}, {"s": "K", "n": "鉀"}, {"s": "Ca", "n": "鈣"}, {"s": "Fe", "n": "鐵"}, {"s": "Cu", "n": "銅"}, {"s": "Zn", "n": "鋅"}]
LV2_DB = [{"s": "Li", "n": "鋰"}, {"s": "Na", "n": "鈉"}, {"s": "K", "n": "鉀"}, {"s": "Be", "n": "鈹"}, {"s": "Mg", "n": "鎂"}, {"s": "Ca", "n": "鈣"}, {"s": "B", "n": "硼"}, {"s": "Al", "n": "鋁"}, {"s": "C", "n": "碳"}, {"s": "Si", "n": "矽"}, {"s": "N", "n": "氮"}, {"s": "P", "n": "磷"}, {"s": "O", "n": "氧"}, {"s": "S", "n": "硫"}, {"s": "F", "n": "氟"}, {"s": "Cl", "n": "氯"}, {"s": "Br", "n": "溴"}, {"s": "I", "n": "碘"}, {"s": "He", "n": "氦"}, {"s": "Ne", "n": "氖"}, {"s": "Ar", "n": "氬"}]
LV3_DB = [{"s": "H<sub>2</sub>O", "n": "水"}, {"s": "CO<sub>2</sub>", "n": "二氧化碳"}, {"s": "NaCl", "n": "食鹽"}, {"s": "HCl", "n": "鹽酸"}, {"s": "H<sub>2</sub>SO<sub>4</sub>", "n": "硫酸"}, {"s": "HNO<sub>3</sub>", "n": "硝酸"}, {"s": "NaOH", "n": "氫氧化鈉"}, {"s": "CaCO<sub>3</sub>", "n": "碳酸鈣"}, {"s": "NaHCO<sub>3</sub>", "n": "小蘇打"}, {"s": "Na<sub>2</sub>CO<sub>3</sub>", "n": "蘇打"}, {"s": "NH<sub>3</sub>", "n": "氨氣"}, {"s": "CH<sub>4</sub>", "n": "甲烷"}, {"s": "C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>", "n": "葡萄糖"}, {"s": "C<sub>2</sub>H<sub>5</sub>OH", "n": "酒精"}, {"s": "CH<sub>3</sub>COOH", "n": "醋酸"}, {"s": "CaO", "n": "生石灰"}, {"s": "Ca(OH)<sub>2</sub>", "n": "熟石灰"}]

# --- 4. CSS 強力修正 (針對字體與縮放) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    /* 極致字體放大：針對所有 secondary 按鈕內的文字容器 */
    button[kind="secondary"] div[data-testid="stMarkdownContainer"] p,
    button[kind="secondary"] span {
        font-size: clamp(28px, 6.5vh, 50px) !important; 
        font-weight: 900 !important;
        color: #1A1A1A !important;
        line-height: 1 !important;
    }
    button[kind="secondary"] {
        height: 12vh !important; 
        min-height: 65px !important;
        border: 3px solid #4A90E2 !important;
        background-color: #FFFFFF !important;
        border-radius: 15px !important;
    }
    button[kind="primary"] { height: 10vh !important; background-color: #FF4B4B !important; }
    button[kind="primary"] p { font-size: 28px !important; color: white !important; }
    #MainMenu, footer, header {visibility: hidden;}
    sub { font-size: 0.6em !important; bottom: -0.1em !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. 遊戲邏輯 ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = "HOME"

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

# --- 6. 介面介面 ---
tab_game, tab_rank = st.tabs(["🎮 挑戰", "🏆 榮譽榜"])

with tab_game:
    if st.session_state.game_state == "HOME":
        st.title("⚡ 元素時速挑戰")
        if st.button("🟢 第一關：原子序 1-30", use_container_width=True):
            st.session_state.current_db, st.session_state.level_name, st.session_state.game_state = LV1_DB, "第一關", "START_CLICK"; st.rerun()
        if st.button("🔵 第二關：主族元素 1A-8A", use_container_width=True):
            st.session_state.current_db, st.session_state.level_name, st.session_state.game_state = LV2_DB, "第二關", "START_CLICK"; st.rerun()
        if st.button("🔴 第三關：必考化合物", use_container_width=True):
            st.session_state.current_db, st.session_state.level_name, st.session_state.game_state = LV3_DB, "第三關", "START_CLICK"; st.rerun()

    elif st.session_state.game_state == "START_CLICK":
        st.subheader(f"目標：{st.session_state.level_name}")
        if st.button("開始！", type="primary", use_container_width=True):
            st.session_state.step, st.session_state.score, st.session_state.feedback, st.session_state.game_state = 1, 0, False, "PLAYING"
            st.session_state.q = get_new_q(st.session_state.current_db); st.rerun()

    elif st.session_state.game_state == "PLAYING":
        c_info, c_back = st.columns([3, 1])
        c_info.write(f"第 {st.session_state.step}/10 題 | 分數: {st.session_state.score}")
        if c_back.button("⬅️ 返回"): st.session_state.game_state = "HOME"; st.rerun()
        
        q = st.session_state.q
        if st.session_state.feedback:
            st.error(f"❌ 正確是：{q['correct']}")
            if st.button("下一題 ➔", type="primary", use_container_width=True):
                st.session_state.feedback = False
                if st.session_state.step < 10:
                    st.session_state.step += 1; st.session_state.q = get_new_q(st.session_state.current_db); st.rerun()
                else: st.session_state.game_state = "FINISHED"; st.rerun()
        else:
            st.markdown(f"### {q['text']}", unsafe_allow_html=True)
            for idx, opt in enumerate(q['options']):
                if st.button(opt, key=f"opt_{idx}", use_container_width=True):
                    elap = time.time() - q['start_time']
                    if opt == q['correct']:
                        pts = 100 if elap <= 1.5 else max(0, int(100 - (elap - 1.5) * 10))
                        st.session_state.score += pts
                        if st.session_state.step < 10:
                            st.session_state.step += 1; st.session_state.q = get_new_q(st.session_state.current_db); st.rerun()
                        else: st.session_state.game_state = "FINISHED"; st.rerun()
                    else: st.session_state.feedback = True; st.rerun()

    elif st.session_state.game_state == "FINISHED":
        st.balloons(); st.header(f"🏁 得分：{st.session_state.score}")
        name = st.text_input("輸入名字登錄榮譽榜：", max_chars=8)
        if st.button("提交並返回主頁 🚀", type="primary", use_container_width=True):
            if name: save_score(name, st.session_state.score, st.session_state.level_name); st.session_state.game_state = "HOME"; st.rerun()
            else: st.warning("請輸入名字")

with tab_rank:
    st.header("🏆 榮譽榜")
    for lv in ["第一關", "第二關", "第三關"]:
        st.subheader(lv)
        res = get_level_rank(lv)
        if res is not None and not res.empty: st.table(res[["姓名", "分數"]])
        else: st.write("尚無資料")
    
    st.divider(); st.subheader("⚙️ 管理員")
    pwd = st.text_input("輸入密碼：", type="password")
    if st.button("🗑️ 清空", disabled=(pwd != "9306696"), use_container_width=True):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.rerun()
