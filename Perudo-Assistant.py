import tkinter as tk
from tkinter import ttk

def binomial_coefficient(n, k):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)
    c = 1
    for i in range(k):
        c = c * (n - i) // (i + 1)
    return c

def calculate_binomial_probability(n, p, k):
    return binomial_coefficient(n, k) * (p ** k) * ((1 - p) ** (n - k))

class PerudoCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Perudo Assistant")
        
        # Setup variables
        self.num_opponents = tk.IntVar(value=3)
        self.total_dice = tk.IntVar(value=20)
        self.bid_quantity = tk.IntVar(value=1)
        self.bid_face = tk.IntVar(value=1)
        self.probability = tk.StringVar(value="Probability will appear here")
        self.suspected_probability = tk.StringVar(value="Suspected probability will appear here")
        self.your_dice_vars = []
        self.opponent_dice_vars = []
        self.opponent_suspected_vars = []
        self.allow_more_players = tk.BooleanVar(value=False)
        
        self.create_widgets()
        self.create_opponent_inputs()
        self.create_your_dice_inputs()
        self.update_total_dice()
        
        # Set up automatic calculation triggers
        self.setup_automatic_calculation()
        
        # Make window resizable and set minimum size
        self.root.minsize(900, 600)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def setup_automatic_calculation(self):
        self.num_opponents.trace_add("write", lambda *args: self.update_opponents())
        self.bid_quantity.trace_add("write", lambda *args: self.calculate_probability())
        self.bid_face.trace_add("write", lambda *args: self.calculate_probability())
        self.allow_more_players.trace_add("write", lambda *args: self.on_allow_more_players_changed())
        
        for var in self.opponent_dice_vars:
            var.trace_add("write", lambda *args: self.update_total_dice())
        
        for var in self.your_dice_vars:
            var.trace_add("write", lambda *args: self.update_total_dice())
    
    def create_widgets(self):
        style = ttk.Style()
        style.configure("TFrame", padding=10)
        style.configure("TLabel", padding=5)
        style.configure("TButton", padding=5)
        
        # Make main frame expandable
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        reset_frame = ttk.Frame(main_frame)
        reset_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        
        ttk.Button(reset_frame, text="Reset Table", 
                  command=self.reset_table).pack(side=tk.RIGHT)
        
        players_frame = ttk.LabelFrame(main_frame, text="Player Configuration")
        players_frame.grid(row=1, column=0, sticky="ew", pady=5)
        players_frame.columnconfigure(0, weight=1)
        
        players_row = ttk.Frame(players_frame)
        players_row.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        ttk.Label(players_row, text="Number of Opponents:").pack(side=tk.LEFT, padx=(0, 5))
        self.opponent_count_label = ttk.Label(players_row, text="3")
        self.opponent_count_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(players_row, text="+", width=3, 
                  command=lambda: self.change_opponents(1)).pack(side=tk.LEFT, padx=5)
        ttk.Button(players_row, text="-", width=3, 
                  command=lambda: self.change_opponents(-1)).pack(side=tk.LEFT, padx=5)
        
        ttk.Checkbutton(players_row, text="Allow >5 players", 
                      variable=self.allow_more_players).pack(side=tk.LEFT, padx=10)
        
        self.opponent_frame = ttk.Frame(players_frame)
        self.opponent_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.opponent_frame.columnconfigure(0, weight=1)
        
        total_row = ttk.Frame(players_frame)
        total_row.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Label(total_row, text="Total Dice on Table:").pack(side=tk.LEFT)
        ttk.Label(total_row, textvariable=self.total_dice).pack(side=tk.LEFT, padx=5)
        
        bid_frame = ttk.LabelFrame(main_frame, text="Bid Information")
        bid_frame.grid(row=2, column=0, sticky="ew", pady=5)
        bid_frame.columnconfigure(0, weight=1)
        
        bid_row = ttk.Frame(bid_frame)
        bid_row.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        ttk.Label(bid_row, text="Bid Quantity:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Spinbox(bid_row, from_=1, to=50, textvariable=self.bid_quantity, 
                   width=5).pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(bid_row, text="Bid Face (1-6):").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Spinbox(bid_row, from_=1, to=6, textvariable=self.bid_face, 
                   width=5).pack(side=tk.LEFT)
        
        your_dice_container = ttk.LabelFrame(main_frame, text="Your Dice")
        your_dice_container.grid(row=3, column=0, sticky="ew", pady=5)
        your_dice_container.columnconfigure(0, weight=1)
        
        button_frame = ttk.Frame(your_dice_container)
        button_frame.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))
        
        self.add_die_btn = ttk.Button(button_frame, text="Add Die", 
                  command=self.add_die)
        self.add_die_btn.pack(side=tk.LEFT, padx=5)
        
        self.remove_die_btn = ttk.Button(button_frame, text="Remove Die", 
                  command=self.remove_die, state=tk.DISABLED)
        self.remove_die_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_dice_btn = ttk.Button(button_frame, text="Reset Dice", 
                  command=self.reset_your_dice_to_ones)
        self.reset_dice_btn.pack(side=tk.LEFT, padx=5)
        
        self.your_dice_frame = ttk.Frame(your_dice_container)
        self.your_dice_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # Result displays
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=4, column=0, sticky="w", pady=10)
        
        ttk.Label(result_frame, text="Probability (Your Dice Only):").pack(side=tk.LEFT)
        probability_label = ttk.Label(result_frame, textvariable=self.probability, 
                                    font=("Arial", 10, "bold"), foreground="blue")
        probability_label.pack(side=tk.LEFT, padx=10)
        
        suspected_frame = ttk.Frame(main_frame)
        suspected_frame.grid(row=5, column=0, sticky="w", pady=5)
        
        ttk.Label(suspected_frame, text="Probability (With Suspected Dice):").pack(side=tk.LEFT)
        suspected_label = ttk.Label(suspected_frame, textvariable=self.suspected_probability, 
                                   font=("Arial", 10, "bold"), foreground="green")
        suspected_label.pack(side=tk.LEFT, padx=10)
    
    def create_opponent_inputs(self):
        # Preserve existing suspected dice
        current_suspected = self.opponent_suspected_vars.copy()
        self.opponent_suspected_vars = []
        
        for widget in self.opponent_frame.winfo_children():
            widget.destroy()
        self.opponent_dice_vars = []
        
        opponents_container = ttk.Frame(self.opponent_frame)
        opponents_container.grid(row=0, column=0, sticky="w")
        
        ttk.Label(opponents_container, text="Dice per Opponent:").pack(side=tk.LEFT, padx=(0, 10))
        
        opponents_dice_frame = ttk.Frame(opponents_container)
        opponents_dice_frame.pack(side=tk.LEFT)
        
        for i in range(self.num_opponents.get()):
            opp_container = ttk.Frame(opponents_dice_frame)
            opp_container.pack(side=tk.LEFT, padx=5)
            
            opp_row = ttk.Frame(opp_container)
            opp_row.pack()
            
            ttk.Label(opp_row, text=f"P{i+1}:").pack(side=tk.LEFT)
            opp_var = tk.IntVar(value=5)
            spin = ttk.Spinbox(opp_row, from_=1, to=10, textvariable=opp_var, 
                              width=3)
            spin.pack(side=tk.LEFT, padx=(0, 10))
            self.opponent_dice_vars.append(opp_var)
            
            suspected_frame = ttk.Frame(opp_container)
            suspected_frame.pack(fill=tk.X, pady=(2, 0))
            
            ttk.Label(suspected_frame, text="Suspected:").pack(side=tk.LEFT)
            
            self.suspected_dice_frame = ttk.Frame(suspected_frame)
            self.suspected_dice_frame.pack(side=tk.LEFT, padx=5)
            
            # Preserve suspected dice for existing opponents
            if i < len(current_suspected):
                self.opponent_suspected_vars.append(current_suspected[i])
                self.update_suspected_display(i)
            else:
                self.opponent_suspected_vars.append([])
            
            # Button frame for suspected actions
            button_frame = ttk.Frame(opp_container)
            button_frame.pack(fill=tk.X, pady=(5, 0))
            
            ttk.Button(button_frame, text="Set Suspected", 
                      command=lambda idx=i: self.set_suspected_dice(idx)).pack(side=tk.LEFT, padx=2)
            
            # Clear suspicion button
            ttk.Button(button_frame, text="Clear", 
                      command=lambda idx=i: self.clear_suspected_dice(idx)).pack(side=tk.LEFT, padx=2)
    
    def create_your_dice_inputs(self):
        for widget in self.your_dice_frame.winfo_children():
            widget.destroy()
        self.your_dice_vars = []
        
        for _ in range(5):
            self.add_die("1")
    
    def reset_your_dice_to_ones(self):
        for widget in self.your_dice_frame.winfo_children():
            widget.destroy()
        self.your_dice_vars = []
        
        for _ in range(5):
            self.add_die("1")
        
        self.update_total_dice()
        self.calculate_probability()
    
    def add_die(self, initial_value=""):
        if len(self.your_dice_vars) >= 5:
            self.add_die_btn.config(state=tk.DISABLED)
            return
            
        die_var = tk.StringVar(value=initial_value)
        self.your_dice_vars.append(die_var)
        
        die_frame = ttk.Frame(self.your_dice_frame)
        die_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        die_number = len(self.your_dice_vars)
        ttk.Label(die_frame, text=f"Die {die_number}:").pack()
        
        die_combobox = ttk.Combobox(die_frame, textvariable=die_var, 
                                  values=["", "1", "2", "3", "4", "5", "6"], 
                                  width=4, state="normal")
        die_combobox.pack()
        
        die_combobox.bind('<KeyRelease>', lambda e: self.validate_die_input(e, die_var))
        die_combobox.bind('<FocusOut>', lambda e: self.validate_die_input(e, die_var))
        
        die_var.trace_add("write", lambda *args: self.update_total_dice())
        
        self.update_dice_button_states()
        self.update_total_dice()
    
    def validate_die_input(self, event, die_var):
        value = die_var.get()
        if value not in ["", "1", "2", "3", "4", "5", "6"]:
            die_var.set("")
    
    def remove_die(self):
        if len(self.your_dice_vars) <= 1:
            self.remove_die_btn.config(state=tk.DISABLED)
            return
            
        self.your_dice_vars.pop()
        last_widget = self.your_dice_frame.winfo_children()[-1]
        last_widget.destroy()
        
        self.renumber_dice()
        self.update_dice_button_states()
        self.update_total_dice()
    
    def update_dice_button_states(self):
        dice_count = len(self.your_dice_vars)
        self.add_die_btn.config(state=tk.NORMAL if dice_count < 5 else tk.DISABLED)
        self.remove_die_btn.config(state=tk.NORMAL if dice_count > 1 else tk.DISABLED)
    
    def renumber_dice(self):
        widgets = self.your_dice_frame.winfo_children()
        for i, widget in enumerate(widgets):
            label = widget.winfo_children()[0]
            label.config(text=f"Die {i+1}:")
    
    def change_opponents(self, delta):
        current = self.num_opponents.get()
        max_opponents = 10 if self.allow_more_players.get() else 5
        
        new_value = current + delta
        
        if new_value < 1:
            return
        if new_value > max_opponents:
            return
            
        self.num_opponents.set(new_value)
        self.opponent_count_label.config(text=str(new_value))
    
    def on_allow_more_players_changed(self):
        if not self.allow_more_players.get():
            current = self.num_opponents.get()
            if current > 5:
                self.num_opponents.set(5)
                self.opponent_count_label.config(text="5")
    
    def reset_table(self):
        self.num_opponents.set(3)
        self.opponent_count_label.config(text="3")
        self.create_opponent_inputs()
        self.reset_your_dice_to_ones()
        self.bid_quantity.set(1)
        self.bid_face.set(1)
        self.opponent_suspected_vars = []
        self.update_total_dice()
        self.setup_automatic_calculation()
    
    def reset_your_dice(self):
        self.reset_your_dice_to_ones()
    
    def set_suspected_dice(self, opponent_idx):
        popup = tk.Toplevel(self.root)
        popup.title(f"Set Suspected Dice for Opponent {opponent_idx+1}")
        popup.transient(self.root)
        popup.grab_set()
        
        main_frame = ttk.Frame(popup, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        dice_count = self.opponent_dice_vars[opponent_idx].get()
        
        if len(self.opponent_suspected_vars) <= opponent_idx:
            self.opponent_suspected_vars.append([tk.StringVar(value="") for _ in range(dice_count)])
        else:
            current = self.opponent_suspected_vars[opponent_idx]
            if len(current) < dice_count:
                for _ in range(dice_count - len(current)):
                    current.append(tk.StringVar(value=""))
            elif len(current) > dice_count:
                self.opponent_suspected_vars[opponent_idx] = current[:dice_count]
        
        dice_frame = ttk.Frame(main_frame)
        dice_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(dice_frame, text="Suspected Dice Faces:").pack(anchor=tk.W)
        
        dice_container = ttk.Frame(dice_frame)
        dice_container.pack(fill=tk.X, pady=5)
        
        for i in range(dice_count):
            die_frame = ttk.Frame(dice_container)
            die_frame.pack(side=tk.LEFT, padx=5, pady=5)
            
            ttk.Label(die_frame, text=f"Die {i+1}:").pack()
            
            die_combobox = ttk.Combobox(die_frame, 
                                        textvariable=self.opponent_suspected_vars[opponent_idx][i], 
                                        values=["", "1", "2", "3", "4", "5", "6"], 
                                        width=4, state="normal")
            die_combobox.pack()
            
            die_combobox.bind('<KeyRelease>', 
                             lambda e, var=self.opponent_suspected_vars[opponent_idx][i]: 
                             self.validate_die_input(e, var))
            die_combobox.bind('<FocusOut>', 
                             lambda e, var=self.opponent_suspected_vars[opponent_idx][i]: 
                             self.validate_die_input(e, var))
        
        button_row = ttk.Frame(main_frame)
        button_row.pack(pady=10)
        
        ttk.Button(button_row, text="Save", 
                  command=lambda: [self.save_suspected_dice(popup, opponent_idx), 
                                 self.update_suspected_display(opponent_idx)]).pack(side=tk.LEFT, padx=5)
        
        # Clear button in popup
        ttk.Button(button_row, text="Clear All", 
                  command=lambda: self.clear_suspected_dice(opponent_idx, popup)).pack(side=tk.LEFT, padx=5)
        
        popup.update_idletasks()
        width = max(400, dice_count * 60 + 50)
        height = 200
        popup.geometry(f"{width}x{height}")
    
    # Clear suspected dice for an opponent
    def clear_suspected_dice(self, opponent_idx, popup=None):
        if opponent_idx < len(self.opponent_suspected_vars):
            # Reset all dice to blank
            for die_var in self.opponent_suspected_vars[opponent_idx]:
                die_var.set("")
            
            # Update display
            self.update_suspected_display(opponent_idx)
            
            # Recalculate probability
            self.calculate_probability()
            
            # Close popup if it's open
            if popup:
                popup.destroy()
    
    def update_suspected_display(self, opponent_idx):
        if opponent_idx < len(self.opponent_suspected_vars):
            suspected_list = self.opponent_suspected_vars[opponent_idx]
            
            opponents_container = self.opponent_frame.winfo_children()[0]
            opponents_dice_frame = opponents_container.winfo_children()[1]
            opp_widgets = opponents_dice_frame.winfo_children()
            opp_widget = opp_widgets[opponent_idx]
            
            suspected_frame = opp_widget.winfo_children()[1]
            suspected_dice_frame = suspected_frame.winfo_children()[1]
            
            for widget in suspected_dice_frame.winfo_children():
                widget.destroy()
            
            for i, die_var in enumerate(suspected_list):
                face = die_var.get()
                if face:
                    label = ttk.Label(suspected_dice_frame, text=face, 
                                    background="light yellow", relief="solid", 
                                    width=2, padding=2)
                    label.pack(side=tk.LEFT, padx=2)
    
    def save_suspected_dice(self, popup, opponent_idx):
        popup.destroy()
        self.calculate_probability()
    
    def update_opponents(self):
        self.create_opponent_inputs()
        self.setup_automatic_calculation()
        self.update_total_dice()
    
    def update_total_dice(self):
        total = 0
        
        for die_var in self.your_dice_vars:
            if die_var.get() != "":
                total += 1
        
        for opp_var in self.opponent_dice_vars:
            total += opp_var.get()
            
        self.total_dice.set(total)
        self.calculate_probability()
    
    def calculate_probability(self):
        try:
            total_dice = self.total_dice.get()
            bid_q = self.bid_quantity.get()
            bid_f = self.bid_face.get()
            
            if total_dice <= 0:
                self.probability.set("Invalid dice count")
                self.suspected_probability.set("Invalid dice count")
                return
            
            known_successes = 0
            your_dice_count = 0
            for die_var in self.your_dice_vars:
                value = die_var.get()
                if value == "":
                    continue
                    
                your_dice_count += 1
                face = int(value)
                if face == bid_f or (face == 1 and bid_f != 1):
                    known_successes += 1
            
            base_unknown_dice = total_dice - your_dice_count
            base_prob = self.calculate_cumulative_probability(known_successes, base_unknown_dice, bid_f, bid_q)
            
            base_info = f" (Known: {known_successes}, Unknown: {base_unknown_dice})"
            self.probability.set(f"{base_prob*100:.2f}%{base_info}")
            
            if len(self.opponent_suspected_vars) > 0:
                suspected_successes = known_successes
                suspected_dice_count = your_dice_count
                
                for opp_idx, suspected_list in enumerate(self.opponent_suspected_vars):
                    if opp_idx >= len(self.opponent_dice_vars):
                        continue
                    
                    opp_dice_count = self.opponent_dice_vars[opp_idx].get()
                    
                    for i in range(min(len(suspected_list), opp_dice_count)):
                        value = suspected_list[i].get()
                        if value == "":
                            continue
                            
                        suspected_dice_count += 1
                        face = int(value)
                        if face == bid_f or (face == 1 and bid_f != 1):
                            suspected_successes += 1
                
                suspected_unknown_dice = total_dice - suspected_dice_count
                suspected_prob = self.calculate_cumulative_probability(suspected_successes, suspected_unknown_dice, bid_f, bid_q)
                
                suspected_info = f" (Known: {suspected_successes}, Suspected: {suspected_dice_count - your_dice_count}, Unknown: {suspected_unknown_dice})"
                self.suspected_probability.set(f"{suspected_prob*100:.2f}%{suspected_info}")
            else:
                self.suspected_probability.set("Set suspected dice to see this probability")
                
        except Exception as e:
            self.probability.set(f"Error: {str(e)}")
            self.suspected_probability.set(f"Error: {str(e)}")
    
    def calculate_cumulative_probability(self, known_successes, unknown_dice, bid_f, bid_q):
        required_unknown = max(0, bid_q - known_successes)
        
        if unknown_dice <= 0:
            if required_unknown <= 0:
                return 1.0
            else:
                return 0.0
        else:
            p_success = 1/6 if bid_f == 1 else 1/3
            
            if required_unknown == 0:
                return 1.0
            elif required_unknown > unknown_dice:
                return 0.0
            else:
                prob = 0.0
                for k in range(required_unknown, unknown_dice + 1):
                    prob += calculate_binomial_probability(unknown_dice, p_success, k)
                return prob

if __name__ == "__main__":
    root = tk.Tk()
    app = PerudoCalculator(root)
    root.mainloop()