import tkinter as tk
from tkinter import *
import sqlite3


def createQuizPage(root):
    root.destroy()
    global create_quiz
    create_quiz = Tk()
    create_quiz.title('Create Quiz')
    
    quiz_name = StringVar()
    question_text = StringVar()
    option_a = StringVar()
    option_b = StringVar()
    option_c = StringVar()
    option_d = StringVar()
    correct_answer = StringVar()
    
    quiz_canvas = Canvas(create_quiz, width=1000, height=700, bg="light green")
    quiz_canvas.pack()

    quiz_frame = Frame(quiz_canvas, bg="green")
    quiz_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    heading = Label(quiz_frame, text="Create Quiz", fg="white", bg="green")
    heading.config(font=('calibri 20'))
    heading.pack(pady=10)

    quiz_name_label = Label(quiz_frame, text="Enter Quiz Name:", fg='white', bg='black')
    quiz_name_label.pack()
    quiz_name_entry = Entry(quiz_frame, bg='white', fg='black', textvariable=quiz_name)
    quiz_name_entry.pack()

    def addQuestion():
        question_data.append((question_text.get(), option_a.get(), option_b.get(), option_c.get(), option_d.get(), correct_answer.get()))

        question_text_entry.delete(0, 'end')
        option_a_entry.delete(0, 'end')
        option_b_entry.delete(0, 'end')
        option_c_entry.delete(0, 'end')
        option_d_entry.delete(0, 'end')
        correct_answer_entry.delete(0, 'end')
    
    def finishQuiz():
        conn = sqlite3.connect('quizzes.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS quizzes (quiz_name text, question text, option_a text, option_b text, option_c text, option_d text, correct_answer text)')
        for question in question_data:
            c.execute("INSERT INTO quizzes VALUES (?, ?, ?, ?, ?, ?, ?)", (quiz_name.get(), *question))
        conn.commit()
        conn.close()
        create_quiz.destroy()
        start()

    add_question_btn = Button(quiz_frame, text="Add Question", command=addQuestion, bg="black", fg="white")
    add_question_btn.pack(pady=5)

    question_text_label = Label(quiz_frame, text="Enter Question:", fg='white', bg='green')
    question_text_label.pack()
    question_text_entry = Entry(quiz_frame, bg='white', fg='black', textvariable=question_text)
    question_text_entry.pack()

    option_a_label = Label(quiz_frame, text="Option A:", fg='white', bg='black')
    option_a_label.pack()
    option_a_entry = Entry(quiz_frame, bg='white', fg='black', textvariable=option_a)
    option_a_entry.pack()

    option_b_label = Label(quiz_frame, text="Option B:", fg='white', bg='black')
    option_b_label.pack()
    option_b_entry = Entry(quiz_frame, bg='white', fg='black', textvariable=option_b)
    option_b_entry.pack()

    option_c_label = Label(quiz_frame, text="Option C:", fg='white', bg='black')
    option_c_label.pack()
    option_c_entry = Entry(quiz_frame, bg='white', fg='black', textvariable=option_c)
    option_c_entry.pack()

    option_d_label = Label(quiz_frame, text="Option D:", fg='white', bg='black')
    option_d_label.pack()
    option_d_entry = Entry(quiz_frame, bg='white', fg='black', textvariable=option_d)
    option_d_entry.pack()

    correct_answer_label = Label(quiz_frame, text="Correct Answer:", fg='white', bg='black')
    correct_answer_label.pack()
    correct_answer_entry = Entry(quiz_frame, bg='white', fg='black', textvariable=correct_answer)
    correct_answer_entry.pack()

    finish_btn = Button(quiz_frame, text="Finish Quiz", command=finishQuiz, bg="black", fg="white")
    finish_btn.pack(pady=5)

    question_data = []

