import tkinter as tk
from tkinter import ttk, messagebox
import os
import json
import calendar

##############################################################################
# BACKEND - Core functionality and data management
##############################################################################

# Configuration constants
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
PLANS_DIR = os.path.join(os.path.dirname(__file__), "plans")

# Ensure directories exist
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(PLANS_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(CONFIG_DIR, "config.txt")

DEFAULT_CLASS_NAMES = {
    "A": "Class 1",
    "B": "Class 2", 
    "C": "Class 3",
    "D": "Class 4"
}

def get_class_names():
    """Load class names from config file or use defaults"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        else:
            # If file doesn't exist, create with default names
            save_class_names(DEFAULT_CLASS_NAMES)
            return DEFAULT_CLASS_NAMES
    except Exception as e:
        print(f"Error loading class names: {e}")
        return DEFAULT_CLASS_NAMES

def save_class_names(class_names):
    """Save class names to config file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(class_names, f, indent=4)
    except Exception as e:
        print(f"Error saving class names: {e}")

def save_plans(class_name, plans):
    """Save plans to appropriate text file"""
    # Get class key (A, B, C, D) from the class name
    class_key = None
    class_names = get_class_names()
    for key, name in class_names.items():
        if name == class_name:
            class_key = key.lower()
            break
    
    if not class_key:
        print(f"Error: Could not find key for {class_name}")
        return
    
    file_path = os.path.join(PLANS_DIR, f"class{class_key}.txt")
    
    try:
        with open(file_path, 'w') as f:
            for plan in plans:
                f.write(f"{plan}\n")
    except Exception as e:
        print(f"Error saving plans: {e}")

def load_plans(class_name):
    """Load plans from appropriate text file"""
    # Get class key (A, B, C, D) from the class name
    class_key = None
    class_names = get_class_names()
    for key, name in class_names.items():
        if name == class_name:
            class_key = key.lower()
            break
    
    if not class_key:
        print(f"Error: Could not find key for {class_name}")
        return []
    
    file_path = os.path.join(PLANS_DIR, f"class{class_key}.txt")
    plans = []
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:  # Skip empty lines
                        plans.append(line)
    except Exception as e:
        print(f"Error loading plans: {e}")
    
    return plans

def validate_date(day, month):
    """Validate if the date is valid"""
    if not day or not month:  # Empty values are ok (optional field)
        return True
    
    try:
        day = int(day)
        month = int(month)
        
        # Check month range
        if month < 1 or month > 12:
            return False
        
        # Check day range based on month
        max_days = calendar.monthrange(2025, month)[1]  # Using current year
        if day < 1 or day > max_days:
            return False
        
        return True
    except ValueError:
        return False

def validate_time(hour, minute):
    """Validate if the time is valid"""
    if not hour or not minute:  # Empty values are ok (optional field)
        return True
    
    try:
        hour = int(hour)
        minute = int(minute)
        
        # Check hour and minute ranges
        if hour < 0 or hour > 23:
            return False
        if minute < 0 or minute > 59:
            return False
        
        return True
    except ValueError:
        return False


##############################################################################
# FRONTEND - User interfaces (Terminal and GUI)
##############################################################################

# Terminal UI functions
def print_todo_header(class_names):
    """Display the main terminal interface header"""
    print("+-------------------------------------+")
    print("|  _____  ___  ____   ___      __     |")
    print("| |_   _|/ _ \\|  _ \\ / _ \\    |  |    |")
    print("|   | | | | | | | | | | | |   |  |    |")
    print("|   | | | |_| | |_| | |_| |   |__|    |")
    print("|   |_|  \\___/|____/ \\___/    |__|    |")
    print("|                                     |")
    print(f"|   [A] {class_names['A']:<30}|")
    print(f"|   [B] {class_names['B']:<30}|")
    print(f"|   [C] {class_names['C']:<30}|")
    print(f"|   [D] {class_names['D']:<30}|")
    print("|   [E] Edit Class Names              |")
    print("|   [X] Exit Program                  |")
    print("|                                     |")
    print("+-------------------------------------+")

def edit_class_names(class_names):
    """Terminal interface for editing class names"""
    print("\n+-------------------------------------+")
    print("|          EDIT CLASS NAMES           |")
    print("+-------------------------------------+")
    print(f"| [A] {class_names['A']:<32}|")
    print(f"| [B] {class_names['B']:<32}|")
    print(f"| [C] {class_names['C']:<32}|")
    print(f"| [D] {class_names['D']:<32}|")
    print("| [X] Return to Main Menu             |")
    print("+-------------------------------------+")
    
    choice = input("Enter class to rename: ").upper()
    
    if choice in ['A', 'B', 'C', 'D']:
        new_name = input(f"Enter new name for {class_names[choice]}: ").strip()
        if new_name:
            class_names[choice] = new_name
            save_class_names(class_names)
            print(f"Class name updated to: {new_name}")
        else:
            print("Name cannot be empty. No changes made.")
    elif choice == 'X':
        return
    else:
        print("Invalid choice")
    
    input("Press Enter to continue...")

# GUI Functions
def open_class_window(class_name, root):
    """Create and display a class plan window with Tkinter"""
    # Create a new window as a Toplevel window
    window = tk.Toplevel(root)
    window.title(class_name)
    window.geometry("600x500")  # Increased window size
    
    # Add a label with the class name
    label = tk.Label(window, text=f"{class_name} Plans", font=("Arial", 16))
    label.pack(pady=10)
    
    # Frame for input elements at the top
    input_frame = tk.Frame(window)
    input_frame.pack(fill="x", padx=20, pady=10)
    
    # Plan description
    desc_label = tk.Label(input_frame, text="Plan Description:")
    desc_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    desc_entry = tk.Text(input_frame, height=3, width=40)
    desc_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    # Due date frame
    date_frame = tk.Frame(input_frame)
    date_frame.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    date_label = tk.Label(input_frame, text="Due Date (Optional):")
    date_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    
    # Day input
    day_entry = tk.Entry(date_frame, width=3)
    day_entry.pack(side="left", padx=2)
    tk.Label(date_frame, text="/").pack(side="left")
    
    # Month input
    month_entry = tk.Entry(date_frame, width=3)
    month_entry.pack(side="left", padx=2)
    
    # Time frame
    time_frame = tk.Frame(input_frame)
    time_frame.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    
    time_label = tk.Label(input_frame, text="Time (Optional):")
    time_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
    
    # Hour input
    hour_entry = tk.Entry(time_frame, width=3)
    hour_entry.pack(side="left", padx=2)
    tk.Label(time_frame, text=":").pack(side="left")
    
    # Minute input
    minute_entry = tk.Entry(time_frame, width=3)
    minute_entry.pack(side="left", padx=2)
    
    # Add placeholder text functionality
    def add_placeholder(entry, placeholder):
        """Add gray placeholder text to entry fields"""
        entry.insert(0, placeholder)
        entry.config(fg='gray')
        
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")
                entry.config(fg='black')
        
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg='gray')
                
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    
    # Add placeholder text to all entry fields
    add_placeholder(day_entry, "dd")
    add_placeholder(month_entry, "mm")
    add_placeholder(hour_entry, "hh")
    add_placeholder(minute_entry, "mm")
    
    # Frame for buttons
    button_frame = tk.Frame(window)
    button_frame.pack(fill="x", padx=20, pady=10)
    
    # Variable to track the currently selected plan and its index
    selected_plan = {"index": None, "text": None}
    
    # Function to clear input fields - update to handle placeholders
    def clear_inputs():
        """Reset all input fields to empty with placeholders"""
        desc_entry.delete("1.0", "end")
        
        # Clear and reset placeholders
        day_entry.delete(0, "end")
        month_entry.delete(0, "end")
        hour_entry.delete(0, "end")
        minute_entry.delete(0, "end")
        
        add_placeholder(day_entry, "dd")
        add_placeholder(month_entry, "mm")
        add_placeholder(hour_entry, "hh")
        add_placeholder(minute_entry, "mm")
        
        # Reset selection
        selected_plan["index"] = None
        selected_plan["text"] = None
        
        # Update button states
        edit_button.config(state="disabled")
        delete_button.config(state="disabled")
        add_button.config(text="Add Plan")
    
    # Function to handle plan selection
    def on_plan_select(event):
        """Handle plan selection from listbox"""
        try:
            # Get selected index
            current_selection = plan_listbox.curselection()
            
            if not current_selection:  # No selection
                return
                
            index = current_selection[0]
            text = plan_listbox.get(index)
            
            # Check if clicking already selected item (toggle selection)
            if selected_plan["index"] == index:
                # Unselect the item
                plan_listbox.selection_clear(0, tk.END)
                selected_plan["index"] = None
                selected_plan["text"] = None
                # Disable buttons
                edit_button.config(state="disabled")
                delete_button.config(state="disabled")
                return
            
            # Update selected plan
            selected_plan["index"] = index
            selected_plan["text"] = text
            
            # Enable edit and delete buttons
            edit_button.config(state="normal")
            delete_button.config(state="normal")
        except IndexError:
            # No selection
            pass
    
    # Function to add or update a plan
    def add_plan():
        """Add a new plan or update an existing one"""
        description = desc_entry.get("1.0", "end-1c").strip()
        if not description:
            messagebox.showwarning("Warning", "Please enter a plan description")
            return
            
        # Get values, ignoring placeholders
        day = day_entry.get().strip()
        if day == "dd": day = ""
        
        month = month_entry.get().strip()
        if month == "mm": month = ""
        
        hour = hour_entry.get().strip()
        if hour == "hh": hour = ""
        
        minute = minute_entry.get().strip()
        if minute == "mm": minute = ""
        
        # Validate date if provided
        if (day or month) and not validate_date(day, month):
            messagebox.showerror("Invalid Date", "Please enter a valid date (DD/MM)")
            return
            
        # Validate time if provided
        if (hour or minute) and not validate_time(hour, minute):
            messagebox.showerror("Invalid Time", "Please enter a valid time (HH:MM, 24-hour format)")
            return
        
        # Build the plan text
        date_time_str = ""
        if day and month:
            date_time_str += f" | Due: {day}/{month}"
        if hour and minute:
            date_time_str += f" | Time: {hour}:{minute}"
        
        # Preserve multiline text with proper formatting
        description_lines = description.split("\n")
        description_formatted = " ".join(description_lines)
            
        plan_text = f"{description_formatted}{date_time_str}"
        
        updating = selected_plan["index"] is not None and add_button.cget("text") == "Update Plan"
        
        if updating:
            # Only update if we're explicitly in update mode
            index = selected_plan["index"]
            plan_listbox.delete(index)
            plan_listbox.insert(index, plan_text)
            # Ensure it remains selected after updating
            plan_listbox.select_set(index)
            messagebox.showinfo("Success", "Plan updated successfully")
        else:
            # Add new plan at the end
            plan_listbox.insert(tk.END, plan_text)
            messagebox.showinfo("Success", "Plan added successfully")
            
        clear_inputs()
    
    # Function to edit a selected plan
    def edit_plan():
        """Edit the selected plan"""
        if selected_plan["index"] is None:
            messagebox.showwarning("Warning", "Please select a plan to edit")
            return
        
        plan_text = selected_plan["text"]
        
        # Extract description and optional date/time
        parts = plan_text.split(" | ")
        description = parts[0]
        
        # Clear previous inputs and placeholders
        desc_entry.delete("1.0", "end")
        day_entry.delete(0, "end")
        month_entry.delete(0, "end")
        hour_entry.delete(0, "end")
        minute_entry.delete(0, "end")
        
        # Reset foreground color for entries
        day_entry.config(fg='black')
        month_entry.config(fg='black')
        hour_entry.config(fg='black')
        minute_entry.config(fg='black')
        
        # Set description
        desc_entry.insert("1.0", description)
        
        # Set date and time if present
        for part in parts[1:]:
            if part.startswith("Due:"):
                date_str = part.replace("Due:", "").strip()
                day_month = date_str.split("/")
                if len(day_month) == 2:
                    day_entry.insert(0, day_month[0])
                    month_entry.insert(0, day_month[1])
            
            if part.startswith("Time:"):
                time_str = part.replace("Time:", "").strip()
                hour_minute = time_str.split(":")
                if len(hour_minute) == 2:
                    hour_entry.insert(0, hour_minute[0])
                    minute_entry.insert(0, hour_minute[1])
        
        # If any field is still empty, add placeholder
        if not day_entry.get():
            add_placeholder(day_entry, "dd")
        if not month_entry.get():
            add_placeholder(month_entry, "mm")
        if not hour_entry.get():
            add_placeholder(hour_entry, "hh")
        if not minute_entry.get():
            add_placeholder(minute_entry, "mm")
        
        # Update button text to indicate we're updating
        add_button.config(text="Update Plan")
        
        # Keep track of the plan being edited
        selected_plan["text"] = plan_text
        selected_plan["index"] = plan_listbox.curselection()[0]
    
    # Function to delete a selected plan
    def delete_plan():
        """Delete the selected plan"""
        if selected_plan["index"] is None:
            messagebox.showwarning("Warning", "Please select a plan to delete")
            return
        
        # Ask for confirmation
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this plan?")
        if confirm:
            plan_listbox.delete(selected_plan["index"])
            clear_inputs()
            messagebox.showinfo("Success", "Plan deleted successfully")
    
    # Function to save plans when window is closed
    def on_window_close():
        """Save plans and close the window"""
        # Get all plans from the listbox
        plans = [plan_listbox.get(i) for i in range(plan_listbox.size())]
        # Save plans to file
        save_plans(class_name, plans)
        # Close the window
        window.destroy()
    
    # Add, Edit, Delete buttons
    add_button = tk.Button(button_frame, text="Add Plan", command=add_plan, width=15)
    add_button.pack(side="left", padx=10)
    
    edit_button = tk.Button(button_frame, text="Edit Plan", command=edit_plan, width=15, state="disabled")
    edit_button.pack(side="left", padx=10)
    
    delete_button = tk.Button(button_frame, text="Delete Plan", command=delete_plan, width=15, state="disabled")
    delete_button.pack(side="left", padx=10)
    
    # Listbox to display plans
    plan_frame = tk.Frame(window)
    plan_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    plan_listbox = tk.Listbox(plan_frame, font=("Arial", 12), height=10)
    plan_listbox.pack(side="left", fill="both", expand=True)
    plan_listbox.bind('<<ListboxSelect>>', on_plan_select)
    
    # Add scrollbar to listbox
    scrollbar = tk.Scrollbar(plan_frame)
    scrollbar.pack(side="right", fill="y")
    
    # Connect scrollbar to listbox
    plan_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=plan_listbox.yview)
    
    # Load saved plans
    saved_plans = load_plans(class_name)
    for plan in saved_plans:
        plan_listbox.insert("end", plan)
    
    # Close button at the bottom
    close_button = tk.Button(window, text="Close Window", command=on_window_close, width=15)
    close_button.pack(pady=10)
    
    # Bind the close window event to our custom handler
    window.protocol("WM_DELETE_WINDOW", on_window_close)

def main():
    """Main program entry point"""
    # Load class names from config
    class_names = get_class_names()
    
    # Create a hidden root window that manages the application
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    running = True
    while running:
        # Reload class names in case they were edited
        class_names = get_class_names()
        print_todo_header(class_names)
        
        # Get user input
        user_command = input("Enter command here: ")
        
        # Process commands
        if user_command.upper() == 'A':
            open_class_window(class_names['A'], root)
        elif user_command.upper() == 'B':
            open_class_window(class_names['B'], root)
        elif user_command.upper() == 'C':
            open_class_window(class_names['C'], root)
        elif user_command.upper() == 'D':
            open_class_window(class_names['D'], root)
        elif user_command.upper() == 'E':
            edit_class_names(class_names)
        elif user_command.upper() == 'X':
            print("Exiting program...")
            running = False
            root.destroy()
        else:
            print("Invalid command")
            input("Press Enter to continue...")  # Pause to show the error message
        
        # Update the root window to process any pending events
        if running:
            root.update()

# This will run when the program starts
if __name__ == "__main__":
    main()