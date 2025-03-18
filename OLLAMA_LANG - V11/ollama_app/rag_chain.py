# ollama_app/ rag_chain.py 
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def get_rag_response(prompt_text, model_name="phi3:mini"):
    try:
        print("1. Received prompt text for Ollama:", prompt_text)  # Debug

        # Initialize the Ollama LLM with the selected model
        llm = Ollama(model=model_name)
        
        # Define the prompt template
        prompt = PromptTemplate(input_variables=["input"], template="{input}")
        
        # Create the LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Print debug statement before getting the response
        print("2. Created LLMChain for Ollama.")  # Debug
        
        # Run the chain and get the response
        response = chain.run({"input": prompt_text})
        
        # Print the response for debugging
        print("3. Ollama response:", response)  # Debug
        
        # Post-process the response to ensure it is under 100 words
        response_words = response.split()
        if len(response_words) > 100:
            response = ' '.join(response_words[:100]) + '...'
        
        return response
    
    except Exception as e:
        print(f"4. Error in Ollama RAG integration: {e}")  # Debug
        return None
