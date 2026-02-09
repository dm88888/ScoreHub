import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import requests

API = "http://127.0.0.1:5001"

root = tk.Tk()
root.title("ScoreHub – Desktop Client")
root.geometry("800x620")
root.configure(bg="#0d0d0d")

# --------------------------
# Tkinter Styling
# --------------------------

style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#1a1a1a",
                foreground="#00eaff",
                rowheight=26,
                fieldbackground="#1a1a1a")

style.configure("Treeview.Heading",
                background="#00eaff",
                foreground="#000000",
                font=("Segoe UI", 11, "bold"))

NEON_BTN = {
    "font": ("Segoe UI", 11, "bold"),
    "bg": "#00eaff",
    "fg": "black",
    "activebackground": "#00cce0",
    "activeforeground": "black",
    "bd": 0,
    "relief": "flat",
    "width": 12,
    "height": 2
}

# --------------------------
# Header
# --------------------------

header = tk.Label(root, text="SCOREHUB – RPG DASHBOARD",
                  bg="#0d0d0d", fg="#00eaff",
                  font=("Segoe UI", 22, "bold"))
header.pack(pady=10)

# --------------------------
# Player List
# --------------------------

tree = ttk.Treeview(root,
                    columns=("name", "score", "xp", "level"),
                    show="headings", height=14)

tree.heading("name", text="Name")
tree.heading("score", text="Score")
tree.heading("xp", text="XP")
tree.heading("level", text="Level")

tree.column("name", width=220)
tree.column("score", width=80)
tree.column("xp", width=80)
tree.column("level", width=80)

tree.pack(fill="x", pady=10)

# --------------------------
# FUNCTIONS
# --------------------------

heroes_available = [
    "Warrior", "Mage", "Rogue", "Paladin", "Hunter"
]

def refresh():
    try:
        res = requests.get(f"{API}/players")
        players = res.json()

        tree.delete(*tree.get_children())
        for p in players:
            tree.insert("", "end", iid=p["id"],
                        values=(p["name"], p["score"], p["xp"], p["level"]))
    except:
        messagebox.showerror("Error", "Cannot connect to server")


def add_player():
    name = simpledialog.askstring("Add Player", "Enter name:")
    if not name:
        return

    requests.post(f"{API}/players", json={"name": name})
    refresh()


def edit_score():
    sel = tree.focus()
    if not sel:
        return

    new_score = simpledialog.askinteger("Edit Score", "New score:")
    if new_score is None:
        return

    requests.put(f"{API}/players/{sel}/score", json={"score": new_score})
    refresh()


# --------------------------------------------
# HERO SELECTION WINDOW
# --------------------------------------------

selected_heroes = {}

def choose_heroes():
    sel = tree.focus()
    if not sel:
        messagebox.showwarning("Warning", "Select a player first!")
        return

    win = tk.Toplevel(root)
    win.title("Choose Heroes")
    win.geometry("300x350")
    win.configure(bg="#0d0d0d")

    tk.Label(win, text="Select 2 Heroes", fg="#00eaff",
             bg="#0d0d0d", font=("Segoe UI", 14, "bold")).pack(pady=10)

    vars_list = []

    for hero in heroes_available:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(win, text=hero, variable=var,
                            bg="#0d0d0d", fg="#00eaff",
                            selectcolor="#1a1a1a",
                            font=("Segoe UI", 12))
        cb.pack(anchor="w", padx=20)
        vars_list.append((hero, var))

    def confirm():
        picked = [h for h, v in vars_list if v.get()]
        if len(picked) != 2:
            messagebox.showerror("Error", "Select exactly 2 heroes!")
            return

        selected_heroes[int(sel)] = picked

        win.destroy()
        messagebox.showinfo("Heroes Selected",
                            f"Selected heroes:\n{picked[0]} & {picked[1]}")

    tk.Button(win, text="Save", command=confirm, **NEON_BTN).pack(pady=15)


# --------------------------------------------
# BATTLE WINDOW
# --------------------------------------------

