import streamlit as st
import ollama
from nltk.stem import PorterStemmer
import re
from config import OLLAMA_HOST, EMBEDDING_MODEL, LANGUAGE_MODEL

# Configure Ollama host
ollama.host = OLLAMA_HOST

# Load the dataset
dataset = []
with open('context.txt', 'r', encoding='utf-8') as file:
    dataset = file.readlines()

# Initialize vector database
VECTOR_DB = []

# Initialize PorterStemmer for singular/plural handling
stemmer = PorterStemmer()

def check_ollama_connection():
    try:
        ollama.embed(model=EMBEDDING_MODEL, input="test")
        return True
    except Exception as e:
        st.error(f"Cannot connect to Ollama server at {OLLAMA_HOST}. Please check if the server is running.")
        return False

def add_chunk_to_database(chunk):
    embedding = ollama.embed(model=EMBEDDING_MODEL, input=chunk)['embeddings'][0]
    VECTOR_DB.append((chunk, embedding))

for chunk in dataset:
    add_chunk_to_database(chunk)

def cosine_similarity(a, b):
    dot_product = sum([x * y for x, y in zip(a, b)])
    norm_a = sum([x ** 2 for x in a]) ** 0.5
    norm_b = sum([x ** 2 for x in b]) ** 0.5
    return dot_product / (norm_a * norm_b)

def retrieve(query, top_n=3):
    query_embedding = ollama.embed(model=EMBEDDING_MODEL, input=query)['embeddings'][0]
    similarities = []
    for chunk, embedding in VECTOR_DB:
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((chunk, similarity))
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:top_n]

def normalize_text(text):
    """Remove special characters and normalize text for matching."""
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return stemmer.stem(text.lower().strip())  # Stem and lowercase

def extract_intent(user_input):
    """Simple intent extraction logic based on keywords."""
    intents = {
        "ask_about_previous": ["what did i ask about", "previous question"],
        "follow_up": ["tell me more", "yes", "continue"],
        "seek_support": ["help", "support", "advice"],
        "learn_more": ["learn", "explain", "understand"],
    }
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in user_input.lower():
                return intent
    return "general"  # Default intent if no match is found

# Streamlit UI setup
st.title("Brigid Bloom")
st.write("Ask me a question, and I will provide a helpful response!")
st.write("I'm here to help you.")

# Check Ollama connection
if not check_ollama_connection():
    st.stop()

# Background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('background_image.png');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

if 'context' not in st.session_state:
    st.session_state.context = None  # To track the current topic

# Create a form with a text input and submit button
with st.form(key='query_form', clear_on_submit=True):
    user_input = st.text_input("Enter your question:", key='input_box')
    submit_button = st.form_submit_button("Submit")

if submit_button and user_input:
    with st.spinner('Processing your request...'):
        # Extract intent
        intent = extract_intent(user_input)

        if user_input.lower() == 'exit':
            st.write("Goodbye!")
        else:
            # Handle follow-ups and context
            if intent == "follow_up" and st.session_state.context:
                user_input = f"{user_input} (Follow-up on: {st.session_state.context})"
            elif intent == "ask_about_previous":
                topic = normalize_text(user_input.lower().replace("what did i ask about", ""))
                previous_questions = [
                    entry for entry in st.session_state.history
                    if topic in normalize_text(entry['user_input'])
                ]
                if previous_questions:
                    last_interaction = previous_questions[-1]
                    with st.chat_message("assistant"):
                        st.markdown(f"**Previous Question**: {last_interaction['user_input']}")
                        st.markdown(f"**Summarized Answer**: {last_interaction['bot_response']}")
                else:
                    with st.chat_message("assistant"):
                        st.markdown(f"No previous questions found about '{topic}'.")
                st.session_state.context = topic  # Update context
            else:
                # Retrieve knowledge based on the user input
                retrieved_knowledge = retrieve(user_input)

                # Enrich the chatbot instruction with the intent
                instruction_prompt = f'''You are a compassionate and understanding mental health support bot. Your role is to provide empathetic and helpful responses to questions, using text from the reference passage included below. 
- Be sure to respond in a complete sentence, offering clear and thoughtful guidance. 
- Use a warm, supportive, and non-judgmental tone to create a safe space for the user. 
- Explain concepts in an accessible way, avoiding technical jargon, and focus on practical, actionable advice when appropriate.
- If the reference passage is irrelevant to the user's question, you may rely on your general knowledge to offer helpful support. 
- Always encourage a sense of hope and remind users to seek professional help if their situation requires it.
- The detected intent of the user is: {intent}.
:
                {'\n'.join([f' - {chunk}' for chunk, similarity in retrieved_knowledge])}
                '''

                # Get the response from the chatbot
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    bot_response = ''
                    try:
                        stream = ollama.chat(
                            model=LANGUAGE_MODEL,
                            messages=[
                                {'role': 'system', 'content': instruction_prompt},
                                {'role': 'user', 'content': user_input},
                            ],
                            stream=True,
                        )

                        for chunk in stream:
                            bot_response += chunk['message']['content']
                            message_placeholder.markdown(f"**Bot**: {bot_response}")
                    except Exception as e:
                        st.error(f"Error getting response from Ollama: {str(e)}")
                        bot_response = "I apologize, but I'm having trouble processing your request right now. Please try again in a moment."

                # Save response and set context
                st.session_state.history.append({
                    'user_input': user_input,
                    'bot_response': bot_response
                })
                st.session_state.context = user_input  # Update context

# Display the conversation history
for entry in reversed(st.session_state.history):
    with st.chat_message("assistant"):
        st.markdown(f"**Bot**: {entry['bot_response']}")
    with st.chat_message("user"):
        st.markdown(f"**You**: {entry['user_input']}")