{\rtf1\ansi\ansicpg950\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import random\
\
# \uc0\u35373 \u23450 \u32178 \u38913 \u27161 \u38988 \u33287 \u22294 \u31034 \
st.set_page_config(page_title="\uc0\u20803 \u32032 \u25361 \u25136 \u36093 ", page_icon="\u55358 \u56810 ")\
\
# \uc0\u20803 \u32032 \u36039 \u26009  (\u21487 \u20197 \u33258 \u34892 \u25844 \u20805 )\
if 'elements' not in st.session_state:\
    st.session_state.elements = [\
        \{"s": "H", "n": "\uc0\u27691 "\}, \{"s": "He", "n": "\u27686 "\}, \{"s": "Li", "n": "\u37616 "\},\
        \{"s": "Be", "n": "\uc0\u37433 "\}, \{"s": "B", "n": "\u30844 "\}, \{"s": "C", "n": "\u30899 "\},\
        \{"s": "N", "n": "\uc0\u27694 "\}, \{"s": "O", "n": "\u27687 "\}, \{"s": "F", "n": "\u27679 "\},\
        \{"s": "Ne", "n": "\uc0\u27670 "\}, \{"s": "Na", "n": "\u37385 "\}, \{"s": "Mg", "n": "\u37762 "\}\
    ]\
\
# \uc0\u21021 \u22987 \u21270 \u36938 \u25138 \u29376 \u24907 \
if 'score' not in st.session_state:\
    st.session_state.score = 0\
    st.session_state.hearts = 3\
    st.session_state.current_ques = random.choice(st.session_state.elements)\
    st.session_state.mode = random.choice(['s2n', 'n2s']) # \uc0\u31526 \u34399 \u29468 \u21517 \u31281  \u25110  \u21517 \u31281 \u29468 \u31526 \u34399 \
\
def next_question():\
    st.session_state.current_ques = random.choice(st.session_state.elements)\
    st.session_state.mode = random.choice(['s2n', 'n2s'])\
\
# \uc0\u32178 \u38913 \u20171 \u38754 \
st.title("\uc0\u55358 \u56810  \u20803 \u32032 \u36913 \u26399 \u34920 \u65306 \u22810 \u37168 \u22283 \u25361 \u25136 \u29256 ")\
st.write(f"### \uc0\u21097 \u39192 \u29983 \u21629 : \{'\u10084 \u65039 ' * st.session_state.hearts\}")\
st.write(f"### \uc0\u30446 \u21069 \u24471 \u20998 : \{st.session_state.score\}")\
\
if st.session_state.hearts > 0:\
    q = st.session_state.current_ques\
    if st.session_state.mode == 's2n':\
        st.subheader(f"\uc0\u35531 \u21839 \u31526 \u34399 \u12300  \{q['s']\} \u12301 \u30340 \u20013 \u25991 \u21517 \u31281 \u26159 \u65311 ")\
        ans = q['n']\
    else:\
        st.subheader(f"\uc0\u35531 \u21839 \u12300  \{q['n']\} \u12301 \u30340 \u20803 \u32032 \u31526 \u34399 \u26159 \u65311 ")\
        ans = q['s']\
\
    user_ans = st.text_input("\uc0\u22312 \u36889 \u35041 \u36664 \u20837 \u31572 \u26696 ...", key="input").strip()\
\
    if st.button("\uc0\u25552 \u20132 \u31572 \u26696 "):\
        if user_ans.lower() == ans.lower():\
            st.success("\uc0\u9989  \u22826 \u26834 \u20102 \u65281 \u31572 \u23565 \u20102 \u65281 ")\
            st.session_state.score += 10\
            next_question()\
            st.rerun()\
        else:\
            st.error(f"\uc0\u10060  \u31572 \u37679 \u22217 \u65281 \u27491 \u30906 \u31572 \u26696 \u26159 \u65306 \{ans\}")\
            st.session_state.hearts -= 1\
            if st.session_state.hearts > 0:\
                next_question()\
                st.rerun()\
else:\
    st.error("\uc0\u55357 \u56448  \u25361 \u25136 \u32080 \u26463 \u65281 \u24859 \u24515 \u29992 \u23436 \u22217 \u12290 ")\
    if st.button("\uc0\u37325 \u26032 \u38283 \u22987 "):\
        st.session_state.score = 0\
        st.session_state.hearts = 3\
        next_question()\
        st.rerun()}