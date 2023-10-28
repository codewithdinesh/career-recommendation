import streamlit as st
from bardapi import Bard

# Set your OpenAI API key here
api_key = 'cghsxScUlSRzW3AgdLYnIGQcw2KdnJkgffmn2ZARftN_qO5Ub8LSaPJ5u6E2LCI71N3GoA.'

def call_bard(query):
    bard = Bard(token=api_key)
    answer = bard.get_answer(query)
    return (answer['content'])

# App title and information
st.title('Career Recommendation App')
st.write("Welcome to the Career Recommendation App. Answer the following questions about your personality traits and receive career recommendations based on your answers.")


# dictionary to map answer choices to scores
answer_to_score = {
    "Not at all": 1,
    "A little bit": 2,
    "Somewhat": 3,
    "Very": 4,
    "Extremely": 5,
}

# Create a list of personality trait questions
personality_trait_questions = [
    "How outgoing are you?",
    "How creative are you?",
    "How analytical are you?",
    "How detail-oriented are you?",
    "How empathetic are you?",
    "How risk-taking are you?",
    "How logical are you?",
    "How adventurous are you?",
    "How methodical are you?",
    "How flexible are you?",
]

# Ask the user the personality trait questions
user_personality_trait_scores = []
for question in personality_trait_questions:
    user_answer = st.selectbox(question, list(answer_to_score.keys()))
    user_personality_trait_scores.append(answer_to_score[user_answer])

# Add a "Recommendation" button
if st.button('Recommendation'):
    user_personality_traits = [question.lower() for question, score in zip(personality_trait_questions, user_personality_trait_scores) if score > 2]

    if user_personality_traits:
        personality_traits_str = ", ".join(user_personality_traits)

        prompt = f"Generate career recommendations based on the following personality traits: {personality_traits_str}."

        recommendations = call_bard(prompt)
        st.write(f"Recommended careers: {recommendations}")
    else:
        st.write("Please select at least one personality trait.")
