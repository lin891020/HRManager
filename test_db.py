from app.database import get_db
from app.models import Employee

# 取得資料庫連接
db = next(get_db())

# 測試插入數據
new_employee = Employee(name="Alice", age=30, position="Engineer", salary=70000)
db.add(new_employee)
db.commit()

# 測試查詢數據
employees = db.query(Employee).all()
for emp in employees:
    print(f"ID: {emp.id}, Name: {emp.name}, Age: {emp.age}, Position: {emp.position}, Salary: {int(emp.salary)}")

# 關閉資料庫連接
db.close()
