import re


# ============================================================
# HELPERS
# ============================================================

def normalize(text):
    if text is None:
        return ""

    text = str(text).lower()

    text = text.replace("_", " ")
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def get_technical_value(bidder, parameter_names):
    """
    Bidder technicalData se matching parameter ki value nikalta hai.
    """

    technical_data = bidder.get("technicalData", [])

    for item in technical_data:

        parameter = normalize(
            item.get("parameter", "")
        )

        for name in parameter_names:

            if normalize(name) in parameter:

                return item.get("value")

    return None


def extract_number(value):

    if value is None:
        return None

    match = re.search(
        r"\d+(?:\.\d+)?",
        str(value)
    )

    if not match:
        return None

    return float(match.group())


# ============================================================
# DOCUMENT MATCHING
# ============================================================

def document_matches(required_name, bidder_document):
    """
    Flexible document name matching.
    """

    required = normalize(required_name)

    name = normalize(
        bidder_document.get("name", "")
    )

    status = normalize(
        bidder_document.get("status", "")
    )

    verified = bidder_document.get(
        "verified",
        False
    )

    # Must actually be submitted/verified
    if status in [
        "not submitted",
        "rejected",
        "expired",
        "defective",
        "incomplete"
    ]:
        return False

    if not verified:
        return False

    # Exact-ish matching
    if required in name or name in required:
        return True

    # Special mappings
    mappings = {

        "experience criteria documents": [
            "experience certificates",
            "experience certificate",
            "experience documents"
        ],

        "section 3 submission": [
            "atc section 3",
            "atc section 3 form",
            "section 3 form"
        ],

        "section 8 submission": [
            "atc section 8",
            "atc section 8 form",
            "section 8 form"
        ]
    }

    alternatives = mappings.get(
        required,
        []
    )

    for alternative in alternatives:

        if normalize(alternative) in name:
            return True

    return False


# ============================================================
# MANDATORY DOCUMENT CHECK
# ============================================================

def check_mandatory_documents(
    tender,
    bidder
):

    required_documents = tender.get(
        "requiredDocuments",
        []
    )

    bidder_documents = bidder.get(
        "documents",
        []
    )

    verified_documents = []
    missing_documents = []

    for required in required_documents:

        if not required.get(
            "mandatory",
            False
        ):
            continue

        required_name = required.get(
            "name",
            ""
        )

        found = False

        for bidder_document in bidder_documents:

            if document_matches(
                required_name,
                bidder_document
            ):

                found = True
                break

        if found:

            verified_documents.append(
                required_name
            )

        else:

            missing_documents.append(
                required_name
            )

    if len(required_documents) == 0:

        score = 100

    else:

        score = (
            len(verified_documents)
            / len(required_documents)
        ) * 100

    return {
        "score": round(score, 2),
        "verifiedDocuments": verified_documents,
        "missingDocuments": missing_documents
    }


# ============================================================
# EXPERIENCE CHECK
# ============================================================

def check_experience(
    tender,
    bidder
):

    eligibility = tender.get(
        "eligibility",
        {}
    )

    required = eligibility.get(
        "minimumExperienceYears"
    )

    experience_required = eligibility.get(
        "experienceRequired",
        False
    )

    bidder_experience = bidder.get(
        "experience",
        {}
    )

    years = bidder_experience.get(
        "years"
    )

    # No experience requirement
    if not experience_required:

        return {
            "applicable": False,
            "score": 100,
            "status": "NOT_APPLICABLE",
            "years": years
        }

    # Experience required but no minimum specified
    if required is None:

        if years is not None and years > 0:

            return {
                "applicable": True,
                "score": 100,
                "status": "SATISFIED",
                "years": years,
                "minimumRequired": None
            }

        return {
            "applicable": True,
            "score": 0,
            "status": "NOT_SATISFIED",
            "years": years,
            "minimumRequired": None
        }

    if years is None:

        return {
            "applicable": True,
            "score": 0,
            "status": "NOT_SATISFIED",
            "years": None,
            "minimumRequired": required
        }

    if float(years) >= float(required):

        return {
            "applicable": True,
            "score": 100,
            "status": "SATISFIED",
            "years": years,
            "minimumRequired": required
        }

    return {
        "applicable": True,
        "score": 0,
        "status": "NOT_SATISFIED",
        "years": years,
        "minimumRequired": required
    }


# ============================================================
# TECHNICAL CHECK
# ============================================================

