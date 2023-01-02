/* Create schema */
CREATE DATABASE `easyflaskapp` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `easyflaskapp`;

/* Create user table */
CREATE TABLE `users` (
  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(128) NULL,
  `password` VARCHAR(128) NULL,
  `name` VARCHAR(45) NULL,
  `status` VARCHAR(45) NULL DEFAULT 'pending' COMMENT 'Active: Active user\nPending: Pending user waiting for activate\nDeleted: Deleted user that no longer available for login',
  `otp_secret` VARCHAR(45) NULL,
  `otp_status` VARCHAR(45) NULL DEFAULT 'disable' COMMENT 'Disable: do not use 2FA verification, \nEnable: 2FA verification enabled, \nPending: waiting for setting up 2FA verification',
  `created_at` TIMESTAMP NULL,
  `created_by` VARCHAR(45) NULL DEFAULT 'System',
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP(),
  PRIMARY KEY (`id`));
