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
  `nouns` VARCHAR(450) NULL,
  PRIMARY KEY (`id`));
