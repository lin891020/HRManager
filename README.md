# HRManager Project

## Overview
HRManager is a Human Resource Management platform designed to simplify employee data management. The platform enables users to:

1. View employee data through a web interface.
2. Perform CRUD operations (Create, Read, Update, Delete) on employee records.
3. Upload bulk employee data via Excel files.
4. Easily deploy the application on any server using containerization (Docker).

---

## Workflow

### Phase 1: Database Design
**Goal:** Define the data model and initialize the database.

| Task                           | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| Define Employee Table          | Fields: `id`, `name`, `age`, `position`, `salary`.                          |
| Initialize SQLite Database     | Create `employees.db` and ensure basic operations like add/query work.     |

**Status:** Completed.

---

### Phase 2: Backend API Development
**Goal:** Develop APIs to handle CRUD operations and bulk uploads.

| Task                           | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| CRUD API                       | Implement `GET`, `POST`, `PUT`, and `DELETE` endpoints for employee data.   |
| Bulk Upload API                | Parse Excel files and insert records using `pandas` and `openpyxl`.         |

**Estimated Time:** 4-6 hours  
**Status:** In progress (CRUD partially completed; bulk upload pending).

---

### Phase 3: Frontend Development
**Goal:** Build a user-friendly web interface for managing employee data.

| Task                           | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| Employee List Page             | Display all employees with options to edit or delete.                      |
| Form Page                      | Provide a form for adding or editing employees.                             |
| Upload Page                    | Enable file upload for bulk employee data.                                  |
| Connect Frontend to Backend    | Use Fetch or Axios to integrate frontend with FastAPI backend.              |
| Style Interface                | Use CSS or frameworks like Bootstrap/Tailwind to improve UI aesthetics.     |

**Estimated Time:** 6-8 hours  
**Status:** Pending.

---

### Phase 4: Containerization
**Goal:** Package the application into a Docker container for easy deployment.

| Task                           | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| Create Dockerfile              | Base image: Python 3.9; Install dependencies and set entry point.           |
| Build and Run Container        | Build image and run container using Docker.                                 |
| Test Containerized Application | Ensure APIs are accessible and functional in the container.                 |

**Estimated Time:** 2-3 hours  
**Status:** Pending.

---

## Next Steps
1. Complete the remaining CRUD operations and implement the bulk upload API.
2. Start frontend development to create user-friendly pages for data management.
3. Finalize the Docker container and test deployment.

---

## Technologies Used
- **Backend:** FastAPI, SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript (or frameworks like React/Vue.js)
- **Containerization:** Docker
- **Libraries for File Handling:** pandas, openpyxl

---

## Contact
For further assistance or collaboration, please contact the project owner.

---

