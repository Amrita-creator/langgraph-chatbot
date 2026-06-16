import os
from dotenv import load_dotenv
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    max_new_tokens=2400,
)
model = ChatHuggingFace(llm=llm)

prompt = f"hey my name is amrita.."
ans = model.invoke(prompt)
print(ans)