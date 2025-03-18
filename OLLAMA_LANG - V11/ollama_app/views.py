# ollama_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
import requests
from ollama_app.langchain_setup import get_response
from ollama_app.rag_chain import get_rag_response
import re

CHROMA_APP_URL = 'http://localhost:8001'  # URL of chroma_app

def combine_text_for_ollama(query_text, similar_texts):
    context = ' '.join(similar_texts)
    # Remove any extra spaces and newlines
    context = re.sub(r'\s+', ' ', context).strip()
    combined_text = f"User Query: {query_text}\nContext: {context}\nPlease provide a concise answer, strictly under 200 words."
    return combined_text

def chatbot_view(request):
    if request.method == 'POST':
        query_text = request.POST.get('query_text', '')
        ollama_model = request.POST.get('ollama_model', 'phi3:mini')

        print("Received POST request in chatbot_view")  # Debug statement
        print("Query text:", query_text)  # Debug statement
        print("Ollama model:", ollama_model)  # Debug statement

        try:
            # Fetch similar documents from ChromaDB
            response = requests.post(f'{CHROMA_APP_URL}/fetch-similar-documents/', data={'query_text': query_text})
            response.raise_for_status()  # Raise HTTPError for non-200 status codes
            documents = response.json().get('documents', [])

            # Print the fetched documents to the terminal
            print("Query Result for Similarity Check:", documents)

            # Verify the structure of documents
            if not documents:
                return JsonResponse({'error': 'No documents found in similarity check'}, status=404)

            # Combine query text and similarity check results into one variable
            combined_text = combine_text_for_ollama(query_text, documents)

            # Print the combined text for Ollama
            print("Combined Text for Ollama:", combined_text)

            # Get response from Ollama model using rag_chain
            bot_response = get_rag_response(combined_text, model_name=ollama_model)

            if bot_response is not None:
                # Print the response from Ollama
                print("Response from Ollama:", bot_response)
                return JsonResponse({'bot_response': bot_response, 'similarity_check_result': documents})
            else:
                return JsonResponse({'error': 'Error fetching response from Ollama'}, status=500)

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with services: {e}")  # Debug statement
            return JsonResponse({'error': f'Error communicating with services: {str(e)}'}, status=500)

    else:
        return render(request, 'chat/chat.html')

def check_connection(request):
    try:
        response = requests.post(f'{CHROMA_APP_URL}/fetch-similar-documents/', data={'query_text': 'test'})
        response.raise_for_status()  # Raise HTTPError for non-200 status codes

        return JsonResponse({'status': 'Connected to ChromaDB successfully', 'response': response.json()})

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to ChromaDB: {e}")  # Debug statement
        return JsonResponse({'status': 'Error connecting to ChromaDB', 'error': str(e)}, status=500)

def fetch_similarity_check(request):
    if request.method == 'POST':
        query_text = request.POST.get('query_text', '')

        if not query_text:
            return JsonResponse({'error': 'Query text is required.'}, status=400)

        print("Received POST request in fetch_similarity_check")  # Debug statement
        print("Query text:", query_text)  # Debug statement

        try:
            # Fetch similar documents from ChromaDB
            response = requests.post(f'{CHROMA_APP_URL}/fetch-similar-documents/', data={'query_text': query_text})
            response.raise_for_status()  # Raise HTTPError for non-200 status codes
            documents = response.json().get('documents', [])

            print("Query Result for Similarity Check:", documents)  # Debug statement

            return JsonResponse({'similarity_check_result': documents})

        except requests.exceptions.RequestException as e:
            print(f"Error fetching similarity check results: {e}")  # Debug statement
            return JsonResponse({'error': 'Error fetching similarity check results', 'details': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

def fetch_ollama_response(request):
    if request.method == 'POST':
        query_text = request.POST.get('query_text', '')
        ollama_model = request.POST.get('ollama_model', 'phi3:mini')

        print("Received POST request in fetch_ollama_response")  # Debug statement
        print("Query text:", query_text)  # Debug statement
        print("Ollama model:", ollama_model)  # Debug statement

        if not query_text:
            return JsonResponse({'error': 'Query text is required.'}, status=400)

        try:
            # Fetch similar documents from ChromaDB
            response = requests.post(f'{CHROMA_APP_URL}/fetch-similar-documents/', data={'query_text': query_text})
            response.raise_for_status()  # Raise HTTPError for non-200 status codes
            documents = response.json().get('documents', [])

            # Print the fetched documents to the terminal
            print("Query Result for Similarity Check:", documents)

            # Combine query text and similarity check results into one variable
            combined_text = combine_text_for_ollama(query_text, documents)

            # Print the combined text for Ollama
            print("Combined Text for Ollama:", combined_text)

            # Get response from Ollama model using langchain_setup
            print("Getting response from Ollama model...")  # Debug statement
            bot_response = get_response(combined_text, model_name=ollama_model)

            if bot_response is not None:
                print("Response from Ollama:", bot_response)  # Debug statement
                return JsonResponse({'bot_response': bot_response})
            else:
                return JsonResponse({'error': 'Error fetching response from Ollama'}, status=500)

        except requests.exceptions.RequestException as e:
            print(f"Error processing request: {e}")  # Debug statement
            return JsonResponse({'error': 'Error processing request', 'details': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
