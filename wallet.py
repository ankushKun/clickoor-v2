import subprocess
import sys, os

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from flask import Flask, render_template, request, send_file
import arweave
from utils import run_cmd

wallet_path = "wallet.json"

app = Flask(__name__)

try:
    hn = run_cmd("hostname -I").split(" ")[0]
except Exception as e:
    hn = run_cmd("hostname")


def valid_filename(filename):
    return filename.endswith(".json") and len(filename.split(".")) == 2


@app.route("/", methods=["GET"])
def home():
    # if len(wallet) > 0:
    #     w = wallet[0]
    # else:
    #     w = None
    # print(w)
    return "OK"
    # w = arweave.Wallet(wallet_path) if os.path.exists(wallet_path) else None
    # return render_template(
    #     "index.html",
    #     data={
    #         "address": w.address if w else "NO WALLET",
    #         "balance": w.balance if w else "NO WALLET",
    #     },
    # )


# @app.route('/gallery')
# def gallery():
#     w = wallet[0]
#     my_addr = wallet.address if wallet else 'NO WALLET'
#     client = GraphqlClient(endpoint="https://arweave.net/graphql")

#     query = """
# query {
#     transactions(owners:["8iD-Gy_sKx98oth27JhjjP2V_xUSIGqs_8-skb63YHg"]) {
#         edges {
#             node {
#                 id
#             }
#         }
#     }
# }
#     """
#     data = client.execute(query=query)
#     print(data)

#     return render_template('gallery.html', data="")


@app.route("/upload", methods=["POST"])
def upload():
    jwk_file = request.files["jwk"]
    filename = jwk_file.filename
    if not valid_filename(filename):
        return "Invalid File, should be a valid wallet.json file"
    # Need to add more checks to verify if the wallet json is valid
    jwk_file.save(wallet_path)
    global wallet
    # Init throws an error if wallet is invalid, catch this exception to use the old wallet or replace with new one
    # wallet = arweave.Wallet(wallet_path)
    return "JWK Uploaded"


@app.route("/download", methods=["GET"])
def download():
    # download wallet.json file
    return send_file(wallet_path, as_attachment=True)


# def run_server():
#     global pid
#     os.system("cd cam-py && gunicorn -w 1 wallet:app -b 0.0.0.0:8080")
# app.run(host='0.0.0.0', port=8080)  # was getting no perms on port 80


class WalletLoadWorker(QThread):
    wallet_loaded = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            wallet = arweave.Wallet(wallet_path)
            self.wallet_loaded.emit({"ok": True, "wallet": wallet})
        except Exception as e:
            print(e)
            self.wallet_loaded.emit({"ok": False, "wallet": None})


class ServerWorker(QThread):
    server_started = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            subprocess.Popen("gunicorn -w 1 wallet:app -b 0.0.0.0:8080", shell=True)
            self.server_started.emit(True)
        except Exception as e:
            print(e)
            self.server_started.emit(False)


class WalletScreen(QWidget):

    def __init__(self, name="", icon_path=""):
        super().__init__()
        self.name = name
        self.icon = QIcon(icon_path)
        self.wallet = None

        self.status = QLabel("Wallet Status: Not Loaded", self)
        self.status.setAlignment(Qt.AlignCenter)

        self.address = QLabel(f"Address: NA", self)
        self.address.setAlignment(Qt.AlignCenter)

        self.balance = QLabel(f"Balance: NA", self)
        self.balance.setAlignment(Qt.AlignCenter)

        self.portal_url = QLabel("Portal at ...", self)
        self.portal_url.setAlignment(Qt.AlignCenter)

        l = QLabel("or", self)
        l.setAlignment(Qt.AlignCenter)

        self.portal_url_1 = QLabel("...", self)
        self.portal_url_1.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.status)
        self.layout.addWidget(self.address)
        self.layout.addWidget(self.balance)
        self.layout.addWidget(self.portal_url)
        self.layout.addWidget(l)
        self.layout.addWidget(self.portal_url_1)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

    def start_server(self):
        self.worker = ServerWorker()
        self.worker.server_started.connect(self.server_started)
        self.status.setText("Starting Server...")
        self.worker.start()

    def stop_server(self):
        try:
            os.system("pkill gunicorn")
            self.worker.terminate()
        except Exception as e:
            print(e)

    def server_started(self, status):
        if status:
            self.status.setText("Server Started")
            self.portal_url.setText("Portal at http://" + hn + ":8080")
            self.portal_url_1.setText("http://clickoor.local:8080")
        else:
            self.status.setText("Failed to start server")
            self.portal_url.setText("Portal at [error]")
            self.portal_url_1.setText("[error]")

    def load_wallet(self):
        self.worker1 = WalletLoadWorker()
        self.worker1.wallet_loaded.connect(self.wallet_loaded)
        self.address.setText("Loading Wallet...")
        self.worker1.start()

    def wallet_loaded(self, d):
        if d["ok"]:
            self.wallet = d["wallet"]
            # self.status.setText("Wallet Loaded")
            self.refresh_data()
        else:
            self.address.setText("Failed to load wallet")

    def refresh_data(self):
        if self.wallet:
            self.address.setText(f"Address: {self.wallet.address}")
            self.balance.setText(f"Balance: {self.wallet.balance}")
