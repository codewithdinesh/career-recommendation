import streamlit as st
import requests
import sqlite3
from bardapi import Bard, SESSION_HEADERS

# API key's

cookie_header = "_ga=GA1.1.1597203599.1698520133; SID=cghsxScUlSRzW3AgdLYnIGQcw2KdnJkgffmn2ZARftN_qO5U_gLxtBILQ7h1257X6ukHLw.; __Secure-1PSID=cghsxScUlSRzW3AgdLYnIGQcw2KdnJkgffmn2ZARftN_qO5Ub8LSaPJ5u6E2LCI71N3GoA.; __Secure-3PSID=cghsxScUlSRzW3AgdLYnIGQcw2KdnJkgffmn2ZARftN_qO5UUpTZji2AZBF1__gjglCWXQ.; HSID=AMynkzozY5PsRtK5I; SSID=A7uG973LGKKbfMkZS; APISID=hbLSbLfL0riTjAHz/AaYoyEYV096HSfia-; SAPISID=qpt4uuAh8xEfeRXq/ABI63ZZSEhIFhI2C_; __Secure-1PAPISID=qpt4uuAh8xEfeRXq/ABI63ZZSEhIFhI2C_; __Secure-3PAPISID=qpt4uuAh8xEfeRXq/ABI63ZZSEhIFhI2C_; AEC=Ackid1QL-ph98Mvl74NInApOPEUYFSsiulR3vOJf6SoNv6x6Uf6dP1PtWQ; NID=511=roVtPGXBMWOabbXfAl6eCMeIXGZ9KGJ2ZUlJuOM0OSkIsF19s-SN9-qS85vqNX91QEU2u1ZKMEaaQ5MKsNpiWBmjyIINL6cqhSHstLrd9_qAtwCWAgw26ffCb0HE6-LaG7hQ6HLkudCCZlfmEjgCvVm2crsm5h2nXr4c2nAdXq9gCrR7ZL4rZsYkzeNm_Y2YIXjkVYwGglqOJSW66M4orF9smzGbR_JL1vtZSqxsCBvSkILyPDdBA0tpSBWtFo6QXOyg6gFkEb-8jkelMrYNJR5d14sYmc7tiJVvYQsOjlFfUbeCEOBtZIX_rf2UB1YVN4LnMZKRHxdzdiCCL4rrCJQumSaKACRVC7POEtgggc3hfApp6kYLLVBrm8-9LRXzUia7zPPtboPFCIeBgcYlUQrHfaGQbQHpsneJhGmZowTDCOQjvxDC1MSP8_8F21njn13GhRWT_N1t5VGj3oEHUQ; 1P_JAR=2023-11-02-05; _ga_WC57KJ50ZZ=GS1.1.1698909660.13.0.1698909662.0.0.0; __Secure-1PSIDTS=sidts-CjIBNiGH7gWGEJqAkrBjIS2TVVgBTIQkcnWdufI84WDr2C9q1vmkpUoKgRTP__IdkjgjmBAA; __Secure-3PSIDTS=sidts-CjIBNiGH7gWGEJqAkrBjIS2TVVgBTIQkcnWdufI84WDr2C9q1vmkpUoKgRTP__IdkjgjmBAA; SIDCC=ACA-OxPZEicIRDrVpLuOeGsP-1nSzExB1enEY82y9eG8mlni-bRAqQ7TSt3Upt6fqk4d_zw_BQ; __Secure-1PSIDCC=ACA-OxOmyQBEJ-ix-ArkIa8xW7FUoHTMORz8kY0YPKBSKBh3ErYm4RrAZ8l9e3-LMxCsF43CGQ; __Secure-3PSIDCC=ACA-OxNV0tGD8vraYrD0dZ8MLVxZdlnU0ghn43eMmdLfVpBq93EkJLt_C9NGyU_cDDOc-JGp-U0"
# Split cookie header into individual cookies
cookie_pairs = cookie_header.split('; ')

# st.text(cookie_pairs)
# dictionary to store the cookies
cookie_dict = {}

# Iterate through the cookie pairs and split them into key-value pairs

for pair in cookie_pairs:
    # st.text(pair.split('='),1)
    key, value = pair.split('=',1)
    cookie_dict[key] = ""+value + ""

session = requests.Session()

token =  cookie_dict["__Secure-1PSID"]

session.headers = SESSION_HEADERS

for key, value in cookie_dict.items():
    session.cookies.set(key, value)

# Initialize SQLite database
conn = sqlite3.connect('career_recommendations.db')
cursor = conn.cursor()

# Create a table to store recommendations if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS career_recommendations (
        id INTEGER PRIMARY KEY,
        personality_traits TEXT,
        recommendations TEXT
    )
''')

conn.commit()

def call_bard(query):
    bard = Bard(token=token, session=session)
    answer = bard.get_answer(query)
    return (answer['content'])

# Function to delete a saved recommendation by ID
def delete_recommendation(recommendation_id):
    cursor.execute("DELETE FROM career_recommendations WHERE id=?", (recommendation_id,))
    conn.commit()

# App title and information
st.title('Career Recommendation App')
st.write("Welcome to the Career Recommendation App. Answer the following questions about your personality traits and receive career recommendations based on your answers.")

# Dictionary to map answer choices to scores
answer_to_score = {
    "Not at all": 1,
    "A little bit": 2,
    "Somewhat": 3,
    "Very": 4,
    "Extremely": 5,
}

# list of personality trait questions
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

# Asking the user the personality trait questions
user_personality_trait_scores = []
for question in personality_trait_questions:
    user_answer = st.selectbox(question, list(answer_to_score.keys()))
    user_personality_trait_scores.append(question + " " + user_answer)

# string from array selected personality
personality_traits_str = ", ".join(user_personality_trait_scores)

# Display Selected Personality Traits and values
st.write("Selected Personality Traits:")
for item in user_personality_trait_scores:
    st.write("- " + item)


# Generate Recommendation button
if st.button('Recommendation'):

    # prompt to generate recommendations
    prompt = f"Generate career recommendations based on combination of the following personality traits: {personality_traits_str} in short points."

    recommendations = call_bard(prompt)

    # Display Recommendation
    st.write(f"{recommendations}")

    st.markdown("<br>", unsafe_allow_html=True)


    # Store recommendations in the database
    cursor.execute("INSERT INTO career_recommendations (personality_traits, recommendations) VALUES (?, ?)", (personality_traits_str, recommendations))
    conn.commit()
# Spacing and break
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Display recommendations from the database
st.header("Saved Recommendations")
saved_recommendations = cursor.execute("SELECT id, personality_traits, recommendations FROM career_recommendations ORDER BY id DESC").fetchall()
for index, (id,traits, rec) in enumerate(saved_recommendations, start=1):
    st.write(f"### {index} Personality Traits:")
    st.text(traits)
    # st.write("\n\n### Personality Traits:", traits)
    st.write("\n #### Recommendations:")
    st.write(rec)

    # "Delete" button with a delete icon for each recommendation
    if st.button(f"Delete Recommendation {index}"):
        delete_recommendation(id)

        # After deletion, update the recommendations list and re-render
        saved_recommendations = cursor.execute(
            "SELECT id, personality_traits, recommendations FROM career_recommendations ORDER BY id DESC").fetchall()

    st.markdown("<hr>", unsafe_allow_html=True)

# Close the database connection
conn.close()
