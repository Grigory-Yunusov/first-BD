
SELECT s.name, g.grade, g.date
FROM students s
JOIN groups gr ON s.group_id = gr.id
JOIN grades g ON s.id = g.student_id
JOIN subjects su ON g.subject_id = su.id
WHERE gr.name = 'group_name' AND su.name = 'subject_name'
