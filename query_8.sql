
SELECT AVG(g.grade) AS average
FROM grades g
JOIN subjects su ON g.subject_id = su.id
JOIN teachers t ON su.teacher_id = t.id
WHERE t.name = 'teacher_name'
