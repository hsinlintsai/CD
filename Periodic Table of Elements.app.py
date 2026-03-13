import streamlit as st
import random
import time
import pandas as pd
import os

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="元素挑戰賽", page_icon="⚡", layout="centered")

# --- 2. 排行榜邏輯 (徹底解決 KeyError 問題) ---
DB_FILE = "leaderboard_stable_v8.csv"

def save_score(name, score, level):
    new_data = pd.DataFrame([[name, score, level, time.strftime("%m/%d %H:%M")]], 
                            columns=["姓名", "分數", "關卡", "時間"])
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            # 確保舊資料有正確欄位，若無則重設
            if "關卡" not in df.columns:
                df = new_data
            else:
                df = pd.concat([df, new_data], ignore_index=True)
        except:
            df = new_data
    else:
        df = new_data
    df.to_csv(DB_FILE, index=False)

def get_level_rank(level_name):
    if not os.path.exists(DB_FILE):
        return None
    try:
        df = pd.read_csv(DB_FILE)
        if "關卡" in df.columns and "分數" in df.columns:
            f = df[df["關卡"] == level_name]
            return f.sort_values(by="分數", ascending=False).head(5)
    except:
        return None
    return None

# --- 3. 遊戲資料庫 ---
LV1_DB = [{"s": "H", "n": "氫"}, {"s": "He", "n": "氦"}, {"s": "Li", "n": "鋰"}, {"s": "Be", "n": "鈹"}, {"s": "B", "n": "硼"}, {"s": "C", "n": "碳"}, {"s": "N", "n": "氮"}, {"s": "O", "n": "氧"}, {"s": "F", "n": "氟"}, {"s": "Ne", "n": "氖"}, {"s": "Na", "n": "鈉"}, {"s": "Mg", "n": "鎂"}, {"s": "Al", "n": "鋁"}, {"s": "Si", "n": "矽"}, {"s": "P", "n": "磷"}, {"s": "S", "n": "硫"}, {"s": "Cl", "n": "氯"}, {"s": "Ar", "n": "氬"}, {"s": "K", "n": "鉀"}, {"s": "Ca", "n": "鈣"}]
LV2_DB = [{"s": "Li", "n": "鋰"}, {"s": "Na", "n": "鈉"}, {"s": "K", "n": "鉀"}, {"s": "Be", "n": "鈹"}, {"s": "Mg", "n": "鎂"}, {"s": "Ca", "n": "鈣"}, {"s": "B", "n": "硼"}, {"s": "Al", "n": "鋁"}, {"s": "C", "n": "碳"}, {"s": "Si", "n": "矽"}, {"s": "N", "n": "氮"}, {"s": "P", "n": "磷"}, {"s": "O", "n": "氧"}, {"s": "S", "n": "硫"}, {"s": "F", "n": "氟"}, {"s": "Cl", "n": "氯"}, {"s": "Br", "n": "溴"}, {"s": "I", "n": "碘"}]
LV3_DB = [{"s": "H<sub>2</sub>O", "n": "水"}, {"s": "CO<sub>2</sub>", "n": "二氧化碳"}, {"s": "NaCl", "n": "食鹽"}, {"s": "HCl", "n": "鹽酸"}, {"s": "H<sub>2</sub>SO<sub>4</sub>", "n": "硫酸"}, {"s": "HNO<sub>3</sub>", "n": "硝酸"}, {"s": "NaOH", "n": "氫氧化鈉"}, {"s": "CaCO<sub>3</sub>", "n": "碳酸鈣"}, {"s": "NaHCO<sub>3</sub>", "n": "小蘇打"}]

