You said:
import tkinter as tk
from tkinter import simpledialog
from tkinter import Scrollbar
from tkinter.scrolledtext import ScrolledText
import nltk
from nltk.tokenize import word_tokenize
import webbrowser
import speech_recognition as sr
import pyttsx3
from tkinter import Text

class CollegeInfo:

    def __init__(self):
        self.branches = {
            "Computer Science": 120,
            "Mechanical": 120,
            "Electronics and Telecommunications": 120,
            "Information Technology": 60,
            "Artificial Intelligence and Data Science": 60
        }
        self.location = "Mumbai, Andheri"
        self.programs_offered = ["Bachelor of Engineering (B.E.) and Master of Engineering(M.E.)"]
        self.admission_process = "Admissions are based on entrance exams of MHT-CET and JEE Main."
        self.fee_structure = "The fees are approximately 125900 for four years for all branches.It may vary depending on the year. Please visit our website or contact the college for detailed fee information."
        self.events = "We organize various events throughout the year, including technical fest Icarus, cultural fest Zodiac, and sports fest Olympia."
        self.committees = "We have several committees, including the student council, technical committee, and cultural committee and other departmental committees made by the students themselves"
        self.autonomy = "The college is affiliated with The University of Mumbai i.e. non-autonomous."
        self.placements = "The college has a strong placement record. Many reputed companies visit the campus for recruitment."
        self.recruiters = "Some of the top recruiters include TCS, L&T, Mahindra, Capgemini, and many more."
        self.timings = "The timings of the college are 8:30 to 4:30 pm."

    def get_branches(self):
        return self.branches

    def get_location(self):
        return self.location

    def get_programs_offered(self):
        return self.programs_offered

    def get_admission_process(self):
        return self.admission_process

    def get_fee_structure(self):
        return self.fee_structure

    def get_events(self):
        return self.events

    def get_committees(self):
        return self.committees

    def get_autonomy(self):
        return self.autonomy

    def get_placements(self):
        return self.placements

    def get_recruiters(self):
        return self.recruiters

    def get_timings(self):
        return self.timings

    def get_seat_number(self, branch):
        if branch in self.branches:
            return self.branches[branch]
        else:
            return "Branch not found"

college_info = CollegeInfo()

def store_feedback(feedback):
    with open('feedback.txt', 'a') as file:
        file.write(feedback + "\n")

def store_unanswered(question):
    with open('unanswered_questions.txt', 'a') as file:
        file.write(question + "\n")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        speak("Listening...")
        try:
            audio = r.listen(source)
            user_input = r.recognize_google(audio)
            user_input_text.delete("1.0", "end")
            user_input_text.insert("1.0", user_input)
        except sr.UnknownValueError:
            user_input_text.delete("1.0", "end")
            user_input_text.insert("1.0", "I couldn't understand you. Please try again.")
            speak("I couldn't understand you. Please try again.")
        except sr.RequestError:
            user_input_text.delete("1.0", "end")
            user_input_text.insert("1.0", "Sorry, there was an issue with the speech recognition service.")
            speak("Sorry, there was an issue with the speech recognition service.")

def handle_user_input():
    user_input = user_input_text.get("1.0", "end-1c").lower()
    response = ""
    link_clicked = False

    tokens = word_tokenize(user_input)

    if 'branches' in tokens or 'seats' in tokens:
        response = "\nAvailable Branches and Seats:\n"
        for branch, seats in college_info.get_branches().items():
            response += f"- {branch}: {seats} seats\n"

    elif 'branch' in tokens and 'seat' in tokens:
        branch_name = ' '.join(tokens[tokens.index('seat') + 1:])
        seat_number = college_info.get_seat_number(branch_name)
        response = f"{branch_name} has {seat_number} seats."

    elif 'location' in tokens or 'address' in tokens:
        response = f"\nLocation:\n- The college is located in {college_info.get_location()}"

    elif 'programs' in tokens:
        programs = college_info.get_programs_offered()
        response = "\nPrograms Offered:\n"
        for program in programs:
            response += f"- {program}\n"

    elif 'admission' in tokens:
        response = f"\nAdmission Process:\n- {college_info.get_admission_process()}"

    elif 'fee' in tokens :
        response = f"\nFee Structure:\n- {college_info.get_fee_structure()}"

    elif 'events' in tokens:
        response = f"\nEvents:\n- {college_info.get_events()}"

    elif 'committees' in tokens:
        response = f"\nCommittees:\n- {college_info.get_committees()}"

    elif 'autonomy' in tokens or 'autonomous' in tokens:
        response = f"\nCollege Autonomy:\n- {college_info.get_autonomy()}"

    elif 'placements' in tokens or 'placement' in tokens:
        response = f"\nPlacements:\n- {college_info.get_placements()}"

    elif 'recruiters' in tokens or 'recruiter' in tokens:
        response = f"\nRecruiters:\n- {college_info.get_recruiters()}"

    elif 'timing' in tokens or 'timings' in tokens:
        response = f"\nTimings:\n- {college_info.get_timings()}"

    elif 'exit' in tokens:
        response = "Thank you for visiting!"

        chat_text.insert("end", f"Bot: {response}\n", 'https://www.mctrgit.ac.in/')

        user_feedback = simpledialog.askstring("Feedback", "Please provide your feedback:")
        if user_feedback:
           store_feedback(user_feedback)
        root.quit()

    elif 'website' in tokens:
        response =  f"[College Website](https://www.mctrgit.ac.in/)\n"
        link_clicked = True

    elif 'instagram' in tokens:
        response = "\nCollege Instagram Profile:\n- [College Instagram Handle](https://instagram.com/mctrgitofficial?igshid=MzMyNGUyNmU2YQ==)"
        link_clicked = True

    else:

        response = "I'm sorry, I don't understand that. Please ask about branch,autonomy,committee,placements,timings,etc ."
        store_unanswered(user_input)
    chat_text.insert("end", '\n')
    chat_text.insert("end", '\n')
    user_input_text.delete("1.0", "end")
   

    chat_text.config(state=tk.NORMAL)
    chat_text.insert("end", f"You: {user_input}\n")
    if link_clicked:
        chat_text.tag_add("link", "end-50c", "end")
        chat_text.tag_config("link", foreground="blue", underline=True)
        chat_text.bind("<Button-1>", lambda e: open_link(e, chat_text))
    chat_text.insert("end", f"Bot: {response}\n")
    chat_text.config(state=tk.DISABLED)
    user_input_text.delete("1.0", "end")
    speak(response) 

def open_link(event, text_widget):
    index = text_widget.index(tk.CURRENT)
    text = text_widget.get(tk.CURRENT, f"{index} lineend")
    if text.startswith("http://") or text.startswith("https://"):
        webbrowser.open(text)

def start_listening():
    recognize_speech()
    handle_user_input()

root = tk.Tk()
root.title("College Information Chatbot")
root.configure(bg="#BEADFA")

welcome_label = tk.Label(root, text="Welcome to Rajiv Gandhi Institute of Technology, how may I help you today?", font=("Sherif", 14), bg="#D0BFFF")
welcome_label.pack()

chat_text = ScrolledText(root, wrap=tk.WORD, width=200, height=40 ,bg="#DFCCFB")
chat_text.pack()

user_input_text = tk.Text(root, wrap=tk.WORD, width=100, height=4 ,bg="white")
user_input_text.pack()

send_button = tk.Button(root, text="Send", command=handle_user_input)
send_button.pack()

listen_button = tk.Button(root, text="Listen", command=start_listening)
listen_button.pack()

root.mainloop()