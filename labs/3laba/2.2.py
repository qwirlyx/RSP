# Lab3Savages2.py
import threading
import time
import random

N = 5   # порций в кастрюле
M = 8   # дикарей (все голодны постоянно)

class Pot:
    def __init__(self, capacity, num_savages):
        self.capacity = capacity
        self.portions = capacity
        self.num_savages = num_savages
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)
        self.turn = 0  # для справедливого чередования

    def get_portion(self, savage_id):
        with self.not_empty:
            # Справедливость: дикарь ждет своей очереди
            while self.portions == 0 or (self.turn % self.num_savages) != savage_id:
                if self.portions == 0:
                    print(f"Дикаря {savage_id} ждет еды...")
                    self.not_full.notify()
                self.not_empty.wait()

            self.portions -= 1
            print(f"Дикаря {savage_id} взял порцию. Осталось: {self.portions}")
            self.turn += 1

            if self.portions == 0:
                self.not_full.notify()

    def refill(self):
        with self.not_full:
            while self.portions > 0:
                self.not_full.wait()
            print("Повар наполняет кастрюлю...")
            time.sleep(0.5)
            self.portions = self.capacity
            print(f"Кастрюля полна! Порций: {self.portions}")
            self.not_empty.notify_all()

def savage(pot, savage_id):
    while True:
        pot.get_portion(savage_id)
        eat_time = random.uniform(0.5, 1.5)
        print(f"  Дикаря {savage_id} ест {eat_time:.2f} сек...")
        time.sleep(eat_time)

def cook(pot):
    while True:
        pot.refill()

def main():
    pot = Pot(N, M)
    threads = []

    # Повар
    cook_thread = threading.Thread(target=cook, args=(pot,), daemon=True)
    cook_thread.start()

    time.sleep(0.1)

    # Дикари
    for i in range(M):
        t = threading.Thread(target=savage, args=(pot, i), daemon=True)
        t.start()
        threads.append(t)

    # Работает бесконечно
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nСимуляция остановлена.")

if __name__ == "__main__":
    main()