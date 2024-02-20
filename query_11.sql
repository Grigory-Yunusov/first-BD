
SELECT AVG(g.grade) AS average
FROM grades g
JOIN subjects su ON g.subject_id = su.id
JOIN teachers t ON su.teacher_id = t.id
JOIN students s ON g.student_id = s.id
WHERE t.name = 'teacher_name' AND s.name = 'student_name'
