from .qa_system import QASystem

qa = QASystem()

def ask(question: str, max_context=3):
    return qa.answer_question(question, max_context=max_context)