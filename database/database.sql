-- ============================================================================
-- DATABASE SCHEMA: Library Management Data Warehouse & Data Mining System
-- Target DBMS: MySQL 8.x / 5.7 (also compatible with SQLite)
-- ============================================================================

CREATE DATABASE IF NOT EXISTS `library_dw_dm` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `library_dw_dm`;

-- ============================================================================
-- 1. OPERATIONAL TABLES (OLTP LAYER)
-- ============================================================================

-- Admin Users Table
CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `full_name` VARCHAR(100) NOT NULL,
    `role` VARCHAR(20) NOT NULL DEFAULT 'Administrator',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Operational Readers Table
CREATE TABLE IF NOT EXISTS `readers` (
    `reader_id` VARCHAR(20) PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `age` INT NOT NULL,
    `gender` VARCHAR(10) NOT NULL,
    `department` VARCHAR(50) NOT NULL,
    `membership_type` VARCHAR(30) NOT NULL,
    `registration_date` DATE NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Operational Books Table
CREATE TABLE IF NOT EXISTS `books` (
    `book_id` VARCHAR(20) PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `author` VARCHAR(100) NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `publisher` VARCHAR(100) NOT NULL,
    `publication_year` INT NOT NULL,
    `language` VARCHAR(30) NOT NULL DEFAULT 'English',
    `description` TEXT,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Operational Borrowing Transactions Table
CREATE TABLE IF NOT EXISTS `borrowing_transactions` (
    `transaction_id` VARCHAR(20) PRIMARY KEY,
    `reader_id` VARCHAR(20) NOT NULL,
    `book_id` VARCHAR(20) NOT NULL,
    `borrow_date` DATE NOT NULL,
    `due_date` DATE NOT NULL,
    `return_date` DATE NULL,
    `fine` DECIMAL(8, 2) NOT NULL DEFAULT 0.00,
    `status` VARCHAR(20) NOT NULL DEFAULT 'Borrowed',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_op_reader` FOREIGN KEY (`reader_id`) REFERENCES `readers`(`reader_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_op_book` FOREIGN KEY (`book_id`) REFERENCES `books`(`book_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================================
-- 2. DATA WAREHOUSE TABLES (OLAP LAYER - STAR SCHEMA)
-- ============================================================================

-- Dimension: Reader
CREATE TABLE IF NOT EXISTS `dim_reader` (
    `reader_key` INT AUTO_INCREMENT PRIMARY KEY,
    `reader_id` VARCHAR(20) NOT NULL UNIQUE,
    `reader_name` VARCHAR(100) NOT NULL,
    `age` INT NOT NULL,
    `gender` VARCHAR(10) NOT NULL,
    `department` VARCHAR(50) NOT NULL,
    `membership_type` VARCHAR(30) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Book
CREATE TABLE IF NOT EXISTS `dim_book` (
    `book_key` INT AUTO_INCREMENT PRIMARY KEY,
    `book_id` VARCHAR(20) NOT NULL UNIQUE,
    `title` VARCHAR(255) NOT NULL,
    `author` VARCHAR(100) NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `publisher` VARCHAR(100) NOT NULL,
    `language` VARCHAR(30) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dimension: Date
CREATE TABLE IF NOT EXISTS `dim_date` (
    `date_key` INT PRIMARY KEY, -- Format YYYYMMDD e.g. 20250115
    `full_date` DATE NOT NULL UNIQUE,
    `day` INT NOT NULL,
    `month` INT NOT NULL,
    `month_name` VARCHAR(20) NOT NULL,
    `quarter` INT NOT NULL,
    `year` INT NOT NULL,
    `day_of_week` VARCHAR(20) NOT NULL
);

-- Fact: Borrowing
CREATE TABLE IF NOT EXISTS `fact_borrowing` (
    `borrowing_id` INT AUTO_INCREMENT PRIMARY KEY,
    `transaction_id` VARCHAR(20) NOT NULL UNIQUE,
    `reader_key` INT NOT NULL,
    `book_key` INT NOT NULL,
    `date_key` INT NOT NULL,
    `borrow_count` INT NOT NULL DEFAULT 1,
    `return_count` INT NOT NULL DEFAULT 0,
    `fine_amount` DECIMAL(8, 2) NOT NULL DEFAULT 0.00,
    `borrowing_duration` INT NOT NULL DEFAULT 0, -- Duration in days
    `status` VARCHAR(20) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT `fk_fact_reader` FOREIGN KEY (`reader_key`) REFERENCES `dim_reader`(`reader_key`) ON DELETE CASCADE,
    CONSTRAINT `fk_fact_book` FOREIGN KEY (`book_key`) REFERENCES `dim_book`(`book_key`) ON DELETE CASCADE,
    CONSTRAINT `fk_fact_date` FOREIGN KEY (`date_key`) REFERENCES `dim_date`(`date_key`) ON DELETE CASCADE
);

-- ETL Execution Logs
CREATE TABLE IF NOT EXISTS `etl_log` (
    `log_id` INT AUTO_INCREMENT PRIMARY KEY,
    `run_timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `source_records_count` INT NOT NULL,
    `cleaned_records_count` INT NOT NULL,
    `warehouse_fact_count` INT NOT NULL,
    `status` VARCHAR(30) NOT NULL,
    `execution_duration_sec` DECIMAL(6, 3) NOT NULL,
    `details` TEXT
);

-- Default Admin User (Password: admin123 hashed via PBKDF2/Werkzeug standard)
-- Hash below matches Werkzeug generate_password_hash('admin123')
INSERT INTO `users` (`username`, `password_hash`, `full_name`, `role`)
VALUES ('admin', 'scrypt:32768:8:1$uH3y5k9GvPqR2n1t$f6eb5e9112423bb0d970e704fe5c70ce89e34e55e08b1a3848ae701389868e4a9089aa14bc8b8519bc16c4c34a266b8e8fb85eb93f21ef2f34731ae56b27eb66', 'Library Administrator', 'Administrator')
ON DUPLICATE KEY UPDATE `username`=`username`;
