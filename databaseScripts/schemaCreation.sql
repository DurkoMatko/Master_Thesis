CREATE SCHEMA `oss_issues` ;

CREATE TABLE `oss_issues`.`issues` (
  `id` INT NOT NULL,
  `title` VARCHAR(450) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `number` INT NULL,
  `created` DATE NULL,
  `closed` DATE NULL,
  `description` VARCHAR(450) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `labels` VARCHAR(450) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `project` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));

  ALTER TABLE `oss_issues`.`issues` 
CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT ;


CREATE TABLE `oss_issues`.`just_bugs` (
  `id` INT NOT NULL,
  `title` VARCHAR(450) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `number` INT NULL,
  `created` DATE NULL,
  `closed` DATE NULL,
  `description` VARCHAR(450) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `labels` VARCHAR(450) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL,
  `project` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));

  ALTER TABLE `oss_issues`.`just_bugs` 
CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT ;

CREATE TABLE `oss_issues`.`so_questions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `question_id` INT NULL,
  `title` VARCHAR(160) NULL,
  `creation_date` DATE NULL,
  `tags` VARCHAR(450) NULL,
  `body` VARCHAR(4000) NULL,
  `project` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `oss_issues`.`so_issue_comments` (
  `id` INT NOT NULL,
  `question_id` INT(11) NULL,
  `comment_id` INT(11) NULL,
  `comment_body` VARCHAR(4000) NULL,
  `project` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));


CREATE TABLE `oss_issues`.`git_so_matches` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `so_id` INT NULL,
  `git_id` INT NULL,
  `so_title` VARCHAR(450) NULL,
  `git_title` VARCHAR(450) NULL,
  `so_body` VARCHAR(4000) NULL,
  `git_body` VARCHAR(4000) NULL,  
  `git_project` VARCHAR(45) NULL,
  `so_tags` VARCHAR(450) NULL,
  PRIMARY KEY (`id`));

  ALTER TABLE `oss_issues`.`git_so_matches` 
CHANGE COLUMN `id` `id` INT(11) NOT NULL AUTO_INCREMENT ;
