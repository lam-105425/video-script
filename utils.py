from langchain_deepseek import ChatDeepSeek
from langchain.prompts import ChatPromptTemplate
import asyncio


title_template = ChatPromptTemplate.from_messages([
    ("human","请为{subject}这个主题的视频想一个吸引人的标题(一个就行，不要多个，不需要解释)")])
script_template = ChatPromptTemplate.from_messages([
    ("human",
    """你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个(是一个不是多个)视频脚本。
    视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
    要求开头抓住限球，中间提供干货内容，结尾有惊喜，脚本格式也请按照【开头、中间，结尾】分隔。
    整体内容的表达方式要根据标题而定(只写脚本就可以，不要有多余的解释)""")])


async def generate_script(subject,video_length,creativity,api_key):
    model = ChatDeepSeek(model="deepseek-chat",api_key=api_key,temperature=creativity)
    title_chain = title_template | model
    script_chain = script_template | model


    title = ""
    async for chunk in title_chain.astream({"subject":subject}):
        title += chunk.content
        yield ("title",chunk.content)

    script = ""
    async for chunk in script_chain.astream({"title":title,"duration":video_length}):
        script += chunk.content
        yield ("script",chunk.content)