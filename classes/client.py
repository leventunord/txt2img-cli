from openai import OpenAI
from pydantic import BaseModel
import base64

class Feedback(BaseModel):
    detail: str
    is_satisfied: bool
    feedback: list[str]


class Client:
    def __init__(self):
        self.client = OpenAI()
        self.prompts = read_prompt_files()
        self.history = [{
            "role": "system", # TODO: maybe developer
            "content": self.prompts["system"] 
        }]

    def reset_history(self):
        self.history = [{
            "role": "system",
            "content": self.prompts["system"] 
        }]
        
    def get_response(self, input, temperature=1.0):
        self.history.append(input)

        response = self.client.responses.parse(
            model="gpt-4o",
            input=self.history,
            text_format=Feedback,
            store=False,
            # temperature=temperature
        )

        self.history += [{"role": el.role, "content": el.content} for el in response.output]
        return response.output_text
        

    def get_initial(self):
        return self.get_response(input_user_text(self.prompts["initial"]), temperature=1.5)

    def get_illusion(self, image_path):
        return self.get_response(input_user_text_image(self.prompts["illusion"], image_path))

    def get_feedback(self, image_path):
        return self.get_response(input_user_text_image(self.prompts["trial"], image_path))

    def get_last_try(self, image_path):
        return self.get_response(input_user_text_image(self.prompts["last try"], image_path))

    def get_fail(self, image_path):
        return self.get_response(input_user_text_image(self.prompts["fail"], image_path))


def read_prompt_files(root_path="./asset/prompts/"):
    with open(f"{root_path}system.txt", "r", encoding="utf-8") as system_prompt_file:
        system_prompt = system_prompt_file.read()

    with open(f"{root_path}illusion.txt", "r", encoding="utf-8") as illusion_prompt_file:
        illusion_prompt = illusion_prompt_file.read()

    with open(f"{root_path}initial.txt", "r", encoding="utf-8") as initial_prompt_file:
        initial_prompt = initial_prompt_file.read()

    with open(f"{root_path}trial.txt", "r", encoding="utf-8") as trial_prompt_file:
        trial_prompt = trial_prompt_file.read()

    with open(f"{root_path}last_try.txt", "r", encoding="utf-8") as last_try_prompt_file:
        last_try_prompt = last_try_prompt_file.read()

    with open(f"{root_path}fail.txt", "r", encoding="utf-8") as fail_prompt_file:
        fail_prompt = fail_prompt_file.read()

    return {
        "system": system_prompt,
        "initial": initial_prompt,
        "illusion": illusion_prompt,
        "trial": trial_prompt,
        "last try": last_try_prompt,
        "fail": fail_prompt,
    }

def input_user_text(text):
    return {
        "role": "user",
        "content": text 
    }

def input_user_text_image(text, image_path):
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    return {
        "role": "user",
        "content": [
            {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{encode_image(image_path)}",
                "detail": "low"
            },
            {
                "type": "input_text",
                "text": text
            }
        ]
    }