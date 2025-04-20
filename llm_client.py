import requests 


class LLMClient : 
    def __init__(self, llm_url):
        self.llm_url = llm_url

    def get_response(self, prompt):
        """
        Send a prompt to the LLM and get the response.
        
        Args:
            prompt (str): The prompt to send to the LLM.
            context (str): The context of the query.
            
        Returns:
            str: The response from the LLM.
        """
        try:
            response = requests.post(self.llm_url+"/response", json={"prompt": prompt})
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.RequestException as e:
            print(f"Error contacting LLM: {e}")
            return ""
        

        
