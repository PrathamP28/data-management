# Role Manager

Role Manager is a GUI-based user management system built using Python and ttkbootstrap. It allows administrators to add, edit, remove, and manage user roles in a MySQL database.

## Features
- User authentication via a login page
- Add, edit, and delete users with role assignments
- Automatically generate usernames
- Display user data in a treeview
- Export user data to an Excel file
- Reset database entries

## Technologies Used
- Python
- ttkbootstrap (GUI framework)
- Tkinter
- MySQL (Database)
- Pandas (for Excel export)

## Installation

### Prerequisites
Make sure you have the following installed:
- Python 3.x
- MySQL Server
- Required Python packages:
  ```sh
  pip install -r requirements.txt
  ```

### Database Setup
1. Create a MySQL database and table using the following SQL script:
   ```sql
   CREATE DATABASE role_manager;
   USE role_manager;
   CREATE TABLE database1 (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255),
       username VARCHAR(255),
       mail VARCHAR(255),
       role VARCHAR(50)
   );
   ```
2. Update the `config.ini` file with your MySQL credentials:
   ```ini
   [database]
   host=your_host
   user=your_user
   password=your_password
   database=role_manager
   
   [login]
   user=admin
   password=admin123
   ```

## Usage
1. Run the application:
   ```sh
   python main.py
   ```
2. Log in with the credentials specified in `config.ini`.
3. Manage user roles through the provided interface.