def check_technical(
    tender,
    bidder
):

    requirements = tender.get(
        "technicalRequirements",
        []
    )

    if not requirements:

        return {
            "applicable": False,
            "score": 100,
            "status": "NOT_APPLICABLE",
            "requirements": []
        }

    results = []

    total_score = 0

    for requirement in requirements:

        parameter = requirement.get(
            "parameter",
            ""
        )

        required_value = requirement.get(
            "value",
            ""
        )

        supplied_value = get_technical_value(
            bidder,
            [
                parameter,
                "Item Category",
                "Item Description",
                "Item Category / Specification"
            ]
        )

        if supplied_value is None:

            result = {
                "parameter": parameter,
                "required": required_value,
                "supplied": None,
                "status": "MISSING",
                "score": 0
            }

            results.append(result)
            continue

        required_normalized = normalize(
            required_value
        )

        supplied_normalized = normalize(
            supplied_value
        )

        if (
            required_normalized
            == supplied_normalized
        ):

            score = 100
            status = "MATCH"

        elif (
            required_normalized
            in supplied_normalized
            or supplied_normalized
            in required_normalized
        ):

            score = 100
            status = "MATCH"

        else:

            score = 0
            status = "MISMATCH"

        total_score += score

        results.append({

            "parameter": parameter,

            "required": required_value,

            "supplied": supplied_value,

            "status": status,

            "score": score
        })

    score = (
        total_score / len(requirements)
    )

    status = (
        "SATISFIED"
        if score == 100
        else "NOT_SATISFIED"
    )

    return {
        "applicable": True,
        "score": round(score, 2),
        "status": status,
        "requirements": results
    }


# ============================================================
# DELIVERY CHECK
# ============================================================

def check_delivery(
    tender,
    bidder
):

    required_days = tender.get(
        "bidInfo",
        {}
    ).get(
        "deliveryDays"
    )

    supplied_value = get_technical_value(
        bidder,
        [
            "Delivery Period",
            "Offered Delivery Period",
            "Delivery"
        ]
    )

    supplied_days = extract_number(
        supplied_value
    )

    if required_days is None:

        return {
            "applicable": False,
            "score": 100,
            "status": "NOT_APPLICABLE"
        }

    if supplied_days is None:

        return {
            "applicable": True,
            "score": 0,
            "status": "NOT_SATISFIED",
            "required": required_days,
            "supplied": None
        }

    if supplied_days <= required_days:

        return {
            "applicable": True,
            "score": 100,
            "status": "SATISFIED",
            "required": required_days,
            "supplied": supplied_days
        }

    return {
        "applicable": True,
        "score": 0,
        "status": "NOT_SATISFIED",
        "required": required_days,
        "supplied": supplied_days
    }


# ============================================================
# QUANTITY CHECK
# ============================================================

def check_quantity(
    tender,
    bidder
):

    required_quantity = tender.get(
        "bidInfo",
        {}
    ).get(
        "quantity"
    )

    supplied_value = get_technical_value(
        bidder,
        [
            "Quantity"
        ]
    )

    supplied_quantity = extract_number(
        supplied_value
    )

    if required_quantity is None:

        return {
            "applicable": False,
            "score": 100,
            "status": "NOT_APPLICABLE"
        }

    if supplied_quantity is None:

        return {
            "applicable": True,
            "score": 0,
            "status": "NOT_SATISFIED",
            "required": required_quantity,
            "supplied": None
        }

    if supplied_quantity >= required_quantity:

        return {
            "applicable": True,
            "score": 100,
            "status": "SATISFIED",
            "required": required_quantity,
            "supplied": supplied_quantity
        }

    return {
        "applicable": True,
        "score": 0,
        "status": "NOT_SATISFIED",
        "required": required_quantity,
        "supplied": supplied_quantity
    }


# ============================================================
# OEM / MSE
# ============================================================

def check_oem_mse(
    tender,
    bidder
):

    eligibility = tender.get(
        "eligibility",
        {}
    )

    oem_required = eligibility.get(
        "oemRequired",
        False
    )

    mse_preference = eligibility.get(
        "msePreference",
        False
    )

    is_oem = bidder.get(
        "isOEM",
        False
    )

    udyam = bidder.get(
        "udyam"
    )

    if oem_required:

        if is_oem:

            return {
                "applicable": True,
                "score": 100,
                "status": "OEM_ELIGIBLE",
                "isOEM": True,
                "udyam": udyam
            }

        return {
            "applicable": True,
            "score": 0,
            "status": "OEM_NOT_ELIGIBLE",
            "isOEM": False,
            "udyam": udyam
        }

    if mse_preference:

        if udyam:

            return {
                "applicable": True,
                "score": 100,
                "status": "MSE_ELIGIBLE",
                "isOEM": is_oem,
                "udyam": udyam
            }

        if is_oem:

            return {
                "applicable": True,
                "score": 100,
                "status": "OEM_ELIGIBLE",
                "isOEM": True,
                "udyam": None
            }

        return {
            "applicable": True,
            "score": 0,
            "status": "NO_MSE_PROOF",
            "isOEM": False,
            "udyam": None
        }

    return {
        "applicable": False,
        "score": 100,
        "status": "NOT_APPLICABLE",
        "isOEM": is_oem,
        "udyam": udyam
    }


