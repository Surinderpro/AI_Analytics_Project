from langchain.text_splitter import RecursiveCharacterTextSplitter
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Anthropic Claude with API key from .env
claude_client = anthropic.Client(api_key=os.getenv("CLAUDE_API_KEY"))

def get_model_response(file, query):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)

    # Create context from the document's text
    context = "\n\n".join(doc.page_content for doc in file)  # Extract content properly
    data = text_splitter.split_text(context)

    # Prepare a simple retrieval using the text data
    relevant_docs = []
    for doc in data:
        if query.lower() in doc.lower():  # Simple keyword matchingp
            relevant_docs.append(doc)

    if not relevant_docs:
        return "No relevant documents found."

    # Prepare the prompt for Claude
    prompt = f"""Answer the following question based on the provided context:
    Context: {' '.join(relevant_docs)}\n
    Question: {query}\n
    Answer:"""

    try:
        response = claude_client.completion(
            prompt=anthropic.HUMAN_PROMPT + prompt + anthropic.AI_PROMPT,
            model="claude-v1",  # Use the correct Claude model version
            max_tokens_to_sample=300
        )
        return response['completion']
    except Exception as e:
        print(f"Error during Claude model processing: {e}")
        return "Error during model processing."