
SELECT s.name
FROM students s
JOIN groups gr ON s.group_id = gr.id
WHERE gr.name = 'group_name'
