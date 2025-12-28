import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

AZURE_AI_KEY = os.getenv("AZURE_AI_KEY")
AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")

def extract_material_info(text: str):
    """
    Uses Azure NLP to extract specific entities related to materials and origins.
    """
    if not AZURE_AI_KEY or not AZURE_AI_ENDPOINT:
        # Simple rule-based extraction for demo if AI is unavailable
        materials = ["cotton", "polyester", "wool", "linen", "silk"]
        found_material = "Unknown"
        for m in materials:
            if m in text.lower():
                found_material = m
                break
        return {"material": found_material}

    try:
        client = TextAnalyticsClient(
            endpoint=AZURE_AI_ENDPOINT, 
            credential=AzureKeyCredential(AZURE_AI_KEY)
        )
        
        response = client.recognize_entities(documents=[text])[0]
        
        # We look for Product or Material categories
        # This logic can be expanded based on custom NER models
        extracted = {}
        for entity in response.entities:
            if entity.category in ["Product", "Material"]:
                extracted["material"] = entity.text
            if entity.category == "Location":
                extracted["location"] = entity.text
                
        return extracted
    except Exception:
        return {"material": "Unknown"}
