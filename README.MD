# SQLite Wallet App

## Overview
The SQLite Wallet App revolutionizes personal finance management with a user-friendly Python terminal interface. Aimed at abstracting SQL complexities, this app provides an accessible platform for managing multiple wallets, focusing on simplicity and security.

---

## Key Features

1. **User and Wallet Management**
   - Stores essential user information, including usernames, passwords, and wallet balances in USD.

2. **Intuitive Python Interface**
   - Utilizes CS50's Library, Python, and SQL modules for a seamless user experience.

3. **Comprehensive Service Suite**
   - Offers 10 services post-login such as viewing wallets, managing funds, and account settings adjustments.

4. **Automated Checks**
   - Implements validation for usernames, passwords, wallet names, and balance sufficiency, ensuring secure transactions and data integrity.

5. **CRUD Operations Support**
   - Enhances functionality and versatility without compromising on simplicity.

---

## Design Considerations (More Details included in DESIGN.md)

- **User-Centric**
  - Designed with the end-user in mind, ensuring easy financial management within a secure environment.

- **Continuous Operation**
  - Allows for uninterrupted use with confirmation prompts post-action, enhancing user convenience.

- **Simplicity vs. Features**
  - Focuses on core functionalities, excluding transaction history, transfers between user-owned wallets, or currency options to streamline use.

---

## Limitations and Future Directions

1. **Interface and Engagement**
   - The terminal-based interface, while user-friendly, may lack the sophistication of professional apps, potentially affecting user engagement.

2. **Unique Constraints**
   - Currently does not prevent duplicate usernames or wallet names, which could lead to account management inaccuracies.

3. **Security Measures**
   - The absence of restrictions on deposit amounts and checks against reusing previous or existing credentials could pose security risks.

4. **Code Modularity**
   - The Python code could be improved with a more modular structure to enhance maintainability and functionality.

---

## Preview Videos
**2-minute preview:**


https://github.com/user-attachments/assets/a2164156-f882-442b-a3a4-3b7c9ce039f6



**[Watch the 10-minute detailed preview video here](https://www.youtube.com/watch?v=lp3UqHoFjQE)**

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mohamedelziat50/SQLite-Wallet-App.git
   ```

2. Navigate to the project directory:
   ```bash
   cd SQLite-Wallet-App
   ```

3. Ensure Python and SQLite are installed on your system.
   - [Download Python](https://www.python.org/downloads/)
   - [Download SQLite](https://www.sqlite.org/download.html)

4. Run the program:
   ```bash
   python program.py
   ```
