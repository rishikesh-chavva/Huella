# Huella Backend - Sustainability Passport API

Huella is a backend service designed to automate the creation of Digital Product Passports. It uses Azure AI Document Intelligence to extract material data from supplier invoices/documents and calculates the estimated carbon footprint (CO2e) based on recognized emission factors.

## Features
- **Automated Extraction**: Upload PDF/Image invoices and extract material types and quantities.
- **Carbon Calculation**: Automatic CO2 mapping based on material properties.
- **Digital Passport**: Persistent storage of product sustainability data.
- **Dashboard API**: Real-time summary of environmental impact across a company's portfolio.
- **Secure Auth**: JWT-based authentication for corporate users.

## Prerequisites
- Python 3.9 or higher
- (Optional) Azure AI Services Account (Document Intelligence & Text Analytics)

## Installation

1. Clone the project and navigate to the directory.
2. Create a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
    pip install -r requirements.txt

4. Configure environment:
    cp .env.example .env
    # Edit .env and add your JWT_SECRET and Azure keys if available.
    # If Azure keys are left blank, the app runs in 'Demo Mock Mode'.

## Running the Application

Start the FastAPI server:
    uvicorn main:app --reload

The API will be available at `http://localhost:8000`.
Interactive documentation (Swagger UI) is at `http://localhost:8000/docs`.

## Usage Flow
1. **Register/Login**: Use `/auth/register` then `/auth/login` to get a Bearer Token.
2. **Upload Document**: Use `/documents/upload` to send an invoice.
3. **View Passports**: Use `/passports/` to see the generated sustainability records.
4. **Dashboard**: Use `/dashboard/summary` to see total impact.

## Project Structure
- `main.py`: Entry point and middleware.
- `models.py`: Database schema (SQLAlchemy).
- `schemas.py`: Validation models (Pydantic).
- `auth.py`: JWT & security logic.
- `ai/`: AI processing logic (Azure & Carbon Math).
- `routers/`: API endpoints grouped by feature.

## Troubleshooting
- **Database Errors**: The app uses SQLite by default. Ensure the folder has write permissions.
- **Azure AI**: If extraction fails, ensure your `AZURE_AI_ENDPOINT` includes the protocol (https://) and your key is valid.