def play_game():
    sel = tree.focus()
    if not sel:
        messagebox.showwarning("Warning", "Select player.")
        return

    sel = int(sel)

    if sel not in selected_heroes:
        messagebox.showwarning("No heroes", "Choose heroes first!")
        return

    heroes = selected_heroes[sel]

    # Start battle in backend
    res = requests.post(f"{API}/battle/start/{sel}",
                        json={"hero1": heroes[0], "hero2": heroes[1]})
    data = res.json()

    if "error" in data:
        messagebox.showerror("Error", data["error"])
        return

    # Build Battle UI
    battle = tk.Toplevel(root)
    battle.title("Card Battle Arena")
    battle.geometry("500x500")
    battle.configure(bg="#0d0d0d")

    tk.Label(battle, text="CARD BATTLE", fg="#00eaff",
             bg="#0d0d0d", font=("Segoe UI", 18, "bold")).pack(pady=10)

    player_hp_var = tk.StringVar()
    enemy_hp_var = tk.StringVar()

    player_hp_var.set(f"Player HP: {data['player_hp']}")
    enemy_hp_var.set(f"Enemy HP: {data['enemy_hp']}")

    tk.Label(battle, textvariable=player_hp_var,
             fg="#00eaff", bg="#0d0d0d",
             font=("Segoe UI", 14)).pack()

    tk.Label(battle, textvariable=enemy_hp_var,
             fg="#ff4444", bg="#0d0d0d",
             font=("Segoe UI", 14)).pack()

    log_box = tk.Text(battle, height=10, width=50,
                      bg="#1a1a1a", fg="#00eaff",
                      font=("Consolas", 11))
    log_box.pack(pady=10)

    def send_move(move):
        res = requests.post(f"{API}/battle/play/{sel}", json={"move": move})
        dt = res.json()

        if dt["result"] == "continue":
            player_hp_var.set(f"Player HP: {dt['player_hp']}")
            enemy_hp_var.set(f"Enemy HP: {dt['enemy_hp']}")
            log_box.insert("end", dt["log"] + "\n")
            log_box.see("end")
        elif dt["result"] == "win":
            messagebox.showinfo("WIN", "You defeated the enemy!\n+20 XP +15 Score")
            battle.destroy()
            refresh()
        elif dt["result"] == "lose":
            messagebox.showinfo("LOSE", "You were defeated!")
            battle.destroy()

    # Action buttons
    action_frame = tk.Frame(battle, bg="#0d0d0d")
    action_frame.pack()

    tk.Button(action_frame, text="Attack", command=lambda: send_move("attack"),
              **NEON_BTN).grid(row=0, column=0, padx=10)

    tk.Button(action_frame, text="Defend", command=lambda: send_move("defend"),
              **NEON_BTN).grid(row=0, column=1, padx=10)

    tk.Button(action_frame, text="Special", command=lambda: send_move("special"),
              **NEON_BTN).grid(row=0, column=2, padx=10)


def daily_reward():
    sel = tree.focus()
    if not sel:
        return

    res = requests.post(f"{API}/players/{sel}/daily").json()
    messagebox.showinfo("Daily Reward", res.get("status", res.get("error", "")))
    refresh()


def delete_player():
    sel = tree.focus()
    if not sel:
        return

    if messagebox.askyesno("Delete", "Are you sure?"):
        requests.delete(f"{API}/players/{sel}")
        refresh()

# --------------------------
# Buttons
# --------------------------

button_panel = tk.Frame(root, bg="#0d0d0d")
button_panel.pack(pady=15)

tk.Button(button_panel, text="Add", command=add_player, **NEON_BTN).grid(row=0, column=0, padx=10, pady=5)
tk.Button(button_panel, text="Edit Score", command=edit_score, **NEON_BTN).grid(row=0, column=1, padx=10, pady=5)
tk.Button(button_panel, text="Choose Heroes", command=choose_heroes, **NEON_BTN).grid(row=1, column=0, padx=10, pady=5)
tk.Button(button_panel, text="Play Game", command=play_game, **NEON_BTN).grid(row=1, column=1, padx=10, pady=5)
tk.Button(button_panel, text="Daily Reward", command=daily_reward, **NEON_BTN).grid(row=2, column=0, padx=10, pady=5)
tk.Button(button_panel, text="Delete", command=delete_player, **NEON_BTN).grid(row=2, column=1, padx=10, pady=5)

refresh()
root.mainloop()
