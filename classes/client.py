from openai import OpenAI
from pydantic import BaseModel
import base64

class Feedback(BaseModel):
    is_satisfied: bool
    feedback: list[str]

class Client:
    def __init__(self):
        self.client = OpenAI()
        self.prompts = read_prompt_files()
        # self.initial_response = None
        # self.trial_responses = []
        self.last_response_id = None
        self.current_response = None
        

    def get_initial(self):
        self.current_response = self.client.responses.parse(
            model="gpt-4o",
            instructions=self.prompts["system"],
            input=self.prompts["initial"],
            text_format=Feedback
        )

        self.last_response_id = self.current_response.id
        return self.current_response.output_text

    def get_illusion(self, image_path):
        self.current_response = self.client.responses.parse(
            model="gpt-4o",
            input=[input_user_text_image(self.prompts["illusion"], image_path)],
            previous_response_id=self.last_response_id,
            text_format=Feedback
        )

        self.last_response_id = self.current_response.id
        return self.current_response.output_text

    def get_feedback(self, image_path):
        self.current_response = self.client.responses.parse(
            model="gpt-4o",
            input=[input_user_text_image(self.prompts["trial"], image_path)],
            previous_response_id=self.last_response_id,
            text_format=Feedback
        )

        self.last_response_id = self.current_response.id
        return self.current_response.output_text

    def get_fail(self):
        self.current_response = self.client.responses.parse(
            model="gpt-4o",
            input=self.prompts["fail"],
            previous_response_id=self.last_response_id,
            text_format=Feedback
        )

        self.last_response_id = self.current_response.id
        return self.current_response.output_text





class Conversation:
    def __init__(self):
        pass

def read_prompt_files(root_path="./asset/prompts/"):
    with open(f"{root_path}system.txt", "r", encoding="utf-8") as system_prompt_file:
        system_prompt = system_prompt_file.read()

    with open(f"{root_path}illusion.txt", "r", encoding="utf-8") as illusion_prompt_file:
        illusion_prompt = illusion_prompt_file.read()

    with open(f"{root_path}initial.txt", "r", encoding="utf-8") as initial_prompt_file:
        initial_prompt = initial_prompt_file.read()

    with open(f"{root_path}trial.txt", "r", encoding="utf-8") as trial_prompt_file:
        trial_prompt = trial_prompt_file.read()

    with open(f"{root_path}fail.txt", "r", encoding="utf-8") as fail_prompt_file:
        fail_prompt = fail_prompt_file.read()

    return {
        "system": system_prompt,
        "initial": initial_prompt,
        "illusion": illusion_prompt,
        "trial": trial_prompt,
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