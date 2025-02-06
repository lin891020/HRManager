from fastapi import FastAPI, Depends, HTTPException, Body, File, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Employee
from typing import List
from pydantic import BaseModel
from fastapi.responses import FileResponse
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmployeeCreate(BaseModel):
    name: str
    age: int
    position: str
    salary: float

class EmployeeUpdate(BaseModel):
    name: str
    age: int
    position: str
    salary: float

class EmployeeResponse(BaseModel):
    id: int
    name: str
    age: int
    position: str
    salary: float

    class Config:
        orm_mode: True

app = FastAPI()

# 添加 CORS 中間件
origins = [
    "http://localhost:3000",  # 允許來自前端應用程序的請求
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 HTTP 標頭
)

# ✅ 確保根路徑 `/` 可以正確回應
@app.get("/")
def root():
    return {"message": "HRManager API is running!"}

# ✅ 查詢所有員工
@app.get("/employees/", response_model=List[EmployeeResponse])
def read_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

# ✅ 查詢單一員工
@app.get("/employees/{id}", response_model=EmployeeResponse)
def read_employee(id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

# ✅ 新增員工
@app.post("/employees/", response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(**employee.dict())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

# ✅ 更新員工
@app.put("/employees/{id}", response_model=EmployeeResponse)
def update_employee(id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    existing_employee = db.query(Employee).filter(Employee.id == id).first()
    if not existing_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in employee.dict().items():
        setattr(existing_employee, key, value)
    
    db.commit()
    db.refresh(existing_employee)
    return existing_employee

# ✅ 刪除員工
@app.delete("/employees/{id}")
def delete_employee(id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

# ✅ 批量刪除員工
@app.delete("/employees/bulk_delete/")
def delete_multiple_employees(employee_ids: List[int] = Body(...), db: Session = Depends(get_db)):
    employees = db.query(Employee).filter(Employee.id.in_(employee_ids)).all()
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found with the given IDs")
    
    for employee in employees:
        db.delete(employee)
    
    db.commit()
    return {"message": f"Deleted {len(employees)} employees successfully"}

# ✅ 查詢員工（條件查詢）
@app.get("/employees/search/")
def search_employees(name: str = None, min_age: int = None, max_age: int = None, position: str = None, min_salary: float = None, max_salary: float = None, db: Session = Depends(get_db)):
    query = db.query(Employee)

    if name:
        query = query.filter(Employee.name.ilike(f"%{name}%"))
    if min_age:
        query = query.filter(Employee.age >= min_age)
    if max_age:
        query = query.filter(Employee.age <= max_age)
    if position:
        query = query.filter(Employee.position.ilike(f"%{position}%"))
    if min_salary:
        query = query.filter(Employee.salary >= min_salary)
    if max_salary:
        query = query.filter(Employee.salary <= max_salary)

    return query.all()

# ✅ 分頁查詢員工
@app.get("/employees/paginated/", response_model=List[EmployeeResponse])
def get_paginated_employees(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    employees = db.query(Employee).offset(offset).limit(limit).all()
    return employees

# ✅ 批量新增員工
@app.post("/employees/bulk_add/")
def add_multiple_employees(employees: List[EmployeeCreate], db: Session = Depends(get_db)):
    new_employees = [Employee(**emp.dict()) for emp in employees]
    db.add_all(new_employees)
    db.commit()
    return {"message": f"Added {len(new_employees)} employees successfully"}

# ✅ 上傳員工資料
@app.post("/employees/upload/")
async def upload_employees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        contents = await file.read()
        file.file.seek(0)  # 重置文件指針
        df = pd.read_excel(pd.io.common.BytesIO(contents))

        required_fields = ["id", "name", "age", "position", "salary"]
        inserted_count = 0
        skipped_records = []  # 存儲被跳過的 ID 及原因 
        invalid_rows = []     # 存儲無效數據及錯誤原因

        for _, row in df.iterrows():
            try:
                # 檢查必需欄位是否為空
                if any(pd.isna(row[field]) for field in required_fields):
                    invalid_rows.append({"row": row.to_dict(), "error": "Missing required fields"})
                    continue

                # 驗證欄位類型
                if pd.isna(row["salary"]) or not isinstance(row["salary"], (int, float)):
                    invalid_rows.append({"row": row.to_dict(), "error": "Invalid salary type"})
                    continue

                if pd.isna(row["age"]) or not isinstance(row["age"], (int, float)) or isinstance(row["age"], bool):
                    invalid_rows.append({"row": row.to_dict(), "error": "Invalid age type"})
                    continue

                # 檢查是否存在相同 ID
                existing_employee = db.query(Employee).filter(Employee.id == row["id"]).first()
                if existing_employee:
                    # 如果 ID 已存在，跳過
                    skipped_records.append({"id": row["id"], "reason": "ID already exists"})
                    continue

                # 插入新數據
                new_employee = Employee(
                    id=row["id"],
                    name=row["name"],
                    age=int(row["age"]),  # 確保 age 是整數
                    position=row["position"],
                    salary=row["salary"]
                )
                db.add(new_employee)
                inserted_count += 1

            except Exception as e:
                invalid_rows.append({"row": row.to_dict(), "error": str(e)})
                logger.error(f"Error processing row {row.to_dict()}: {str(e)}")
                continue

        db.commit()

        # Convert out-of-range float values to a JSON-compliant format
        def sanitize_for_json(data):
            if isinstance(data, float):
                if data == float('inf') or data == float('-inf') or data != data:  # NaN check
                    return str(data)
            elif isinstance(data, dict):
                return {k: sanitize_for_json(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [sanitize_for_json(i) for i in data]
            return data

        return {
            "message": f"Uploaded {inserted_count} new employees.",
            "skipped_records": sanitize_for_json(skipped_records),
            "invalid_rows": sanitize_for_json(invalid_rows)
        }
    except Exception as e:
        logger.error(f"An error occurred while processing the file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

# ✅ 匯出員工資料
@app.get("/employees/export/")
def export_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    df = pd.DataFrame([emp.__dict__ for emp in employees])
    df.drop(columns=["_sa_instance_state"], inplace=True)

    # 明確指定列的順序
    columns_order = ["id", "name", "age", "position", "salary"]
    df = df[columns_order]
    
    filename = "employees_export.xlsx"
    df.to_excel(filename, index=False)

    return FileResponse(filename, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=filename)
