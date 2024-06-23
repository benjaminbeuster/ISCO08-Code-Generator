import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version=os.environ["AZURE_OPENAI_API_VERSION"]
)

response = client.chat.completions.create(
    model="gpt-4o", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Whos was Boris becker"}
    ]
)

print(response.choices[0].message.content)