# Lab3Savages1.py
import threading
import time

N = 5  # вместимость кастрюли
M = 10  # количество дикарей (> N)

class Pot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.portions = capacity
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def get_portion(self, savage_id):
        with self.not_empty:
            while self.portions == 0:
                print(f"Дикаря {savage_id} ждет, пока повар наполнит кастрюлю...")
                self.not_full.notify()  # уведомляем повара
                self.not_empty.wait()
            self.portions -= 1
            print(f"Дикаря {savage_id} взял порцию. Осталось: {self.portions}")
            if self.portions == 0:
                self.not_full.notify()

    def refill(self):
        with self.not_full:
            while self.portions > 0:
                self.not_full.wait()
            print("Повар наполняет кастрюлю...")
            time.sleep(1)  # имитация готовки
            self.portions = self.capacity
            print(f"Кастрюля наполнена! Порций: {self.portions}")
            self.not_empty.notify_all()

def savage(pot, savage_id):
    print(f"Дикаря {savage_id} пришел к кастрюле")
    pot.get_portion(savage_id)
    print(f"Дикаря {savage_id} поел и ушел")

def cook(pot):
    while True:
        pot.refill()

def main():
    pot = Pot(N)
    threads = []

    # Повар
    cook_thread = threading.Thread(target=cook, args=(pot,), daemon=True)
    cook_thread.start()
    threads.append(cook_thread)

    time.sleep(0.1)  # дать повару запуститься

    # Дикари (каждый ест 1 раз)
    for i in range(M):
        t = threading.Thread(target=savage, args=(pot, i))
        threads.append(t)
        t.start()
        time.sleep(0.05)  # имитация прихода

    # Ждем только дикарей
    for t in threads[1:]:
        t.join()

    print("Все дикари поели (по разу). Симуляция завершена.")

if __name__ == "__main__":
    main()