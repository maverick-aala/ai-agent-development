# Menu maps to system prompts in ai_assistant.py — same content Days 03–06.

roles = {
    1: "The Patient Tutor: Breaks down complex subjects into simple terms. It explains difficult math problems, teaches coding languages, and creates custom quizzes tailored to your learning pace",
    2: "The Daily Lifestyle Coach: Supports your personal well-being and habits. It suggests healthy recipes based on ingredients you have, creates workout routines, and helps manage daily reminders. Also suggest only vegetarian food and keep this in mind egg is not vegetarian.",
}


def get_user_choice():
    """Read menu choice 1 or 2; return persona text for system message, or "" if invalid."""
    choiceStr = input(
        "\nChoose your assistant: \n\n 1. The Patient Tutor\n 2. The Daily Lifestyle Coach\n\nEnter your choice: "
    )

    if choiceStr.isdigit():
        choiceInt = int(choiceStr)
        if choiceInt == 1 or choiceInt == 2:
            return roles[choiceInt]
        else:
            return ""
    else:
        return ""
