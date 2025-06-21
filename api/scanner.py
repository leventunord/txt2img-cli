import subprocess
from datetime import datetime

def scan():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    png_filename = f"scan_{timestamp}.png"

    cmd = [
        "scanimage",
        "--device-name=fujitsu:fi-6125dj:140948",
        # "--source='ADF Front'",
        "--mode=Gray",
        "--resolution=300",
        "--page-width=105",
        "--page-height=148",
        "--format=png",
        "-o", f"./imgs/{png_filename}"
        # "-o", png_filename
    ]

    scan = subprocess.run(cmd, capture_output=True, text=True)
    # print(scan.stderr)

    if scan.returncode != 0:
        print("Scan Failed.")
        exit(1)

    return None