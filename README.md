# qblogs
Course Work LNU 2021

![image](https://github.com/graveetone/qblogs/assets/98279909/338185f1-b1f1-4c33-9451-165a4c573a7b)

![image](https://github.com/graveetone/qblogs/assets/98279909/0f824833-5339-48ce-9896-9b9a25d4457b)

![image](https://github.com/graveetone/qblogs/assets/98279909/68a5f5bb-c97a-4b6b-887b-0a6fe1b924f3)

Steps to deploy locally
1. You need MySQL database amanagement system to run the project.
   <br>
   Ubuntu guide: https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04
   <br>
   Windows guide: https://dev.mysql.com/downloads/installer/
3. Default user for MySQL database of the project is:
   <br>
   username: root
   password: root
4. To create database qblogs_db run the following command in terminal:
   <br>
   mysql -u root -p -e "CREATE DATABASE qblogs_db"
   <br>
6. Create virtual env for better packages management:
   <br>
   python -m venv venv
   <br>
7. Activate virtual environment (ubuntu):
   <br>
   source venv/bin/activate
   <br>
8. Install all dependencies listed in requirements.txt:
   <br>
   pip install -r requirements.txt
   <br>
9. Run migrations:
   <br>
   flask db upgrade
   <br>
10. Seed the database to create user and posts:
   <br>
   python seed.py
   <br>
11. Run Flask server
   <br>
  flask run
   <br>
12. Run Flask in Debug Mode (optional):
   <br>
    flask --debug run
   <br>
13. Run localhost:5000. Now you should be able to log in using creadentials:
   <br>
    login: user1
    password: pass1234
