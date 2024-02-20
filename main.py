import sqlite3
from faker import Faker

# Створюємо об'єкт Faker для генерації випадкових даних
fake = Faker()

# Створюємо з'єднання з базою даних
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Створюємо таблиці
cursor.execute('''
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    group_id INTEGER,
    FOREIGN KEY (group_id) REFERENCES groups(id)
)
''')

cursor.execute('''
CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY,
    name TEXT,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id)
)
''')

cursor.execute('''
CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    subject_id INTEGER,
    grade INTEGER,
    date TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
)
''')

# Заповнюємо таблиці випадковими даними
# Генеруємо 3 групи
for i in range(1, 4):
    group_name = fake.word()
    cursor.execute('INSERT INTO groups (name) VALUES (?)', (group_name,))

# Генеруємо 3-5 викладачів
teacher_count = fake.random_int(3, 5)
for i in range(1, teacher_count + 1):
    teacher_name = fake.name()
    cursor.execute('INSERT INTO teachers (name) VALUES (?)', (teacher_name,))

# Генеруємо 5-8 предметів
subject_count = fake.random_int(5, 8)
for i in range(1, subject_count + 1):
    subject_name = fake.word()
    # Вибираємо випадкового викладача для кожного предмета
    teacher_id = fake.random_int(1, teacher_count)
    cursor.execute('INSERT INTO subjects (name, teacher_id) VALUES (?, ?)', (subject_name, teacher_id))

# Генеруємо 30-50 студентів
student_count = fake.random_int(30, 50)
for i in range(1, student_count + 1):
    student_name = fake.name()
    # Вибираємо випадкову групу для кожного студента
    group_id = fake.random_int(1, 3)
    cursor.execute('INSERT INTO students (name, group_id) VALUES (?, ?)', (student_name, group_id))
    # Генеруємо до 20 оцінок для кожного студента з усіх предметів
    grade_count = fake.random_int(1, 20)
    for j in range(grade_count):
        # Вибираємо випадковий предмет і оцінку
        subject_id = fake.random_int(1, subject_count)
        grade = fake.random_int(1, 5)
        # Генеруємо випадкову дату
        date = fake.date()
        cursor.execute('INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)', (i, subject_id, grade, date))

# Зберігаємо зміни в базі даних
conn.commit()

# Записуємо SQL запити у окремі файли

# Знайти 5 студентів із найбільшим середнім балом з усіх предметів
query_1 = '''
SELECT s.name, AVG(g.grade) AS average
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average DESC
LIMIT 5
'''
with open('query_1.sql', 'w') as f:
    f.write(query_1)

# Знайти студента із найвищим середнім балом з певного предмета
# Замінити subject_name на назву предмета
query_2 = '''
SELECT s.name, AVG(g.grade) AS average
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects su ON g.subject_id = su.id
WHERE su.name = 'subject_name'
GROUP BY s.id
ORDER BY average DESC
LIMIT 1
'''
with open('query_2.sql', 'w') as f:
    f.write(query_2)

# Знайти середній бал у групах з певного предмета
# Замінити subject_name на назву предмета
query_3 = '''
SELECT gr.name, AVG(g.grade) AS average
FROM groups gr
JOIN students s ON gr.id = s.group_id
JOIN grades g ON s.id = g.student_id
JOIN subjects su ON g.subject_id = su.id
WHERE su.name = 'subject_name'
GROUP BY gr.id
'''
with open('query_3.sql', 'w') as f:
    f.write(query_3)

# Знайти середній бал на потоці (по всій таблиці оцінок)
query_4 = '''
SELECT AVG(grade) AS average
FROM grades
'''
with open('query_4.sql', 'w') as f:
    f.write(query_4)

# Знайти які курси читає певний викладач
# Замінити teacher_name на ім'я викладача
query_5 = '''
SELECT su.name
FROM subjects su
JOIN teachers t ON su.teacher_id = t.id
WHERE t.name = 'teacher_name'
'''
with open('query_5.sql', 'w') as f:
    f.write(query_5)

# Знайти список студентів у певній групі
# Замінити group_name на назву групи
query_6 = '''
SELECT s.name
FROM students s
JOIN groups gr ON s.group_id = gr.id
WHERE gr.name = 'group_name'
'''
with open('query_6.sql', 'w') as f:
    f.write(query_6)

# Знайти оцінки студентів у окремій групі з певного предмета
# Замінити group_name на назву групи
# Замінити subject_name на назву предмета
query_7 = '''
SELECT s.name, g.grade, g.date
FROM students s
JOIN groups gr ON s.group_id = gr.id
JOIN grades g ON s.id = g.student_id
JOIN subjects su ON g.subject_id = su.id
WHERE gr.name = 'group_name' AND su.name = 'subject_name'
'''
with open('query_7.sql', 'w') as f:
    f.write(query_7)

# Знайти середній бал, який ставить певний викладач зі своїх предметів
# Замінити teacher_name на ім'я викладача
query_8 = '''
SELECT AVG(g.grade) AS average
FROM grades g
JOIN subjects su ON g.subject_id = su.id
JOIN teachers t ON su.teacher_id = t.id
WHERE t.name = 'teacher_name'
'''
with open('query_8.sql', 'w') as f:
    f.write(query_8)

# Знайти список курсів, які відвідує студент
# Замінити student_name на ім'я студента
query_9 = '''
SELECT DISTINCT su.name
FROM subjects su
JOIN grades g ON su.id = g.subject_id
JOIN students s ON g.student_id = s.id
WHERE s.name = 'student_name'
'''
with open('query_9.sql', 'w') as f:
    f.write(query_9)

# Список курсів, які певному студенту читає певний викладач
# Замінити student_name на ім'я студента
# Замінити teacher_name на ім'я викладача
query_10 = '''
SELECT DISTINCT su.name
FROM subjects su
JOIN grades g ON su.id = g.subject_id
JOIN students s ON g.student_id = s.id
JOIN teachers t ON su.teacher_id = t.id
WHERE s.name = 'student_name' AND t.name = 'teacher_name'
'''
with open('query_10.sql', 'w') as f:
    f.write(query_10)


# Середній бал, який певний викладач ставить певному студентові
# Замінити teacher_name на ім'я викладача
# Замінити student_name на ім'я студента
query_11 = '''
SELECT AVG(g.grade) AS average
FROM grades g
JOIN subjects su ON g.subject_id = su.id
JOIN teachers t ON su.teacher_id = t.id
JOIN students s ON g.student_id = s.id
WHERE t.name = 'teacher_name' AND s.name = 'student_name'
'''
with open('query_11.sql', 'w') as f:
    f.write(query_11)

# Оцінки студентів у певній групі з певного предмета на останньому занятті
# Замінити group_name на назву групи
# Замінити subject_name на назву предмета
query_12 = '''
SELECT s.name, g.grade, g.date
FROM students s
JOIN groups gr ON s.group_id = gr.id
JOIN grades g ON s.id = g.student_id
JOIN subjects su ON g.subject_id = su.id
WHERE gr.name = 'group_name' AND su.name = 'subject_name'
AND g.date = (
    SELECT MAX(date)
    FROM grades
    WHERE subject_id = su.id
)
'''
with open('query_12.sql', 'w') as f:
    f.write(query_12)