import base64
import json
import random

from flask import Flask
from functools import lru_cache
from web3.auto import w3
from cache import timed_lru_cache

app = Flask(__name__)

NOUN_ADDRESS = "0x9C8fF314C9Bc7F6e59A9d9225Fb22946427eDC03"
NOUN_ABI = open('abi.json').read()
NOUN_CONTRACT = w3.eth.contract(address=NOUN_ADDRESS, abi=NOUN_ABI)


@timed_lru_cache
def get_max_nouns():
    return NOUN_CONTRACT.caller().totalSupply()

@lru_cache(maxsize=4096)
def get_noun_svg(idx):
    noun_data = NOUN_CONTRACT.caller().dataURI(idx)
    noun_b64 = noun_data.split(',')[-1]
    noun_json = base64.b64decode(noun_b64)
    json_data = json.loads(noun_json)
    image_data = json_data['image']
    svg_b64_data = image_data.split(',')[-1]
    svg_data = base64.b64decode(svg_b64_data)
    return svg_data

@app.route('/')
def hello_world():
    max_nouns = get_max_nouns()
    random_noun = random.randint(0, max_nouns-1)
    svg_data = get_noun_svg(random_noun)
    return svg_data, 200, {'Content-Type': 'image/svg+xml'}
