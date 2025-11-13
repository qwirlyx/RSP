from aviation.plane import Plane

class Airline:
    def __init__(self, name):
        self._name = name
        self._planes = []

    def add_plane(self, plane):
        if isinstance(plane, Plane):
            self._planes.append(plane)

    def calculate_total_capacity(self):
        return sum(p.get_passenger_capacity() for p in self._planes)

    def calculate_total_cargo_capacity(self):
        return sum(p.get_cargo_capacity() for p in self._planes)

    def sort_by_flight_range(self):
        return sorted(self._planes, key=lambda p: p.get_flight_range())

    def find_planes_in_range(self, min_range, max_range):
        return [p for p in self._planes if min_range <= p.get_flight_range() <= max_range]