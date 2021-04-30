import streamlit as st
from util import *
import time

st.header("Transcribe Audio")
sample = st.file_uploader(label="Upload Your Song File Here")
# st.subheader("OR RECORD YOURSELF")
# name = st.text_input(label="Enter name for the recorded file")
# duration = st.number_input(label="Enter Duration of recording")
# bt = st.button(label="Speak")


if sample:
    API_TOKEN, transcribe_id = upload_sample(sample)
    result = {}
    sleep = 1
    per_complete = 0
    progress_bar = st.progress(per_complete)
    st.text('In Queue')

    while result.get("status") != 'processing':
        per_complete += sleep
        time.sleep(sleep)
        progress_bar.progress(per_complete / 10)
        result = get_status(API_TOKEN, transcribe_id)

    sleep_duration = 0.01

    for percent in range(per_complete, 101):
        time.sleep(sleep_duration)
        progress_bar.progress(percent)

    with st.spinner("Processing....."):
        while result.get("status") != 'completed':
            result = get_status(API_TOKEN, transcribe_id)

    st.balloons()
    st.header("Transcribed Text")
    st.subheader(result['text'])
    print('Done')
