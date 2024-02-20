
SELECT DISTINCT su.name
FROM subjects su
JOIN grades g ON su.id = g.subject_id
JOIN students s ON g.student_id = s.id
WHERE s.name = 'student_name'
