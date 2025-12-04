# ===================== SERVER B — индивидуальная задержка 10 секунд =====================
import socket
import threading
import time
from datetime import datetime

TCP_HOST = "0.0.0.0"
TCP_PORT = 1501
MULTICAST_GROUP = "233.0.0.1"
MULTICAST_PORT = 1502

# Очередь сообщений: (timestamp, name, text)
queue = []
lock = threading.Lock()


def message_scheduler():
    """Отправляет КАЖДОЕ сообщение ровно через 10 секунд после получения"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

    while True:
        now = time.time()
        to_send = []

        with lock:
            # собираем все старше 10 секунд
            for item in queue:
                ts, name, text = item
                if now - ts >= 10:
                    to_send.append(item)

            # удаляем их из очереди
            queue[:] = [x for x in queue if x not in to_send]

        # Отправляем каждое сообщение отдельно
        for ts, name, text in to_send:
            time_written = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            time_sent = datetime.now().strftime("%H:%M:%S")

            packet = f"[написано: {time_written} | отправлено: {time_sent}] {name}: {text}"
            sock.sendto(packet.encode("utf-8"), (MULTICAST_GROUP, MULTICAST_PORT))

            print("Отправлено:", packet)

        time.sleep(0.1)  # высокая точность проверок


def handle_client(conn, addr):
    try:
        conn.send(b"Enter your name: ")
        raw_name = conn.recv(1024).decode("utf-8", errors="ignore").strip()
        name = raw_name[:20] if raw_name else "Гость"
        conn.send(b"OK\n")

        print(f"{addr} вошел как {name}")

        while True:
            data = conn.recv(1024)
            if not data:
                break

            decoded = data.decode("utf-8", errors="ignore").strip()
            if not decoded:
                continue

            # Формат: "Имя|время_написания|текст"
            try:
                parts = decoded.split("|", 2)
                name_msg = parts[0]
                write_time = parts[1]  # строка, но сервер сохранит свой timestamp
                text_msg = parts[2]
            except:
                continue

            timestamp = time.time()

            with lock:
                queue.append((timestamp, name_msg, text_msg))

            print(f"Принято от {name_msg} @ {write_time}: {text_msg}")

    except Exception as e:
        print("Ошибка:", e)

    finally:
        conn.close()


def main():
    # Запускаем планировщик
    threading.Thread(target=message_scheduler, daemon=True).start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((TCP_HOST, TCP_PORT))
    server.listen(10)

    print("Server B запущен")
    print("Каждое сообщение → отправляется через 10 секунд!\n")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
