from fastapi import APIRouter, File, HTTPException, UploadFile
import os
import shutil
import tempfile

from app.services.integrated_pipeline import run_tender_pipeline

router = APIRouter(
    prefix="/ai-pipeline",
    tags=["AI Tender Pipeline"]
)


@router.post("/analyze")
async def analyze_tender_with_bidders(
    tender_pdf: UploadFile = File(...),

    bidder1_pdf: UploadFile = File(...),
    bidder2_pdf: UploadFile = File(...),
    bidder3_pdf: UploadFile = File(...)
):

    # --------------------------------
    # COLLECT 3 BIDDER FILES
    # --------------------------------

    bidder_pdfs = [
        bidder1_pdf,
        bidder2_pdf,
        bidder3_pdf
    ]

    # --------------------------------
    # CHECK TENDER PDF
    # --------------------------------

    if not tender_pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Tender must be a PDF file."
        )

    # --------------------------------
    # CHECK BIDDER PDFs
    # --------------------------------

    for bidder in bidder_pdfs:

        if not bidder.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail=f"{bidder.filename} must be a PDF file."
            )

    # --------------------------------
    # TEMP DIRECTORY
    # --------------------------------

    with tempfile.TemporaryDirectory() as temp_dir:

        # --------------------------------
        # SAVE TENDER
        # --------------------------------

        tender_path = os.path.join(
            temp_dir,
            "tender.pdf"
        )

        with open(tender_path, "wb") as buffer:

            shutil.copyfileobj(
                tender_pdf.file,
                buffer
            )

        # --------------------------------
        # SAVE BIDDER PDFs
        # --------------------------------

        bidder_paths = []

        for index, bidder in enumerate(
            bidder_pdfs,
            start=1
        ):

            bidder_path = os.path.join(
                temp_dir,
                f"bidder_{index}.pdf"
            )

            with open(
                bidder_path,
                "wb"
            ) as buffer:

                shutil.copyfileobj(
                    bidder.file,
                    buffer
                )

            bidder_paths.append(
                bidder_path
            )

        # --------------------------------
        # RUN PIPELINE
        # --------------------------------

        try:

            result = run_tender_pipeline(
                tender_pdf=tender_path,
                bidder_pdfs=bidder_paths
            )

            return result

        except Exception as e:
            message = str(e)
            status_code = 500

            if "quota" in message.lower() or "billing" in message.lower() or "api key" in message.lower() or "gemini" in message.lower() and "failed" in message.lower():
                status_code = 502

            raise HTTPException(
                status_code=status_code,
                detail=message
            )