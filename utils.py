import subprocess
import cv2
import arweave
from arweave.transaction_uploader import get_uploader
import os, sys
import config


def run_cmd(cmd: str):
    res = subprocess.run(cmd, shell=True, capture_output=True, timeout=0.1)
    try:
        res.check_returncode()
        return res.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode("utf-8").strip()


def make_alpha(path: str):
    # Read the PNG image
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    # Get the alpha channel
    alpha_channel = img[:, :, 3]

    # Save the alpha channel as a grayscale image
    f = path.split(".")
    cv2.imwrite("".join(f[:-1]) + ".mask.png", alpha_channel)


def is_json(filename):
    return filename.endswith(".json") and len(filename.split(".")) == 2



def upload_file(path, wallet):
    if wallet:
        file_handler = open(path, "rb", buffering=0)

        tx = arweave.Transaction(
            wallet, file_handler=file_handler, file_path=path
        )
        tx.add_tag("Content-Type", "image/png")
        tx.add_tag("Type", "image")
        tx.add_tag("App-Name", config.app_name)
        tx.add_tag("App-Version", config.app_version)
        tx.sign()
        uploader = get_uploader(tx,file_handler)

        return tx, uploader, file_handler

