# Lab3NoSync_Delay.py — добавь задержку для гонки
import threading
import time
import sys

class Counter:
    def __init__(self):
        self.value = 0

def increment(counter, iterations):
    for _ in range(iterations):
        temp = counter.value
        time.sleep(0.000001)  # ← ДОБАВЬ: микрозадержка (1 мкс) — имитирует "медленное" чтение
        temp += 1
        counter.value = temp

def decrement(counter, iterations):
    for _ in range(iterations):
        temp = counter.value
        time.sleep(0.000001)  # ← Аналогично здесь
        temp -= 1
        counter.value = temp

# main() — тот же, что в 1.1
def main():
    if len(sys.argv) != 3:
        print("Использование: python Lab3NoSync_Delay.py <n> <m>")
        sys.exit(1)

    n = int(sys.argv[1])
    m = int(sys.argv[2])
    iterations = 100000

    counter = Counter()
    threads = []

    start_time = time.time()

    for _ in range(n):
        t = threading.Thread(target=increment, args=(counter, iterations))
        threads.append(t)
        t.start()

    for _ in range(m):
        t = threading.Thread(target=decrement, args=(counter, iterations))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()

    print(f"Финальное значение счетчика: {counter.value}")
    print(f"Время выполнения: {end_time - start_time:.4f} сек")

if __name__ == "__main__":
    main()