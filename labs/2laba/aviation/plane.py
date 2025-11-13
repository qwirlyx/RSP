class Plane:
    def __init__(self, model, passenger_capacity, cargo_capacity, flight_range):
        self._model = model
        self._passenger_capacity = passenger_capacity
        self._cargo_capacity = cargo_capacity
        self._flight_range = flight_range

    def get_model(self):
        return self._model

    def get_passenger_capacity(self):
        return self._passenger_capacity

    def get_cargo_capacity(self):
        return self._cargo_capacity

    def get_flight_range(self):
        return self._flight_range

    def describe(self):
        return (f"Модель: {self._model}, "
                f"Пассажиры: {self._passenger_capacity}, "
                f"Груз: {self._cargo_capacity} кг, "
                f"Дальность: {self._flight_range} км")


class PassengerPlane(Plane):
    def __init__(self, model, passenger_capacity, cargo_capacity, flight_range):
        super().__init__(model, passenger_capacity, cargo_capacity, flight_range)

    def describe(self):
        return "Пассажирский — " + super().describe()


class CargoPlane(Plane):
    def __init__(self, model, passenger_capacity, cargo_capacity, flight_range):
        super().__init__(model, passenger_capacity, cargo_capacity, flight_range)

    def describe(self):
        return "Грузовой — " + super().describe()