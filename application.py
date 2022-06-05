from flask import Flask, request, render_template, session
from database import db, cursor, fetch_tables, dbname
from config import Config


app = Flask(__name__)
app.config['SECRET_KEY'] = '5ed94ace7c981dde71c70bb2352b5ace'

cursor.execute(f'USE {dbname};')

tables = fetch_tables()

def parse_headings(headings):
    """Capital First Letter"""
    return [" ".join(x.split('_')).title() for x in headings]


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/science_field', methods=['GET', 'POST'])
def science():
    sql = "SELECT sc_id, name FROM science;"
    cursor.execute(sql)
    sciences = cursor.fetchall()
    sciences = [f"{x[0]} | {x[1].capitalize()} " for x in sciences]
    # print(sciences)

    selection = request.form.get("form_sc_id")
    if selection is None: # on first load of page is None
        result = []
        headings = []
        name_science = []
    else:
        sc_id = selection.split()[0]
        name_science = selection.split()[1:]
        
        sql = """ SELECT b.task_id, b.title, c.first_name, c.last_name FROM
                    (
                    SELECT s.name, s.sc_id, st.task_id FROM science s 
                    INNER JOIN science_task st
                    ON s.sc_id = st.sc_id 
                    WHERE s.sc_id = %s 
                    ) a
                    INNER JOIN (
                    SELECT t.title, t.task_id FROM task t 
                    WHERE t.end_date >= curdate() ) b
                    ON a.task_id = b.task_id 

                    INNER JOIN (

                    SELECT w.task_id, r.first_name, r.last_name FROM researcher r 
                    INNER JOIN work_on w 
                    ON w.res_id = r.res_id ) c 
                    ON c.task_id = b.task_id
                    order by b.task_id;"""
       
        cursor.execute(sql, (sc_id,))
        headings = parse_headings(cursor.column_names)
        result = cursor.fetchall()
    print(result)

    return render_template('science.html', sciences=sciences, headings=headings, data=result, science_name=name_science)

@app.route('/organization', methods=['GET', 'POST'])
def organizations():
    button = request.form.get("form_button")
    print(button)
    if button is None:
        result = []
        headings = []
    else:
        sql =   """ select distinct a.name as "Organizations' Name" from 
                (select t.org_id, o.name, extract(year from start_date) as year, count(*) tasks from task t
                inner join organization o 
                on t.org_id = o.org_id
                group by t.org_id, year
                having tasks > 1
                order by t.org_id) a,
                (select org_id, extract(year from start_date) as year, count(*) tasks from task
                group by org_id, year
                having tasks >= 10
                order by org_id) b 
                where (a.org_id = b.org_id) and (a.year = b.year + 1) and (a.tasks = b.tasks); """
        cursor.execute(sql)
        headings = parse_headings(cursor.column_names)
        result = cursor.fetchall()
        print(result)    
    return render_template('organizations.html',headings=headings, data=result,button=button.title() if button is not None else "")

@app.route('/top3', methods=['GET', 'POST'])
def top3():
    button = request.form.get("form_button")
    print(button)
    if button is None:
        result = []
        headings = []
    else:
        sql =   """ select  a.name as "Science 1", b.name as "Science 2", count(*) Appeared_times
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
                    order by Appeared_times desc limit 3; """
        cursor.execute(sql)
        headings = parse_headings(cursor.column_names)
        result = cursor.fetchall()
        print(result)   
    return render_template('top3.html',headings=headings, data=result,button=button.title() if button is not None else "")

@app.route('/young_researchers', methods=['GET', 'POST'])
def young_researchers():
    button = request.form.get("form_button")
    print(button)
    if button is None:
        result = []
        headings = []
    else:
        sql =   """ select r.first_name, r.last_name, count(*) Number_of_Tasks from researcher r
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
                    );"""
        cursor.execute(sql)
        headings = parse_headings(cursor.column_names)
        result = cursor.fetchall()
        print(result)   
    return render_template('young_researchers.html',headings=headings, data=result,button=button.title() if button is not None else "")

@app.route('/executives', methods=['GET', 'POST'])
def executives():
    button = request.form.get("form_button")
    print(button)
    if button is None:
        result = []
        headings = []
    else:
        sql =   """ select e.name as "Executive's Name", o.name as "Organization's Name", sum(amount) as Total_Funding from task t
                    inner join executive e on e.exe_id = t.exe_id
                    inner join organization o on o.org_id = t.org_id 
                    group by e.exe_id
                    order by Total_Funding desc limit 5;"""
        cursor.execute(sql)
        headings = parse_headings(cursor.column_names)
        result = cursor.fetchall()
        print(result)   
    return render_template('executives.html',headings=headings, data=result,button=button.title() if button is not None else "")

