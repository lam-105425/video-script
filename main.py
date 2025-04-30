import streamlit as st
import asyncio
from utils import generate_script
#from 半流式输出.前端 import subject

st.set_page_config(page_title="视频脚本生成器")
st.title("🎬视频脚本生成器")

with st.sidebar:
    st.header("⚙️配置参数")
    api_key = st.text_input("请输入DeepSeek API密钥",type="password")
    st.markdown("[获取DeepSeek API密钥](https://platform.deepseek.com/usage)")

subject = st.text_input("💡请输入视频主题")

creativity = st.slider("🧠请输入视频脚本的创造力(数字小说明更严谨，数字大说明更多样)",
                           min_value=0.00,max_value=1.20,value=1.00,step=0.01)
video_length = st.number_input("请输入视频大致时长(单位:分钟)",min_value=0.1,step=0.1)

submit = st.button("🚀生成脚本")

if submit and not api_key:
    st.error("请输入你的DeepSeek API密钥")
    st.stop()
if submit and not subject:
    st.error("请输入视频主题")
    st.stop()
if submit and not video_length >= 0.1:
    st.error("视频长度需大于或等于0.1")
    st.stop()
if submit:
    with st.spinner("思考中，请稍等..."):
        title_placeholder = st.empty()
        script_placeholder = st.empty()

        async def run_generation():

            current_title = ""
            current_script = ""

            async for data_type,chunk in generate_script(subject,video_length,creativity,api_key):
                if data_type == "title":
                    current_title += chunk
                    title_placeholder.markdown(f"## 🔥标题\n{current_title}")
                elif data_type == "script":
                    current_script += chunk
                    script_placeholder.markdown(f"## 📝视频脚本\n{current_script}")
            st.success("视频脚本已生成")

        asyncio.run(run_generation())