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


CREATE TABLE `oss_issues`.`just_bigs` (
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
