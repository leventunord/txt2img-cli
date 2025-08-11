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
        time.sleep(10) # wait for printer to print
        self.trial += 1

    def start(self, max_trial=4):
        # Open Serial
        sensor_ser = Serial('sensor')
        platform_ser = Serial('platform')
        img_path = None

        # Round 1: get initial hints
        platform_ser.send_data('0')
        self.single_round(self.client.get_initial)

        platform_ser.send_data('9')
        
        if sensor_ser.start_listening():

            img_path = f"./imgs/{scan()}"
            platform_ser.send_data('0')

        # Round 2: start illusion
        self.single_round(lambda : self.client.get_illusion(img_path))
        platform_ser.send_data('9')
        
        if sensor_ser.start_listening():
            img_path = f"./imgs/{scan()}"
            platform_ser.send_data('0')


        while (not self.is_satisfied) and (self.trial < max_trial):
            self.single_round(lambda : self.client.get_feedback(img_path))
            platform_ser.send_data('9')

            if sensor_ser.start_listening():
                img_path = f"./imgs/{scan()}"
                platform_ser.send_data('0')

        # Last Round
        self.single_round(lambda : self.client.get_last_try(img_path))
        platform_ser.send_data('9')
        
        if sensor_ser.start_listening():
            img_path = f"./imgs/{scan()}"
            platform_ser.send_data('0')

        # Fail or Success
        # self.single_round(lambda : self.client.get_fail(img_path))
        fed = parse_feedback(self.client.get_fail(img_path))
        print(fed["detail"])
        self.is_satisfied = fed["is_satisfied"]

        if self.is_satisfied:
            print_success(PDFArg([], self.short_id, self.trial), self.conn)
        else:
            print_fail(PDFArg([], self.short_id, self.trial), self.conn)

        
def parse_feedback(feedback):
    data = json.loads(feedback)
    return data