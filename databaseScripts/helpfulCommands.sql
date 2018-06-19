select count(*), project from oss_issues.so_questions group by project;

select * from oss_issues.so_questions where body like '%angularjs/issues%';

select count(*) from oss_issues.so_questions where project in ('angularjs','nodejs','bower','rubyonrails','vuejs','emberjs') group by project;

Select count(*), project FROM oss_issues.just_bugs group by project;

Select count(*) FROM oss_issues.issues group by project;

Select number,title,description from oss_issues.just_bugs where project='angularjs';

select * from oss_issues.just_bugs limit 100;

Select count(*), git_project FROM oss_issues.git_so_matches group by git_project;