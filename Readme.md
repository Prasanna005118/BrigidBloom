# **Brigid Bloom: Mental Health Support Chatbot**

Brigid Bloom is a compassionate, understanding, and supportive chatbot designed to assist users with mental health-related queries. It provides empathetic and helpful responses using a combination of a retrieval-augmented generation (RAG) framework and intent extraction to enhance user interaction and provide meaningful answers.

## **Features**
- **Retrieval-Augmented Responses**: Retrieves the most relevant information from a predefined knowledge base to provide contextually accurate answers.
- **Intent Recognition**: Dynamically detects user intent (e.g., follow-ups, previous question reference, or seeking support) to tailor responses effectively.
- **Warm and Supportive Tone**: Responds with empathy and encouragement, creating a safe and welcoming space for users.
- **Conversation History**: Maintains a record of user queries and responses for continuity and context.
- **Customizable Background**: Offers a visually appealing UI with support for background images.

---

## **Getting Started**

### **Prerequisites**
- Python 3.8 or higher
- Libraries: 
  - `streamlit`
  - `ollama`
  - `nltk`
  - `re`
- A dataset file named `context.txt` containing the knowledge base.
- Access to embedding and language models hosted on Hugging Face:
  - Embedding model: `CompendiumLabs/bge-base-en-v1.5-gguf`
  - Language model: `bartowski/Llama-3.2-1B-Instruct-GGUF`

### **Installation**
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/brigid-bloom.git
   cd brigid-bloom
   ```

2. Install the required Python packages:
   ```bash
   pip install streamlit ollama nltk
   ```

3. Download and configure the models:
   - Ensure you have access to the Hugging Face models mentioned in the code.
   - Set up API access for `ollama` if required.

4. Prepare your knowledge base:
   - Create a file named `context.txt` with your knowledge chunks (one chunk per line).

5. (Optional) Add a background image:
   - Place an image named `background_image.png` in the project root directory.

---

### **Running the App**
1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open the app in your browser at `http://localhost:8501`.

---

## **Usage**
1. **Ask a Question**: Enter a query in the text box and press "Submit."
2. **Follow-up Questions**: Reference your previous question or ask for additional details.
3. **Intent Detection**: The bot identifies your intent (e.g., asking about previous questions or seeking support) and adjusts its response accordingly.
4. **Exit**: Type `exit` to end the session.

---

## **File Structure**
```plaintext
brigid-bloom/
├── app.py                # Main application code
├── context.txt           # Knowledge base
├── background_image.png  # Optional background image
├── README.md             # Documentation
```

---

## **Customization**
- **Knowledge Base**: Update the `context.txt` file with new knowledge chunks.
- **Background Image**: Replace `background_image.png` with an image of your choice.
- **Intent Keywords**: Modify the `extract_intent()` function to include additional intents or keywords.

---

## **Technical Details**
- **Embedding Model**: Generates vector representations for text chunks and user queries for similarity comparisons.
- **Cosine Similarity**: Measures the relevance of knowledge chunks to the user query.
- **Streamlit UI**: Provides an interactive interface for user input and conversation history display.
- **NLP Pipeline**: Uses `nltk`'s `PorterStemmer` for text normalization to improve matching.

---

## **Future Enhancements**
- Add multilingual support for global accessibility.
- Implement advanced sentiment analysis for improved emotional intelligence.
- Enhance the knowledge base with dynamic updates from external sources.
- Integrate with professional mental health resources.

---

## **License**
This project is licensed under the MIT License. Feel free to use, modify, and distribute it.

---

## **Acknowledgments**
Special thanks to:
- [Hugging Face](https://huggingface.co) for providing excellent NLP models.
- The creators of `Streamlit` for enabling rapid web app development.