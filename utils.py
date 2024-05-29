import subprocess
import cv2
import arweave
from arweave.transaction_uploader import get_uploader
import os, sys


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


class AR:
    def __init__(self) -> None:
        self._jwk_path = "wallet.json"
        self.wallet = None
        self.tx = None
        self.load_wallet()

    def load_wallet(self):
        if os.path.exists(self._jwk_path):
            try:
                self.wallet = arweave.Wallet(self._jwk_path)
            except Exception as e:
                print(e)
                self.wallet = None

    def upload_file(self, path: str):
        if self.wallet:
            self.file_handler = open(path, "rb", buffering=0)
            tx = arweave.Transaction(
                self.wallet, file_handler=self.file_handler, file_path=path
            )
            tx.add_tag("Content-Type", "image/png")
            tx.add_tag("Type", "image")
            tx.add_tag("App-Name", globals.state["app_name"])
            tx.add_tag("App-Version", globals.get_version())
            tx.sign()
            self.tx = tx
            self.uploader = get_uploader(self.tx, self.file_handler)
            return self.uploader


ar = AR()
