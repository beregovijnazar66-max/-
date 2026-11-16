from collections import deque
class Passenger:
    def __init__(self, name):
        self.name = name
        self.registered = False
        self.boarded = False
    
    def register(self):
            self.registered = True

    def board(self):
        if self.registered:
            self.boarded = True
        else:
            print(f"{self.name} не пройшов реєстрацію")

class Ticket:
    def __init__(self, number, passenger, flight_number, seat):
        self.number = number
        self.passenger = passenger
        self.flight_number = flight_number
        self.seat = seat
    def show_info(self):
        print(
            f"Квиток №{self.number}, "
            f"пасажир: {self.passenger.name}, "
            f"рейс: {self.flight_number}, "
            f"місце: {self.seat}"
        )

class Airplane:
     def __init__(self, flight_number, destination, delay=0):
         self.flight_number = flight_number
         self.destination = destination
         self.delay = delay
         self.status = "очікується"
         self.tickets = []
         self.runway = None

     def add_ticket(self, ticket):
        if ticket.flight_number != self.flight_number:
            print("Квиток належить іншому рейсу")
            return

        self.tickets.append(ticket)

     def count_passengers(self):
        return len(self.tickets)

     def count_registered(self):
        return sum(
            1 for ticket in self.tickets
            if ticket.passenger.registered
        )
     
     def count_boarded(self):
        return sum(
            1 for ticket in self.tickets
            if ticket.passenger.boarded
        )
     
     def register_passengers(self):
         self.status = "реєстрація"

         print(
             f"Рейс {self.flight_number}: "
             f"зареєстровано{self.count_registered()} "
             f"з {self.count_passengers()} пасажирів"
         )
         
     def board_passengers(self):
         self.status = "посадка"
         
         print(
             f"Рейс {self.flight_number}: "
             f"на літак сіли {self.count_boarded()} пасажирів"
         )
         
         missed = self.count_registered() - self.count_boarded()

         print(f"Не сіли на літак: {missed} пасажирів")
             
     def delay_flight(self):
         if self.delay > 0:
            print(
                f"Рейс {self.flight_number} "
                f"затримано на {self.delay} хвилин"
            )
         else:
             print(
                 f"Рейс {self.flight_number} "
                 f"Відправляється без затримки"
             )

     def change_status(self, new_status):
        self.status = new_status

     def show_info(self):
         print(
             f"Рейс {self.flight_number}: "
             f"{self.destination}, "
             f"пасажирів: {self.count_passengers()}, "
             f"зареєстровано: {self.count_registered()}, "
             f"сіли: {self.count_boarded()},"
             f"статус: {self.status}"
       ) 
class Runway:
    def __init__(self, number):
        self.number = number
        self.available = True
        self.total_departures = 0

    def take_off(self, plane):
        if not self.available:
            print(f"Злітна смуга №{self.number} зайнята")
            return False

        self.available = False     

        print(f"\nЗлітна смуга №{self.number} зайнята")
        print(f"Літак {plane.flight_number} готується до зльоту")

        plane.runway = self.number
        plane.change_status("вилетів")   

        print(
            f"Рейс {plane.flight_number} успішно вилетів "
            f"зі злітної смуги №{self.number}!"
        )

        self.total_departures += 1
        self.available = True

        return True
    
class Airport:
    def __init__(self):
        self.planes = deque()
        self.runways = [Runway(1), Runway(2)]
        self.departed_planes = []

        self.total_flights = 0
        self.total_passengers = 0
        self.total_registered = 0
        self.total_boarded = 0

        self.delayed_flights = 0
        self.total_delay = 0

    def add_plane(self, plane):
        self.planes.append(plane)

    def show_planes(self):
        print("\n========== ЛІТАКИ В АЕРОПОРТУ ==========")

        if not self.planes:
            print("Літаків немає")
            return

        for plane in self.planes:
            plane.show_info()

    def process_next_plane(self, runway):
        if not self.planes:
            print("\nВ аеропорту немає літаків")
            return
        
        if not runway.available:
            print("\nЗлітна смуга зайнята")
            return
        
        plane = self.planes.popleft()

        print("\n====================================")
        print(f"ОБСЛУГОВУВАННЯ РЕЙСУ {plane.flight_number}")
        print(f"Напрямок: {plane.destination}")
        print("====================================")

        plane.register_passengers()
        plane.board_passengers()
        plane.delay_flight() 

        plane.change_status("готовий до вильоту")

        if runway.take_off(plane):
            self.departed_planes.append(plane)

            self.total_flights += 1
            self.total_passengers += plane.count_passengers()
            self.total_registered += plane.count_registered()
            self.total_boarded += plane.count_boarded()

            if plane.delay > 0:
                self.delayed_flights += 1
                self.total_delay += plane.delay

        else:
            self.planes.appendleft(plane)

    def process_all_planes(self):
        runway_index = 0

        while self.planes:
            runway = self.runways[runway_index]

            self.process_next_plane(runway)

            runway_index = (
                runway_index + 1
            ) % len(self.runways)

    def show_statistics(self):
        missed = self.total_registered - self.total_boarded
        not_registered = (
            self.total_passengers - self.total_registered
        )

        print("\n========== СТАТИСТИКА АЕРОПОРТУ ==========")

        print(f"Успішно вилетіло рейсів: {self.total_flights}")
        print(f"Всього пасажирів: {self.total_passengers}")
        print(f"Зареєстровано пасажирів: {self.total_registered}")
        print(f"Не зареєструвалися: {not_registered}")
        print(f"Сіли на літак: {self.total_boarded}")
        print(f"Не сіли на літак: {missed}")

        print(f"Затримано рейсів: {self.delayed_flights}")
        print(f"Загальний час затримок: {self.total_delay} хв")

        print("\nСТАТИСТИКА ЗЛІТНИХ СМУГ:")

        for runway in self.runways:
            print(
                f"Злітна смуга №{runway.number}: "
                f"{runway.total_departures} вильоти"
            )

        print("\nСТАТУСИ ВСІХ ЛІТАКІВ:")

        for plane in self.departed_planes:
            print(
                f"Рейс {plane.flight_number}: "
                f"{plane.status}, "
                f"смуга №{plane.runway}"
            )

            print("=========================================")

plane1 = Airplane("PS101", "Львів", 15)
plane2 = Airplane("PS202", "Варшава", 0)
plane3 = Airplane("PS303", "Бухарест", 0)
plane4 = Airplane("PS404", "Париж", 40)

flights = [
    (plane1, 130, 125, 120),
    (plane2, 150, 148, 145),
    (plane3, 100, 96, 93),
    (plane4, 200, 194, 191)
]

for plane, total, registered, boarded in flights:

    for i in range(1, total + 1):
        passenger = Passenger(
            f"Пасажир {plane.flight_number}-{i}"
        )

        ticket = Ticket(
            f"{plane.flight_number}-{i}",
            passenger,
            plane.flight_number,
            i
        )

        if i <= registered:
            passenger.register()

        if i <= boarded:
            passenger.board()

        plane.add_ticket(ticket)

airport = Airport()

airport.add_plane(plane1)
airport.add_plane(plane2)
airport.add_plane(plane3)
airport.add_plane(plane4)

airport.show_planes()

airport.process_all_planes()

print("\n========== ЛІТАКИ, ЯКІ ЗАЛИШИЛИСЯ ==========")

if not airport.planes:
    print("Усі літаки успішно вилетіли!")
else:
    airport.show_planes()

airport.show_statistics()