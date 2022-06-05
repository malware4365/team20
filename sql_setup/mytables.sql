CREATE TABLE executive (
  exe_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(30) NULL,
  PRIMARY KEY (exe_id)
);

CREATE TABLE organization (
  org_id INT NOT NULL AUTO_INCREMENT,
  abbreviation VARCHAR(10) NULL,
  name VARCHAR(45) NULL,
  zip INT NULL,
  street VARCHAR(45) NULL,
  city VARCHAR(35) NULL,
  PRIMARY KEY (org_id)
);

CREATE TABLE program (
  prog_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(70) NULL,
  department VARCHAR(55) NULL,
  PRIMARY KEY (prog_id)
);

CREATE TABLE researcher (
  res_id INT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(20) NULL,
  last_name VARCHAR(20) NULL,
  gender VARCHAR(10) NULL,
  birth_date DATE NULL,
  join_date DATE NULL,
  org_id INT NULL,
  PRIMARY KEY (res_id)
);

CREATE TABLE task (
  task_id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(45),
  amount INT NULL,
  start_date DATE NULL,
  end_date DATE NULL,
  abstract VARCHAR(150),
  exe_id INT NULL,
  prog_id INT NULL,
  org_id INT NULL,
  res_id INT NULL,
  PRIMARY KEY (task_id),
  CONSTRAINT fk_task_executive
    FOREIGN KEY (exe_id)
    REFERENCES executive (exe_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_task_organization1
    FOREIGN KEY (org_id)
    REFERENCES organization (org_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_task_program1
    FOREIGN KEY (prog_id)
    REFERENCES program (prog_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_task_researcher1
    FOREIGN KEY (res_id)
    REFERENCES researcher (res_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE company (
  org_id INT NOT NULL,
  fund INT NULL,
  PRIMARY KEY (org_id),
  CONSTRAINT fk_company_organization1
    FOREIGN KEY (org_id)
    REFERENCES organization (org_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE university (
  org_id INT NOT NULL,
  public_budget INT NULL,
  PRIMARY KEY (org_id),
  CONSTRAINT fk_university_organization1
    FOREIGN KEY (org_id)
    REFERENCES organization (org_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE research_center (
  org_id INT NOT NULL,
  public_budget INT NULL,
  private_budget INT NULL,
  PRIMARY KEY (org_id),
  CONSTRAINT fk_research_center_organization1
    FOREIGN KEY (org_id)
    REFERENCES organization (org_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE science (
  sc_id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) NULL,
  PRIMARY KEY (sc_id)
);

CREATE TABLE science_task (
  sc_id INT NOT NULL,
  task_id INT NOT NULL,
  PRIMARY KEY (sc_id, task_id),
  CONSTRAINT fk_science_task_task1
    FOREIGN KEY (task_id)
    REFERENCES task (task_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_science_task_science1
    FOREIGN KEY (sc_id)
    REFERENCES science (sc_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE delivery (
  task_id INT NOT NULL,
  title VARCHAR(6) NOT NULL,
  abstract VARCHAR(45) NULL,
  delivery_date DATE NULL,
  PRIMARY KEY (task_id, title),
  CONSTRAINT fk_delivery_task1
    FOREIGN KEY (task_id)
    REFERENCES task (task_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE work_on (
  task_id INT NOT NULL,
  res_id INT NOT NULL,
  PRIMARY KEY (task_id, res_id),
  CONSTRAINT fk_work_on_task1
    FOREIGN KEY (task_id)
    REFERENCES task (task_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_work_on_researcher1
    FOREIGN KEY (res_id)
    REFERENCES researcher (res_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE evaluation (
  task_id INT NOT NULL,
  res_id INT NOT NULL,
  grade INT NULL,
  eval_date DATE NULL,
  PRIMARY KEY (task_id),
  CONSTRAINT fk_evaluation_task1
    FOREIGN KEY (task_id)
    REFERENCES task (task_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_evaluation_researcher1
    FOREIGN KEY (res_id)
    REFERENCES researcher (res_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE phone (
  org_id INT NOT NULL,
  phone_number VARCHAR(14) NOT NULL,
  PRIMARY KEY (org_id, phone_number),
  CONSTRAINT fk_phone_organization1
    FOREIGN KEY (org_id)
    REFERENCES organization (org_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);