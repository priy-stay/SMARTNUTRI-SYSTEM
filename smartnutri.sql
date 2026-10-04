use smartnutri;

create table food (
fdc_id bigint primary key,
data_type varchar(100),
description text,
food_category_id int null,
publication_date date null
);

create table nutrient (
id int primary key,
name varchar(255),
unit_name varchar(50),
nutrient_nbr varchar(50),
rank int null
);

create table food_nutrient (
id bigint primary key,
fdc_id bigint,
nutrient_id int,
amount decimal(18,6) null,
data_points int null,
derivation_id int null,
min decimal(18,6) null,
max decimal(18,6) null,
median decimal(18,6) null,
footnote text null,
min_year_acquired int null
);

create table disease_food_rules (
rule_id int auto_increment primary key,
disease varchar(100),
age_group varchar(50),
food_category varchar(100),
food_name varchar(255),
recommendation varchar(50),
priority varchar(20),
reason text
);

show tables;

use smartnutri;
alter table food drop column publication_data;
describe food;

use smartnutri;
truncate table food;

use smartnutri;
alter table food_nutrient modify column footnote text character set utf8mb4 collate utf8mb4_unicode_ci;

truncate table food_nutrient;

use smartnutri;
truncate table food_nutrient;
truncate table nutrient;
truncate table food;

use smartnutri;
select count(*) as food_count from food;
select count(*) as nutrient_count from nutrient;
select count(*) as food_nutrient_count from food_nutrient;
select count(*) as disease_rules_count from disease_food_rules;

USE smartnutri;
SELECT COUNT(*) AS total_foods FROM food;
SELECT COUNT(*) AS total_nutrients FROM nutrient;
SELECT COUNT(*) AS total_food_nutrients FROM food_nutrient;
SELECT COUNT(*) AS total_disease_rules FROM disease_food_rules;
SELECT disease,age_group,food_category,food_name,recommendation,priority,reason FROM disease_food_rules ORDER BY disease, age_group, priority;
SELECT DISTINCT disease FROM disease_food_rules ORDER BY disease;
SELECT DISTINCT age_group FROM disease_food_rules ORDER BY age_group;

select distinct disease from disease_food_rules order by disease;
SELECT disease,age_group,food_category,food_name,recommendation,priority,reason FROM disease_food_rules where disease = 'diabetes' and age_group = '50+' order by priority;

use smartnutri;
SELECT disease,age_group,food_category,food_name,recommendation,priority,reason FROM disease_food_rules ORDER BY disease, age_group, priority;

use smartnutri;
select disease,age_group,food_category,food_name,recommendation,priority,reason from disease_food_rules where lower(recommendation) like '%avoid%' order by disease, age_group;
  
  use smartnutri;
  truncate table disease_food_rules;
  
  use smartnutri;
  set foreign_key_checks = 0;
  truncate table food_nutrient;
  truncate table nutrient;
  truncate table food;
  truncate table disease_food_rules;
  set foreign_key_checks = 1;
  
  select count(*) from food;
  select count(*) from nutrient;
  select count(*) from food_nutrient;
  select count(*) from disease_food_rules;
  
  use smartnutri;
  select disease,age_group,food_name,food_category,recommendation,priority,reason from disease_food_rules where lower(recommendation) = 'avoid' order by disease,age_group;
  
  use smartnutri;
  select * from disease_food_rules where lower(recommendation) = 'avoid';
  
  use smartnutri;
  select count(*) as total_rows from smartnutri_recommendations;

use smartnutri;
select * from smartnutri_recommendations limit 10;

select count(*) as total_recommendations from smartnutri_recommendations;   

select disease,age_group,recommendation,count(*) as total from smartnutri_recommendations group by disease,age_group,recommendation order by disease, age_group;

show tables;
select * from disease_food_rules limit 10;
select count(*) as total_rules from disease_food_rules;
select distinct disease from disease_food_rules;
select disease, count(*) as rule_count from disease_food_rules group by disease;

select max(rule_id) as last_rule_id from disease_food_rules;

select fdc_id, description from food where lower(description) like '%oat%' limit 10;

select distinct food_category_id from food limit 50;
select fdc_id, description, food_category_id from food limit 50;

select fdc_id, description, food_category_id from food where lower(description) like '%hummus%' limit 20;
select fdc_id, description, food_category_id from food where lower(description) like '%lentil%' limit 20;
select fdc_id, description, food_category_id from food where lower(description) like '%chickpea%' limit 20;

select fdc_id, description, food_category_id from food where lower(description) like '%hummus%' limit 1;
select distinct disease, age_group, food_category, recommendation, priority from disease_food_rules order by disease, age_group;

SELECT
    rule_id,
    disease,
    age_group,
    food_name,
    food_category,
    recommendation,
    priority,
    reason
FROM disease_food_rules
WHERE LOWER(TRIM(disease)) = 'diabetes'
  AND TRIM(age_group) = '16-25'
  AND LOWER(TRIM(recommendation)) = 'avoid';
  
  use smartnutri;
  describe smartnutri_recommendations;
  
  use smartnutri;
  select * from smartnutri_recommendations;
  
  use smartnutri;
  truncate table smartnutri_recommendations;
  select count(*) as total_recommendations from smartnutri_recommendations;
  use smartnutri;
  select * from smartnutri_recommendations;
  select count(*) as total_recommendations from smartnutri_recommendations;
  
  use smartnutri;
  truncate table smartnutri_recommendations;
  
  select count(*) as total from smartnutri_recommendations;