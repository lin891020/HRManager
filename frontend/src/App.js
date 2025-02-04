import React, { useState, useEffect } from "react";
import axios from "axios";
import fileDownload from 'js-file-download';

function App() {
    const [employees, setEmployees] = useState([]);
    const [newEmployee, setNewEmployee] = useState({
        name: "",
        age: "",
        position: "",
        salary: "",
    });
    const [editingEmployee, setEditingEmployee] = useState(null); // 用於存儲正在編輯的員工
    const [editData, setEditData] = useState({
        name: "",
        age: "",
        position: "",
        salary: "",
    });
    const [deleteConfirm, setDeleteConfirm] = useState(null); // 用於存儲要刪除的員工
    const [selectedEmployees, setSelectedEmployees] = useState([]); // 存儲選中的員工 ID
    const [file, setFile] = useState(null); // 存儲上傳的文件
    const [uploadResult, setUploadResult] = useState(null); // 顯示上傳結果

    // Fetch employees from the backend
    useEffect(() => {
        fetchEmployees();
    }, []);

    const fetchEmployees = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/employees/");
            setEmployees(response.data);
        } catch (error) {
            console.error("Error fetching employees:", error);
        }
    };

    const addEmployee = async () => {
        try {
            await axios.post("http://127.0.0.1:8000/employees/", newEmployee);
            fetchEmployees();
            setNewEmployee({
                name: "",
                age: "",
                position: "",
                salary: "",
            });
        } catch (error) {
            console.error("Error adding employee:", error);
        }
    };

    const confirmDelete = (employee) => {
        setDeleteConfirm(employee); // 將要刪除的員工存儲起來
    };

    const deleteEmployee = async () => {
        if (deleteConfirm) {
            try {
                await axios.delete(`http://127.0.0.1:8000/employees/${deleteConfirm.id}`);
                setEmployees(employees.filter((employee) => employee.id !== deleteConfirm.id));
                setDeleteConfirm(null); // 清空確認對話框
            } catch (error) {
                console.error("Error deleting employee:", error);
            }
        }
    };

    const cancelDelete = () => {
        setDeleteConfirm(null); // 取消刪除
    };

    const saveEmployee = async () => {
        try {
            await axios.put(`http://127.0.0.1:8000/employees/${editingEmployee.id}`, editData);
            setEmployees(
                employees.map((emp) =>
                    emp.id === editingEmployee.id ? { ...emp, ...editData } : emp
                )
            );
            setEditingEmployee(null); // 關閉編輯模式
        } catch (error) {
            console.error("Error saving employee:", error);
        }
    };

    const startEditing = (employee) => {
        setEditingEmployee(employee);
        setEditData({
            name: employee.name,
            age: employee.age,
            position: employee.position,
            salary: employee.salary,
        });
    };

    const handleCheckboxChange = (id) => {
        setSelectedEmployees((prevSelected) =>
            prevSelected.includes(id)
                ? prevSelected.filter((employeeId) => employeeId !== id) // 取消選擇
                : [...prevSelected, id] // 添加選擇
        );
    };

    const deleteSelectedEmployees = async () => {
        if (selectedEmployees.length === 0) {
            alert("No employees selected for deletion.");
            return;
        }

        if (!window.confirm(`Are you sure you want to delete selected employees?`)) {
            return;
        }

        try {
            await axios.delete("http://127.0.0.1:8000/employees/bulk_delete/", {
                data: selectedEmployees, // 傳遞選中的員工 ID 列表
            });
            setEmployees(employees.filter((emp) => !selectedEmployees.includes(emp.id)));
            setSelectedEmployees([]); // 清空選擇
        } catch (error) {
            console.error("Error deleting employees:", error);
        }
    };

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const uploadFile = async () => {
        if (!file) {
            alert("Please select a file before uploading.");
            return;
        }

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/employees/upload/",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );
            setUploadResult(response.data.message); // 顯示返回的結果
            fetchEmployees(); // 刷新員工列表
        } catch (error) {
            console.error("Error uploading file:", error);
            setUploadResult("Error uploading file.");
        }
    };

    const exportEmployees = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/employees/export/", {
                responseType: 'blob',
            });
            fileDownload(response.data, 'employees_export.xlsx');
        } catch (error) {
            console.error("Error exporting employees:", error);
        }
    };

    return (
        <div className="App">
            <h1>HR Manager</h1>
            <button onClick={deleteSelectedEmployees}>Delete Selected</button>
            <button onClick={exportEmployees}>Export Employees</button>

            {/* 文件上傳區域 */}
            <div>
                <h2>Upload Employees (Excel)</h2>
                <input type="file" onChange={handleFileChange} />
                <button onClick={uploadFile}>Upload</button>
            </div>

            {uploadResult && <p>{uploadResult}</p>}

            <table border="1">
                <thead>
                    <tr>
                        <th>Select</th>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Position</th>
                        <th>Salary</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {employees.map((employee) => (
                        <tr key={employee.id}>
                            <td>
                                <input
                                    type="checkbox"
                                    checked={selectedEmployees.includes(employee.id)}
                                    onChange={() => handleCheckboxChange(employee.id)}
                                />
                            </td>
                            <td>{employee.id}</td>
                            <td>{employee.name}</td>
                            <td>{employee.age}</td>
                            <td>{employee.position}</td>
                            <td>{employee.salary}</td>
                            <td>
                                <button onClick={() => startEditing(employee)}>Edit</button>
                                <button onClick={() => confirmDelete(employee)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            {editingEmployee && (
                <div>
                    <h2>Edit Employee</h2>
                    <form
                        onSubmit={(e) => {
                            e.preventDefault();
                            saveEmployee();
                        }}
                    >
                        <input
                            type="text"
                            placeholder="Name"
                            value={editData.name}
                            onChange={(e) => setEditData({ ...editData, name: e.target.value })}
                        />
                        <input
                            type="number"
                            placeholder="Age"
                            value={editData.age}
                            onChange={(e) => setEditData({ ...editData, age: e.target.value })}
                        />
                        <input
                            type="text"
                            placeholder="Position"
                            value={editData.position}
                            onChange={(e) => setEditData({ ...editData, position: e.target.value })}
                        />
                        <input
                            type="number"
                            placeholder="Salary"
                            value={editData.salary}
                            onChange={(e) => setEditData({ ...editData, salary: e.target.value })}
                        />
                        <button type="submit">Save</button>
                        <button onClick={() => setEditingEmployee(null)}>Cancel</button>
                    </form>
                </div>
            )}

            {deleteConfirm && (
                <div className="delete-confirm">
                    <p>
                        Are you sure you want to delete ID: {deleteConfirm.id}, Name:{" "}
                        {deleteConfirm.name}?
                    </p>
                    <button onClick={deleteEmployee}>Confirm</button>
                    <button onClick={cancelDelete}>Cancel</button>
                </div>
            )}

            <h2>Add Employee</h2>
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    addEmployee();
                }}
            >
                <input
                    type="text"
                    placeholder="Name"
                    value={newEmployee.name}
                    onChange={(e) => setNewEmployee({ ...newEmployee, name: e.target.value })}
                />
                <input
                    type="number"
                    placeholder="Age"
                    value={newEmployee.age}
                    onChange={(e) => setNewEmployee({ ...newEmployee, age: e.target.value })}
                />
                <input
                    type="text"
                    placeholder="Position"
                    value={newEmployee.position}
                    onChange={(e) => setNewEmployee({ ...newEmployee, position: e.target.value })}
                />
                <input
                    type="number"
                    placeholder="Salary"
                    value={newEmployee.salary}
                    onChange={(e) => setNewEmployee({ ...newEmployee, salary: e.target.value })}
                />
                <button type="submit">Add Employee</button>
            </form>
        </div>
    );
}

export default App;