# --- 4. CSS 樣式修正 (顏色與佈局) ---
st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem !important; }
    
    /* 修正選項：確保背景白、字體黑且巨大 */
    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #4A90E2 !important;
        height: 11vh !important;
        min-height: 60px !important;
        border-radius: 12px !important;
    }
    
    div.stButton > button[kind="secondary"] div[data-testid="stMarkdownContainer"] p {
        font-size: clamp(28px, 7vw, 55px) !important;
        font-weight: 900 !important;
        color: #1A1A1A !important; /* 強制文字顏色 */
    }

    /* 迷你返回鍵縮小 */
    .small-btn button {
        height: 30px !important;
        padding: 0px 8px !important;
        font-size: 12px !important;
    }

    /* 管理員按鈕列 */
    .admin-btn button { height: 35px !important; font-size: 13px !important; }

    button[kind="primary"] { background-color: #FF4B4B !important; height: 9vh !important; }
    button[kind="primary"] p { font-size: 24px !important; color: white !important; }
    
    #MainMenu, footer, header {visibility: hidden;}
    sub { font-size: 0.6em !important; }
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

# --- 6. 介面主體 ---
tab_game, tab_rank = st.tabs(["🎮 挑戰模式", "🏆 榮譽榜"])

with tab_game:
    # 標題與返回鍵並排
    t_col, b_col = st.columns([3, 1])
    
    if st.session_state.game_state == "HOME":
        t_col.title("⚡ 元素挑戰")
        if st.button("🟢 原子序1-30", use_container_width=True):
            st.session_state.current_db, st.session_state.level_name, st.session_state.game_state = LV1_DB, "第一關", "START_CLICK"; st.rerun()
        if st.button("🔵 主族1A-8A", use_container_width=True):
            st.session_state.current_db, st.session_state.level_name, st.session_state.game_state = LV2_DB, "第二關", "START_CLICK"; st.rerun()
        if st.button("🔴 必考化合物", use_container_width=True):
            st.session_state.current_db, st.session_state.level_name, st.session_state.game_state = LV3_DB, "第三關", "START_CLICK"; st.rerun()

    else:
        # 遊戲進行中，顯示縮小的返回鍵
        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
        if b_col.button("⬅️回首頁"):
            st.session_state.game_state = "HOME"; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if st.session_state.game_state == "START_CLICK":
            t_col.subheader(st.session_state.level_name)
            if st.button("開始遊戲！", type="primary", use_container_width=True):
                st.session_state.step, st.session_state.score, st.session_state.feedback, st.session_state.game_state = 1, 0, False, "PLAYING"
                st.session_state.q = get_new_q(st.session_state.current_db); st.rerun()

        elif st.session_state.game_state == "PLAYING":
            t_col.write(f"第 {st.session_state.step}/10 題 | 分數: {st.session_state.score}")
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
            st.balloons(); st.header(f"🏁 完成！總分：{st.session_state.score}")
            name = st.text_input("輸入名字：", max_chars=8)
            if st.button("提交並回首頁 🚀", type="primary", use_container_width=True):
                if name: save_score(name, st.session_state.score, st.session_state.level_name); st.session_state.game_state = "HOME"; st.rerun()

with tab_rank:
    st.header("🏆 榮譽榜")
    r1, r2, r3 = st.columns(3)
    with r1: st.write("**L1**"); lb1 = get_level_rank("第一關")
    if lb1 is not None: st.table(lb1[["姓名", "分數"]])
    with r2: st.write("**L2**"); lb2 = get_level_rank("第二關")
    if lb2 is not None: st.table(lb2[["姓名", "分數"]])
    with r3: st.write("**L3**"); lb3 = get_level_rank("第三關")
    if lb3 is not None: st.table(lb3[["姓名", "分數"]])
    
    st.divider(); st.write("⚙️ 管理員")
    st.markdown('<div class="admin-btn">', unsafe_allow_html=True)
    c_pwd, c_clr, c_ref = st.columns([2, 1, 1])
    with c_pwd: pwd = st.text_input("密碼", type="password", label_visibility="collapsed")
    with c_clr:
        if st.button("🗑️清空", disabled=(pwd != "9306696"), use_container_width=True):
            if os.path.exists(DB_FILE): os.remove(DB_FILE)
            st.rerun()
    with c_ref: st.button("🔄刷新", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