@app.route('/no_deliverables', methods=['GET', 'POST'])
def no_deliverables():
    button = request.form.get("form_button")
    print(button)
    if button is None:
        result = []
        headings = []
    else:
        sql =   """ select r.first_name, r.last_name, count(*) Number_of_tasks from researcher r
                    inner join (select w.res_id, w.task_id from work_on w
                    where w.task_id not in
                        (select d.task_id from delivery d
		
                    ) and w.task_id in
                    (select task_id from task  
                        where end_date >= CURDATE())
                    )  w2
                    on  w2.res_id = r.res_id
                    group by r.res_id
                    having Number_of_tasks >= 5
                    order by Number_of_tasks desc;"""
        cursor.execute(sql)
        headings = parse_headings(cursor.column_names)
        result = cursor.fetchall()
        print(result)   
    return render_template('no_deliverables.html',headings=headings, data=result,button=button.title() if button is not None else "")

@app.route('/criteria', methods=['GET', 'POST'])
def criteria():
    
    sql = "SELECT distinct e.exe_id ,e.name FROM executive e INNER JOIN task t on t.exe_id = e.exe_id WHERE t.end_date < curdate() order by e.exe_id;"
    cursor.execute(sql)
    executives = cursor.fetchall()
    executives = [f"{x[0]} | {x[1].capitalize()} " for x in executives]

    sql = "SELECT distinct p.prog_id ,p.name FROM program p INNER JOIN task t on p.prog_id = t.prog_id WHERE t.end_date > curdate() order by p.prog_id;"
    cursor.execute(sql)
    programs = cursor.fetchall()
    programs = [f"{x[0]} | {x[1].capitalize()} " for x in programs]

    prog = request.form.get("form_prog_id")
    
    date_include = request.form.get("form_date_include")
    if date_include == 'on':
        date = request.form.get("form_date_of_deadline")
    
    duration_include = request.form.get("form_duration_include")
    if duration_include == 'on':
        duration = request.form.get("form_duration_value")
    
    executive_include = request.form.get("form_executive_include")
    if executive_include == 'on':
        executive = request.form.get("form_exec_id")
    
    if (None in [prog]): # on first load of page is None
        result = []
        headings = []
    else:
        prog_id = prog.split()[0]
        sql =   """ SELECT p.prog_id, t.title FROM task t 
                    INNER JOIN program p 
                    ON t.prog_id = p.prog_id
                    WHERE (t.end_date > curdate()) AND (p.prog_id = %s); """
        sql_params = [prog_id]
        
        if not all(i=='on' for i in [date_include, duration_include, executive_include]) and not(all(i=='on' for i in [date_include, duration_include]) or all(i=='on' for i in [date_include, executive_include]) or all(i=='on' for i in [duration_include, executive_include])) : #date XOR duration XOR executive
            if date_include == 'on':
                sql =   """ SELECT a.prog_id, a.title , b.first_name, b.last_name FROM 
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
                            WHERE ( a.prog_id = %s ) AND (a.end_date > %s ); """
                sql_params += [date]
            elif duration_include == 'on':
                sql =   """ SELECT a.prog_id, a.title , b.first_name, b.last_name FROM 
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
                        """
                sql_params += [duration]
            elif executive_include == 'on':
                exec_id = executive.split()[0]
                sql =   """ SELECT a.prog_id, a.title , b.first_name, b.last_name FROM 
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
                        """
                sql_params += [exec_id]
     
        cursor.execute(sql, tuple(sql_params))
        headings = parse_headings(cursor.column_names)
        result = cursor.fetchall()
    
    return render_template('criteria.html', programs=programs, executives=executives, headings=headings, data=result)

