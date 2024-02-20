
SELECT su.name
FROM subjects su
JOIN teachers t ON su.teacher_id = t.id
WHERE t.name = 'teacher_name'
