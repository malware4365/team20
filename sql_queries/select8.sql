select r.first_name, r.last_name, count(*) num_of_tasks from researcher r
inner join (select w.res_id, w.task_id from work_on w
where w.task_id not in
	(select d.task_id from delivery d
		-- where d.task_id is not null
	) and w.task_id in
	(select task_id from task  
		where end_date >= CURDATE())
)  w2
on  w2.res_id = r.res_id
group by r.res_id
having num_of_tasks >= 5
order by num_of_tasks desc;