
SELECT gr.name, AVG(g.grade) AS average
FROM groups gr
JOIN students s ON gr.id = s.group_id
JOIN grades g ON s.id = g.student_id
JOIN subjects su ON g.subject_id = su.id
WHERE su.name = 'subject_name'
GROUP BY gr.id
