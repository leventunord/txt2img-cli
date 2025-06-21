from weasyprint import HTML

def print_prompt(prompt, conn):
    printer = "Canon_iP100_series"
    filename = get_pdf(prompt)
    title = "tmp"
    options = {
        "PageSize": "Custom.105x148mm",
        "fit-to-page": "true",
        "CNIJGrayScale": "1"
    }

    conn.printFile(printer, filename, title, options)




def get_pdf(prompt):
    pdf_filepath = "./tmp/temp.pdf"

    with open("./asset/template.html", "r") as file:
        template = file.read()

    html = template.replace("placeholder", prompt)
    HTML(string=html).write_pdf(pdf_filepath)

    return pdf_filepath