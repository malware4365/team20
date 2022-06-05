select a.name, a.sc_id, b.title, c.first_name, c.last_name from
(
select s.name, s.sc_id, st.task_id from science s 
inner join science_task st
on s.sc_id = st.sc_id 
where s.sc_id = 1 
) a
inner join (
select t.title, t.task_id from task t 
where t.end_date >= curdate() ) b
on a.task_id = b.task_id 

inner join (

select w.task_id, r.first_name, r.last_name from researcher r 
inner join work_on w 
on w.res_id = r.res_id ) c 
on c.task_id = b.task_id;

---------------------------------------------
-- Ekana kati allages sxetika me to ti tha emfanizei, diladi mono sto prwto select

select b.task_id, b.title, c.first_name, c.last_name from
(
select s.name, s.sc_id, st.task_id from science s 
inner join science_task st
on s.sc_id = st.sc_id 
where s.sc_id = 1 
) a
inner join (
select t.title, t.task_id from task t 
where t.end_date >= curdate() ) b
on a.task_id = b.task_id 

inner join (

select w.task_id, r.first_name, r.last_name from researcher r 
inner join work_on w 
on w.res_id = r.res_id ) c 
on c.task_id = b.task_id;