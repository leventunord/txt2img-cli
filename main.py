import argparse
import cups
from api import *

def main():
    # parser = argparse.ArgumentParser()
    # args = parser.parse_args()

    # connect the printer
    conn = cups.Connection()
    
    is_satisfied = False
    is_scan_ready = False

    while not is_satisfied:
        prompt = input("Write your prompt: ") 
        print_prompt(prompt, conn)
        # print(prompt)

        while not is_scan_ready:
            is_scan_ready = bool(input("Ready to scan? "))

        # is_satisfied, next_prompt = scan()
        scan()
        is_scan_ready = False
        is_satisfied = bool(input("Satisfied? "))

    print("Satisfied!")

if __name__ == "__main__":
    main()