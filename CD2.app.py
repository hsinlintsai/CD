import streamlit as st
import random

# 設定網頁標題
st.set_page_config(page_title="元素週期表挑戰賽", page_icon="🧪")

# 1. 元素資料庫 (國中必背範圍)
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

# 2. 遊戲邏輯函數
def get_new_question():
    target = random.choice(st.session_state.elements_db)
    mode = random.choice(['s2n', 'n2s'])
    correct_ans = target['n'] if mode == 's2n' else target['s']
    
    # 產生干擾項
    all_vals = [el['n'] if mode == 's2n' else el['s'] for el in st.session_state.elements_db]
    all_vals = list(set(all_vals))
    all_vals.remove(correct_ans)
    options = random.sample(all_vals, 3) + [correct_ans]
    random.shuffle(options)
    
    return {
        "text": f"符號「 {target['s']} 」的名稱是？" if mode == 's2n' else f"元素「 {target['n']} 」的符號是？",
        "correct": correct_ans,
        "options": options,
        "full_info": f"{target['n']} ({target['s']})"
    }

# 初始化 Session State
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.show_feedback = False # 是否顯示答錯回饋
    st.session_state.last_result = None    # 紀錄上一題對錯
    st.session_state.q = get_new_question()

# --- 介面開始 ---
st.title("🧪 元素週期表 20題大挑戰")

if not st.session_state.game_over:
    # 顯示進度
    progress = st.session_state.current_step / 20
    st.progress(progress)
    st.write(f"第 {st.session_state.current_step} / 20 題 | 目前得分: {st.session_state.score}")
    
    q = st.session_state.q

    # 如果正在顯示回饋 (答錯的情況)
    if st.session_state.show_feedback:
        st.error(f"### ❌ 答錯了！")
        st.info(f"正確答案是：**{q['correct']}**")
        st.write(f"記得喔：{q['full_info']}")
        
        if st.button("我記住了，下一題 ➔"):
            st.session_state.show_feedback = False
            if st.session_state.current_step < 20:
                st.session_state.current_step += 1
                st.session_state.q = get_new_question()
            else:
                st.session_state.game_over = True
            st.rerun()

    else:
        # 顯示題目
        st.subheader(q['text'])
        
        # 四選一按鈕
        cols = st.columns(2)
        for i, option in enumerate(q['options']):
            with cols[i % 2]:
                if st.button(option, key=f"btn_{i}", use_container_width=True):
                    if option == q['correct']:
                        st.success("✅ 答對了！")
                        st.session_state.score += 5
                        # 答對直接跳下一題
                        if st.session_state.current_step < 20:
                            st.session_state.current_step += 1
                            st.session_state.q = get_new_question()
                            st.rerun()
                        else:
                            st.session_state.game_over = True
                            st.rerun()
                    else:
                        # 答錯則進入回饋模式
                        st.session_state.show_feedback = True
                        st.rerun()

else:
    # 結算畫面
    st.balloons()
    st.success(f"🏆 挑戰完成！最終得分：{st.session_state.score} / 100")
    if st.button("再玩一次"):
        st.session_state.current_step = 1
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.show_feedback = False
        st.session_state.q = get_new_question()
        st.rerun()
