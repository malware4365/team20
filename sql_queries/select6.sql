select r.first_name, r.last_name, count(*) Number_of_Tasks from researcher r
inner join work_on w on r.res_id = w.res_id
inner join task t on w.task_id = t.task_id
where (TIMESTAMPDIFF(year,r.birth_date,curdate()) < 40) and (t.end_date > curdate())
group by r.res_id
having count(*) = 
(
    select count(*) from researcher r
    inner join work_on w on r.res_id = w.res_id
    inner join task t on w.task_id = t.task_id
    where (TIMESTAMPDIFF(year,r.birth_date,curdate()) < 40) and (t.end_date > curdate())
    group by r.res_id
    order by count(*) desc limit 1
 );