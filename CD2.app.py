import streamlit as st
import random

# 設定網頁標題
st.set_page_config(page_title="元素週期表挑戰賽", page_icon="🧪")

# 1. 擴充元素資料庫 (包含國中常見元素)
elements_db = [
    {"s": "H", "n": "氫"}, {"s": "He", "n": "氦"}, {"s": "Li", "n": "鋰"}, {"s": "Be", "n": "鈹"},
    {"s": "B", "n": "硼"}, {"s": "C", "n": "碳"}, {"s": "N", "n": "氮"}, {"s": "O", "n": "氧"},
    {"s": "F", "n": "氟"}, {"s": "Ne", "n": "氖"}, {"s": "Na", "n": "鈉"}, {"s": "Mg", "n": "鎂"},
    {"s": "Al", "n": "鋁"}, {"s": "Si", "n": "矽"}, {"s": "P", "n": "磷"}, {"s": "S", "n": "硫"},
    {"s": "Cl", "n": "氯"}, {"s": "Ar", "n": "氬"}, {"s": "K", "n": "鉀"}, {"s": "Ca", "n": "鈣"},
    {"s": "Fe", "n": "鐵"}, {"s": "Cu", "n": "銅"}, {"s": "Zn", "n": "鋅"}, {"s": "Ag", "n": "銀"},
    {"s": "Au", "n": "金"}, {"s": "Hg", "n": "汞"}, {"s": "I", "n": "碘"}, {"s": "Ba", "n": "鋇"}
]

# 2. 初始化遊戲狀態
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1      # 目前第幾題
    st.session_state.score = 0             # 總分
    st.session_state.total_questions = 20  # 總題數
    st.session_state.game_over = False
    
    # 生成題目與選項的函數
    def generate_question():
        target = random.choice(elements_db)
        mode = random.choice(['s2n', 'n2s']) # 符號猜名稱 或 名稱猜符號
        
        # 準備正確答案與干擾項
        correct_ans = target['n'] if mode == 's2n' else target['s']
        all_options = [target['n'] if mode == 's2n' else target['s'] for target in elements_db]
        all_options.remove(correct_ans)
        
        # 隨機選 3 個錯的，加上 1 個對的
        distractors = random.sample(list(set(all_options)), 3)
        options = distractors + [correct_ans]
        random.shuffle(options)
        
        return {
            "question_text": f"符號「 {target['s']} 」的名稱是？" if mode == 's2n' else f"元素「 {target['n']} 」的符號是？",
            "correct": correct_ans,
            "options": options
        }

    st.session_state.current_ques = generate_question()

# 3. 介面設計
st.title("🧪 元素週期表 20題大挑戰")

if not st.session_state.game_over:
    # 顯示進度
    progress = st.session_state.current_step / st.session_state.total_questions
    st.progress(progress)
    st.write(f"第 {st.session_state.current_step} / {st.session_state.total_questions} 題")

    # 顯示題目
    q = st.session_state.current_ques
    st.subheader(q['question_text'])

    # 四選一按鈕
    cols = st.columns(2)
    for i, option in enumerate(q['options']):
        with cols[i % 2]:
            if st.button(option, key=f"btn_{i}", use_container_width=True):
                if option == q['correct']:
                    st.toast("✅ 答對了！", icon="🎉")
                    st.session_state.score += 5
                else:
                    st.toast(f"❌ 答錯了，正確答案是 {q['correct']}", icon="⚠️")
                
                # 進入下一題或結束
                if st.session_state.current_step < st.session_state.total_questions:
                    st.session_state.current_step += 1
                    # 重新定義 generate_question 逻辑來更新題目
                    target = random.choice(elements_db)
                    mode = random.choice(['s2n', 'n2s'])
                    correct_ans = target['n'] if mode == 's2n' else target['s']
                    all_options = [el['n'] if mode == 's2n' else el['s'] for el in elements_db]
                    all_options.remove(correct_ans)
                    distractors = random.sample(list(set(all_options)), 3)
                    new_options = distractors + [correct_ans]
                    random.shuffle(new_options)
                    
                    st.session_state.current_ques = {
                        "question_text": f"符號「 {target['s']} 」的名稱是？" if mode == 's2n' else f"元素「 {target['n']} 」的符號是？",
                        "correct": correct_ans,
                        "options": new_options
                    }
                    st.rerun()
                else:
                    st.session_state.game_over = True
                    st.rerun()

else:
    # 遊戲結束結算
    st.balloons()
    st.success(f"🏆 挑戰完成！你的最終得分是：{st.session_state.score} / 100")
    
    if st.button("再挑戰一次"):
        st.session_state.current_step = 1
        st.session_state.score = 0
        st.session_state.game_over = False
        # 重新生成題目 (邏輯同上)
        target = random.choice(elements_db)
        mode = random.choice(['s2n', 'n2s'])
        correct_ans = target['n'] if mode == 's2n' else target['s']
        all_options = [el['n'] if mode == 's2n' else el['s'] for el in elements_db]
        all_options.remove(correct_ans)
        distractors = random.sample(list(set(all_options)), 3)
        new_options = distractors + [correct_ans]
        random.shuffle(new_options)
        st.session_state.current_ques = {
            "question_text": f"符號「 {target['s']} 」的名稱是？" if mode == 's2n' else f"元素「 {target['n']} 」的符號是？",
            "correct": correct_ans,
            "options": new_options
        }
        st.rerun()
