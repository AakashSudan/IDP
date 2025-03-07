from fastapi import FastAPI, File, Form, UploadFile
import os
import re
from paddleocr import PaddleOCR

app = FastAPI()

def extract_information(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(image_path, cls=True)

    extracted_text = ""
    for line in result[0]:
        text = line[1][0]
        extracted_text += text + '\n'

    return extracted_text

def search_and_match(extracted_text, user_input):
    results = []
    for field, value in user_input.items():
        if re.search(re.escape(value), extracted_text, re.IGNORECASE):
            results.append(f"For {field}, value: '{value}' found successfully.")
        else:
            results.append(f"For {field}, value: '{value}' not found.")
    return results

# FastAPI route for Aadhaar and PAN card verification
@app.post("/verify/")
async def verify_document(
    document_type: str = Form(...),  # Either "aadhaar" or "pan"
    name: str = Form(...),
    dob: str = Form(...),
    gender: str = Form(None),  # Optional for PAN
    aadhaar_number: str = Form(None),  # Optional for PAN
    pan_number: str = Form(None),  # Optional for Aadhaar
    file: UploadFile = File(...)
):
    """
    API endpoint to verify Aadhaar or PAN card details.
    """

    image_path = f"temp_{file.filename}"
    with open(image_path, "wb") as f:
        f.write(await file.read())

    try:

        extracted_text = extract_information(image_path)

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
                "PAN Number": pan_number
            }
        else:
            return {"error": "Invalid document type. Please specify 'aadhaar' or 'pan'."}

        results = search_and_match(extracted_text, user_input)

    finally:
        
        os.remove(image_path)

    return {
        "Document Type": document_type.capitalize(),
        "User Input": user_input,
        "Extracted Text": extracted_text,
        "Results": results
    }
