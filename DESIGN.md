# Design Document

By moheshamm

Video overview: <https://youtu.be/lp3UqHoFjQE>

## Scope

In this section you should answer the following questions:

* What is the purpose of your database?
The purpose of this database is to act as the foundation for an SQLite Wallet App!
* Which people, places, things, etc. are you including in the scope of your database?
Users, which includes usernames and password
Wallets, which includes the wallet's name, the amount stored inside of it in dollars($), and the user which is associated with that wallet!
* Which people, places, things, etc. are *outside* the scope of your database?
Out of scope elements may include: The lack of a table that tracks transactions and processes, Transfering from a user's own wallet to another wallet he has in his own account.

-- The primary goal of this database is to serve as the backbone for an innovative SQLite Wallet App. This application aims to simplify financial management for users by providing a user-friendly python terminal interface for managing various wallets. The database is designed to store essential information about users and their respective wallets. Specifically, it includes details such as usernames, passwords, wallet names, and the balance within each wallet, denoted in US dollars ($). This design ensures that users can efficiently manage their finances within a secure environment.

-- It's important to clarify that certain elements fall outside the scope of this database to maintain simplicity and focus on core functionalities. These exclusions include the ability to track detailed transaction histories, such as deposits, withdrawals, and transfers. Furthermore, the database does not support transferring funds between wallets owned by the same user or selecting different currencies. By limiting the scope in this manner, the design remains straightforward and focused on providing a robust foundation for the wallet app.

## Functional Requirements

In this section you should answer the following questions:

* What should a user be able to do with your database?
So basically I've decided instead of letting the user run queries manually and get too deep into the weeds and fancy SQLite words; I decided to take the approach of abstracting everything away by implementing a user-friendly python program along with the help of CS50's Libary in Python and SQL module! A user should be able to Login, Create an account, or simply Exit a Program as provided by the base menu. If a user logs in; He is provided with 10 Services: Display Wallets, Deposit, Withdraw, Transfer To a User, Add Wallet, Delete Wallet, Change Password, Change Username, DELETE Account, and lastly Sign Out! All of this is automated by simply choosing the process and service number as asked by the program. Every service is automated and applied on to the database (wallet.db) automatically. Not only does it stop there, but every thing is checked: Usernames(If exist), Passwords, Wallet names(If exist), Sufficent funds in the Wallet, and more! If any of these checks are violated, every process undos like it never happend! To avoid logging in for every process, a user is simply asked a Yes OR No Question to continue. Yet in some cases if a check like in a password; a user may be signed out as a safety precaution. And Of course CRUD operations are supported!

* What's beyond the scope of what a user should be able to do with your database?
Not being able to track transactions history/logs whether its a deposit,withdraw,or transfer; Transfering from a user's own wallet to another wallet he has in his own account; and Selecting a currency.

-- The database is crafted with the end-user in mind, aiming to abstract the complexities of SQL queries through a friendly Python program interface. This approach leverages CS50's Library, alongside Python and SQL modules, to offer a seamless experience. Upon interacting with the base menu, users can choose to log in, create an account, or exit the program. Successful login grants access to a suite of 10 services, including displaying wallets, depositing funds, withdrawing funds, transferring to another user, adding a new wallet, deleting an existing wallet, changing passwords, changing usernames, deleting an account, and signing out.

Each service is carefully automated, ensuring direct and hassle-free interaction with the wallet.db database. The system incorporates comprehensive checks to validate usernames, passwords, wallet names, and sufficient funds. These precautions prevent unauthorized actions and maintain the integrity of each transaction. In instances where checks fail, the system reverts any changes to preserve data accuracy. Additionally, to enhance user convenience, the program allows continuous operation without repeated logins, only requiring confirmation to proceed after each action. This thoughtful consideration towards user experience underscores the database's aim to provide a reliable and efficient financial management tool.

Moreover, the design supports CRUD operations, reinforcing its functionality and versatility. However, it's worth noting that the database does not facilitate transaction history tracking, transfers between a user's own wallets, or currency selection. These decisions streamline the database's focus but may limit its appeal to users seeking more comprehensive financial tracking features.

## Representation
Entities are captured in SQLite tables with the following schema.

### Entities

The `users` table includes:

* `id`, which specifies the unique ID for the user as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `username`, which specifies the user's username as `TEXT`, given `TEXT` is appropriate for username fields.
* `password`, which specifies the user's password as `TEXT`, given `TEXT` should be appropiate for password fields.

All columns in the `users` table are required and hence should have the `NOT NULL` constraint applied. No other constraints are necessary.

