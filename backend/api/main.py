from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import session
from model import Word
from dotenv import load_dotenv
import base64
import requests
import os
import time
import json

DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_STEPS = 10
DEFAULT_SEED = 0
DEFAULT_CFG_SCALE = 7
DEFAULT_SAMPLES = 1
DEFAULT_STYLE_PRESET = "enhance"

app = FastAPI()
load_dotenv()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

def get_api_info():
    url = os.environ.get("STABILITY_AI_API_URL")
    api_key = os.environ.get("STABILITY_AI_API_KEY_4")
    if not url or not api_key:
        raise EnvironmentError("API URL or API key not found in environment variables.")
    return url, api_key

def get_words():
    words_count = 0
    words = session.query(Word).all()
    for word in words:
        words_count += 1
    return words_count

@app.get("/get_words/")
def get_words():
    words = session.query(Word).all()
    return words

@app.post("/register_word/")
def register_word(word: str):
    db_word = Word(word=word)
    session.add(db_word)
    session.commit()
    session.close()
    return "register word"

@app.post("/generate_image/")
async def ai_generate_image():
    try:
        need_words = 10
        word_count = session.query(Word).count()
        ten_words = ""
        if word_count >= need_words:
            words = session.query(Word).all()
            for i in range(10):
                ten_words += words[i].word + " "
            
            url, api_key = get_api_info()
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": api_key,
            }
            
            body = {
                "width": DEFAULT_WIDTH,
                "height": DEFAULT_HEIGHT,
                "steps": DEFAULT_STEPS,
                "seed": DEFAULT_SEED,
                "cfg_scale": DEFAULT_CFG_SCALE,
                "samples": DEFAULT_SAMPLES,
                "style_preset": DEFAULT_STYLE_PRESET,
                "text_prompts": [{"text": ten_words, "weight": 1}],
            }
            
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()  # ステータスコードが200以外の場合に例外を発生させる
            
            time.sleep(5)
            ai_image_data = response.json()
            file_path = None
            for i, image in enumerate(ai_image_data["artifacts"]):
                with open(f"./images/txt2img_{image['seed']}.png", "wb") as f:
                    f.write(base64.b64decode(image["base64"]))
                    if file_path is None:
                        file_path = f"./images/txt2img_{image['seed']}.png"
            session.close()
            response = {"words": ten_words, "file_path": file_path}
            response = json.dumps(response)
            return response
        else:
            session.close()
            response = {"words": "error", "file_path": "error", "word_count": word_count}
            response = json.dumps(response)
            return response
    except Exception as e:
        session.close()
        error_response = {"error": str(e)}
        error_response = json.dumps(error_response)
        return error_response     
        
@app.delete("/delete_all_words/")
def delete_all_words():
    words_to_delete = session.query(Word).order_by(Word.id.asc()).limit(10).all()
    for word in words_to_delete:
        session.delete(word)
    session.commit()
    session.close()
    return "delete all words"
