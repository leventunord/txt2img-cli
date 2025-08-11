import uuid
import json
from hardware import *

class User:
    def __init__(self, conn, client):
        self.conn = conn
        self.client = client

        self.id = uuid.uuid4()
        self.short_id = str(self.id.int)[:5]

        self.is_satisfied = False
        self.trial = 1

        self.current_drawing = None

    def print(self, prompt_list):
        print_prompt(PDFArg(prompt_list, self.short_id, self.trial), self.conn)

    def single_round(self, get):
        fed = parse_feedback(get())
        print(fed["detail"])
        self.print(fed["feedback"])
        self.trial += 1

    def start(self, max_trial=4):
        # Open serial
        ser = Serial("/dev/tty.usbseria1-0001")

        # Round 1: get initial hints
        self.single_round(self.client.get_initial)
        
        if ser.start_listening():
            image_path = f"./imgs/{scan()}"

        # Round 2: start illusion
        self.single_round(lambda : self.client.get_illusion(image_path))

        if ser.start_listening():
            image_path = f"./imgs/{scan()}"

        while (not self.is_satisfied) and (self.trial < max_trial):
            self.single_round(lambda : self.client.get_feedback(image_path))
            if ser.start_listening():
                image_path = f"./imgs/{scan()}"

        # Last Round
        self.single_round(lambda : self.client.get_last_try(image_path))
        if ser.start_listening():
            image_path = f"./imgs/{scan()}"

        # Fail or Success
        fed = parse_feedback(self.client.get_fail(image_path))
        print(fed["detail"])
        self.is_satisfied = fed["is_satisfied"]

        if self.is_satisfied:
            print_success(PDFArg([], self.short_id, self.trial), self.conn)
        else:
            print_fail(PDFArg([], self.short_id, self.trial), self.conn)

        
def parse_feedback(feedback):
    data = json.loads(feedback)
    return data