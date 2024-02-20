SELECT s.name, AVG(g.grade) AS average
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects su ON g.subject_id = su.id
WHERE su.name = 'subject_name'
GROUP BY s.id
ORDER BY average DESC
LIMIT 1
