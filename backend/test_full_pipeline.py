import json
from pypdf import PdfReader

from app.services.gemini_service import (
    parse_document_with_gemini,
    evaluate_bid_with_gemini
)


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def read_pdf(pdf_path: str) -> str:

    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text() or ""

        if text.strip():
            pages.append(text)

    return "\n".join(pages)


# ============================================================
# GEMINI JSON CLEANER
# ============================================================

def clean_json_response(response: str) -> dict:

    response = response.strip()

    # Remove ```json and ```
    if response.startswith("```json"):
        response = response[7:]

    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    return json.loads(response)


# ============================================================
# PDF PATHS
# ============================================================

# YOUR TENDER PDF
TENDER_PDF = r"C:\Users\NAINA\Downloads\GeM-Bidding-9828351.pdf"


# ============================================================
# IMPORTANT:
# Put your actual BIDDER PDF path here.
#
# Example:
# BIDDER_PDF = r"C:\Users\NAINA\Downloads\ABC-Technologies-Bid.pdf"
# ============================================================

BIDDER_PDF = r"C:\Users\NAINA\Downloads\bidder_submission.pdf"


# ============================================================
# STEP 1 — READ TENDER PDF
# ============================================================

print("\n================================")
print("STEP 1: Reading Tender PDF")
print("================================")

tender_text = read_pdf(TENDER_PDF)

print("Tender PDF text extracted.")
print("Characters:", len(tender_text))


# ============================================================
# STEP 2 — PARSE TENDER PDF
# ============================================================

print("\n================================")
print("STEP 2: Gemini Tender Parser")
print("================================")

tender_response = parse_document_with_gemini(
    tender_text
)

print("\n========== TENDER PARSER RESULT ==========\n")
print(tender_response)


bid_requirements = clean_json_response(
    tender_response
)


print("\n================================")
print("Parsed Tender JSON")
print("================================")

print(
    json.dumps(
        bid_requirements,
        indent=2
    )
)


# ============================================================
# STEP 3 — READ BIDDER PDF
# ============================================================

print("\n================================")
print("STEP 3: Reading Bidder PDF")
print("================================")

bidder_text = read_pdf(BIDDER_PDF)

print("Bidder PDF text extracted.")
print("Characters:", len(bidder_text))


# ============================================================
# STEP 4 — PARSE BIDDER PDF
# ============================================================

print("\n================================")
print("STEP 4: Gemini Bidder Parser")
print("================================")

bidder_response = parse_document_with_gemini(
    bidder_text
)

print("\n========== BIDDER PARSER RESULT ==========\n")
print(bidder_response)


bidder_submission = clean_json_response(
    bidder_response
)


print("\n================================")
print("Parsed Bidder JSON")
print("================================")

print(
    json.dumps(
        bidder_submission,
        indent=2
    )
)


# ============================================================
# STEP 5 — RULE ENGINE
# ============================================================

print("\n================================")
print("STEP 5: Rule Engine")
print("================================")


rule_result = evaluate_bid_with_gemini(

    json.dumps(
        bid_requirements,
        indent=2
    ),

    json.dumps(
        bidder_submission,
        indent=2
    )
)


print("\n========== FINAL RULE ENGINE RESULT ==========\n")

print(rule_result)


# ============================================================
# STEP 6 — FINAL JSON
# ============================================================

try:

    final_result = clean_json_response(
        rule_result
    )

except Exception:

    print("\nWARNING: Gemini returned non-standard JSON.")

    final_result = {
        "raw_result": rule_result
    }


print("\n================================")
print("FINAL JSON")
print("================================")

print(
    json.dumps(
        final_result,
        indent=2
    )
)