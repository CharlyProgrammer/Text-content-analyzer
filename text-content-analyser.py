import os
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

def analyze_text():
    load_dotenv()
    key = os.getenv("CONTENT_SAFETY_KEY")
    endpoint = os.getenv("CONTENT_SAFETY_ENDPOINT")

    # Create a Content Safety client
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    # Open text file
    with open('content/cont-text.txt','r', encoding='utf-8') as file:
        text_content=file.read()
        
    print(text_content)    
    # Construct a request
    request = AnalyzeTextOptions(text=text_content)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    hate_result = next(item for item in response.categories_analysis if item.category == TextCategory.HATE)
    self_harm_result = next(item for item in response.categories_analysis if item.category == TextCategory.SELF_HARM)
    sexual_result = next(item for item in response.categories_analysis if item.category == TextCategory.SEXUAL)
    violence_result = next(item for item in response.categories_analysis if item.category == TextCategory.VIOLENCE)

    if hate_result:
        print(f"Hate severity: {hate_result.severity}")
    if self_harm_result:
        print(f"SelfHarm severity: {self_harm_result.severity}")
    if sexual_result:
        print(f"Sexual severity: {sexual_result.severity}")
    if violence_result:
        print(f"Violence severity: {violence_result.severity}")
    severity=''
    print('Conclusion:')
    if hate_result.severity>=4:
        
        severity+=f'{hate_result.category} severity,'
    if self_harm_result.severity>=4:
        
        severity+=f' {self_harm_result.category} severity,'
    if sexual_result.severity>=4:
        
        severity+=f' {sexual_result.category} severity,'
    if violence_result.severity>=4:
        
        severity+=f' {violence_result.category} severity,'
    print(f'the current text had very high content of {severity} please take note.')
    
    # [END analyze_text]
    

if __name__ == "__main__":
    analyze_text()