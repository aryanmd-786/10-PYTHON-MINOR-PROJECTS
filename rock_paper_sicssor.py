import tkinter as tk
import random


class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("500x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#111827")

        # Scores
        self.player_score = 0
        self.computer_score = 0
        self.rounds = 0

        # Title
        title = tk.Label(
            root,
            text="✊ ROCK  PAPER  SCISSORS ✌️",
            font=("Segoe UI", 22, "bold"),
            bg="#111827",
            fg="white"
        )
        title.pack(pady=(30, 10))

        # Subtitle
        subtitle = tk.Label(
            root,
            text="Choose your move!",
            font=("Segoe UI", 14),
            bg="#111827",
            fg="#9CA3AF"
        )
        subtitle.pack(pady=5)

        # Score Frame
        score_frame = tk.Frame(
            root,
            bg="#1F2937"
        )
        score_frame.pack(
            fill="x",
            padx=30,
            pady=25
        )

        # Player Score
        player_label = tk.Label(
            score_frame,
            text="YOU",
            font=("Segoe UI", 14, "bold"),
            bg="#1F2937",
            fg="#60A5FA"
        )
        player_label.grid(row=0, column=0, padx=40, pady=(15, 5))

        self.player_score_label = tk.Label(
            score_frame,
            text="0",
            font=("Segoe UI", 28, "bold"),
            bg="#1F2937",
            fg="white"
        )
        self.player_score_label.grid(row=1, column=0, padx=40, pady=(0, 15))

        # Computer Score
        computer_label = tk.Label(
            score_frame,
            text="COMPUTER",
            font=("Segoe UI", 14, "bold"),
            bg="#1F2937",
            fg="#F87171"
        )
        computer_label.grid(row=0, column=1, padx=40, pady=(15, 5))

        self.computer_score_label = tk.Label(
            score_frame,
            text="0",
            font=("Segoe UI", 28, "bold"),
            bg="#1F2937",
            fg="white"
        )
        self.computer_score_label.grid(row=1, column=1, padx=40, pady=(0, 15))

        # Result
        self.result_label = tk.Label(
            root,
            text="Make your choice!",
            font=("Segoe UI", 18, "bold"),
            bg="#111827",
            fg="white"
        )
        self.result_label.pack(pady=20)

        # Choices Frame
        choices_frame = tk.Frame(
            root,
            bg="#111827"
        )
        choices_frame.pack(pady=15)

        # Rock Button
        rock_button = tk.Button(
            choices_frame,
            text="✊\nROCK",
            font=("Segoe UI", 15, "bold"),
            width=8,
            height=3,
            bg="#374151",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=lambda: self.play("Rock")
        )
        rock_button.grid(row=0, column=0, padx=8)

        # Paper Button
        paper_button = tk.Button(
            choices_frame,
            text="✋\nPAPER",
            font=("Segoe UI", 15, "bold"),
            width=8,
            height=3,
            bg="#374151",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=lambda: self.play("Paper")
        )
        paper_button.grid(row=0, column=1, padx=8)

        # Scissors Button
        scissors_button = tk.Button(
            choices_frame,
            text="✌️\nSCISSORS",
            font=("Segoe UI", 15, "bold"),
            width=8,
            height=3,
            bg="#374151",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=lambda: self.play("Scissors")
        )
        scissors_button.grid(row=0, column=2, padx=8)

        # Choice display
        self.choice_label = tk.Label(
            root,
            text="You: -     Computer: -",
            font=("Segoe UI", 13),
            bg="#111827",
            fg="#D1D5DB"
        )
        self.choice_label.pack(pady=20)

        # Round counter
        self.round_label = tk.Label(
            root,
            text="Round: 0",
            font=("Segoe UI", 12),
            bg="#111827",
            fg="#9CA3AF"
        )
        self.round_label.pack()

        # Reset button
        reset_button = tk.Button(
            root,
            text="RESET GAME",
            font=("Segoe UI", 13, "bold"),
            bg="#DC2626",
            fg="white",
            activebackground="#EF4444",
            activeforeground="white",
            bd=0,
            width=18,
            height=2,
            cursor="hand2",
            command=self.reset_game
        )
        reset_button.pack(pady=25)

    # Game logic
    def play(self, player_choice):

        choices = ["Rock", "Paper", "Scissors"]

        computer_choice = random.choice(choices)

        self.rounds += 1

        # Display choices
        self.choice_label.config(
            text=f"You: {player_choice}     Computer: {computer_choice}"
        )

        # Decide winner
        if player_choice == computer_choice:
            result = "🤝 It's a Draw!"

        elif (
            (player_choice == "Rock" and computer_choice == "Scissors")
            or
            (player_choice == "Paper" and computer_choice == "Rock")
            or
            (player_choice == "Scissors" and computer_choice == "Paper")
        ):
            result = "🎉 You Win!"
            self.player_score += 1

        else:
            result = "😔 Computer Wins!"
            self.computer_score += 1

        # Update result
        self.result_label.config(text=result)

        # Update scores
        self.player_score_label.config(
            text=str(self.player_score)
        )

        self.computer_score_label.config(
            text=str(self.computer_score)
        )

        # Update round
        self.round_label.config(
            text=f"Round: {self.rounds}"
        )

    # Reset game
    def reset_game(self):

        self.player_score = 0
        self.computer_score = 0
        self.rounds = 0

        self.player_score_label.config(text="0")
        self.computer_score_label.config(text="0")

        self.result_label.config(
            text="Make your choice!"
        )

        self.choice_label.config(
            text="You: -     Computer: -"
        )

        self.round_label.config(
            text="Round: 0"
        )


# Main program
root = tk.Tk()

game = RockPaperScissors(root)

root.mainloop()