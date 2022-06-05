select  a.name, b.name , count(*) total
from 
(select st.task_id, s.name from science s 
inner join science_task st 
on s.sc_id = st.sc_id
order by st.task_id) a
inner join 
(select st.task_id, s.name from science s 
inner join science_task st 
on s.sc_id = st.sc_id
order by st.task_id) b
on a.task_id = b.task_id
and a.name > b.name
group by a.name,b.name
order by total desc limit 3;