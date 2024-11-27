import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QGridLayout, QMessageBox, QSpinBox, QFormLayout, QLineEdit
import sys

# Các lớp đại diện cho các thực thể trong lịch học
class CourseClass:
    def __init__(self, id, name, duration, requires_lab, teacher):
        self.id = id
        self.name = name
        self.duration = duration
        self.requires_lab = requires_lab
        self.teacher = teacher


class Room:
    def __init__(self, id, name, seats, is_lab):
        self.id = id
        self.name = name
        self.seats = seats
        self.is_lab = is_lab

class Schedule:
    def __init__(self):
        self.classes = {}
        self.slots = []
        self.score = 0

    def add_class_to_slot(self, course_class, slot):
        # Kiểm tra lớp học đã được lên lịch chưa
        if course_class in self.classes:
            raise ValueError("Course already scheduled.")

        while len(self.slots) <= slot:
            self.slots.append([])

        # Kiểm tra xung đột lịch học
        if any(other == course_class for other in self.slots[slot]):
            raise ValueError("Slot conflict detected.")

        # Thêm lớp học vào slot
        self.slots[slot].append(course_class)
        self.classes[course_class] = slot

    def calculate_score(self, rooms):
        self.score = 0
        for course, slot in self.classes.items():
            room = rooms[slot % len(rooms)]

            # Kiểm tra các ràng buộc
            if room.seats < course.duration:
                continue  # Không đủ chỗ ngồi
            if course.requires_lab and not room.is_lab:
                continue  # Phòng không phải phòng thí nghiệm
            if any(other != course for other in self.slots[slot]):
                self.score += 1  # Không có xung đột

            self.score += 1  # Tăng điểm cho lớp học hợp lệ

# Hàm khởi tạo quần thể ban đầu
def initialize_population(population_size, courses, total_slots):
    population = []
    for _ in range(population_size):
        schedule = Schedule()
        for course in courses:
            random_slot = random.randint(0, total_slots - 1)
            try:
                schedule.add_class_to_slot(course, random_slot)
            except ValueError:
                continue
        population.append(schedule)
    return population

# Hàm lai tạo hai cá thể
def crossover(parent1, parent2, crossover_points):
    child = Schedule()
    size = len(parent1.classes)
    crossover_mask = [False] * size
    for _ in range(crossover_points):
        point = random.randint(0, size - 1)
        crossover_mask[point] = True

    for course in parent1.classes.keys():
        slot = parent1.classes[course] if crossover_mask[course.id % size] else parent2.classes[course]
        child.add_class_to_slot(course, slot)
    return child

# Hàm đột biến
def mutate(schedule, total_slots, mutation_chance=0.05):
    for course in schedule.classes.keys():
        if random.random() < mutation_chance:
            new_slot = random.randint(0, total_slots - 1)
            schedule.slots[schedule.classes[course]].remove(course)
            try:
                schedule.add_class_to_slot(course, new_slot)
            except ValueError:
                continue

# Hàm chọn cha mẹ cho phép chọn ngẫu nhiên trong quần thể
def select_parent(population):
    tournament_size = 3
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=lambda sched: sched.score)

# Thuật toán di truyền chính
def genetic_algorithm(courses, rooms, total_slots, generations, population_size):
    population = initialize_population(population_size, courses, total_slots)

    for generation in range(generations):
        for schedule in population:
            schedule.calculate_score(rooms)

        best_schedule = max(population, key=lambda sched: sched.score)
        if best_schedule.score == len(courses):
            return best_schedule

        new_population = []
        while len(new_population) < population_size:
            parent1 = select_parent(population)
            parent2 = select_parent(population)
            child = crossover(parent1, parent2, crossover_points=2)
            mutate(child, total_slots)
            child.calculate_score(rooms)
            new_population.append(child)

        population = new_population

    return max(population, key=lambda sched: sched.score)

