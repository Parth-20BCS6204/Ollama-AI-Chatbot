# chroma_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .vector_store import fetch_similar_documents, add_document_to_chroma
from ollama_app.langchain_setup import get_response

@csrf_exempt
@require_http_methods(["POST"])
def upload_document(request):
    """Handle document upload and add to ChromaDB."""
    if 'pdf_file' in request.FILES:
        pdf_file = request.FILES['pdf_file']
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        pdf_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        # Add the extracted document to ChromaDB
        add_document_to_chroma(pdf_path, pdf_file.name)
        
        return JsonResponse({'status': 'success', 'message': f'Document {filename} uploaded and processed.'})

    return JsonResponse({'error': 'No file provided.'}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def fetch_similar_documents_view(request):
    """Fetch similar documents from ChromaDB."""
    query_text = request.POST.get('query_text', '').strip()

    if not query_text:
        return JsonResponse({'error': 'Query text is required.'}, status=400)

    try:
        documents = fetch_similar_documents(query_text)
        return JsonResponse({'documents': documents})
    except Exception as e:
        return JsonResponse({'error': f'Error fetching similar documents: {str(e)}'}, status=500)

def combine_text_for_ollama(query_text, similar_texts):
    context = ' '.join(similar_texts)
    # Remove any extra spaces and newlines
    context = re.sub(r'\s+', ' ', context).strip()
    combined_text = f"User Query: {query_text}\nContext: {context}\nPlease provide a concise answer, strictly under 200 words."
    return combined_text


def chatbot_view(request):
    context = {}
    similarity_check_result = None
    bot_response = None

    if request.method == 'POST':
        if 'pdf_file' in request.FILES:
            pdf_file = request.FILES['pdf_file']
            fs = FileSystemStorage()
            filename = fs.save(pdf_file.name, pdf_file)
            pdf_path = os.path.join(settings.MEDIA_ROOT, filename)
            
            # Add the extracted document to ChromaDB
            add_document_to_chroma(pdf_path, pdf_file.name)

        user_input = request.POST.get('prompt')
        if user_input:
            # Fetch documents similar to the user input from ChromaDB
            similar_documents = fetch_similar_documents(user_input, top_k=3)
            if similar_documents:
                combined_text = combine_text_for_ollama(user_input, similar_documents)
                bot_response = get_response(combined_text)
                similarity_check_result = combined_text
                print(f"Bot Response: {bot_response}")
            else:
                bot_response = "No similar documents found in ChromaDB. Please enter a different prompt."
                similarity_check_result = "No similar documents found in ChromaDB."
        else:
            bot_response = "Please enter a prompt."
        
        context['bot_response'] = bot_response
        context['similarity_check_result'] = similarity_check_result
        return JsonResponse({'bot_response': bot_response, 'similarity_check_result': similarity_check_result})

    return render(request, 'chat/chat.html', context)
