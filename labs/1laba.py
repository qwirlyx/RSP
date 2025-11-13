class Car:
    def __init__(self, car_id=0, brand="", model="", year=2000, color="", price=0.0, reg_number=""):
        self.__id = car_id
        self.__brand = brand
        self.__model = model
        self.__year = year
        self.__color = color
        self.__price = price
        self.__reg_number = reg_number

        self.__fields = ["id", "brand", "model", "year", "color", "price", "reg_number"]

    def set(self, key, value):
        for field in self.__fields:
            if key == field:
                setattr(self, f"_{self.__class__.__name__}__{field}", value)
                return
        raise KeyError(f"Поля '{key}' нет в классе Car")

    def get(self, key):
        for field in self.__fields:
            if key == field:
                return getattr(self, f"_{self.__class__.__name__}__{field}")
        raise KeyError(f"Поля '{key}' нет в классе Car")

    def __str__(self):
        return ", ".join([f"{field}: {self.get(field)}" for field in self.__fields])

    def __hash__(self):
        return hash((self.__id, self.__reg_number))

    def __eq__(self, other):
        if not isinstance(other, Car):
            return False
        return self.__id == other.__id and self.__reg_number == other.__reg_number


class CarManager:
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    # (a) список по марке
    def get_cars_by_brand(self, brand):
        return [car for car in self.cars if car.get("brand") == brand]

    # (b) список по модели и возрасту
    def get_cars_by_model_and_age(self, model, min_age, current_year=2025):
        return [car for car in self.cars if car.get("model") == model and current_year - car.get("year") >= min_age]

    # (c) список по году и цене
    def get_cars_by_year_and_price(self, year, min_price):
        return [car for car in self.cars if car.get("year") == year and car.get("price") > min_price]


if __name__ == "__main__":
    manager = CarManager()

    car1 = Car(1, "Toyota", "Camry", 2018, "Серый", 20000, "AA1234")
    car2 = Car(2, "BMW", "X5", 2015, "Черный", 35000, "BB5678")

    car1.set("price", 21000)
    car2.set("color", "Белый")

    car1.__setattr__("owner", "Иван Иванов")

    manager.add_car(car1)
    manager.add_car(car2)

    print("(a) Toyota:")
    for c in manager.get_cars_by_brand("Toyota"):
        print(c)

    print("\n(b) X5 старше 5 лет:")
    for c in manager.get_cars_by_model_and_age("X5", 5):
        print(c)

    print("\n(c) Авто 2015 года дороже 30000:")
    for c in manager.get_cars_by_year_and_price(2015, 30000):
        print(c)
