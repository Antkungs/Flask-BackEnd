## Steps to Run the Application

### 1. Clone the Repository
```bash
git clone https://github.com/Antkungs/Flask-BackEnd
cd Flask-BackEnd
```

### 2. Create a .env File
```bash
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_databasename
DB_HOST=name_host

PGADMIN_DEFAULT_EMAIL=git 
PGADMIN_DEFAULT_PASSWORD=admin

FLASK_APP=app.py
FLASK_ENV=development
```

### 3. Build and Run the Containers
Once the .env file is in place, use Docker Compose to build and start your containers:
bash
Copy code
```bash
docker-compose up --build
```
