import requests
import json
import time

from dotenv import load_dotenv
import os

load_dotenv()

import logging
log = logging.getLogger("logger_bot")
log.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
log.addHandler(console_handler)


# generame una peticion para esta urls:
# --request POST 'https://stablediffusionapi.com/api/v3/dreambooth' \
# el cuerto debe tener el siguiente formato:
# {
#  "key": "",
#  "model_id": "your_model_id",
#  "prompt": "actual 8K portrait photo of gareth person, portrait, happy colors, bright eyes, clear eyes, warm smile, smooth soft skin, big dreamy eyes, beautiful intricate colored hair, symmetrical, anime wide eyes, soft lighting, detailed face, by makoto shinkai, stanley artgerm lau, wlop, rossdraws, concept art, digital painting, looking into camera",
#  "negative_prompt": "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",
#  "width": "512",
#  "height": "512",
#  "samples": "1",
#  "num_inference_steps": "30",
#  "safety_checker": "no",
#  "enhance_prompt": "yes",
#  "seed": null,
#  "guidance_scale": 7.5,
#  "webhook": null,
#  "track_id": null
# }
# el response debe de ser la url de una imagen, controlar los errroes de esta y retornar la url
# en caso de error retornar un mensaje de error

URL = 'https://stablediffusionapi.com/api/v3/dreambooth'
KEY = os.getenv("STABLEDIFFUSION_API_KEY")  

async def generate_image(text):
    headers = {'Content-Type': 'application/json'}
    data = {
        "key": KEY,
        "model_id": "anything-v4",
        "prompt": text,
        "negative_prompt": "painting, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, deformed, ugly, blurry, bad anatomy, bad proportions, extra limbs, cloned face, skinny, glitchy, double torso, extra arms, extra hands, mangled fingers, missing lips, ugly face, distorted face, extra legs, anime",
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "30",
        "safety_checker": "no",
        "enhance_prompt": "yes",
        "seed": None,
        "guidance_scale": 7.5,
        "webhook": None,
        "track_id": None
    }
    response = requests.post(URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        log.info("Stable Diffusion API: " + str(response.status_code) + " - " + str(response.reason))
        log.info(response.json())
        response = response.json()
        url_img = response['output'][0]
        status = response['status']
        id_image = response['id']
        time_generate = response['generationTime']
        return url_img
    else:
        return 'error'

