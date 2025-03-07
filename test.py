from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from paddleocr import PaddleOCR
from pdf2image import convert_from_path
from fuzzywuzzy import fuzz
import os
import re
from typing import Dict
from uuid import uuid4

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Function to extract text from images
def extract_text_from_image(image_path: str) -> str:
    result = ocr.ocr(image_path, cls=True)
    extracted_text = "\n".join([line[1][0] for line in result[0]])
    return extracted_text

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path: str) -> str:
    images = convert_from_path(pdf_path, dpi=300)
    combined_text = ""
    for idx, image in enumerate(images):
        temp_image_path = f"temp_page_{idx + 1}.jpg"
        image.save(temp_image_path, "JPEG")
        combined_text += extract_text_from_image(temp_image_path) + '\n'
        os.remove(temp_image_path)
    return combined_text

# Search and match user input with extracted text
def search_and_match(extracted_text: str, user_input: Dict[str, str], fuzzy_threshold: int = 80) -> list:
    results = []
    for field, value in user_input.items():
        if re.search(re.escape(value), extracted_text, re.IGNORECASE):
            results.append({"field": field, "value": value, "status": "Exact Match"})
        else:
            max_similarity = 0
            matched_text = None
            for extracted_line in extracted_text.splitlines():
                similarity = fuzz.ratio(value.lower(), extracted_line.lower())
                if similarity > max_similarity:
                    max_similarity = similarity
                    matched_text = extracted_line

            if max_similarity >= fuzzy_threshold:
                results.append({"field": field, "value": value, "status": f"Fuzzy Match ({max_similarity}%)", "matched_text": matched_text})
            else:
                results.append({"field": field, "value": value, "status": "Not Found", "similarity": max_similarity})
    return results

# Endpoint to verify Aadhaar or PAN card details
@app.post("/verify/")
async def verify_document(
    document_type: str = Form(...),  # Either "aadhaar" or "pan"
    name: str = Form(...),
    dob: str = Form(...),
    fathers_name = Form(None),
    gender: str = Form(None),  # Optional for PAN
    aadhaar_number: str = Form(None),  # Optional for PAN
    pan_number: str = Form(None),  # Optional for Aadhaar
    file: UploadFile = File(...)
):
    """
    API endpoint to verify Aadhaar or PAN card details.
    """

    # Save the uploaded file temporarily
    temp_filename = f"temp_{uuid4().hex}_{file.filename}"
    with open(temp_filename, "wb") as temp_file:
        temp_file.write(await file.read())

    try:
        # Check file type and extract text
        if file.filename.lower().endswith(".pdf"):
            extracted_text = extract_text_from_pdf(temp_filename)
        else:
            extracted_text = extract_text_from_image(temp_filename)

        # Define user input fields based on document type
        if document_type.lower() == "aadhaar":
            user_input = {
                "name": name,
                "dob": dob,
                "Gender": gender,
                "Aadhaar Number": aadhaar_number
            }
        elif document_type.lower() == "pan":
            user_input = {
                "name": name,
                "dob": dob,
                "father_name":fathers_name,
                "PAN Number": pan_number
            }
        else:
            return JSONResponse(content={"error": "Invalid document type. Please specify 'aadhaar' or 'pan'."}, status_code=400)

        # Perform matching
        results = search_and_match(extracted_text, user_input)

    finally:
        # Remove the temporary file
        os.remove(temp_filename)

    # Return the results
    return {
        "Document Type": document_type.capitalize(),
        "User Input": user_input,
        "Extracted Text": extracted_text,
        "Results": results
    }
