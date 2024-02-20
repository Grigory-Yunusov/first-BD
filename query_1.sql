
SELECT s.name, AVG(g.grade) AS average
FROM students s
JOIN grades g ON s.id = g.student_id
GROUP BY s.id
ORDER BY average DESC
LIMIT 5
