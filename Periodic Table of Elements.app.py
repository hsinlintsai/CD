import streamlit as st
import random
import time
import pandas as pd
import os

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="元素時速挑戰賽", page_icon="⚡", layout="centered")

# --- 2. 排行榜邏輯 ---
DB_FILE = "leaderboard_final.csv"

def save_score(name, score, level):
    new_data = pd.DataFrame([[name, score, level, time.strftime("%Y-%m-%d %H:%M")]], 
                            columns=["姓名", "分數", "關卡", "時間"])
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else: df = new_data
    df.to_csv(DB_FILE, index=False)

def get_level_rank(level_name, limit=5):
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        filtered = df[df["關卡"] == level_name]
        return filtered.sort_values(by="分數", ascending=False).head(limit)
    return None

# --- 3. 遊戲資料庫 (含 HTML 下標) ---
LV1_DB = [{"s": "H", "n": "氫"}, {"s": "He", "n": "氦"}, {"s": "Li", "n": "鋰"}, {"s": "Be", "n": "鈹"}, {"s": "B", "n": "硼"}, {"s": "C", "n": "碳"}, {"s": "N", "n": "氮"}, {"s": "O", "n": "氧"}, {"s": "F", "n": "氟"}, {"s": "Ne", "n": "氖"}, {"s": "Na", "n": "鈉"}, {"s": "Mg", "n": "鎂"}, {"s": "Al", "n": "鋁"}, {"s": "Si", "n": "矽"}, {"s": "P", "n": "磷"}, {"s": "S", "n": "硫"}, {"s": "Cl", "n": "氯"}, {"s": "Ar", "n": "氬"}, {"s": "K", "n": "鉀"}, {"s": "Ca", "n": "鈣"}, {"s": "Fe", "n": "鐵"}, {"s": "Cu", "n": "銅"}, {"s": "Zn", "n": "鋅"}]
LV2_DB = [{"s": "Li", "n": "鋰"}, {"s": "Na", "n": "鈉"}, {"s": "K", "n": "鉀"}, {"s": "Be", "n": "鈹"}, {"s": "Mg", "n": "鎂"}, {"s": "Ca", "n": "鈣"}, {"s": "B", "n": "硼"}, {"s": "Al", "n": "鋁"}, {"s": "C", "n": "碳"}, {"s": "Si", "n": "矽"}, {"s": "N", "n": "氮"}, {"s": "P", "n": "磷"}, {"s": "O", "n": "氧"}, {"s": "S", "n": "硫"}, {"s": "F", "n": "氟"}, {"s": "Cl", "n": "氯"}, {"s": "Br", "n": "溴"}, {"s": "I", "n": "碘"}, {"s": "He", "n": "氦"}, {"s": "Ne", "n": "氖"}, {"s": "Ar", "n": "氬"}]
LV3_DB = [
    {"s": "H<sub>2</sub>O", "n": "水"}, {"s": "CO<sub>2</sub>", "n": "二氧化碳"}, {"s": "NaCl", "n": "食鹽"}, {"s": "HCl", "n": "鹽酸"}, 
    {"s": "H<sub>2</sub>SO<sub>4</sub>", "n": "硫酸"}, {"s": "HNO<sub>3</sub>", "n": "硝酸"}, {"s": "NaOH", "n": "氫氧化鈉"}, 
    {"s": "CaCO<sub>3</sub>", "n": "碳酸鈣"}, {"s": "NaHCO<sub>3</sub>", "n": "小蘇打"}, {"s": "Na<sub>2</sub>CO<sub>3</sub>", "n": "蘇打"}, 
    {"s": "NH<sub>3</sub>", "n": "氨氣"}, {"s": "CH<sub>4</sub>", "n": "甲烷"}, {"s": "C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>", "n": "葡萄糖"}, 
    {"s": "C<sub>2</sub>H<sub>5</sub>OH", "n": "酒精"}, {"s": "CH<sub>3</sub>COOH", "n": "醋酸"}, {"s": "CaO", "n": "生石灰"}, 
    {"s": "Ca(OH)<sub>2</sub>", "n": "熟石灰"}, {"s": "H<sub>2</sub>O<sub>2</sub>", "n": "雙氧水"}
]

