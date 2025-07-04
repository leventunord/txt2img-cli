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

    def start(self, max_trial=4):
        initial = parse_feedback(self.client.get_initial())
        self.print(initial["feedback"])
        self.trial += 1

        input("scan?")
        illusion = parse_feedback(self.client.get_illusion(f"./imgs/{scan()}"))
        self.is_satisfied = illusion["is_satisfied"]
        self.print(illusion["feedback"])
        self.trial += 1


        while not self.is_satisfied:
            input("scan?")
            feedback = parse_feedback(self.client.get_feedback(f"./imgs/{scan()}"))
            self.is_satisfied = illusion["is_satisfied"]
            self.print(feedback["feedback"])

            self.trial += 1

            if self.trial > max_trial:
                fail = parse_feedback(self.client.get_fail())
                self.print(fail["feedback"])
                return

def parse_feedback(feedback):
    data = json.loads(feedback)
    return data
