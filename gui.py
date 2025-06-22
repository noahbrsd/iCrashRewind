import tkinter as tk
from tkinter import ttk
from utils import format_time

class IncidentGUI:
    def __init__(self, root, replay_callback):
        self.replay_callback = replay_callback
        self.tree = ttk.Treeview(root, columns=('car', 'name', 'time', 'type', 'action'), show='headings')
        self.tree.heading('car', text='#')
        self.tree.heading('name', text='Driver')
        self.tree.heading('time', text='Time')
        self.tree.heading('type', text='Type')
        self.tree.heading('action', text='Replay')

        self.tree.pack(fill='both', expand=True)
        self.tree.bind("<Double-1>", self.on_double_click)

    def add_incident(self, incident):
        self.tree.insert('', 'end', values=(
            incident['car_idx'],
            incident['driver_name'],
            format_time(incident['time']),
            incident['type'],
            '▶️ Replay'
        ))

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        car_idx = int(values[0])
        time_str = values[2]
        self.replay_callback(car_idx, time_str)



