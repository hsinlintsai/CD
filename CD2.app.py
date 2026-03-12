import streamlit as st
import random
import time
import pandas as pd
import os

# 設定網頁標題
st.set_page_config(page_title="元素時速挑戰", page_icon="⚡")

# --- 1. 排行榜邏輯 ---
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

def get_leaderboard():
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        # 排序分數，並去除重複名字取最高分
        df = df.sort_values(by="分數", ascending=False)
        return df.head(5)
    return None

# --- 2. CSS：文字極大、框框精簡 ---
st.markdown("""
    <style>
    button[kind="secondary"] p { font-size: 42px !important; font-weight: 900 !important; }
    button[kind="secondary"] { height: 75px !important; border-radius: 12px !important; border: 2px solid #E0E0E0 !important; }
    .next-btn button { background-color: #FF4B4B !important; color: white !important; height: 85px !important; }
    .next-btn button p { font-size: 32px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 遊戲資料庫 (國中必考) ---
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
    return {"text": f"「 {target['s'] } 」是什麼？" if mode == 's2n' else f"「 {target['n']} 」的符號？",
            "correct": correct, "options": options, "start_time": time.time()}

# 初始化狀態 (改為 10 題)
TOTAL_STEPS = 10

if 'step' not in st.session_state:
    st.session_state.step, st.session_state.score = 1, 0
    st.session_state.game_over, st.session_state.feedback = False, False
    st.session_state.q = get_new_q()

def play(url):
    st.components.v1.html(f"""<audio autoplay><source src="{url}" type="audio/mpeg"></audio>""", height=0)

# --- 4. 介面渲染 ---
st.title("⚡ 元素 10 題速考王")

if not st.session_state.game_over:
    st.progress(st.session_state.step / TOTAL_STEPS)
    st.write(f"第 {st.session_state.step}/{TOTAL_STEPS} 題 | 總分: **{st.session_state.score}**")
    q = st.session_state.q

    if st.session_state.feedback:
        st.error(f"### ❌ 答錯了！正確是：{q['correct']}")
        st.markdown('<div class="next-btn">', unsafe_allow_html=True)
        if st.button("下一題 ➔", use_container_width=True):
            st.session_state.feedback = False
            if st.session_state.step < TOTAL_STEPS:
                st.session_state.step += 1
                st.session_state.q = get_new_q()
            else: st.session_state.game_over = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.subheader(q['text'])
        for idx, opt in enumerate(q['options']):
            if st.button(opt, key=f"opt_{idx}", use_container_width=True):
                dur = time.time() - q['start_time']
                if opt == q['correct']:
                    # 答對：基礎 15 分，每秒扣 2.5 分 (更嚴格的時間獎勵)
                    pts = max(1, int(15 - (dur * 2.5)))
                    st.session_state.score += pts
                    play("https://www.soundjay.com/buttons/sounds/button-37.mp3")
                    if st.session_state.step < TOTAL_STEPS:
                        st.session_state.step += 1
                        st.session_state.q = get_new_q()
                        st.rerun()
                    else: st.session_state.game_over = True; st.rerun()
                else:
                    play("https://www.soundjay.com/buttons/sounds/button-10.mp3")
                    st.session_state.feedback = True; st.rerun()
else:
    st.balloons()
    st.header(f"🏁 挑戰完成！總得分：{st.session_state.score}")
    
    # 排行榜登錄
    with st.expander("👑 登錄排行榜 (前五強)", expanded=True):
        name = st.text_input("輸入你的暱稱：", max_chars=10)
        if st.button("提交成績"):
            if name:
                save_score(name, st.session_state.score)
                st.success("成功登錄！")
                st.rerun()
            else: st.warning("請輸入名字喔！")

    st.subheader("🏆 全班最強 TOP 5")
    lb = get_leaderboard()
    if lb is not None:
        st.table(lb)
    
    if st.button("再戰一次 🔄", use_container_width=True):
        st.session_state.step, st.session_state.score = 1, 0
        st.session_state.game_over, st.session_state.feedback = False, False
        st.session_state.q = get_new_q()
        st.rerun()
