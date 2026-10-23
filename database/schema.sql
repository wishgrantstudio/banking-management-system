-- Banking Management System
-- Database schema for MySQL 8

CREATE TABLE banks (
    bank_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    bank_code VARCHAR(20) NOT NULL UNIQUE,
    head_office VARCHAR(150)
) ENGINE=InnoDB;


CREATE TABLE branches (
    branch_id INT AUTO_INCREMENT PRIMARY KEY,
    bank_id INT NOT NULL,
    branch_name VARCHAR(100) NOT NULL,
    ifsc_code VARCHAR(11) NOT NULL UNIQUE,
    address VARCHAR(255),
    city VARCHAR(100),

    FOREIGN KEY (bank_id)
        REFERENCES banks(bank_id)
) ENGINE=InnoDB;


CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    phone VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;


CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    account_type ENUM('savings', 'current') NOT NULL,
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    opening_date DATE NOT NULL,
    status ENUM('active', 'frozen', 'closed')
        NOT NULL DEFAULT 'active',

    CONSTRAINT chk_account_balance
        CHECK (balance >= 0),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id)
) ENGINE=InnoDB;


CREATE TABLE deposits (
    deposit_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    deposit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deposit_method ENUM('cash', 'cheque', 'online') NOT NULL,

    CONSTRAINT chk_deposit_amount
        CHECK (amount > 0),

    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
) ENGINE=InnoDB;


CREATE TABLE withdrawals (
    withdrawal_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    withdrawal_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    withdrawal_method ENUM('atm', 'branch', 'online') NOT NULL,

    CONSTRAINT chk_withdrawal_amount
        CHECK (amount > 0),

    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
) ENGINE=InnoDB;


CREATE TABLE transfers (
    transfer_id INT AUTO_INCREMENT PRIMARY KEY,
    from_account_id INT NOT NULL,
    to_account_id INT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'completed', 'failed')
        NOT NULL DEFAULT 'pending',

    CONSTRAINT chk_transfer_amount
        CHECK (amount > 0),

    CONSTRAINT chk_different_accounts
        CHECK (from_account_id <> to_account_id),

    FOREIGN KEY (from_account_id)
        REFERENCES accounts(account_id),

    FOREIGN KEY (to_account_id)
        REFERENCES accounts(account_id)
) ENGINE=InnoDB;


CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    branch_id INT NOT NULL,
    loan_type VARCHAR(50) NOT NULL,
    loan_amount DECIMAL(15, 2) NOT NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    start_date DATE NOT NULL,
    duration_months INT NOT NULL,
    status ENUM('pending', 'approved', 'rejected', 'closed')
        NOT NULL DEFAULT 'pending',

    CONSTRAINT chk_loan_amount
        CHECK (loan_amount > 0),

    CONSTRAINT chk_interest_rate
        CHECK (interest_rate >= 0),

    CONSTRAINT chk_loan_duration
        CHECK (duration_months > 0),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id),

    FOREIGN KEY (branch_id)
        REFERENCES branches(branch_id)
) ENGINE=InnoDB;


CREATE TABLE loan_payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT NOT NULL,
    payment_amount DECIMAL(15, 2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method ENUM('cash', 'cheque', 'online') NOT NULL,

    CONSTRAINT chk_payment_amount
        CHECK (payment_amount > 0),

    FOREIGN KEY (loan_id)
        REFERENCES loans(loan_id)
) ENGINE=InnoDB;
