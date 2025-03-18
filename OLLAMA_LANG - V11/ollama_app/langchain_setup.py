#  ollama_app/lanchain_setup.py 
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def initialize_chromadb():
    # Add any initialization logic for ChromaDB here
    print("ChromaDB initialized")

def get_response(prompt_text, model_name="phi3:mini"):
    try:
        # Initialize the Ollama LLM with the selected model
        llm = Ollama(model=model_name)
        
        # Define the prompt template
        prompt = PromptTemplate(input_variables=["input"], template="{input}")
        
        # Create the LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Run the chain and get the response
        response = chain.run({"input": prompt_text})
        print(f"Ollama response: {response}")  # Debug
        
        return response
    
    except Exception as e:
        print(f"Error in Ollama integration: {e}")
        return None
