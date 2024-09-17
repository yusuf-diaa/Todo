import tkinter as tk
import json
import os

button_colors = {}

def change_color(button, task):
    current_color = button.cget('bg')
    if current_color == 'BLACK':
        button.config(bg='GREEN', fg='BLACK', text="✔")
        button_colors[task] = 'GREEN'
    else:
        button.config(bg='BLACK', fg='GREEN', text="✔")
        button_colors[task] = 'BLACK'
    save_button_colors()

def save_button_colors():
    with open("button_colors.json", "w") as file:
        json.dump(button_colors, file)

def load_button_colors():
    if os.path.exists("button_colors.json"):
        with open("button_colors.json", "r") as file:
            return json.load(file)
    return {}

def clear_task(task_name, frame):
    try:
        with open("tasks.json", "r") as file:
            data = json.load(file)

        data.pop(task_name, None)

        with open("tasks.json", "w") as file:
            json.dump(data, file, indent=4)
        
        # Directly remove the task from the frame
        for widget in frame.winfo_children():
            if task_name in widget.cget("text"):
                widget.destroy()
                break
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    update_tasks(frame)
def load_tasks():
    if os.path.exists("tasks.json"):
        try:
            with open("tasks.json", "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}
    return {}

def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

def update_tasks(task_list_frame):
    for widget in task_list_frame.winfo_children():
        widget.destroy()  # Clear existing task labels

    tasks = load_tasks()
    colors = load_button_colors()

    for i, (task, description) in enumerate(tasks.items()):
        # Task label
        task_label = tk.Label(task_list_frame,
                              text=f"{task}: {description}",
                              bg='BLACK',
                              fg='WHITE',
                              font=("Arial", 14))
        task_label.grid(row=i, column=0, sticky="w", padx=5, pady=5)  # Align left

        # Clear button
        clear_button = tk.Button(task_list_frame,
                                 text="DEL",
                                 bg='BLACK',
                                 fg='RED',
                                 font=("Arial", 16, 'bold'),
                                 command=lambda t=task: clear_task(t, task_list_frame))
        clear_button.grid(row=i, column=1, sticky="e", padx=5, pady=5)  # Align right

        # Check button
        check_button = tk.Button(task_list_frame,
                                 text="✔",
                                 bg=colors.get(task, 'BLACK'),
                                 fg='GREEN' if colors.get(task, 'BLACK') == 'BLACK' else 'BLACK',
                                 font=("Arial", 16, 'bold'))
        check_button.grid(row=i, column=2, sticky="e", padx=5, pady=5)
        
        check_button.config(command=lambda b=check_button, t=task: change_color(b, t))

def add_task(task_list_frame):
    def submit_task():
        task_text = text.get("1.0", tk.END).strip()
        if task_text:
            try:
                task, description = task_text.split(": ", 1)
            except ValueError:
                task = task_text
                description = ""
            
            tasks = load_tasks()
            tasks[task] = description
            save_tasks(tasks)
            update_tasks(task_list_frame)  # Refresh the tasks list
            add_window.destroy()  # Close the add task window
    
    add_window = tk.Toplevel()  # Use Toplevel instead of Tk for additional windows
    add_window.geometry('300x400')
    add_window.resizable(width=False, height=False)
    
    label = tk.Label(add_window, text="Enter the task and description like Task 1: do something")
    label.pack(pady=10)
    
    text = tk.Text(add_window, height=5, width=40)
    text.pack(pady=10)
    
    button = tk.Button(add_window,
                       background='#4DB6AC',
                       foreground='WHITE',
                       activebackground='#80CBC4',
                       activeforeground='WHITE',
                       highlightthickness=2,
                       highlightbackground='#009688',
                       highlightcolor='BLACK',
                       width=20,
                       height=2,
                       border=0,
                       cursor='hand1',
                       text='Submit',
                       font=('Arial', 16, 'bold'),
                       command=submit_task)
    button.pack(pady=20)

def my_tasks():
    tasks_window = tk.Tk()  # Use Toplevel for additional windows
    tasks_window.attributes('-fullscreen', True)
    tasks_window.geometry('600x600')
    tasks_window.resizable(width=True, height=True)
    
    def toggle_fullscreen(event=None):
        tasks_window.attributes('-fullscreen', not tasks_window.attributes('-fullscreen'))
        return "break"

    tasks_window.bind("<F11>", toggle_fullscreen)
    tasks_window.bind("<Escape>", lambda e: tasks_window.attributes('-fullscreen', False))
    
    main_frame = tk.Frame(tasks_window, bg='BLACK')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Top bar frame
    top_frame = tk.Frame(main_frame, bg='#4DB6AC', height=80)
    top_frame.pack(fill=tk.X, side=tk.TOP)
    
    label = tk.Label(top_frame,
                     fg='WHITE',
                     bg='#4DB6AC',
                     text="Your Tasks",
                     font=("Arial", 20, "bold"))
    label.pack(pady=20)
    
    # Button to add a task
    add_button = tk.Button(top_frame,
                           background='#4DB6AC',
                           foreground='WHITE',
                           activebackground='#80CBC4',
                           activeforeground='WHITE',
                           highlightthickness=2,
                           highlightbackground='#009688',
                           highlightcolor='BLACK',
                           width=20,
                           height=2,
                           border=0,
                           cursor='hand1',
                           text='+',
                           font=('Arial', 16, 'bold'),
                           command=lambda: add_task(task_list_frame))
    add_button.place(relx=0.95, rely=0.5, anchor="center")
    
    # Content area
    content_frame = tk.Frame(main_frame, bg='BLACK')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Separate frame for task list (to avoid clearing the back button)
    task_list_frame = tk.Frame(content_frame, bg='BLACK')
    task_list_frame.pack(fill=tk.BOTH, expand=True)

    update_tasks(task_list_frame)  # Load and display tasks
    
    # Button to go back to the menu (outside the task_list_frame so it's not cleared)
    back_button = tk.Button(content_frame,
                            text="Back to Menu",
                            command=lambda: [tasks_window.destroy(), menu()],
                            bg='#4DB6AC',
                            fg='WHITE',
                            font=("Arial", 12, "bold"),
                            width=20)
    back_button.pack(pady=20)

def menu():
    global root
    
 
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.geometry('600x600')
    root.resizable(width=True, height=True)
    
    def toggle_fullscreen(event=None):
        root.attributes('-fullscreen', not root.attributes('-fullscreen'))
        return "break"

    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", lambda e: root.attributes('-fullscreen', False))
    
    main_frame = tk.Frame(root, bg='BLACK')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    my_tasks_button = tk.Button(
        main_frame,
        background='#4DB6AC',
        foreground='WHITE',
        activebackground='#80CBC4',
        activeforeground='WHITE',
        highlightthickness=2,
        highlightbackground='#009688',
        highlightcolor='BLACK',
        width=20,
        height=2,
        border=0,
        cursor='hand1',
        text='My Tasks',
        font=('Arial', 16, 'bold'),
        command=open_my_tasks
    )
    my_tasks_button.place(relx=0.5, rely=0.4, anchor="center")
    
    exit_button = tk.Button(
        main_frame,
        background='#4DB6AC',
        foreground='WHITE',
        activebackground='#80CBC4',
        activeforeground='WHITE',
        highlightthickness=2,
        highlightbackground='#009688',
        highlightcolor='BLACK',
        width=20,
        height=2,
        border=0,
        cursor='hand1',
        text='Exit',
        font=('Arial', 16, 'bold'),
        command=root.destroy
    )
    exit_button.place(relx=0.5, rely=0.6, anchor="center")
    
    root.mainloop()

def open_my_tasks():
    global root
    root.destroy()  # Close the menu window
    my_tasks()      # Open the tasks window

menu()
