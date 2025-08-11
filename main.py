import argparse
import cups
import os
from classes import *

def main():

    # Open Camera & Check Connection
    cam = Camera()
    conn = cups.Connection()
    client = Client()

    # While loop:
    # If detected human, start & close camera
    while True:
        if cam.start_detection():
            user = User(conn, client)
            user.start()
            client.reset_history()

if __name__ == "__main__":
    main()