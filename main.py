import argparse
import cups
import os
from classes import *

def main():

    # conn = cups.Connection()
    conn = None

    client = Client()
    user = User(conn, client)

    user.start()

if __name__ == "__main__":
    main()