# ============================================================
# RULE ENGINE
# ============================================================

def evaluate_bid(
    tender,
    bidder
):

    mandatory = check_mandatory_documents(
        tender,
        bidder
    )

    experience = check_experience(
        tender,
        bidder
    )

    technical = check_technical(
        tender,
        bidder
    )

    delivery = check_delivery(
        tender,
        bidder
    )

    quantity = check_quantity(
        tender,
        bidder
    )

    oem_mse = check_oem_mse(
        tender,
        bidder
    )

    # --------------------------------------------------------
    # WEIGHTS
    # --------------------------------------------------------

    weights = {

        "mandatoryDocuments": 30,

        "experience": 15,

        "technicalMatch": 25,

        "delivery": 15,

        "quantity": 5,

        "oemMse": 10
    }

    score_breakdown = {

        "mandatoryDocuments":
            mandatory["score"]
            * weights["mandatoryDocuments"]
            / 100,

        "experience":
            experience["score"]
            * weights["experience"]
            / 100,

        "technicalMatch":
            technical["score"]
            * weights["technicalMatch"]
            / 100,

        "delivery":
            delivery["score"]
            * weights["delivery"]
            / 100,

        "quantity":
            quantity["score"]
            * weights["quantity"]
            / 100,

        "oemMse":
            oem_mse["score"]
            * weights["oemMse"]
            / 100
    }

    score = round(
        sum(score_breakdown.values()),
        2
    )

    # --------------------------------------------------------
    # REASONS
    # --------------------------------------------------------

    reasons = []

    for document in mandatory[
        "missingDocuments"
    ]:

        reasons.append(
            f"Mandatory document missing: {document}"
        )

    if (
        delivery.get("status")
        == "NOT_SATISFIED"
    ):

        reasons.append(
            f"Delivery period of "
            f"{delivery.get('supplied')} days "
            f"exceeds required "
            f"{delivery.get('required')} days."
        )

    if (
        quantity.get("status")
        == "NOT_SATISFIED"
    ):

        reasons.append(
            f"Quantity offered "
            f"({quantity.get('supplied')}) "
            f"is below required quantity "
            f"({quantity.get('required')})."
        )

    for requirement in technical.get(
        "requirements",
        []
    ):

        if requirement.get(
            "status"
        ) == "MISMATCH":

            reasons.append(
                f"Technical requirement "
                f"{requirement.get('parameter')} "
                f"mismatch: required "
                f"'{requirement.get('required')}', "
                f"supplied "
                f"'{requirement.get('supplied')}'"
            )

        elif requirement.get(
            "status"
        ) == "MISSING":

            reasons.append(
                f"Technical requirement "
                f"{requirement.get('parameter')} "
                f"is missing."
            )

    # --------------------------------------------------------
    # CRITICAL CONDITIONS
    # --------------------------------------------------------

    critical_failure = (

        len(
            mandatory["missingDocuments"]
        ) > 0

        or technical["score"] < 100

        or delivery["score"] < 100

        or quantity["score"] < 100
    )

    # --------------------------------------------------------
    # STATUS / RISK
    # --------------------------------------------------------

    if critical_failure:

        status = "Reject"
        risk_level = "CRITICAL"
        risk_reason = (
            "Major compliance gaps are present."
        )
        recommendation = (
            "Reject due to critical compliance failures."
        )

    elif score >= 80:

        status = "Compliant"
        risk_level = "LOW"
        risk_reason = (
            "No major compliance gaps detected."
        )
        recommendation = (
            "Proceed subject to normal verification."
        )

    else:

        status = "Needs Review"
        risk_level = "MEDIUM"
        risk_reason = (
            "Some compliance requirements need review."
        )
        recommendation = (
            "Review the identified compliance gaps."
        )

    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    return {

        "bidderId": bidder.get(
            "bidderId"
        ),

        "company": bidder.get(
            "company"
        ),

        "score": score,

        "status": status,

        "riskLevel": risk_level,

        "riskReason": risk_reason,

        "scoreBreakdown": {
            key: round(value, 2)
            for key, value
            in score_breakdown.items()
        },

        "requirementSatisfaction": {

            "mandatoryDocuments": mandatory,

            "experience": experience,

            "technical": technical,

            "delivery": delivery,

            "quantity": quantity,

            "oemMse": oem_mse
        },

        "verifiedDocuments":
            mandatory[
                "verifiedDocuments"
            ],

        "missingDocuments":
            mandatory[
                "missingDocuments"
            ],

        "technicalMatch":
            technical,

        "reasons": reasons,

        "recommendation":
            recommendation
    }