# import os
# import subprocess

# def install_wheels_from_folder(folder_path):
#     for root, dirs, files in os.walk(folder_path):
#         for file in files:
#             if file.endswith(".whl"):
#                 wheel_path = os.path.join(root, file)
#                 subprocess.run(["pip", "install", wheel_path])

# # Example usage:
# folder_path = "chroma_wheel"  # Replace this with the actual path to your folder
# install_wheels_from_folder(folder_path)


# from scraper import scrape

# scrape("https://www.arata.in/pages/our-ingredients")

from model import generate_answer,generate_questions
from flask import Flask, jsonify, request
from flask_cors import CORS ,cross_origin
import uvicorn
from asgiref.wsgi import WsgiToAsgi

# import system_usage
from google_search import compile_results_content

#(compile_results_content("Obama Signs Executive Order Banning National Anthem"))

app = Flask(__name__)
# asgi_app = WsgiToAsgi(app)




@app.route('/')
def index():
  return  {
        "message": "API running successfully",
        "endpoints": [
          "/chat/?q=hey",
          "/sys/"
        ]
    }


@app.route('/chat/')
@cross_origin(supports_credentials=True)
def chat(na=None):
  question_json = request.args
  question=question_json["q"]
  gen_answer = generate_answer(question)
  # gen_questions=generate_questions(question)
  return jsonify(gen_answer)


# @app.route('/sys/')
# @cross_origin(supports_credentials=True)
# def sys_usage(na=None):
#   return jsonify(system_usage.get_system_usage())


app.run(host='0.0.0.0', port=81)
# if __name__ == "__main__":
#   uvicorn.run(asgi_app,host="0.0.0.0",port="5500")