@app.route("/views", methods=['POST', 'GET'])
def views():
    view = request.form.get("form_view")

    if view is None:
        result = []
        headings = []
    else:
        if view == 'tasks':
            sql = """select r.res_id as "Researcher's ID", r.first_name as "First Name", r.last_name as "Last Name", t.task_id as "Task's ID", t.title as "Task's Titla" from researcher r 
                    inner join work_on w 
                    on w.res_id = r.res_id
                    inner join task t 
                    on t.task_id = w.task_id
                    order by r.res_id;"""
        elif view == 'programs':
            sql = """select p.prog_id as "Program's ID", p.name as "Program's Name",t.task_id as "Task's ID", t.title as "Task's Title" from program p
                    inner join task t
                    on t.prog_id = p.prog_id
                    order by p.prog_id;"""
        cursor.execute(sql)
        headings = parse_headings(cursor.column_names)
        result = cursor.fetchall()
        
        print(result)

    return render_template('views.html', headings=headings, data=result, view=view.title() if view is not None else "")

@app.route('/insert',methods=['GET','POST'])
def insert():
    #Science fields
    sql = "SELECT sc_id, name FROM science;"
    cursor.execute(sql)
    sciences = cursor.fetchall()
    sciences = [f"{x[0]} | {x[1].capitalize()} " for x in sciences]
    
    #Executives fileds
    sql = "SELECT exe_id, name FROM executive;"
    cursor.execute(sql)
    executives = cursor.fetchall()
    executives = [f"{x[0]} | {x[1].capitalize()} " for x in executives]

    #Organization fields
    sql = "SELECT org_id, name FROM organization;"
    cursor.execute(sql)
    organizations = cursor.fetchall()
    organizations = [f"{x[0]} | {x[1].capitalize()} " for x in organizations]

    #Research Director
    sql = "SELECT org_id, res_id, first_name, last_name FROM researcher order by org_id;"
    cursor.execute(sql)
    researchers = cursor.fetchall()
    researchers = [f"{x[1]} | {x[0]} | {x[2].capitalize()}  {x[3].capitalize()}" for x in researchers]
    
    #Program
    sql = "SELECT prog_id, name FROM program order by prog_id;"
    cursor.execute(sql)
    programs = cursor.fetchall()
    programs = [f"{x[0]} | {x[1].capitalize()}" for x in programs]

    msg=''   
    #applying empty validation
    if request.method == 'POST' and 'title' in request.form and 'amount' in request.form and 'start_date' in request.form and 'end_date' in request.form and 'abstract' in request.form and 'grade' in request.form and 'form_exe_id' in request.form and 'form_org_id' in request.form and 'form_res_id' in request.form and 'form_prog_id' in request.form and 'form_sc_id' in request.form:
        #passing HTML form data into python variable
        
        #Task title
        t = request.form['title']
        
        #Amount
        a = request.form['amount']
        
        #Start date
        sd = request.form['start_date']
        
        #End date
        ed = request.form['end_date']
        
        #Abstact
        ab = request.form['abstract']
        
        #Grade
        gr = request.form['grade']
        
        #Executive
        executive = request.form.get("form_exe_id")
        exe_id = executive.split()[0]
        
        #Organization
        organization = request.form.get("form_org_id")
        org_id = organization.split()[0]
        
        #Program
        program = request.form.get("form_prog_id")
        prog_id = program.split()[0]      
        
        #Researcher
        researcher = request.form.get("form_res_id")
        res_id = researcher.split()[0]                 
        
        #Science field
        science = request.form.get("form_sc_id")
        sc_id = science.split()[0]
        
        #Evaluator
        evaluator = request.form.get("form_eval_id")
        eval_id = researcher.split()[0]         
        
        #Insert the new task in the Table "task"
        cursor.execute('INSERT INTO task VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (t, a, sd, ed,ab,exe_id,prog_id,org_id,res_id,))
        db.commit()
        
        task_id = cursor.lastrowid  #We need to keep the id of the last row of task table 
        
        #Auto complete the evaluation relationship with eval_date = start_date
        cursor.execute('INSERT INTO evaluation VALUES (%s,%s,%s,%s);',(task_id,eval_id,gr,sd,))
        db.commit()
        
        #Auto complete the work_on relationship   
        cursor.execute('select a.task_id, b.res_id from(select r.res_id, r.org_id from researcher r where org_id = %s) b inner join (select t.task_id,t.org_id from task t where t.task_id = %s)a on b.org_id = a.org_id',(org_id,task_id,)) 
        values = list(cursor.fetchall())
        cursor.executemany('INSERT INTO work_on VALUES (%s,%s)',values)
        db.commit()
        
    return render_template('insert.html', sciences=sciences, executives=executives, programs=programs, researchers=researchers, organizations=organizations)


if __name__ == "__main__":
    app.debug = True
    app.run()