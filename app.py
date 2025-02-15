import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import gradio as gr
from dotenv import load_dotenv

load_dotenv()

def get_deepseek_response(prompt):
    """Fetches a response from the DeepSeek API based on the given prompt."""
    client = ChatCompletionsClient(
    endpoint=os.environ["ENDPOINT"],
    credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
    )
    response = client.complete(
    messages=[
        SystemMessage("You are a helpful code reviewer."),
        UserMessage(prompt),
    ],
    # max_tokens=1000,
    model=os.environ["MODEL_NAME"],
    stream=False,
    )
    # print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()

def review_code(code_snippet):
    prompt = f"""
    Code Snippet:
    {code_snippet}

    Task: Analyze the provided code snippet. Identify any errors or potential improvements, suggest optimizations, and provide alternative implementations if applicable.
    """
    return get_deepseek_response(prompt)



def code_reviewer_ui(code):
    return review_code(code)

description = """
<div style="text-align: center; font-weight: bold; font-size: 18px;">
Analyze your code snippets, receive expert feedback, and unlock improvements effortlessly! 🚀
</div>
"""

interface = gr.Interface(
    fn=code_reviewer_ui,
    inputs=gr.Code(language="python", lines=20, label="📝 Paste Your Code Here"),
    outputs=gr.Textbox(label="🔍 Review Feedback"),
    title="AI Code Reviewer Assistant 🤖",
    description=description
)

interface.launch()
# interface.launch(share=True)