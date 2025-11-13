# Lab3ReentrantLock.py
import threading
import time
import sys

class Counter:
    def __init__(self):
        self.value = 0
        self.lock = threading.RLock()  # ReentrantLock аналог

def increment(counter, iterations):
    for _ in range(iterations):
        with counter.lock:
            counter.value += 1

def decrement(counter, iterations):
    for _ in range(iterations):
        with counter.lock:
            counter.value -= 1

def main():
    if len(sys.argv) != 3:
        print("Использование: python Lab3ReentrantLock.py <n> <m>")
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