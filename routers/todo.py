

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List

# app = FastAPI()

# # 模擬資料庫
# todo_list = []
# todo_id_counter = 1  # 自動遞增 ID

# # 定義 TodoItem 資料結構
# class TodoItem(BaseModel):
#     id: int
#     title: str
#     completed: bool = False

# # 🔹 1️⃣ 取得所有待辦事項
# @app.get("/todos/", response_model=List[TodoItem])
# def get_todos():
#     return todo_list

# # 🔹 2️⃣ 新增待辦事項
# @app.post("/todos/", response_model=TodoItem)
# def add_todo(todo: TodoItem):
#     global todo_id_counter
#     todo.id = todo_id_counter
#     todo_id_counter += 1
#     todo_list.append(todo)
#     return todo

# # 🔹 3️⃣ 更新待辦事項
# @app.put("/todos/{todo_id}", response_model=TodoItem)
# def update_todo(todo_id: int, updated_todo: TodoItem):
#     for index, todo in enumerate(todo_list):
#         if todo.id == todo_id:
#             todo_list[index] = updated_todo
#             return updated_todo
#     raise HTTPException(status_code=404, detail="找不到該事項")

# # 🔹 4️⃣ 刪除待辦事項
# @app.delete("/todos/{todo_id}")
# def delete_todo(todo_id: int):
#     global todo_list
#     todo_list = [todo for todo in todo_list if todo.id != todo_id]
#     return {"message": f"已刪除 ID {todo_id}"}

