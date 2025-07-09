import streamlit as st
import time
import pandas as pd
import datetime

st.set_page_config(layout='wide')
# st.set_page_config(layout='centered')

st.title('Streamlit Dialog')

if 'input_value' not in st.session_state:
    st.session_state['input_value'] = 'Hi~ How are you?'

if 'num_value' not in st.session_state:
    st.session_state['num_value'] = 0

if 'enabled' not in st.session_state:
    st.session_state['enabled'] = False

if 'gender' not in st.session_state:
    st.session_state['gender'] = 'Male'

if 'message' not in st.session_state:
    st.session_state['message'] = None

def update_radio():
    if st.session_state['gender'] == 'Male':
        st.toast("I'm a man", icon='👨')
    else:
        st.toast("I'm a woman", icon='👩')


st.header('Progress Bar')
progress_bar = st.progress(0, text='Ready')

col1, col2 = st.columns(2)
if col1.button("Start", use_container_width=False):
    for i in range(100):
        progress_bar.progress(i, text='Running...')
        time.sleep(0.1)
col2.button("Stop", use_container_width=True)
st.divider()

st.header('Text Input')
st.text_input("입력창", value=st.session_state['input_value'])
col3, col4 = st.columns(2)
if col3.button("문자 입력값 가져오기", use_container_width=True):
    st.write(st.session_state['input_value'])
if col4.button("문자 입력값 설정하기", use_container_width=True):
    st.session_state['input_value'] = 'Fine, Thank you and you?'
    st.rerun()
st.divider()

st.header('Number Input')
st.number_input("숫자를 입력하세요", min_value=0, max_value=10, step=1, value = st.session_state['num_value'])
col5, col6 = st.columns(2)
if col5.button("숫자 입력값 가져오기", use_container_width=True):
    st.write(st.session_state['num_value'])
if col6.button("숫자 입력값 설정하기", use_container_width=True):
    st.session_state['num_value'] = 5
    st.rerun()
st.divider()

col7, col8 = st.columns(2)
with col7:
    st.header("Radio Button")
    init_radio = 0
    st.radio("Select your gender", ["Male", "Femail"], index=init_radio, key="gender", on_change=update_radio)
    st.write(st.session_state['gender'])

with col8:
    st.header('Check Box')
    init_cb = False
    # st.checkbox("Select enabled or disabled", value=init_cb, key="enabled")
    # st.write(st.session_state['enabled'])
    cb = st.checkbox("Select enabled or disabled", value=init_cb)
    st.write(cb)
st.divider()

st.header('Select Box')
name = st.selectbox("What's your family name?", ('Kim', 'Park', 'Lee'), index=None)
st.write(name)
st.divider()

st.header('Color Picker')
color = st.color_picker("Pick A Color", "#00f900")
st.write("The current color is", color)
st.divider()

st.header('Date Picker')
d = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
st.write("Your birthday is:", d)
st.divider()

st.header('Toggle')
on = st.toggle("Power")
if on:
    st.write("Power is On")
else:
    st.write("Power is Off")
st.divider()

st.header("Message")
col9, col10 = st.columns(2)
with col9:
    if st.button("Show Warning Message", use_container_width=True):
        st.session_state['message'] = "warning"

    if st.button("Show Success Message", use_container_width=True):
        st.session_state['message'] = "success"

with col10:
    if st.button("Show Error Message", use_container_width=True):
        st.session_state['message'] = "error"

    if st.button("Show Exception Message", use_container_width=True):
        st.session_state['message'] = "exception"

if st.session_state['message'] == 'warning':
    st.warning("Warning Message", icon="⚠️")
elif st.session_state['message'] == 'success':
    st.success("Success Message", icon="✅")
elif st.session_state['message'] == 'error':
    st.error("Error Message", icon="🚨")
elif st.session_state['message'] == 'exception':
    e = RuntimeError("This is an exception of type RuntimeError")
    st.exception(e)
st.divider()

st.header("Metric")
col11, col12, col13 = st.columns(3)
col11.metric("Temperature", "70 °F", "1.2 °F")
col12.metric("Wind", "9 mph", "-8%")
col13.metric("Humidity", "86%", "4%")
st.divider()

def df_on_change(df):
    state = st.session_state["df_editor"]
    print(state)
    for index, change_dict in state["edited_rows"].items():
        df.loc[df.index == index, "edited"] = True

df = pd.read_csv('Euro_2012_stats_TEAM.csv')

st.header("DataFrame")
st.dataframe(df, hide_index=True, height=200)
st.divider()

st.header("DataEditor")
st.data_editor(df, hide_index=True, key='df_editor', on_change=df_on_change, args=[df], height=200)
st.divider()

st.header('Table')
st.table(df)
st.divider()

st.header('Display SessionState')
st.write(st.session_state)
