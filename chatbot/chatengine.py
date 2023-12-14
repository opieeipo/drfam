import os
from langchain.llms import OpenAI
import openai


OPENAI_API_KEY = os.environ['OPEN_API_KEY']
openai.api_key = OPENAI_API_KEY

def askChatGPT(question):
  messages = [ {"role": "system", "content":"You are a intelligent assistant."} ]
  messages.append({"role": "user", "content": question})
  chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
  answer = chat.choices[0].message.content
  return answer

def askADA(question):  
  messages = [ {"role": "system", "content":"You are a intelligent assistant."} ]
  messages.append({"role": "user", "content": question})
  chat = openai.ChatCompletion.create(model="text-ada-001", messages=messages)
  answer = chat.choices[0].message.content
  return answer


def queryAI(query,qae):
  try:
   result = qae({"query": query})["result"]  
  except openai.error.Timeout as e:
   #Handle timeout error, e.g. retry or log
   result=f"OpenAI API request timed out: {e}"
   pass
  except openai.error.APIError as e:
   #Handle API error, e.g. retry or log
   result=f"OpenAI API returned an API Error: {e}"
   pass
  except openai.error.APIConnectionError as e:
   #Handle connection error, e.g. check network or log
   result=f"OpenAI API request failed to connect: {e}"
   pass
  except openai.error.InvalidRequestError as e:
   #Handle invalid request error, e.g. validate parameters or log
   result=f"OpenAI API request was invalid: {e}"
   pass
  except openai.error.AuthenticationError as e:
   #Handle authentication error, e.g. check credentials or log
   result=f"OpenAI API request was not authorized: {e}"
   pass
  except openai.error.PermissionError as e:
   #Handle permission error, e.g. check scope or log
   result=f"OpenAI API request was not permitted: {e}"
   pass
  except openai.error.RateLimitError as e:
   #Handle rate limit error, e.g. wait or log
   result=f"OpenAI API request exceeded rate limit: {e}"
   pass
  return result

def getReference(answer,qae):
  prompt="Provide only the name of the reference that explains the following "+answer
  result=queryAI(prompt,qae)
  return result
