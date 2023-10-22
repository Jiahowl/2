import tkinter as tk
import sqlite3

# Connect to the database
conn = sqlite3.connect('calculator_history.db')
cursor = conn.cursor()

# Create a table to store calculation history if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    expression TEXT,
                    result TEXT
                );''')
conn.commit()

def button_click(value):
    current = result.get()
    result.delete(0, tk.END)
    result.insert(tk.END, current + value)

def calculate_result():
    try:
        expression = result.get()
        result.delete(0, tk.END)
        result_str = str(eval(expression))
        result.insert(tk.END, result_str)
        
        # Save the calculation to the database
        cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?);", (expression, result_str))
        conn.commit()
    except Exception as e:
        result.delete(0, tk.END)
        result.insert(tk.END, "Error")

def clear_result():
    result.delete(0, tk.END)

def retrieve_history():
    cursor.execute("SELECT expression, result FROM history ORDER BY id DESC LIMIT 10;")
    rows = cursor.fetchall()
    history_window = tk.Toplevel(window)
    history_window.title("History")
    if not rows:
        tk.Label(history_window, text="No history available.").pack()
    else:
        for row in rows:
            expression, result_value = row
            history_text = f"Expression: {expression}\nResult: {result_value}"
            tk.Label(history_window, text=history_text).pack()

def button_click(value):
    current = result.get()
    if value == "ans":
        # Retrieve the last calculation result from the database
        cursor.execute("SELECT result FROM history ORDER BY id DESC LIMIT 1;")
        row = cursor.fetchone()
        if row:
            result_str = row[0]
            result.delete(0, tk.END)
            result.insert(tk.END, result_str)
    else:
        result.delete(0, tk.END)
        result.insert(tk.END, current + value)

# Create the main window
window = tk.Tk()
window.title("Calculator")

# Create the display
result = tk.Entry(window, width=30)
result.grid(row=0, column=0, columnspan=4)

# Create the buttons
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+",
    "%", "ans"
]

row = 1
col = 0
for button in buttons:
    if button == "=":
        tk.Button(window, text=button, command=calculate_result, width=5).grid(row=row, column=col)
    else:
        tk.Button(window, text=button, command=lambda value=button: button_click(value), width=5).grid(row=row, column=col)
    col += 1
    if col > 3:
        col = 0
        row += 1

tk.Button(window, text="C", command=clear_result, width=5).grid(row=row, column=col)
tk.Button(window, text="History", command=retrieve_history, width=10).grid(row=row+1, column=col-1, columnspan=2)

# Start the main loop
window.mainloop()

# Close the database connection
conn.close()
