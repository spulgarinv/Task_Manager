import tkinter as tk
from tkinter import ttk
import process as ps
import time

class Task_Manager():

    def __init__(self, root):
        self.root = root
        self.wrapper1 = tk.LabelFrame(self.root)
        self.wrapper1.pack(fill='both', expand='yes', padx=20, pady=10)
        self.label = tk.Label(self.wrapper1, text='List of processes', fg='black', font='Times 20')
        self.label.pack()
        self.table = ttk.Treeview(self.wrapper1, columns=(1,2,3,4), show='headings', height='50')
        self.table.heading(1, text = "PID")
        self.table.heading(2, text = "NAME")
        self.table.heading(3, text = "% MEMORY")
        self.table.heading(4, text = "% PROCESSOR")
        self.table.pack(side='left')
        self.menu = tk.Menu(root, tearoff=0)
        self.menu.add_command(label="Kill")
        self.table.bind("<Button-3>", self.kill_process)
        self.yscrollbar = ttk.Scrollbar(self.wrapper1, orient='vertical', command=self.table.yview)
        self.yscrollbar.pack(side="right", fill="y")
        self.table.configure(yscrollcommand=self.yscrollbar.set)
        self.list_processes()

    def list_processes(self):
        r_processes = ps.get_current_processes()
        for x in r_processes:
            self.table.insert('', 'end', values=(x, r_processes[x]['name'],round(r_processes[x]['memory_percent'],1),r_processes[x]['cpu_percent']))
        self.root.after(5000, self.refresh)

    def kill_process(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
            curItem = self.table.focus()
            pid = self.table.item(curItem)['values'][0]
            ps.kill_process(pid)
            self.table.delete(curItem)
        finally:
            self.menu.grab_release()

    def refresh(self):
        for row in self.table.get_children():
            self.table.delete(row)
        self.list_processes()

if __name__== "__main__":
    root = tk.Tk()
    root.title('Task Manager')
    root.geometry('900x700')
    root.resizable(False, False)
    app = Task_Manager(root)
    root.mainloop()