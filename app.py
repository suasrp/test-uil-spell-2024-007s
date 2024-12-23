import streamlit as st
from gtts import gTTS
from playsound import playsound
from nltk.corpus import wordnet
import nltk
import random

# Download required NLTK data if not already present
nltk.download('wordnet')

# Updated list of words
words = [
    "abbreviate", "abnormality", "abode", "abrasion", "abundantly", "academic",
    "xylophone", "yacht", "yearling", "zealous", "zestfully"
]

# Create 26 tests (A-Z)
def create_tests(words_list):
    tests = {}
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        filtered_words = [word for word in words_list if word.startswith(letter)]
        tests[letter] = filtered_words
    return tests

tests = create_tests(words)

# Streamlit app class
class SpellingApp:
    def __init__(self):
        # Default background and text color
        self.bg_color = '#ffffff'  # Default background color
        self.text_color = '#000000'  # Default text color
        self.score = 0
        self.results = []
        self.incorrect_words = set()
        self.words_to_test = None
        self.current_word = None
        self.test_in_progress = False
        self.current_index = 0
        
        self.start_screen()

    def start_screen(self):
        st.markdown(f"<h1 style='color: {self.text_color}; background-color: {self.bg_color}; text-align:center;'>Spelling Test</h1>", unsafe_allow_html=True)
        
        if self.test_in_progress:
            st.write(f"Test in Progress: {self.current_word}")
        
        st.button("Start Test", on_click=self.select_test)
        st.button("View Words", on_click=self.view_words)
        st.button("Settings", on_click=self.settings)

        if self.incorrect_words:
            st.button("Review Incorrect Words", on_click=self.review_incorrect_words)

    def select_test(self):
        self.test_in_progress = True
        letter = st.selectbox("Select a Letter", list(tests.keys()))
        self.words_to_test = tests[letter]
        self.current_word = self.words_to_test[0]
        self.show_test_interface()

    def show_test_interface(self):
        st.markdown(f"<h2 style='color: {self.text_color}; background-color: {self.bg_color}; text-align:center;'>Spell the Word</h2>", unsafe_allow_html=True)
        st.write(f"Word: {self.current_word}")

        # Input field for the user to enter the spelling
        user_input = st.text_input("Spell the word:", "")
        
        # Button to check the user's input
        if st.button("Submit"):
            self.check_spelling(user_input)

    def check_spelling(self, user_input):
        if user_input.lower() == self.current_word.lower():
            self.score += 1
            st.success(f"Correct! Your score is: {self.score}")
        else:
            self.incorrect_words.add(self.current_word)
            st.error(f"Incorrect. The correct spelling is: {self.current_word}")
        
        self.next_word()

    def next_word(self):
        self.current_index += 1
        if self.current_index < len(self.words_to_test):
            self.current_word = self.words_to_test[self.current_index]
            self.show_test_interface()
        else:
            self.test_in_progress = False
            st.write(f"Test completed! Your final score is: {self.score}")
            st.button("Start New Test", on_click=self.start_screen)

    def view_words(self):
        st.markdown(f"<h2 style='color: {self.text_color}; background-color: {self.bg_color}; text-align:center;'>List of Words</h2>", unsafe_allow_html=True)
        
        for letter, words_list in tests.items():
            st.write(f"**Words starting with '{letter.upper()}':**")
            st.write(", ".join(words_list))
        
        st.button("Back to Main Menu", on_click=self.start_screen)

    def settings(self):
        st.markdown(f"<h2 style='color: {self.text_color}; background-color: {self.bg_color}; text-align:center;'>Settings</h2>", unsafe_allow_html=True)
        
        # Color pickers for background and text colors
        self.bg_color = st.color_picker("Pick a Background Color", self.bg_color)
        self.text_color = st.color_picker("Pick a Text Color", self.text_color)
        
        st.button("Back to Main Menu", on_click=self.start_screen)

    def review_incorrect_words(self):
        st.markdown(f"<h2 style='color: {self.text_color}; background-color: {self.bg_color}; text-align:center;'>Review Incorrect Words</h2>", unsafe_allow_html=True)
        
        if self.incorrect_words:
            st.write("The following words were spelled incorrectly:")
            for word in self.incorrect_words:
                st.write(word)
        else:
            st.write("You have not made any mistakes yet.")
        
        st.button("Back to Main Menu", on_click=self.start_screen)

# Initialize the app
app = SpellingApp()
