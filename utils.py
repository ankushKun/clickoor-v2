import subprocess
import arweave
from arweave.transaction_uploader import get_uploader
import os, sys
import config

from settings import SettingsOptions


def run_cmd(cmd: str):
    res = subprocess.run(cmd, shell=True, capture_output=True, timeout=0.1)
    try:
        res.check_returncode()
        return res.stdout.decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode("utf-8").strip()


def is_json(filename):
    return filename.endswith(".json") and len(filename.split(".")) == 2



def upload_file(path, wallet):
    if wallet:
        SettingsOptions.load()
        file_handler = open(path, "rb", buffering=0)

        tx = arweave.Transaction(
            wallet, file_handler=file_handler, file_path=path
        )
        tx.add_tag("Content-Type", "image/png")
        tx.add_tag("Type", "image")
        tx.add_tag("App-Name", config.app_name)
        tx.add_tag("App-Version", config.app_version)
        tx.add_tag("Commercial-Use", SettingsOptions.commercial_use)
        tx.add_tag("Derivation", SettingsOptions.derivation)
        tx.sign()
        uploader = get_uploader(tx,file_handler)

        return tx, uploader, file_handler

