import sys, queue, os
import tkinter as tk
from tkinter import Text, ttk, font
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from GymModel import GymModel

class StdinRedirect:
    def __init__(self):
        self.queue = queue.Queue()

    def readline(self):
        return self.queue.get()

    def write(self, s):
        self.queue.put(s + "\n")

class StdoutRedirect:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, s):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, s)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)
    
    def flush(self):
        pass

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.bind("<Alt-f>", lambda e: self.state('zoomed'))
        self.bind("<Alt-Delete>", lambda e: self.quit())
        self.setup_env()
        self.mainloop()

    def set_model(self, env):
        self.model = GymModel(env=env)
        self.rf_dir = self.model.rf_dir
        self.training_active = self.testing_active = self.test_physical_active = False
        self.training_thread, self.testing_thread = None, None
        code_vars = {"BallBeam": [["K_pos", "K_vel", "K_ang"], "setpoint", "pos", [["Setpoint", "Initial Velocity"], ["Setpoint", "Velocity"]]],
                     "CartPole": [["K_pos", "K_vel", "K_ang", "K_ang_v"], "upright", "ang", [[], []]]} # TODO: implement initial and randomize variables for cartpole
        self.reward_vars, goal_var, return_var = code_vars[env][:-1]
        self.initial_params, self.randomize_params = code_vars[env][-1]
        self.def_funct = "def user_reward(self):"
        self.initial_code = f'{", ".join([i[2:] for i in self.reward_vars])} = self.state\n{", ".join(self.reward_vars)} = self.reward_scale\n{goal_var} = self.goal\nreturn -({return_var}-{goal_var})**2'
        for widget in self.winfo_children():
            widget.unbind_all("<Key-1>")
            widget.unbind_all("<Key-2>")
            widget.unbind_all("<Alt-b>")
            widget.unbind_all("<Alt-c>")
            widget.destroy()
        self.setup_ui()

    def setup_env(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.title("Envrionment")
        label = tk.Label(self, text="Select Environment", font=("Arial", 16, "bold"), pady=10)
        label.pack(pady=10)
        ballbeam = ttk.Button(self, text="Ball Beam", command=lambda: self.set_model("BallBeam"))
        ballbeam.bind_all("<Key-1>", lambda e: self.set_model("BallBeam"))
        ballbeam.bind_all("<Alt-b>", lambda e: self.set_model("BallBeam"))
        ballbeam.pack(pady=10)
        cartpole = ttk.Button(self, text="Cart Pole", command=lambda: self.set_model("CartPole"))
        cartpole.bind_all("<Key-2>", lambda e: self.set_model("CartPole"))
        cartpole.bind_all("<Alt-c>", lambda e: self.set_model("CartPole"))
        cartpole.pack(pady=10)
        
    def setup_ui(self):
        self.title("GUI")
        self.geometry("900x600")
        self.configure(bg="#e0e0e0")
        
        # basic
        tab_control = ttk.Notebook(self)
        training_tab = ttk.Frame(tab_control)
        tab_control.add(training_tab, text='Training')
        tab_control.pack(expand=True, fill="both")
        title_label = tk.Label(training_tab, text=self.model.env_shortname, font=("Arial", 16, "bold"), bg="#e0e0e0", pady=10)
        title_label.pack(fill="x")

        # image and graph
        image_graph_frame = tk.Frame(training_tab, bg="#ffffff", padx=10, pady=10, relief=tk.GROOVE, borderwidth=3)
        image_graph_frame.pack(fill="both", expand=True, padx=15, pady=10)
        image = Image.open(f"img/{self.model.env_shortname}.png").resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(image_graph_frame, image=photo, bg="#ffffff")
        image_label.image = photo
        image_label.pack(side=tk.LEFT, padx=10, pady=10)

        # training display
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Avg Reward")
        ax.set_title("Training Progress")
        self.line, = ax.plot([], [], 'r-')
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=image_graph_frame)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.RIGHT, fill="both", expand=True)
        self.ax = ax
        self.canvas = canvas
        plt.close(self.canvas.figure) # FIX THIS PROPERLY

        # params display
        control_frame = tk.Frame(training_tab, bg="#e0e0e0", padx=10, pady=10)
        control_frame.pack(fill="x", padx=15, pady=10)
        self.entries = {}
        if self.model.env_shortname == "BallBeam":
            params_frame = tk.LabelFrame(control_frame, text="Hyperparameters", bg="#e0e0e0", padx=10, pady=10)
            params_frame.pack(side=tk.LEFT, fill="y", padx=10, pady=5)
            for var in self.initial_params:
                tk.Label(params_frame, text=f"{var}:", bg="#e0e0e0").pack(anchor="w", padx=5, pady=2)
                entry = tk.Entry(params_frame, width=15)
                entry.insert(0, "0")
                entry.pack(padx=5, pady=2)
                self.entries[var] = entry
            note_label = tk.Label(params_frame, text=f"Setpoint is a\ndecimal fraction\n\nInitial velocity\ngiven in cm/s\n\nCalculations\ndone in meters", font=("Arial", 10), bg="#e0e0e0")
            note_label.pack(side=tk.TOP, fill="x", padx=10, pady=10)
        
        checkmark_frame = tk.LabelFrame(control_frame, text="Randomize initial values", bg="#e0e0e0", padx=10, pady=10)
        checkmark_frame.pack(side=tk.LEFT, fill="y", padx=10, pady=5)
        self.check_vars = {}
        for chk in self.randomize_params:
            var = tk.BooleanVar(value=True)
            check = tk.Checkbutton(checkmark_frame, text=chk, bg="#e0e0e0", variable=var)
            check.pack(anchor="w", padx=5, pady=2)
            self.check_vars[chk] = var
        
        weights_frame = tk.LabelFrame(control_frame, text="Reward weights", bg="#e0e0e0", padx=10, pady=10)
        weights_frame.pack(side=tk.LEFT, fill="y", padx=10, pady=5)
        variables = self.reward_vars
        for var in variables:
            tk.Label(weights_frame, text=var, bg="#e0e0e0").pack(anchor="w", padx=5, pady=2)
            entry = tk.Entry(weights_frame, width=15)
            entry.insert(0, "1")
            entry.pack(padx=5, pady=2)
            self.entries[var.split(" ")[0]] = entry
        
        # code input
        def sync_scroll(*args):
            if args[0] == "moveto":
                self.text_box.yview_moveto(args[1])
                self.line_numbers.yview_moveto(args[1])
            else:
                self.text_box.yview_moveto(args[0])
                self.line_numbers.yview_moveto(args[0])
        def on_enter():
            self.text_box.after(1, lambda: sync_scroll("moveto", self.text_box.yview()[0]))
        def update_line_numbers():
            self.line_numbers.config(state=tk.NORMAL)
            num_lines = int(self.text_box.index("end-1c").split(".")[0])
            current_lines = self.line_numbers.get("1.0", tk.END).strip().split("\n")
            if current_lines == [""]:
                current_lines = []
            if len(current_lines) > num_lines:
                self.line_numbers.delete(f"{num_lines + 1}.0", tk.END)
                self.line_numbers.insert(f"{num_lines+1}.0", "\n")
            for i in range(len(current_lines) + 1, num_lines + 1):
                self.line_numbers.insert(tk.END, f"{i}\n")
            self.line_numbers.config(state=tk.DISABLED)
        code_editor_frame = tk.Frame(control_frame, relief=tk.RIDGE, borderwidth=2, bg="#f7f7f7")
        code_editor_frame.pack(side=tk.LEFT, fill="y", expand=False, padx=10, pady=5)
        function_label = tk.Label(code_editor_frame, text=self.def_funct, font=("Arial", 10, "bold"), fg="black", bg="#f7f7f7", anchor="w")
        function_label.pack(side=tk.TOP, fill="x", padx=10, pady=5)
        self.use_new_rf = tk.BooleanVar(value=False)
        custom_rf = tk.Checkbutton(code_editor_frame, text="Use custom reward function", variable=self.use_new_rf, bg="#f7f7f7")
        custom_rf.pack(side=tk.BOTTOM, anchor="w", padx=10, pady=5)
        code_scroll_y = tk.Scrollbar(code_editor_frame, orient="vertical", command=sync_scroll)
        code_scroll_y.pack(side="right", fill="y")
        code_scroll_x = tk.Scrollbar(code_editor_frame, orient="horizontal")
        code_scroll_x.pack(side="bottom", fill="x")
        self.line_numbers = tk.Text(code_editor_frame, width=4, font=("Courier", 10), bg="#f7f7f7", fg="black", state=tk.DISABLED, bd=0, yscrollcommand=lambda *args: sync_scroll(*args))
        self.line_numbers.pack(side=tk.LEFT, fill="y")
        self.text_box = Text(code_editor_frame, width=40, font=("Courier", 10), bg="white", fg="black", insertbackground="black", bd=0, wrap="none", yscrollcommand=lambda *args: sync_scroll(*args), xscrollcommand=code_scroll_x.set)
        self.text_box.insert("1.0", self.initial_code)
        self.text_box.bind("<KeyRelease>", lambda e: update_line_numbers())
        self.text_box.bind("<Return>", lambda e: on_enter())
        self.text_box.pack(side=tk.LEFT, fill="both", expand=True)
        code_scroll_x.config(command=self.text_box.xview)
        update_line_numbers()
        
        # action buttons
        def focus_last_line():
            self.text_box.focus_set()
            self.text_box.mark_set("insert", tk.END)
            self.text_box.see(tk.END)
        button_frame = tk.Frame(control_frame, bg="#e0e0e0")
        button_frame.pack(side=tk.RIGHT, fill="y", padx=10)
        self.status_label = tk.Label(button_frame, text="Status: Not started", fg="red", font=("Arial", 10, "bold"), bg="#e0e0e0")
        self.status_label.pack(pady=5)
        self.start_button = ttk.Button(button_frame, text="Start train (Alt+S)", command=self.start_train)
        self.start_button.bind_all("<Alt-s>", lambda e: self.start_train())
        self.start_button.pack(fill="x", pady=5)
        stop_button = ttk.Button(button_frame, text="Stop (Alt+P)", command=self.stop_execution)
        stop_button.bind_all("<Alt-p>", lambda e: self.stop_execution())
        stop_button.pack(fill="x", pady=5)
        self.test_button = ttk.Button(button_frame, text="Test Agent (Alt+T)", command=self.start_test)
        self.test_button.bind_all("<Alt-t>", lambda e: self.start_test())
        self.test_button.pack(fill="x", pady=5)
        terminal_button = ttk.Button(button_frame, text="Focus terminal (Alt+Enter)", command=lambda: self.input_entry.focus_set())
        terminal_button.bind_all("<Alt-Return>", lambda e: self.input_entry.focus_set())
        terminal_button.pack(fill="x", pady=5)
        code_button = ttk.Button(button_frame, text="Focus code (Alt+C)", command=focus_last_line)
        code_button.bind_all("<Alt-c>", lambda e: focus_last_line())
        code_button.pack(fill="x", pady=5)
        back_button = ttk.Button(button_frame, text="Back (Alt+B)", command=self.go_menu)
        back_button.bind_all("<Alt-b>", lambda e: self.go_menu())
        back_button.pack(fill="x", pady=5)
        close_button = ttk.Button(button_frame, text="Quit (Alt+Delete)", command=self.quit)
        close_button.bind_all("<Alt-Delete>", lambda e: self.quit())
        close_button.pack(fill="x", pady=5)
        test_physical = ttk.Button(button_frame, text="Test physical (Alt+Z)", command=lambda: self.start_test_physical())
        test_physical.bind_all("<Alt-z>", lambda e: self.start_test_physical())
        test_physical.pack(fill="x", pady=5)
        
        # terminal
        def on_input_enter():
            user_input = self.input_entry.get()
            if user_input == "Terminal input: ":
                return
            self.input_entry.delete(0, tk.END)
            self.terminal_text.config(state=tk.NORMAL)
            self.terminal_text.insert(tk.END, f"> {user_input}\n")
            self.terminal_text.see(tk.END)
            self.terminal_text.config(state=tk.DISABLED)
            self.stdin_redirector.write(user_input)
        terminal_frame = tk.Frame(control_frame, bg="#f7f7f7", relief=tk.RIDGE, borderwidth=2)
        terminal_frame.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=5)
        terminal_title = tk.Label(terminal_frame, text="Terminal", font=("Arial", 10, "bold"), bg="#f7f7f7", anchor="w")
        terminal_title.pack(fill="x", padx=10, pady=5)
        self.input_entry = tk.Entry(terminal_frame, font=("Courier", 10))
        self.input_entry.pack(side=tk.BOTTOM, fill="x", expand=True)
        self.terminal_text = Text(terminal_frame, font=("Courier", 10), width=40, bg="white", fg="black", insertbackground="black", bd=0, state=tk.DISABLED)
        self.terminal_text.pack(fill="both", expand=True)
        self.input_entry.insert(0, "Terminal input: ")
        self.input_entry.bind("<FocusIn>", lambda e: self.input_entry.delete(0, tk.END) if self.input_entry.get() == "Terminal input: " else None)
        self.input_entry.bind("<FocusOut>", lambda e: self.input_entry.insert(0, "Terminal input: ") if not self.input_entry.get() else None)
        self.input_entry.bind("<Return>", lambda e: on_input_enter())
        self.stdout_redirector = StdoutRedirect(self.terminal_text)
        sys.stdout = self.stdout_redirector
        self.stdin_redirector = StdinRedirect()
        sys.stdin = self.stdin_redirector

    def get_args(self):
        # assumes forms are filled
        self.terminal_text.update_idletasks()
        args = {}
        if self.model.env_shortname == "BallBeam":
            initial, randomize = ["setpoint", "init_velocity"], ["random_set", "random_init_vel"]
        else:
            initial, randomize = [], []
        initial_entries = {self.initial_params[i]: initial[i] for i in range(len(initial))}
        randomize_checks = {self.randomize_params[i]: randomize[i] for i in range(len(randomize))}
        reward_scale = [1]*self.model.state_dim
        for var, entry in self.entries.items():
            n = entry.get()
            if var in self.reward_vars:
                reward_scale[self.reward_vars.index(var)] = float(n)
            else:
                args[initial_entries[var]] = float(n)
        for var, check in self.check_vars.items():
            args[randomize_checks[var]] = check.get()
        args["reward_scale"] = reward_scale
        args["use_new_rf"] = self.use_new_rf.get()
        args["char_width"] = self.terminal_text.winfo_width() // font.Font(font=self.terminal_text.cget("font")).measure("0")
        return args

    def save_rf(self):
        code = self.text_box.get("1.0", tk.END)
        tabbed = ""
        for line in code.splitlines():
            tabbed += "\t" + line + "\n"
        code = self.def_funct+"\n" + tabbed
        if self.use_new_rf.get():
            exec(code)
        if not os.path.exists(self.rf_dir):
            os.makedirs(self.rf_dir)
        with open(f"{self.rf_dir+self.model.env_shortname}_rf.py", "w+") as f:
            f.write(code)
    
    def run_train(self):
        self.training_active = True
        try:
            self.model.set_args(self.get_args())
            self.save_rf()
            self.status_label.config(text="Status: Training", fg="green")
            self.model.train()
        except Exception as e:
            print(f"Error: {e}")
            self.status_label.config(text="Status: Syntax Error", fg="red")
        else:
            self.status_label.config(text="Status: Stopped", fg="red")
        finally:
            self.training_active = False
            self.start_button.config(state=tk.NORMAL)

    def start_train(self):
        try:
            if self.training_active:
                raise Exception("Training already active")
            self.status_label.config(text="Status: Starting...", fg="orange")
            self.start_button.config(state=tk.DISABLED)
            self.training_thread = Thread(target=self.run_train, daemon=True)
            self.training_thread.start()
            self.after(500, self.update_graph)
        except Exception as e:
            print(f"An error has occurred: {e}")
            self.status_label.config(text="Status: Syntax Error", fg="red")

    def wait_stop_train(self):
        if self.training_thread.is_alive() or self.model.is_training:
            self.after(100, self.wait_stop_train)
        else:
            self.status_label.config(text="Status: Stopped", fg="red")
            self.start_button.config(state=tk.NORMAL)
            self.stdout_redirector.write(f"{self.model.big_block}\n\n")
    
    def update_graph(self):
        training_data = self.model.get_training_data()
        if training_data:
            epoch, rewards = zip(*training_data)
            self.line.set_data(epoch, rewards)
            self.ax.set_xlim(0, max(epoch) + 1)
            self.ax.set_ylim(min(rewards) - 1, max(rewards) + 1)
            self.canvas.draw()
        if self.training_active:
            self.after(500, self.update_graph)

    def start_test(self):
        try:
            if self.training_active:
                raise Exception("Testing already active")
            self.status_label.config(text="Status: Testing...", fg="blue")  
            self.test_button.config(state=tk.DISABLED)
            self.test_thread = Thread(target=self.run_test)
            self.test_thread.start()
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="red")        
    
    def run_test(self):
        self.testing_active = True
        try:
            self.model.set_args(self.get_args())
            self.save_rf()
            self.status_label.config(text="Status: Testing", fg="green")
            self.model.test()
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="red")
        else:
            self.status_label.config(text="Status: Stopped", fg="red")
        finally:
            self.testing_active = False
            self.test_button.config(state=tk.NORMAL)

    def wait_stop_test(self):
        if self.testing_thread.is_alive() or self.model.is_testing:
            self.after(100, self.wait_stop_test)
        else:
            self.status_label.config(text="Status: Stopped", fg="red")
            self.test_button.config(state=tk.NORMAL)

    def start_test_physical(self):
        try:
            if self.test_physical_active:
                raise Exception("Physical testing already active")
            self.status_label.config(text="Status: Testing...", fg="blue")  
            self.test_physical.config(state=tk.DISABLED)
            self.test_physical_thread = Thread(target=self.run_test_physical)
            self.test_physical_thread.start()
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="red")

    def run_test_physical(self):
        self.test_physical_active = True
        try:
            self.model.set_args(self.get_args())
            self.save_rf()
            self.status_label.config(text="Status: Testing", fg="green")
            self.model.test_physical()
        except Exception as e:
            self.status_label.config(text=f"Error: {e}", fg="red")
        else:
            self.status_label.config(text="Status: Stopped", fg="red")
        finally:
            self.test_physical_active = False
            self.test_physical.config(state=tk.NORMAL)

    def wait_stop_test_physical(self):
        if self.test_physical_thread.is_alive() or self.model.is_testing_physical:
            self.after(100, self.wait_stop_test_physical)
        else:
            self.status_label.config(text="Status: Stopped", fg="red")
            self.test_physical.config(state=tk.NORMAL)
            self.stdout_redirector.write(f"{self.model.big_block}\n\n")

    def stop_execution(self):
        if self.training_active:
            self.training_active = False
            self.status_label.config(text="Status: Stopping...", fg="orange")
            self.model.stop_train()
            # self.wait_stop_train()
            return
        if self.testing_active:
            self.testing_active = False
            self.status_label.config(text="Status: Stopping...", fg="orange")
            self.model.stop_test()
            # self.wait_stop_test()
            return
        if self.test_physical_active:
            self.test_physical_active = False
            self.status_label.config(text="Status: Stopping...", fg="orange")
            self.model.stop_test_physical()
            # self.wait_stop_test_physical()
            return
        print("No current code execution\n")

    def go_menu(self):
        self.setup_env()
        
    def quit(self):
        self.destroy()


GUI()
