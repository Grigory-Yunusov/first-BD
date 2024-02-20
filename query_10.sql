
SELECT DISTINCT su.name
FROM subjects su
JOIN grades g ON su.id = g.subject_id
JOIN students s ON g.student_id = s.id
JOIN teachers t ON su.teacher_id = t.id
WHERE s.name = 'student_name' AND t.name = 'teacher_name'