# --- 4. CSS 樣式修正 (強化字體顯現) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    /* 選項按鈕：強化字體自適應 */
    button[kind="secondary"] {
        height: 10vh !important; min-height: 55px !important;
        border-radius: 12px !important; margin-bottom: 8px !important;
        border: 2px solid #4A90E2 !important; background-color: #FFFFFF !important;
    }
    /* 強制放大按鈕內的文字 span */
    button[kind="secondary"] span { 
        font-size: clamp(24px, 6vh, 45px) !important; 
        font-weight: 900 !important; color: #1A1A1A !important; 
    }
    /* 遊戲中標題稍微縮小給返回鍵空間 */
    .game-header { display: flex; justify-content: space-between; align-items: center; }
    
    button[kind="primary"] { height: 9vh !important; background-color: #FF4B4B !important; }
    button[kind="primary"] p { font-size: clamp(20px, 4vh, 32px) !important; color: #FFFFFF !important; }
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

# --- 6. 介面介面 ---
tab_game, tab_rank = st.tabs(["🎮 挑戰", "🏆 榮譽榜"])

with tab_game:
    if st.session_state.game_state == "HOME":
        st.title("⚡ 元素時速挑戰")
        if st.button("🟢 第一關：原子序 1-30", use_container_width=True):
            st.session_state.current_db, st.session_state.level_name, st.session_state.game_state = LV1_DB, "第一關", "START_CLICK"
            st.rerun()
        if st.button("🔵 第二關：主族元素 1A-8A", use_container_width=True):
            st.session_state.current_db, st.session_state.level_name, st.session_state.game_state = LV2_DB, "第二關", "START_CLICK"
            st.rerun()
        if st.button("🔴 第三關：必考化合物", use_container_width=True):
            st.session_state.current_db, st.session_state.level_name, st.session_state.game_state = LV3_DB, "第三關", "START_CLICK"
            st.rerun()

    elif st.session_state.game_state == "START_CLICK":
        st.subheader(f"目標：{st.session_state.level_name}")
        if st.button("開始！", type="primary", use_container_width=True):
            st.session_state.step, st.session_state.score, st.session_state.feedback, st.session_state.game_state = 1, 0, False, "PLAYING"
            st.session_state.q = get_new_q(st.session_state.current_db)
            st.rerun()

    elif st.session_state.game_state == "PLAYING":
        # 頂部返回區
        col_info, col_back = st.columns([3, 1])
        with col_info:
            st.write(f"第 {st.session_state.step}/10 題 | 分數: {st.session_state.score}")
        with col_back:
            if st.button("⬅️ 返回", key="back_home"):
                st.session_state.game_state = "HOME"; st.rerun()
        
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
            st.markdown(f"### {q['text']}", unsafe_allow_html=True)
            for idx, opt in enumerate(q['options']):
                if st.button(opt, key=f"opt_{idx}", use_container_width=True):
                    elapsed = time.time() - q['start_time']
                    if opt == q['correct']:
                        pts = 100 if elapsed <= 1.5 else max(0, int(100 - (elapsed - 1.5) * 10))
                        st.session_state.score += pts
                        if st.session_state.step < 10:
                            st.session_state.step += 1
                            st.session_state.q = get_new_q(st.session_state.current_db); st.rerun()
                        else: st.session_state.game_state = "FINISHED"; st.rerun()
                    else: st.session_state.feedback = True; st.rerun()

    elif st.session_state.game_state == "FINISHED":
        st.balloons()
        st.header(f"🏁 {st.session_state.level_name} 完成！")
        st.subheader(f"最終得分：{st.session_state.score}")
        name = st.text_input("輸入名字登錄榮譽榜：", max_chars=8)
        if st.button("提交並返回主頁 🚀", type="primary", use_container_width=True):
            if name: 
                save_score(name, st.session_state.score, st.session_state.level_name)
                st.session_state.game_state = "HOME"; st.rerun()
            else: st.warning("請輸入名字喔！")
        if st.button("不留名直接返回", use_container_width=True):
            st.session_state.game_state = "HOME"; st.rerun()

with tab_rank:
    st.header("🏆 榮譽榜")
    c1, c2, c3 = st.columns(3)
    with c1: st.subheader("L1"); r1 = get_level_rank("第一關"); st.table(r1[["姓名", "分數"]]) if r1 is not None else st.write("無")
    with c2: st.subheader("L2"); r2 = get_level_rank("第二關"); st.table(r2[["姓名", "分數"]]) if r2 is not None else st.write("無")
    with c3: st.subheader("L3"); r3 = get_level_rank("第三關"); st.table(r3[["姓名", "分數"]]) if r3 is not None else st.write("無")

    st.divider()
    # 密碼保護清除區
    st.subheader("⚙️ 管理員選單")
    pwd = st.text_input("輸入清除密碼：", type="password")
    if st.button("🗑️ 執行清空排行榜", disabled=(pwd != "9306696"), use_container_width=True):
        if os.path.exists(DB_FILE): os.remove(DB_FILE)
        st.success("排行榜已成功歸零！")
        st.rerun()
    if st.button("🔄 刷新頁面"): st.rerun()
