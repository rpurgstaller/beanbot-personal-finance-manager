# Beanbot: Double-Entry Accounting CLI with Beancount

## Description

Beanbot is a CLI for your financial transactions. 

It is possible to import and save your transactions from csv to a sqlite database. You can also create rules to transform attributes from your transactions and export your database to a double-entry accounting text file based on beancount.


## Requirements

```
pip install -r requirements.txt
```

## Technologies and Frameworks

- python 3
- sqlite3
- SQLAlchemy
- scikit-learn
- PyInquirer

## Setup

Set Environment Variable:

- BEANBOT_HOME_DIR
- settings.json
  - Configuration of Database file names
  - Configuration of Giro account
  - Transaction mapping: Map columns from import file to database columns 

## Features

- Import transactions from CSV into a sqlite database
- Create rules to transform transactions before saving them
- Transform transactions to a double entry accounting text file suitable for beancount.

### To Do

- Creation of macros to easily track cash transactions
- Find similar transactions for new transactions based on text similarity using scikit-learn