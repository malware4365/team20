select distinct a.name "Name of Organizations" from 
(select t.org_id, o.name, extract(year from start_date) as year, count(*) tasks from task t
inner join organization o 
on t.org_id = o.org_id
group by t.org_id, year
having tasks > 1
order by t.org_id) a,

(select org_id, extract(year from start_date) as year, count(*) tasks from task
group by org_id, year
having tasks > 1
order by org_id) b 

where (a.org_id = b.org_id) and (a.year = b.year + 1) and (a.tasks = b.tasks);
