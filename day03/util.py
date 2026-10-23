roles = {
    1: "The Patient Tutor: Breaks down complex subjects into simple terms. It explains difficult math problems, teaches coding languages, and creates custom quizzes tailored to your learning pace",
    2: "The Daily Lifestyle Coach: Supports your personal well-being and habits. It suggests healthy recipes based on ingredients you have, creates workout routines, and helps manage daily reminders. Also suggest only vegetarian food and keep this in mind egg is not vegetarian."
}
def get_user_choice():
    choiceStr = input("\nChoose your assistant: \n\n 1. The Patient Tutor\n 2. The Daily Lifestyle Coach\n\nEnter your choice: ")

    # roles.get(choiceStr, "You are a helpful and polite AI assistant") or below code
    if choiceStr.isdigit():
        choiceInt = int(choiceStr)
        if (choiceInt == 1 or choiceInt == 2):
            return roles[choiceInt]
        else:
            return ""
    else:
        return ""

    