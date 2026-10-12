import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import subprocess


class DesktopNotifier:
    def __init__(self, root):
        self.root = root

        # =====================================================
        # WINDOW SETTINGS
        # =====================================================

        self.root.title("Desktop Notifier")
        self.root.geometry("700x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#F4F7FB")

        # =====================================================
        # COLORS
        # =====================================================

        self.bg_color = "#F4F7FB"
        self.white = "#FFFFFF"
        self.navy = "#173B63"
        self.blue = "#2563A6"
        self.light_blue = "#EEF5FC"
        self.border = "#D7E2EE"
        self.text = "#202938"
        self.muted = "#667085"
        self.green = "#2E8B57"
        self.red = "#D64545"

        # Store reminders
        self.reminders = []

        # =====================================================
        # TTK STYLE
        # =====================================================

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Modern.TCombobox",
            fieldbackground=self.white,
            background=self.white,
            foreground=self.text,
            bordercolor=self.border,
            lightcolor=self.border,
            darkcolor=self.border,
            padding=5
        )

        # =====================================================
        # HEADER
        # =====================================================

        header = tk.Frame(
            root,
            bg=self.navy,
            height=125
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="🔔",
            font=("Arial", 26),
            bg=self.navy,
            fg="white"
        ).pack(pady=(15, 0))

        tk.Label(
            header,
            text="Desktop Notifier",
            font=("Arial", 24, "bold"),
            bg=self.navy,
            fg="white"
        ).pack()

        tk.Label(
            header,
            text="Simple reminders for your daily tasks",
            font=("Arial", 10),
            bg=self.navy,
            fg="#D6E5F5"
        ).pack(pady=(3, 0))

        # =====================================================
        # CURRENT TIME
        # =====================================================

        self.current_time_label = tk.Label(
            root,
            text="",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.blue
        )
        self.current_time_label.pack(pady=(17, 8))

        self.update_current_time()

        # =====================================================
        # CREATE REMINDER CARD
        # =====================================================

        create_card = tk.Frame(
            root,
            bg=self.white,
            highlightbackground=self.border,
            highlightthickness=1
        )
        create_card.pack(
            padx=35,
            pady=8,
            fill="x"
        )

        tk.Label(
            create_card,
            text="Create Reminder",
            font=("Arial", 15, "bold"),
            bg=self.white,
            fg=self.navy
        ).grid(
            row=0,
            column=0,
            columnspan=7,
            sticky="w",
            padx=20,
            pady=(17, 13)
        )

        # =====================================================
        # DATE
        # =====================================================

        tk.Label(
            create_card,
            text="Date",
            font=("Arial", 10, "bold"),
            bg=self.white,
            fg=self.muted
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(20, 8),
            pady=5
        )

        self.date_entry = tk.Entry(
            create_card,
            width=14,
            font=("Arial", 10),
            bg=self.white,
            fg=self.text,
            relief="solid",
            bd=1
        )
        self.date_entry.grid(
            row=1,
            column=1,
            sticky="w",
            pady=5
        )

        self.date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        # =====================================================
        # TIME
        # =====================================================

        tk.Label(
            create_card,
            text="Time",
            font=("Arial", 10, "bold"),
            bg=self.white,
            fg=self.muted
        ).grid(
            row=1,
            column=2,
            sticky="w",
            padx=(25, 8),
            pady=5
        )

        self.hour_box = ttk.Combobox(
            create_card,
            values=[f"{i:02d}" for i in range(1, 13)],
            width=3,
            state="readonly",
            style="Modern.TCombobox"
        )
        self.hour_box.grid(
            row=1,
            column=3,
            sticky="w",
            pady=5
        )

        tk.Label(
            create_card,
            text=":",
            font=("Arial", 11, "bold"),
            bg=self.white,
            fg=self.text
        ).grid(
            row=1,
            column=4,
            pady=5
        )

        self.minute_box = ttk.Combobox(
            create_card,
            values=[f"{i:02d}" for i in range(60)],
            width=3,
            state="readonly",
            style="Modern.TCombobox"
        )
        self.minute_box.grid(
            row=1,
            column=5,
            sticky="w",
            pady=5
        )

        self.period_box = ttk.Combobox(
            create_card,
            values=["AM", "PM"],
            width=4,
            state="readonly",
            style="Modern.TCombobox"
        )
        self.period_box.grid(
            row=1,
            column=6,
            padx=(8, 20),
            pady=5
        )

        current = datetime.now()

        self.hour_box.set(
            current.strftime("%I")
        )

        self.minute_box.set(
            f"{(current.minute + 1) % 60:02d}"
        )

        self.period_box.set(
            current.strftime("%p")
        )

        # =====================================================
        # TITLE
        # =====================================================

        tk.Label(
            create_card,
            text="Title",
            font=("Arial", 10, "bold"),
            bg=self.white,
            fg=self.muted
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(20, 8),
            pady=5
        )

        self.title_entry = tk.Entry(
            create_card,
            width=46,
            font=("Arial", 10),
            bg=self.white,
            fg=self.text,
            relief="solid",
            bd=1
        )
        self.title_entry.grid(
            row=2,
            column=1,
            columnspan=6,
            sticky="w",
            padx=(0, 20),
            pady=5
        )

        # =====================================================
        # MESSAGE
        # =====================================================

        tk.Label(
            create_card,
            text="Message",
            font=("Arial", 10, "bold"),
            bg=self.white,
            fg=self.muted
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=(20, 8),
            pady=5
        )

        self.message_entry = tk.Entry(
            create_card,
            width=46,
            font=("Arial", 10),
            bg=self.white,
            fg=self.text,
            relief="solid",
            bd=1
        )
        self.message_entry.grid(
            row=3,
            column=1,
            columnspan=6,
            sticky="w",
            padx=(0, 20),
            pady=5
        )

        # =====================================================
        # ADD REMINDER BUTTON
        # =====================================================

        tk.Button(
            create_card,
            text="＋  Add Reminder",
            font=("Arial", 10, "bold"),
            bg=self.blue,
            fg="white",
            activebackground="#1D4F80",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=22,
            pady=9,
            command=self.add_reminder
        ).grid(
            row=4,
            column=0,
            columnspan=7,
            pady=(12, 18)
        )

        # =====================================================
        # YOUR REMINDERS TITLE
        # =====================================================

        tk.Label(
            root,
            text="Your Reminders",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.navy
        ).pack(
            anchor="w",
            padx=35,
            pady=(17, 8)
        )

        # =====================================================
        # REMINDERS CONTAINER
        # =====================================================

        reminders_outer = tk.Frame(
            root,
            bg=self.white,
            highlightbackground=self.border,
            highlightthickness=1
        )
        reminders_outer.pack(
            padx=35,
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            reminders_outer,
            bg=self.white,
            highlightthickness=0
        )
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            reminders_outer,
            orient="vertical",
            command=self.canvas.yview
        )
        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.reminders_frame = tk.Frame(
            self.canvas,
            bg=self.white
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.reminders_frame,
            anchor="nw"
        )

        self.reminders_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.update_canvas_width
        )

        # =====================================================
        # STATUS
        # =====================================================

        self.status_label = tk.Label(
            root,
            text="Ready — monitoring reminders",
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.green
        )
        self.status_label.pack(
            pady=(8, 10)
        )

        # Display reminders
        self.refresh_reminders()

        # Start reminder checking
        self.check_reminders()

    # =========================================================
    # CURRENT TIME
    # =========================================================

    def update_current_time(self):

        current_time = datetime.now().strftime(
            "%A, %d %B %Y  •  %I:%M:%S %p"
        )

        self.current_time_label.config(
            text=current_time
        )

        self.root.after(
            1000,
            self.update_current_time
        )

    # =========================================================
    # ADD REMINDER
    # =========================================================

    def add_reminder(self):

        date_text = self.date_entry.get().strip()
        title_text = self.title_entry.get().strip()
        message_text = self.message_entry.get().strip()

        hour = self.hour_box.get()
        minute = self.minute_box.get()
        period = self.period_box.get()

        # Check message
        if not message_text:
            messagebox.showwarning(
                "Missing Message",
                "Please enter a reminder message."
            )
            return

        # Default title
        if not title_text:
            title_text = "Reminder"

        # Validate date and time
        try:
            reminder_datetime = datetime.strptime(
                f"{date_text} {hour}:{minute} {period}",
                "%Y-%m-%d %I:%M %p"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please use the date format:\n\n"
                "YYYY-MM-DD\n\n"
                "Example: 2026-10-07"
            )
            return

        # Check future time
        if reminder_datetime <= datetime.now():
            messagebox.showwarning(
                "Invalid Time",
                "Please select a future date and time."
            )
            return

        # Add reminder
        reminder = {
            "datetime": reminder_datetime,
            "title": title_text,
            "message": message_text
        }

        self.reminders.append(
            reminder
        )

        # Sort reminders
        self.reminders.sort(
            key=lambda item: item["datetime"]
        )

        # Refresh display
        self.refresh_reminders()

        # Clear title and message automatically
        self.title_entry.delete(
            0,
            tk.END
        )

        self.message_entry.delete(
            0,
            tk.END
        )

        self.status_label.config(
            text="Reminder added successfully",
            fg=self.green
        )

    # =========================================================
    # DISPLAY REMINDERS
    # =========================================================

    def refresh_reminders(self):

        # Remove old cards
        for widget in self.reminders_frame.winfo_children():
            widget.destroy()

        # No reminders
        if not self.reminders:

            tk.Label(
                self.reminders_frame,
                text="No reminders scheduled.",
                font=("Arial", 11),
                bg=self.white,
                fg=self.muted
            ).pack(
                pady=35
            )

            return

        # Create reminder cards
        for reminder in self.reminders:

            card = tk.Frame(
                self.reminders_frame,
                bg=self.light_blue,
                highlightbackground=self.border,
                highlightthickness=1
            )

            card.pack(
                fill="x",
                padx=12,
                pady=6
            )

            # Information area
            info = tk.Frame(
                card,
                bg=self.light_blue
            )
            info.pack(
                side="left",
                fill="x",
                expand=True,
                padx=15,
                pady=10
            )

            # Title
            tk.Label(
                info,
                text=reminder["title"],
                font=("Arial", 11, "bold"),
                bg=self.light_blue,
                fg=self.navy
            ).pack(
                anchor="w"
            )

            # Date and time
            formatted_time = reminder[
                "datetime"
            ].strftime(
                "%d %B %Y  •  %I:%M %p"
            )

            tk.Label(
                info,
                text=formatted_time,
                font=("Arial", 9, "bold"),
                bg=self.light_blue,
                fg=self.blue
            ).pack(
                anchor="w",
                pady=(2, 0)
            )

            # Message
            tk.Label(
                info,
                text=reminder["message"],
                font=("Arial", 9),
                bg=self.light_blue,
                fg=self.text,
                wraplength=480,
                justify="left"
            ).pack(
                anchor="w",
                pady=(2, 0)
            )

            # Delete button for this reminder
            tk.Button(
                card,
                text="Delete",
                font=("Arial", 9, "bold"),
                bg=self.red,
                fg="white",
                activebackground="#B93737",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                padx=12,
                pady=7,
                command=lambda r=reminder: self.delete_reminder(r)
            ).pack(
                side="right",
                padx=15
            )

    # =========================================================
    # DELETE REMINDER
    # =========================================================

    def delete_reminder(self, reminder):

        confirm = messagebox.askyesno(
            "Delete Reminder",
            "Are you sure you want to delete this reminder?\n\n"
            f"{reminder['title']}\n"
            f"{reminder['datetime'].strftime('%d %B %Y, %I:%M %p')}"
        )

        if not confirm:
            return

        if reminder in self.reminders:
            self.reminders.remove(
                reminder
            )

        self.refresh_reminders()

        self.status_label.config(
            text="Reminder deleted successfully",
            fg=self.green
        )

    # =========================================================
    # CHECK REMINDERS
    # =========================================================

    def check_reminders(self):

        current_time = datetime.now()

        due_reminders = []

        for reminder in self.reminders:

            if current_time >= reminder["datetime"]:

                self.send_notification(
                    reminder
                )

                due_reminders.append(
                    reminder
                )

        # Remove reminders after notification
        for reminder in due_reminders:

            if reminder in self.reminders:
                self.reminders.remove(
                    reminder
                )

        if due_reminders:
            self.refresh_reminders()

        # Check every second
        self.root.after(
            1000,
            self.check_reminders
        )

    # =========================================================
    # SEND LINUX NOTIFICATION
    # =========================================================

    def send_notification(self, reminder):

        try:

            subprocess.run(
                [
                    "notify-send",
                    "--app-name=Desktop Notifier",
                    "--urgency=normal",
                    reminder["title"],
                    reminder["message"]
                ],
                check=True
            )

            self.status_label.config(
                text="🔔 Notification sent",
                fg=self.blue
            )

        except FileNotFoundError:

            messagebox.showerror(
                "Notification Error",
                "notify-send is not installed.\n\n"
                "Run:\n"
                "sudo dnf install libnotify"
            )

        except subprocess.CalledProcessError:

            messagebox.showerror(
                "Notification Error",
                "Linux could not display the notification."
            )

    # =========================================================
    # SCROLLING
    # =========================================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def update_canvas_width(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )


# =============================================================
# MAIN
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = DesktopNotifier(root)

    root.mainloop()