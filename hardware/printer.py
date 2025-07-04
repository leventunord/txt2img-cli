from weasyprint import HTML
from datetime import datetime
import random
from dataclasses import dataclass
from typing import List

@dataclass
class PDFArg:
    prompt: List
    human_id: str
    trial: int

def print_prompt(pdf_arg: PDFArg, conn):
    printer = "Canon_iP100_series"
    filename = get_pdf(pdf_arg)
    title = "tmp"
    options = {
        "PageSize": "Custom.105x140mm",
        "fit-to-page": "true",
        "CNIJGrayScale": "1"
    }

    conn.printFile(printer, filename, title, options)

def print_success(pdf_arg: PDFArg, conn):
    printer = "Canon_iP100_series"
    filename = "./asset/success.pdf"
    title = "tmp"
    options = {
        "PageSize": "Custom.105x140mm",
        "fit-to-page": "true",
        "CNIJGrayScale": "1"
    }

    conn.printFile(printer, filename, title, options)

def print_fail(pdf_arg: PDFArg, conn):
    printer = "Canon_iP100_series"
    filename = "./asset/fail.pdf"
    title = "tmp"
    options = {
        "PageSize": "Custom.105x140mm",
        "fit-to-page": "true",
        "CNIJGrayScale": "1"
    }

    conn.printFile(printer, filename, title, options)

def get_pdf(arg: PDFArg):
    current_trial = 1

    date = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    location = "Shanghai China"
    model = f"Model: Human #{arg.human_id}"
    trial = f"Trail: 0{arg.trial}"

    pdf_filepath = "./tmp/temp.pdf"

    with open("./asset/template.html", "r") as file:
        template = file.read()

    html = template.replace("date_and_location", f"{date} {location}") \
                   .replace("model", model) \
                   .replace("trial", trial) \
                   .replace("prompt_line_1", arg.prompt[0]) \
                   .replace("prompt_line_2", arg.prompt[1]) \
                   .replace("prompt_line_3", arg.prompt[2])
    
    HTML(string=html, base_url="./").write_pdf(pdf_filepath)

    return pdf_filepath