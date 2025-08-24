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

        self.print_time = 10
        self.paper_time = 3

    def print(self, prompt_list):
        print_prompt(PDFArg(prompt_list, self.short_id, self.trial), self.conn)

    def single_round(self, get):
        fed = parse_feedback(get())
        self.is_satisfied = fed["is_satisfied"]
        print(fed["detail"])
        self.print(fed["feedback"])
        self.trial += 1

    def start(self, max_trial=4):
        # Open serial
        ser = Serial("/dev/tty.usbseria1-0001") # for paper sensor only
        serr = Serial("/dev/tty.usbserial-0002") # for interface, light and pen

        # Waiting for pen
        if serr.start_listening():
            print("human detected")

        # Initialize image_path
        image_path = ""

        # Round 1: get initial hints
        # self.single_round(self.client.get_initial)
        initial_fed = parse_feedback(self.client.get_initial())
        target_vision = initial_fed["detail"]
        
        # Open the door
        serr.send_data("1")
        self.print(initial_fed["feedback"])
        self.trial += 1

        # Wait for printer to print and close the door
        time.sleep(self.print_time)
        serr.send_data("9")

        if ser.start_listening():
            time.sleep(self.paper_time)
            image_path = f"./imgs/{scan()}"

        # # Round 2: start illusion
        # self.single_round(lambda: self.client.get_illusion(image_path))

        # if ser.start_listening():
        #     image_path = f"./imgs/{scan()}"

        while (not self.is_satisfied) and (self.trial < max_trial):
            serr.send_data("1")
            self.single_round(lambda: self.client.get_feedback(image_path, target_vision))
            time.sleep(self.print_time)
            serr.send_data("9")
            if ser.start_listening():
                time.sleep(self.paper_time)
                image_path = f"./imgs/{scan()}"

        # Last Round
        serr.send_data("1")
        self.single_round(lambda: self.client.get_last_try(image_path, target_vision))
        time.sleep(self.print_time)
        serr.send_data("9")
        if ser.start_listening():
            time.sleep(self.paper_time)
            image_path = f"./imgs/{scan()}"

        # Fail or Success
        fed = parse_feedback(self.client.get_fail(image_path, target_vision))
        print(fed["detail"])
        self.is_satisfied = fed["is_satisfied"]

        if self.is_satisfied:
            print_success(PDFArg([], self.short_id, self.trial), self.conn)
        else:
            print_fail(PDFArg([], self.short_id, self.trial), self.conn)

        
def parse_feedback(feedback):
    data = json.loads(feedback)
    return data