
import json
import os
import re

from pypdf import PdfReader

from app.services.gemini_service import (
    parse_document_with_gemini
)

from app.services.compliance_engine import (
    evaluate_bid
)


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract text from a PDF.
    """

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:

        try:
            text = page.extract_text()

            if text:
                pages.append(text)

        except Exception as e:

            print(
                f"Warning: Could not extract page: {e}"
            )

    final_text = "\n".join(pages).strip()

    if not final_text:
        raise ValueError(
            f"No readable text found in PDF: {pdf_path}"
        )

    return final_text


# ============================================================
# JSON CLEANING
# ============================================================

def clean_json_response(response_text: str):
    """
    Gemini sometimes returns JSON inside markdown fences.
    This function extracts the JSON safely.
    """

    if response_text is None:
        raise ValueError(
            "Gemini returned None."
        )

    text = str(response_text).strip()

    # Remove markdown code fences
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    text = text.strip()

    # Direct JSON
    try:

        return json.loads(text)

    except json.JSONDecodeError:
        pass

    # Try extracting JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:

        json_text = text[start:end + 1]

        try:

            return json.loads(json_text)

        except json.JSONDecodeError as e:

            raise ValueError(
                "Gemini response contained invalid JSON."
            ) from e

    raise ValueError(
        "Could not find valid JSON in Gemini response."
    )


# ============================================================
# PARSE ONE PDF
# ============================================================

def parse_pdf_to_json(
    pdf_path: str,
    document_type: str
):
    """
    PDF
      ↓
    Text extraction
      ↓
    Gemini parser
      ↓
    JSON
    """

    print("\n" + "=" * 60)
    print(
        f"PARSING {document_type.upper()}"
    )
    print("=" * 60)

    print(
        f"File: {os.path.basename(pdf_path)}"
    )

    # --------------------------------------------------------
    # STEP 1: PDF TEXT
    # --------------------------------------------------------

    print(
        "\n[1/2] Extracting PDF text..."
    )

    pdf_text = extract_pdf_text(
        pdf_path
    )

    print(
        f"Extracted characters: {len(pdf_text)}"
    )

    # --------------------------------------------------------
    # STEP 2: GEMINI
    # --------------------------------------------------------

    print(
        "\n[2/2] Sending document to Gemini..."
    )

    raw_response = parse_document_with_gemini(
        pdf_text
    )

    # --------------------------------------------------------
    # STEP 3: JSON
    # --------------------------------------------------------

    parsed_json = clean_json_response(
        raw_response
    )

    if not isinstance(
        parsed_json,
        dict
    ):

        raise ValueError(
            f"{document_type} parser did not return a JSON object."
        )

    # Keep source file information
    parsed_json["_source_file"] = os.path.basename(
        pdf_path
    )

    print(
        f"{document_type} JSON parsed successfully."
    )

    return parsed_json


# ============================================================
# PARSE TENDER
# ============================================================

def parse_tender(
    tender_pdf: str
):
    """
    Parse tender PDF into Tender JSON.
    """

    return parse_pdf_to_json(
        tender_pdf,
        "Tender"
    )


# ============================================================
# PARSE BIDDER
# ============================================================

def parse_bidder(
    bidder_pdf: str
):
    """
    Parse bidder PDF into Bidder JSON.
    """

    return parse_pdf_to_json(
        bidder_pdf,
        "Bidder"
    )


# ============================================================
# EVALUATE ONE BIDDER
# ============================================================

def evaluate_single_bidder(
    tender_json,
    bidder_json
):
    """
    Tender JSON + Bidder JSON
        ↓
    Rule Engine
        ↓
    Compliance result
    """

    print("\n" + "-" * 60)

    print(
        f"RULE ENGINE: "
        f"{bidder_json.get('company', 'Unknown Bidder')}"
    )

    print("-" * 60)

    evaluation = evaluate_bid(
        tender=tender_json,
        bidder=bidder_json
    )

    # Keep original bidder JSON
    evaluation["bidderJson"] = bidder_json

    evaluation["sourceFile"] = bidder_json.get(
        "_source_file"
    )

    return evaluation


# ============================================================
# BUILD COMPARISON
# ============================================================

def build_comparison(
    evaluations
):
    """
    Sort bidders by score and create
    compact comparison output.
    """

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    sorted_evaluations = sorted(
        evaluations,
        key=lambda x: x.get(
            "score",
            0
        ),
        reverse=True
    )

    comparison = []

    for position, evaluation in enumerate(
        sorted_evaluations,
        start=1
    ):

        evaluation["comparisonPosition"] = (
            position
        )

        comparison.append({

            "position": position,

            "bidderId": evaluation.get(
                "bidderId"
            ),

            "company": evaluation.get(
                "company"
            ),

            "score": evaluation.get(
                "score"
            ),

            "status": evaluation.get(
                "status"
            ),

            "riskLevel": evaluation.get(
                "riskLevel"
            ),

            "missingDocuments": evaluation.get(
                "missingDocuments",
                []
            ),

            "reasons": evaluation.get(
                "reasons",
                []
            )
        })

    return (
        sorted_evaluations,
        comparison
    )


# ============================================================
# MAIN PIPELINE
# ============================================================

def run_tender_pipeline(
    tender_pdf: str,
    bidder_pdfs: list[str]
):
    """
    COMPLETE PIPELINE

    Tender PDF
        ↓
    Tender JSON
        ↓
    3+ Bidder PDFs
        ↓
    Bidder JSONs
        ↓
    Rule Engine
        ↓
    Requirement Satisfaction
        ↓
    Score
        ↓
    Risk Level
        ↓
    Comparison
    """

    print("\n")
    print("=" * 70)
    print("             BIDSURE AI - COMPLETE PIPELINE")
    print("=" * 70)

    # ========================================================
    # VALIDATION
    # ========================================================

    if not tender_pdf:
        raise ValueError(
            "Tender PDF is required."
        )

    if not bidder_pdfs:
        raise ValueError(
            "At least 3 bidder PDFs are required."
        )

    if len(bidder_pdfs) < 3:

        raise ValueError(
            f"Minimum 3 bidder PDFs required. "
            f"Received: {len(bidder_pdfs)}"
        )

    print(
        f"\nTender PDF: "
        f"{os.path.basename(tender_pdf)}"
    )

    print(
        f"Number of bidders: "
        f"{len(bidder_pdfs)}"
    )

    # ========================================================
    # STEP 1
    # TENDER PARSING
    # ========================================================

    print("\n")
    print("=" * 70)
    print("STEP 1: TENDER PDF -> TENDER JSON")
    print("=" * 70)

    tender_json = parse_tender(
        tender_pdf
    )

    # ========================================================
    # STEP 2
    # BIDDER PARSING
    # ========================================================

    print("\n")
    print("=" * 70)
    print("STEP 2: BIDDER PDFs -> BIDDER JSON")
    print("=" * 70)

    bidder_jsons = []

    for index, bidder_pdf in enumerate(
        bidder_pdfs,
        start=1
    ):

        print(
            f"\n******** BIDDER {index} ********"
        )

        bidder_json = parse_bidder(
            bidder_pdf
        )

        bidder_jsons.append(
            bidder_json
        )

    # ========================================================
    # STEP 3
    # RULE ENGINE
    # ========================================================

    print("\n")
    print("=" * 70)
    print("STEP 3: RULE ENGINE")
    print("=" * 70)

    evaluations = []

    for bidder_json in bidder_jsons:

        evaluation = evaluate_single_bidder(
            tender_json=tender_json,
            bidder_json=bidder_json
        )

        evaluations.append(
            evaluation
        )

        print(
            f"\nBidder: "
            f"{evaluation.get('company')}"
        )

        print(
            f"Score: "
            f"{evaluation.get('score')}"
        )

        print(
            f"Status: "
            f"{evaluation.get('status')}"
        )

        print(
            f"Risk: "
            f"{evaluation.get('riskLevel')}"
        )

    # ========================================================
    # STEP 4
    # COMPARISON
    # ========================================================

    print("\n")
    print("=" * 70)
    print("STEP 4: BIDDER COMPARISON")
    print("=" * 70)

    evaluations, comparison = build_comparison(
        evaluations
    )

    # ========================================================
    # FINAL RESULT
    # ========================================================

    final_result = {

        "pipeline":
            "Tender -> 3+ Bidder PDFs -> "
            "JSON Parsing -> Rule Engine -> "
            "Requirement Satisfaction -> "
            "Risk -> Comparison",

        "tender": tender_json,

        "bidderCount": len(
            bidder_jsons
        ),

        "evaluations": evaluations,

        "comparison": comparison
    }

    # ========================================================
    # PRINT SUMMARY
    # ========================================================

    print("\n")
    print("=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print(
        f"\nTender: "
        f"{tender_json.get('bidInfo', {}).get('title', 'N/A')}"
    )

    print(
        f"Bidder Count: "
        f"{len(evaluations)}"
    )

    print("\nComparison:")

    for item in comparison:

        print(
            f"{item['position']}. "
            f"{item['company']} | "
            f"Score={item['score']} | "
            f"Status={item['status']} | "
            f"Risk={item['riskLevel']}"
        )

    return final_result