The `wallets` table includes:

* `id`, which specifies the unique ID for each wallet as an `INTEGER`. This column thus has the `PRIMARY KEY` constraint applied.
* `name`, which specifies the wallet's name as `TEXT`, given `TEXT` is appropriate for name fields.
* `amount`, which specifies the amount stored in that wallet as `NUMERIC`, since `NUMERIC` allows for the suitable conversions of numbers. Additionally there is a `CHECK` applied to ensure the amount doesn't go below an amount of zero.
* `user_id`, which is the ID of the user who is associated with that wallet as an `INTEGER`. This column thus has the `FOREIGN KEY` constraint applied, referencing the `id` column in the `users` table to ensure data integrity. Aswell as having `ON DELETE CASCADE` column constraint to have the benefit of automatically deleting the wallet in case a user is deleted.

All columns in the `wallets` table are required and hence should have the `NOT NULL` constraint applied. No other constraints are necessary.

-- The users table is a crucial component of the database, storing unique identifiers, usernames, and passwords for each user. This table employs the PRIMARY KEY constraint on the id column to ensure each user has a distinct identity within the system. The username and password fields are defined as TEXT to appropriately handle the data, with the NOT NULL constraint applied to all columns to guarantee the completeness of user information.

Similarly, the wallets table plays a vital role in managing financial data. It includes columns for a unique id, name, amount, and user_id. The id column serves as the PRIMARY KEY, while the name field allows textual representation of the wallet's name. The amount column, defined as NUMERIC, ensures accurate financial representation and includes a CHECK constraint to prevent negative balances. The user_id establishes a link to the users table, embodying the FOREIGN KEY constraint for data integrity and implementing ON DELETE CASCADE to automatically remove wallets if a user is deleted. This careful structuring ensures a robust and interconnected data model.

### Relationships

The below entity relationship diagram describes the relationships among the entities in the database.

![ER Diagram](ER Diagram.png)

Or to provide a link: https://drawsql.app/teams/elziats-team/diagrams/cs50sql-final-project

* A One-To-Many Relationship is observed between the users and wallets tables, illustrating that each user can possess multiple wallets, but each wallet is uniquely tied to a single user. This relationship facilitates the efficient management of multiple financial accounts under a single user profile, enhancing the app's utility.

## Optimizations

To optimize database performance, especially considering the frequent access patterns involving usernames and user-associated wallets, indexes have been created on the username and user_id columns. These indexes significantly improve query execution times, making the user experience smoother and more responsive. This optimization demonstrates a thoughtful approach to database design, ensuring that the system remains efficient as it scales.

## Limitations

In this section you should answer the following questions:

* What are the limitations of your design?
* What might your database not be able to represent very well?

User interface may not be at a professional or an actual application level since it's a terminal based application accessed through a python program. Usernames and Wallet names may be repeated ,thus having multiple users having the same username/wallet name which may interfere with the queries (Which is not assessed in this version with a `UNIQUE` Column constraint nor a `ValueError` condition in the python program) leading to unexpected results. Deposits are allowed with any amount with no restrictions which could allow someone to maliciously interfere and insert a really large number to cause some errors in the database and program. Python Code may have been cleaner if I had prior knowledge of python methods/functions to implement a method that is being reused over and over, leading to a cleaner code structure and fewer lines of code(570 lines of code!).{May revist the project's code and try to clean it up if i take a python course like CS50Python in the future!}. Neither TRIGGERS nor VIEWS were used in this version of the program. When changing username or password, You can use the old ones and process will still work which will affect the login process aswell.

-- The current design of the database and its accompanying Python program emphasizes simplicity and user-friendliness but comes with certain limitations. The interface, being terminal-based, may not match the sophistication of professional applications, potentially affecting user engagement. Additionally, the absence of constraints to prevent duplicate usernames or wallet names could lead to confusion and inaccuracies in managing accounts. The system's handling of deposits also lacks restrictions on the amount, which could be exploited for malicious purposes.

The Python code, spanning approximately 570 lines, could benefit from a more modular approach, employing functions or methods to avoid repetition and improve maintainability. The project does not utilize advanced database features like TRIGGERS or VIEWS, which could enhance functionality and efficiency. Moreover, the process for changing usernames or passwords lacks checks to prevent the reuse of previous credentials, posing a security risk.

Despite these limitations, the database serves as a robust foundation for the SQLite Wallet App, offering essential features for financial management. Future iterations could address these issues, expanding the app's capabilities and improving user experience.
