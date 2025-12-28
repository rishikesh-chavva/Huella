import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()

AZURE_AI_KEY = os.getenv("AZURE_AI_KEY")
AZURE_AI_ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")

async def analyze_invoice(file_content: bytes):
    """
    Analyzes an invoice document using Azure AI Document Intelligence.
    If Azure credentials are missing, returns a mock response for demo purposes.
    """
    if not AZURE_AI_KEY or not AZURE_AI_ENDPOINT:
        # Demo Mock Data
        return {
            "raw_text": "Invoice #1234 - Supplier: Organic Textiles Ltd. Item: 50kg Organic Cotton. Origin: Tiruppur, India.",
            "items": [{"description": "Organic Cotton", "quantity": 50.0}],
            "location": "Tiruppur, India",
            "vendor": "Organic Textiles Ltd"
        }

    try:
        document_analysis_client = DocumentAnalysisClient(
            endpoint=AZURE_AI_ENDPOINT, 
            credential=AzureKeyCredential(AZURE_AI_KEY)
        )

        poller = document_analysis_client.begin_analyze_document(
            "prebuilt-invoice", file_content
        )
        result = poller.result()

        extracted_items = []
        vendor_name = "Unknown"
        location = "Global"

        if result.vendor_name:
            vendor_name = result.vendor_name.value

        for invoice in result.documents:
            for item in invoice.fields.get("Items").value:
                description = item.value.get("Description").value if item.value.get("Description") else ""
                quantity = item.value.get("Quantity").value if item.value.get("Quantity") else 0
                extracted_items.append({
                    "description": description,
                    "quantity": float(quantity) if quantity else 0
                })
            
            # Simplified location extraction
            address = invoice.fields.get("VendorAddress")
            if address:
                location = address.value_data.content

        return {
            "raw_text": str(result.content),
            "items": extracted_items,
            "location": location,
            "vendor": vendor_name
        }
    except Exception as e:
        print(f"Azure Error: {e}")
        # Fallback to demo mock
        return {
            "raw_text": "Error processing document. Falling back to mock.",
            "items": [{"description": "Polyester", "quantity": 100.0}],
            "location": "Unknown",
            "vendor": "Unknown"
        }
