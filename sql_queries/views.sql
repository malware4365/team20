select r.res_id as "Researcher's ID", r.first_name as "First Name", r.last_name as "Last Name", t.task_id as "Task's ID", t.title as "Task's Titla" from researcher r 
inner join work_on w 
on w.res_id = r.res_id
inner join task t 
on t.task_id = w.task_id
order by r.res_id;



select p.prog_id as "Program's ID", p.name as "Program's Name",t.task_id as "Task's ID", t.title as "Task's Title" from program p
inner join task t
on t.prog_id = p.prog_id
order by p.prog_id;