# Giao diện người dùng với PyQt6
class ScheduleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Schedule Generator")
        self.setGeometry(100, 100, 800, 600)
        self.total_slots = 30
        self.generations = 100
        self.population_size = 50

        self.rooms = [
            Room(1, "Room 1", seats=30, is_lab=False),
            Room(2, "Room 2", seats=25, is_lab=True)
           
        ]

        self.courses = [
    CourseClass(1, "Math 101 - Class A", duration=2, requires_lab=False, teacher="Mr. Smith"),
    CourseClass(2, "Physics 101 - Class A", duration=2, requires_lab=True, teacher="Dr. Johnson"),
    CourseClass(3, "Chemistry 101 - Class A", duration=2, requires_lab=True, teacher="Dr. Lee"),
    CourseClass(4, "History 101 - Class A", duration=1, requires_lab=False, teacher="Ms. Brown"),
    CourseClass(5, "Math 101 - Class B", duration=2, requires_lab=False, teacher="Mr. Smith"),
    CourseClass(6, "Computer Science 101 - Class B", duration=2, requires_lab=True, teacher="Dr. Walker"),
    CourseClass(7, "English 101 - Class B", duration=1, requires_lab=False, teacher="Ms. Green"),
    CourseClass(8, "Biology 101 - Class B", duration=2, requires_lab=True, teacher="Dr. Adams"),
    CourseClass(9, "Math 101 - Class C", duration=2, requires_lab=False, teacher="Mr. Smith"),
    CourseClass(10, "Physics 101 - Class C", duration=2, requires_lab=True, teacher="Dr. Johnson"),
    CourseClass(11, "Chemistry 101 - Class C", duration=2, requires_lab=True, teacher="Dr. Lee"),
    CourseClass(12, "History 101 - Class C", duration=1, requires_lab=False, teacher="Ms. Brown"),
    CourseClass(13, "Math 101 - Class D", duration=2, requires_lab=False, teacher="Mr. Smith"),
    CourseClass(14, "Computer Science 101 - Class D", duration=2, requires_lab=True, teacher="Dr. Walker"),
    CourseClass(15, "English 101 - Class D", duration=1, requires_lab=False, teacher="Ms. Green"),
    CourseClass(16, "Biology 101 - Class D", duration=2, requires_lab=True, teacher="Dr. Adams"),
    CourseClass(17, "Math 101 - Class E", duration=2, requires_lab=False, teacher="Mr. Smith"),
    CourseClass(18, "Physics 101 - Class E", duration=2, requires_lab=True, teacher="Dr. Johnson"),
    CourseClass(19, "Chemistry 101 - Class E", duration=2, requires_lab=True, teacher="Dr. Lee"),
    CourseClass(20, "History 101 - Class E", duration=1, requires_lab=False, teacher="Ms. Brown"),
    CourseClass(21, "Math 101 - Class F", duration=2, requires_lab=False, teacher="Mr. Smith"),
    CourseClass(22, "Computer Science 101 - Class F", duration=2, requires_lab=True, teacher="Dr. Walker"),
    CourseClass(23, "English 101 - Class F", duration=1, requires_lab=False, teacher="Ms. Green"),
    CourseClass(24, "Biology 101 - Class F", duration=2, requires_lab=True, teacher="Dr. Adams"),
    CourseClass(25, "Math 101 - Class G", duration=2, requires_lab=False, teacher="Mr. Smith"),
    CourseClass(26, "Physics 101 - Class G", duration=2, requires_lab=True, teacher="Dr. Johnson"),
    CourseClass(27, "Chemistry 101 - Class G", duration=2, requires_lab=True, teacher="Dr. Lee"),
    CourseClass(28, "History 101 - Class G", duration=1, requires_lab=False, teacher="Ms. Brown"),
    CourseClass(29, "Math 101 - Class H", duration=2, requires_lab=False, teacher="Mr. Smith"),
    CourseClass(30, "Computer Science 101 - Class H", duration=2, requires_lab=True, teacher="Dr. Walker"),
    CourseClass(31, "English 101 - Class H", duration=1, requires_lab=False, teacher="Ms. Green"),
    CourseClass(32, "Biology 101 - Class H", duration=2, requires_lab=True, teacher="Dr. Adams")
]



        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.schedule_grid = QGridLayout()
        self.setup_schedule_grids()

        form_layout = QFormLayout()
        self.gen_spin = QSpinBox()
        self.gen_spin.setValue(self.generations)
        form_layout.addRow("Generations:", self.gen_spin)

        self.pop_spin = QSpinBox()
        self.pop_spin.setValue(self.population_size)
        form_layout.addRow("Population Size:", self.pop_spin)

        run_button = QPushButton("Run Genetic Algorithm")
        run_button.clicked.connect(self.run_ga)

        layout.addLayout(form_layout)
        layout.addLayout(self.schedule_grid)
        layout.addWidget(run_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def setup_schedule_grids(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for col, day in enumerate(days):
            self.schedule_grid.addWidget(QLabel(day), 0, col + 1)

        for row in range(1, 7):
            self.schedule_grid.addWidget(QLabel(f"Period {row}"), row, 0)
            for col in range(1, 6):
                frame = QLabel("")
                frame.setStyleSheet("border: 1px solid black; min-width: 150px; min-height: 50px;")
                self.schedule_grid.addWidget(frame, row, col)

    def display_schedule(self, schedule):
        # Thụt lề đúng cho phần thân hàm
        for i in range(1, 7):
            for j in range(1, 6):
                frame = self.schedule_grid.itemAtPosition(i, j).widget()
                if frame:
                    frame.setText("")  # Xóa nội dung trước khi hiển thị lịch mới

        for course, slot in schedule.classes.items():
            room_name = "Room 1" if not course.requires_lab else "Room 2"
            day = (slot % 5) + 1  # Xác định ngày trong tuần
            period = (slot // 5) + 1  # Xác định tiết học
            frame = self.schedule_grid.itemAtPosition(period, day).widget()
            if frame:
                frame.setText(f"{course.name}\n{course.teacher}\n({course.duration} periods)")  # Hiển thị lịch học   


    def run_ga(self):
        self.generations = self.gen_spin.value()
        self.population_size = self.pop_spin.value()

        best_schedule = genetic_algorithm(self.courses, self.rooms, self.total_slots, self.generations, self.population_size)
        self.display_schedule(best_schedule)
        QMessageBox.information(self, "Result", f"Best Schedule Score: {best_schedule.score}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ScheduleApp()
    window.show()
    sys.exit(app.exec())
