
# 📊 Fraud Detection Dataset Documentation

This document describes the structure and purpose of each dataset used in the synthetic fraud detection use case.

---

## 📦 Table 1: `transactions` (Suggested: `user_transactions`)
Captures all financial transactions performed by users.

| Column Name         | Type    | Description                                                                 |
|---------------------|---------|-----------------------------------------------------------------------------|
| `transaction_id`     | string  | Unique identifier for the transaction.                                     |
| `user_id`            | string  | Foreign key referencing `user_profile.user_id`. Identifies the user who performed the transaction. |
| `transaction_date`   | string  | Date of the transaction (format: YYYY-MM-DD).                             |
| `amount`             | double  | Monetary value of the transaction.                                        |
| `transaction_type`   | string  | Mode of transaction (e.g., Online, POS, ATM, Transfer).                   |
| `merchant_category`  | string  | Category of the merchant (e.g., Grocery, Electronics, Travel).            |
| `tran_location`      | string  | City or locality where the transaction occurred.                          |

---

## 📦 Table 2: `activity_log` (Suggested: `user_system_activity_log`)
Tracks system access events and geolocation behavior of users.

| Column Name             | Type      | Description                                                                 |
|-------------------------|-----------|-----------------------------------------------------------------------------|
| `log_id`                 | string    | Unique identifier for the activity log entry.                              |
| `user_id`               | string    | Foreign key referencing `user_profile.user_id`. Identifies the accessing user. |
| `system_accessed`       | string    | System name or ID accessed by the user (e.g., Internal Portal, Payment API). |
| `access_time`           | timestamp | Actual time of access event (login, query, etc.).                          |
| `access_type`           | string    | Type of access (e.g., Read, Write, Execute, Admin).                        |
| `act_geo_dev_location`  | string    | City/geographical location derived from the user's device/IP.             |
| `access_timestamp`      | timestamp | Duplicate or transformed value of `access_time`; included for pipeline compatibility. |

---

## 📦 Table 3: `user_profile` (No Change Needed)
Stores demographic and identity details of users.

| Column Name         | Type    | Description                                                                 |
|---------------------|---------|-----------------------------------------------------------------------------|
| `user_id`            | string  | Primary key. Unique identifier for each user.                              |
| `name`               | string  | Full legal name of the user.                                               |
| `dob`                | date    | Date of birth of the user.                                                 |
| `email`              | string  | Registered email address.                                                  |
| `phone`              | string  | Mobile or landline number.                                                 |
| `ssn`                | string  | Social Security Number or equivalent government ID.                        |
| `address`            | string  | Full residential address of the user.                                      |
| `registration_date`  | string  | Date when the user first registered with the institution.                  |

---

## 📦 Table 4: `user_credit_profile` (Suggested: `credit_profile`)
Contains credit and financial behavior indicators of users.

| Column Name         | Type    | Description                                                                 |
|---------------------|---------|-----------------------------------------------------------------------------|
| `user_id`            | string  | Foreign key referencing `user_profile.user_id`.                            |
| `total_credit_limit`| double  | Sum of all approved credit lines for the user.                             |
| `credit_score`       | bigint  | Credit bureau score (range typically 300-850).                             |
| `current_utilization`| bigint  | Amount of credit currently used by the user.                               |
| `delinquencies`      | bigint  | Count of missed or late payments reported.                                 |
| `num_loans`          | bigint  | Number of open or active loan accounts.                                    |

---

## 📦 Table 5: `city_lat_long` (Suggested: `city_geolocation_map`)
Lookup table for mapping cities to their geographical coordinates.

| Column Name   | Type    | Description                                                         |
|---------------|---------|---------------------------------------------------------------------|
| `city`         | string  | City name used in logs or transactions.                            |
| `latitude`     | double  | Latitude of the city center.                                       |
| `longitude`    | double  | Longitude of the city center.                                      |

---

## 📦 Table 6: `fraud_disposition` (Suggested: `fraud_labels`)
Target label for supervised learning. Provided by investigation or fraud analytics team.

| Column Name   | Type    | Description                                                                  |
|---------------|---------|------------------------------------------------------------------------------|
| `user_id`      | string  | Foreign key referencing `user_profile.user_id`.                             |
| `is_synthetic` | string  | Binary classification label: `1` for synthetic/fraudulent identity, `0` for legitimate. |

---
