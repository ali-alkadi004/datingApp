import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QComboBox, QMessageBox, QRadioButton, QButtonGroup

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_user(self, user_data):
        new_node = Node(user_data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def get_users(self):
        users = []
        current = self.head
        while current:
            users.append(current)
            current = current.next
        return users

class DatingAppUI(QWidget):
    def __init__(self):
        super().__init__()

        self.user_profiles = LinkedList()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Dating App')

        self.name_label = QLabel('Name:')
        self.name_entry = QLineEdit()

        self.age_label = QLabel('Age:')
        self.age_entry = QLineEdit()

        self.country_label = QLabel('Country:')
        self.country_entry = QLineEdit()

        self.gender_label = QLabel('Gender:')
        self.gender_dropdown = QComboBox()
        self.gender_dropdown.addItems(['Male', 'Female'])

        self.hobbies_label = QLabel('Hobbies:')
        self.hobbies_radiobuttons, self.hobbies_button_group = self.create_hobbies_radiobuttons()

        self.horoscope_label = QLabel('Horoscope:')
        self.horoscope_dropdown = QComboBox()
        self.horoscope_dropdown.addItems(['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'])

        self.criterion_label = QLabel('Choose Match Criterion:')
        self.criterion_dropdown = QComboBox()
        self.criterion_dropdown.addItems(['Hobbies', 'Age', 'Horoscope'])

        self.questions_label = QLabel('Answer the following question:')
        self.questions_dropdown = self.create_question_dropdown()

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.add_user)

        self.match_button = QPushButton('Find Match', self)
        self.match_button.clicked.connect(self.find_match)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_entry)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_entry)
        layout.addWidget(self.country_label)
        layout.addWidget(self.country_entry)
        layout.addWidget(self.gender_label)
        layout.addWidget(self.gender_dropdown)
        layout.addWidget(self.hobbies_label)
        layout.addLayout(self.hobbies_radiobuttons)
        layout.addWidget(self.horoscope_label)
        layout.addWidget(self.horoscope_dropdown)
        layout.addWidget(self.criterion_label)
        layout.addWidget(self.criterion_dropdown)
        layout.addWidget(self.questions_label)
        layout.addWidget(self.questions_dropdown)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.match_button)

        self.setLayout(layout)

    def create_hobbies_radiobuttons(self):
        hobbies = [
            "Reading",
            "Writing",
            "Sports",
            "Music",
            "Movies",
            "Cooking",
            "Traveling",
            "Gaming",
            "Art",
            "Photography",
            "Dancing",
            "Hiking",
        ]

        radiobutton_layout = QVBoxLayout()
        button_group = QButtonGroup()

        for idx, hobby in enumerate(hobbies):
            radiobutton = QRadioButton(hobby)
            radiobutton_layout.addWidget(radiobutton)
            button_group.addButton(radiobutton, idx)

        return radiobutton_layout, button_group

    def create_question_dropdown(self):
        questions = [
            "What is your ideal date?",
            "Pick a favorite movie genre:",
            "Choose a dream vacation destination:"
        ]

        dropdown = QComboBox()
        dropdown.addItems(questions)

        return dropdown

    def add_user(self):
        name = self.name_entry.text()
        age = self.age_entry.text()
        country = self.country_entry.text()
        gender = self.gender_dropdown.currentText()
        hobbies = [radiobutton.text() for radiobutton in self.hobbies_button_group.buttons() if radiobutton.isChecked()]
        horoscope = self.horoscope_dropdown.currentText()
        answer_index = self.questions_dropdown.currentIndex()

        if all([name, age, country, hobbies]):
            user_data = {
                "Name": name,
                "Age": age,
                "Country": country,
                "Gender": gender,
                "Hobbies": hobbies,
                "Horoscope": horoscope,
                "AnswerIndex": answer_index
            }

            self.user_profiles.add_user(user_data)
            QMessageBox.information(self, 'Success', 'User added successfully!')
        else:
            QMessageBox.warning(self, 'Warning', 'Please fill in all required fields (Name, Age, Country, Hobbies).')

    def find_match(self):
        if len(self.user_profiles.get_users()) < 2:
            QMessageBox.warning(self, 'Warning', 'Need at least two users for matchmaking.')
            return

        user_profiles = self.user_profiles.get_users()
        user1 = user_profiles[0].data
        user2 = user_profiles[1].data

        criterion = self.criterion_dropdown.currentText()

        if user1['Gender'] != user2['Gender']:
            if criterion == 'Hobbies':
                match_found = set(user1['Hobbies']) & set(user2['Hobbies'])
            elif criterion == 'Age':
                age_range = 5  # Adjust the range as needed
                match_found = abs(int(user1['Age']) - int(user2['Age'])) <= age_range
            elif criterion == 'Horoscope':
                match_found = user1['Horoscope'] == user2['Horoscope']
            else:
                match_found = False

            if match_found:
                user1_info = f"User 1: {user1['Name']}, Age: {user1['Age']}, Country: {user1['Country']}, Gender: {user1['Gender']}"
                user2_info = f"User 2: {user2['Name']}, Age: {user2['Age']}, Country: {user2['Country']}, Gender: {user2['Gender']}"
                QMessageBox.information(self, 'Match Found', f'Match found!\n\n{user1_info}\n\n{user2_info}')
            else:
                QMessageBox.information(self, 'No Match', 'Sorry, no match found.')
        else:
            QMessageBox.warning(self, 'Warning', 'Matchmaking only allowed between different genders.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DatingAppUI()
    window.show()
    sys.exit(app.exec_())
