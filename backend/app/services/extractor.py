import re


def extract_requirements_from_pages(
    pages: list[dict]
) -> list[dict]:
    """
    Extract compliance requirements page-by-page.

    Each page dictionary should contain:
    {
        "page": 1,
        "text": "..."
    }
    """

    requirement_rules = [
        {
            "type": "GST",
            "patterns": [r"\bGST\b", r"Goods and Services Tax"],
            "text": "Bidder must satisfy applicable GST registration and compliance requirements.",
            "mandatory": True
        },
        {
            "type": "PAN_INCOME_TAX",
            "patterns": [r"\bPAN\b", r"Income Tax"],
            "text": "Bidder must provide valid PAN and satisfy applicable Income Tax requirements.",
            "mandatory": True
        },
        {
            "type": "MSME_UDYAM",
            "patterns": [r"Udyam", r"MSME", r"MSE"],
            "text": "Bidder claiming MSME/MSE benefits must provide valid Udyam/MSME registration evidence.",
            "mandatory": False
        },
        {
            "type": "STARTUP",
            "patterns": [r"Startup India", r"\bstartup\b"],
            "text": "Bidder claiming Startup benefits must provide applicable Startup India registration evidence.",
            "mandatory": False
        },
        {
            "type": "OEM",
            "patterns": [r"\bOEM\b", r"Original Equipment Manufacturer"],
            "text": "Bidder must satisfy applicable OEM authorization requirements.",
            "mandatory": True
        },
        {
            "type": "MAKE_IN_INDIA",
            "patterns": [
                r"Make in India",
                r"local content",
                r"Class-I local",
                r"Class-II local"
            ],
            "text": "Bidder must satisfy applicable Make in India/local content requirements.",
            "mandatory": True
        },
        {
            "type": "EPFO",
            "patterns": [r"\bEPFO\b", r"Employees.? Provident Fund"],
            "text": "Bidder must satisfy applicable EPFO registration/compliance requirements.",
            "mandatory": True
        },
        {
            "type": "ESIC",
            "patterns": [r"\bESIC\b", r"Employees.? State Insurance"],
            "text": "Bidder must satisfy applicable ESIC registration/compliance requirements.",
            "mandatory": True
        },
        {
            "type": "BLACKLIST",
            "patterns": [
                r"blacklist",
                r"blacklisted",
                r"debarred",
                r"debarment"
            ],
            "text": "Bidder must not be blacklisted or debarred by the applicable authority.",
            "mandatory": True
        },
        {
            "type": "ATC_DOCUMENT",
            "patterns": [
                r"Additional Doc",
                r"Additional Document",
                r"\bATC\b",
                r"Additional Terms and Conditions"
            ],
            "text": "Bidder must provide documents required under the applicable Additional Terms and Conditions.",
            "mandatory": True
        },
        {
            "type": "LAND_BORDER_ELIGIBILITY",
            "patterns": [
                r"land border",
                r"border sharing",
                r"countries sharing.*land border"
            ],
            "text": "Bidder must satisfy applicable eligibility conditions relating to countries sharing a land border with India.",
            "mandatory": True
        }
    ]

    results = []
    detected_types = set()

    for page_data in pages:
        page_number = page_data["page"]
        page_text = page_data["text"]

        if not page_text:
            continue

        for rule in requirement_rules:

            # Avoid duplicate requirement types
            if rule["type"] in detected_types:
                continue

            matched = False
            evidence = ""

            for pattern in rule["patterns"]:
                match = re.search(
                    pattern,
                    page_text,
                    re.IGNORECASE
                )

                if match:
                    matched = True

                    # Get a small evidence window
                    start = max(0, match.start() - 150)
                    end = min(
                        len(page_text),
                        match.end() + 250
                    )

                    evidence = page_text[start:end].strip()
                    break

            if matched:
                results.append({
                    "requirement_type": rule["type"],
                    "requirement_text": rule["text"],
                    "mandatory": rule["mandatory"],
                    "source_page": str(page_number),
                    "evidence": evidence
                })

                detected_types.add(rule["type"])

    return results