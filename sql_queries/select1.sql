SELECT a.prog_id, a.title , b.first_name, b.last_name FROM 
(
SELECT p.prog_id, t.title, t.task_id, t.end_date FROM task t 
INNER JOIN program p 
ON t.prog_id = p.prog_id 
) a
INNER JOIN 
(
SELECT w.task_id, r.first_name, r.last_name FROM researcher r 
INNER JOIN work_on w 
ON w.res_id = r.res_id 
) b
ON a.task_id = b.task_id    
WHERE ( a.prog_id = %s ) AND (a.end_date > %s );


SELECT a.prog_id, a.title , b.first_name, b.last_name FROM 
(
SELECT p.prog_id, t.title, t.task_id, t.end_date, t.start_date FROM task t 
INNER JOIN program p 
ON t.prog_id = p.prog_id 
) a
INNER JOIN 
(
SELECT w.task_id, r.first_name, r.last_name FROM researcher r 
INNER JOIN work_on w 
ON w.res_id = r.res_id 
) b
ON a.task_id = b.task_id    
WHERE ( a.prog_id = %s ) AND (a.end_date > curdate() ) 
AND (extract(year from a.end_date) - extract(year from a.start_date)) = %s;



SELECT a.prog_id, a.title , b.first_name, b.last_name FROM 
(
SELECT p.prog_id, t.title, t.task_id, t.end_date, t.exe_id FROM task t 
INNER JOIN program p 
ON t.prog_id = p.prog_id 
) a
INNER JOIN 
(
SELECT w.task_id, r.first_name, r.last_name FROM researcher r 
INNER JOIN work_on w 
ON w.res_id = r.res_id 
) b
ON a.task_id = b.task_id    
WHERE ( a.prog_id = %s ) AND (a.end_date > curdate() ) 
AND a.exe_id = %s;