import json
from aviation.airline import Airline
from aviation.plane import PassengerPlane, CargoPlane

def main():
    airline = initialize_airline("config.json")
    while True:
        print("\n")
        print("   АВИАКОМПАНИЯ   ")
        print("\n")
        print("1. Общая пассажировместимость")
        print("2. Общая грузоподъёмность")
        print("3. Сортировка по дальности")
        print("4. Поиск по диапазону")
        print("5. Выход")
        choice = input("\nВыбор: ")

        if choice == "1":
            print(f"Всего пассажиров: {airline.calculate_total_capacity()}")
        elif choice == "2":
            print(f"Всего груза: {airline.calculate_total_cargo_capacity()} кг")
        elif choice == "3":
            print("\nПо дальности полёта:")
            for p in airline.sort_by_flight_range():
                print(f"  • {p.get_model()} → {p.get_flight_range()} км")
        elif choice == "4":
            try:
                min_r = float(input("От (км): "))
                max_r = float(input("До (км): "))
                found = airline.find_planes_in_range(min_r, max_r)
                print("\nРезультат:" if found else "\nНичего не найдено.")
                for p in found:
                    print(f"  • {p.get_model()} — {p.get_flight_range()} км")
            except ValueError:
                print("Введите числа!")
        elif choice == "5":
            print("Пока!")
            break
        else:
            print("Ошибка ввода.")

def initialize_airline(config_file):
    with open(config_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    airline = Airline(data["name"])
    for p in data["planes"]:
        plane = (PassengerPlane if p["type"] == "passenger" else CargoPlane)(
            p["model"], p["passengerCapacity"], p["cargoCapacity"], p["flightRange"]
        )
        airline.add_plane(plane)
    return airline

if __name__ == "__main__":
    main()