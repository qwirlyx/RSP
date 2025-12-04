# ===================== CLIENT.PY =====================
import socket
import struct
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox
from datetime import datetime

SERVER_HOST = "127.0.0.1"
TCP_PORT = 1501
MCAST_GRP = "233.0.0.1"
MCAST_PORT = 1502


class ChatClient:
    def __init__(self):
        self.tcp_sock = None
        self.name = None
        self.seen_messages = set()

        self.root = tk.Tk()
        self.root.title("Чат — multicast 233.0.0.1:1502")
        self.root.geometry("800x600")

        self.chat_box = scrolledtext.ScrolledText(
            self.root, state="disabled", font=("Consolas", 11)
        )
        self.chat_box.pack(padx=10, pady=10, fill="both", expand=True)

        bottom = tk.Frame(self.root)
        bottom.pack(fill="x", padx=10, pady=10)

        self.entry = tk.Entry(bottom, font=("Arial", 12))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.send_message)

        send_btn = tk.Button(bottom, text="Отправить", command=self.send_message)
        send_btn.pack(side="right")

        self.connect_to_server()

    def log(self, text):
        if text in self.seen_messages:
            return
        self.seen_messages.add(text)

        self.chat_box.config(state="normal")
        self.chat_box.insert("end", text + "\n")
        self.chat_box.config(state="disabled")
        self.chat_box.see("end")

    def connect_to_server(self):
        try:
            self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_sock.connect((SERVER_HOST, TCP_PORT))

            self.tcp_sock.recv(1024)
            self.root.after(200, self.ask_name)

            threading.Thread(target=self.receive_multicast, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
            self.root.quit()

    def ask_name(self):
        name = simpledialog.askstring("Имя", "Введите ваше имя:")
        if not name:
            name = "Аноним"

        self.name = name.strip()[:20]
        self.tcp_sock.send(self.name.encode("utf-8"))
        self.log(f"Вы вошли как: {self.name}")

    def send_message(self, event=None):
        text = self.entry.get().strip()
        if text:
            try:
                write_time = datetime.now().strftime("%H:%M:%S")
                packet = f"{self.name}|{write_time}|{text}"
                self.tcp_sock.send(packet.encode("utf-8"))
            except:
                self.log("Ошибка отправки TCP")
        self.entry.delete(0, "end")

    def receive_multicast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", MCAST_PORT))

        mreq = struct.pack("4s4s", socket.inet_aton(MCAST_GRP), socket.inet_aton("0.0.0.0"))
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        self.log("Слушаю multicast 233.0.0.1:1502...")

        while True:
            try:
                data, _ = sock.recvfrom(8192)
                for line in data.decode("utf-8").split("\n"):
                    if line.strip():
                        self.root.after(0, self.log, line.strip())
            except:
                break

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    ChatClient().run()
