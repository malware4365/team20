select e.name as "Executive's Name", o.name as "Organization's Name", sum(amount) as Total_Funding from task t
inner join executive e on e.exe_id = t.exe_id
inner join organization o on o.org_id = t.org_id 
group by e.exe_id
order by Total_Funding desc limit 5;