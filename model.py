import os
import chromadb
from chromadb.config import Settings
from api import *
from flask import Flask
from flask_cors import CORS, cross_origin
# from nova import nova_llm
from google_search import compile_results_content


markdown_to_emoji = {
    # '**': '🟡 ',    # Strongly emphasized text
    '##': '📌',
    '**': '',
    '*': '👉 ',      # Emphasized text
    
    '#': '📌',    # Heading level 2
    '###': '📍 ',   # Heading level 3
    # '`': '💻 ',     # Inline code
    # '```': '📝 ',   # Code block
    # '[link]': '🔗 ', # Links
    '>': '💬 ',     # Blockquote
    # '-': '🔹 ',     # List item
}

def convert_markdown_to_emojis(text):
    for markdown, emoji in markdown_to_emoji.items():
        text = text.replace(markdown, emoji)
    return text


app = Flask(__name__)


def load_directory(directory):
  """Loads a directory and all files in it with .txt extension."""
  files = []
  for filename in os.listdir(directory):
    if filename.endswith(".txt"):
      files.append(os.path.join(directory, filename))
  return files


def text_to_chunks(texts, word_length=512, start_documents=1):
  files = load_directory(directory)

  chunks = []
  text_tokens = [t.split(" ") for t in texts]

  for idx, words in enumerate(text_tokens):
    for i in range(0, len(words), word_length):
      chunk = words[i:i + word_length]
      if ((i + word_length) > len(words) and (len(chunk) < word_length)
          and (len(text_tokens) != (idx + 1))):
        text_tokens[idx + 1] = chunk + text_tokens[idx + 1]
        continue
      chunk = ' '.join(chunk).strip()
      chunks.append({"source": files[idx], "content": chunk})
  return chunks


directory = "./Datasets"
files = load_directory(directory)

texts = []
for file in files:
  with open(file, "r") as f:
    text = f.read()
    texts.append(text)

chunks = text_to_chunks(texts, word_length=128, start_documents=1)


def create_chroma_db(chunks_list, name):
  client = chromadb.PersistentClient(path="./chatbots",
                                     settings=Settings(allow_reset=True))
  client.reset()
  client.heartbeat(
  )  # returns a nanosecond heartbeat. Useful for making sure the client remains connected.
  db = client.create_collection(name=name)
  documents = []
  metadatas = []
  embeddings = []
  ids = []

  for index, data in enumerate(chunks_list):
    documents.append(data["content"])
    embedding = get_embeddings(data['content'])
    embeddings.append(embedding)
    metadatas.append({'source': data["source"]})
    ids.append(str(index + 1))

  db.add(ids, embeddings, metadatas, documents)
  return db


# Set up the DB
chunks_list = []
for word_chunk in chunks:
  chunk = word_chunk
  chunks_list.append(chunk)

db = create_chroma_db(chunks_list, "chatbot")


# def semanticSearch(query):
#   input_em = get_embeddings(query)
#   results = db.query(query_embeddings=[input_em], n_results=3)
#   return results


def generate_questions(question):
  # topn_chunks = semanticSearch(question)
  chat_history = []
  escaped = ""
  # for document in topn_chunks["documents"][0]:
  #   escaped += document.replace("'", "").replace('"', "").replace("\n", " ")
  
  
  prompt = (
    """INSTRUCTION: You will be provided with a question and some context related to it act as a question recommender system for AI chatbot.\
    Your job is to predict 3 preceeding questions related to the query that might be relevent to the customer and try to keep the questions in context with the query you will always wrap the recommended questions inside a HTML button tag with the class='recommended-question'\
    QUESTION: '{query}'
    
  
    ANSWER:
    """).format(query=question,
                relevant_passage=escaped)

  answer = get_response(prompt=prompt)
  if answer.candidates == []:
    answer = "Apologies, couldn't retrieve answer from my knowledgebase, Please try rephrasing the Query"
  else:
    # print(answer)
    answer = answer.candidates[0]['output']

  chat_history += [{"user": question, "Assistant": answer}]
  # answer=nova_llm(prompt)

  return {"Rem": answer}


def generate_answer(question):
  # topn_chunks = semanticSearch(question)
  chat_history = []
  # escaped = ""
  # for document in topn_chunks["documents"][0]:
  #   escaped += document.replace("'", "").replace('"', "").replace("\n", " ")
  Citation=""
  relevant=""
  escaped=compile_results_content(question)
  # print(escaped)
  for result in escaped["results"]:
    print("Restult: ",result)
    try:
      if len(result['content'])>=100:
        if len(relevant)<10000:
          relevant+=result['content']+"\n"
        Citation=Citation+result['links']+"\n"
    except Exception as error:
      print(error)
    
  print(relevant)
  # xyz=PASSAGE: '{relevant_passage}'\
  prompt = f"""###Instruction: Write a research of 1000 words on\
    Use different heading and sub headings using proper research paper conventions\
    Strictly only use this articles for references\
    PASSAGE: '{relevant}'\
    ANSWER:
    """
  #.format(relevant_passage=escaped)

  answer = get_response(prompt=prompt)
  print(prompt)
  if answer.candidates == []:
    answer = "Apologies, couldn't retrieve answer from my knowledgebase, Please try rephrasing the Query"
  else:
    # print(answer)
    answer = answer.candidates[0]['output']
  # answer=nova_llm(prompt)

  # chat_history += [{"user": question, "Assistant": answer}]

  # return {"answer": answer, "chat_history": chat_history}
  return {"answer": f"""{convert_markdown_to_emojis(answer)}
  \n Citation: {Citation} """}


# while True:
#   question = input('User: ')
#   answer, chat_history = generate_answer(question)
#   if question == 'exit':
#     print(chat_history)
#     break
#   else:
#     print("LumaticAI: ", answer)