def attemptQuizPage(root):
    root.destroy()
    global attempt_quiz
    attempt_quiz = Tk()
    attempt_quiz.title('Attempt Quiz')
    
    quizzes = []

    def loadQuizzes():
        conn = sqlite3.connect('quizzes.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS quizzes (quiz_name text, question text, option_a text, option_b text, option_c text, option_d text, correct_answer text)')
        c.execute('SELECT DISTINCT quiz_name FROM quizzes')
        for row in c.fetchall():
            quizzes.append(row[0])
        conn.close()

    def startQuiz(quiz_name):
        attempt_quiz.destroy()
        startQuizSession(quiz_name)

    loadQuizzes()

    quiz_canvas = Canvas(attempt_quiz, width=1000, height=700, bg="#800080")
    quiz_canvas.pack()

    quiz_frame = Frame(quiz_canvas, bg="light pink")
    quiz_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    heading = Label(quiz_frame, text="Attempt Quiz", fg="black", bg="light pink")
    heading.config(font=('calibri 60'))
    heading.pack(pady=10)

    if quizzes:
        for idx, quiz_name in enumerate(quizzes):
            btn = Button(quiz_frame, text=quiz_name, command=lambda name=quiz_name: startQuiz(name), bg="black", fg="white")
            btn.pack(pady=5)
    else:
        no_quizzes_label = Label(quiz_frame, text="No quizzes available to attempt.", fg="white", bg="pink")
        no_quizzes_label.pack()

def startQuizSession(quiz_name):
    global quiz_session
    quiz_session = Tk()
    quiz_session.title(f'Quiz: {quiz_name}')
    quiz_session.geometry('900x500')

    quiz_canvas = Canvas(quiz_session, width=1000, height=700, bg="blue")
    quiz_canvas.pack()

    quiz_frame = Frame(quiz_canvas, bg="light blue")
    quiz_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    heading = Label(quiz_frame, text=f'Quiz: {quiz_name}', fg="black", bg="light blue")
    heading.config(font=('calibri 50'))
    heading.pack(pady=20)

    conn = sqlite3.connect('quizzes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM quizzes WHERE quiz_name=?', (quiz_name,))
    questions = c.fetchall()
    conn.close()

    for idx, question in enumerate(questions, 1):
        q_text, option_a, option_b, option_c, option_d, *_ = question
        question_label = Label(quiz_frame, text=f'{idx}. {q_text}', fg="white", bg="#800080")
        question_label.pack()

        options = [option_a, option_b, option_c, option_d]
        for option in options:
            option_radio = Radiobutton(quiz_frame, text=option, variable=StringVar(), value=option, bg="light blue")
            option_radio.pack()

        # Add timer for each question
        timer_label = Label(quiz_frame, text="Time Left: ", fg="black", bg="light blue")
        timer_label.pack()

        def countdown(t):
            if t > 0:
                timer_label.configure(text=f"Time Left: {t} seconds")
                quiz_frame.after(1000, lambda: countdown(t - 1))
            else:
                # Time's up logic can be added here
                pass

        # Set timer for each question (let's say 30 seconds)
        quiz_frame.after(1000, lambda: countdown(30))

    submit_btn = Button(quiz_frame, text="Submit", command=submitQuiz, bg="black", fg="white")
    submit_btn.pack(pady=30)
    leaderboard_label = Label(quiz_frame, text="Leaderboard", fg="black", bg="#800080")
    leaderboard_label.pack()

    leaderboard = {"Player 1": 10, "Player 2": 8, "Player 3": 6, "Player 4": 4}  # Example leaderboard data

    for player, score in leaderboard.items():
        player_score_label = Label(quiz_frame, text=f"{player}: {score}", fg="black", bg="light pink")
        player_score_label.pack()


def submitQuiz():
    # Add logic to grade the quiz and display the result
    pass

def start():
    home_page = Tk()
    home_page.title('Welcome To Quiz App')

    quiz_canvas = Canvas(home_page, width=800, height=600, bg="light pink")
    quiz_canvas.pack()

    quiz_frame = Frame(quiz_canvas, bg="#800080")
    quiz_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

    heading = Label(quiz_frame, text="Welcome To Quiz App", fg="white", bg="#800080")
    heading.config(font=('calibri 40'))
    heading.pack(pady=10)

    create_quiz_button = Button(quiz_frame, text='Create Quiz', command=lambda: createQuizPage(home_page), bg="black", fg="white")
    create_quiz_button.pack(pady=5)

    attempt_quiz_button = Button(quiz_frame, text='Attempt Quiz', command=lambda: attemptQuizPage(home_page), bg="black", fg="white")
    attempt_quiz_button.pack(pady=5)

    home_page.mainloop()

start()
