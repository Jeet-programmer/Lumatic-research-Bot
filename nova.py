import openai
import os



openai.api_base = 'https://api.nova-oss.com/v1'
openai.api_key = os.environ['key']

def nova_llm(message):
  
  completion = openai.ChatCompletion.create(
          model='gpt-3.5-turbo',
          messages=[{'role': 'user','content': message,}])
  print(completion)

  return(completion["choices"][0]["message"]["content"])