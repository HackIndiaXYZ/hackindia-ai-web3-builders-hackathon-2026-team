from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.bidder import Bidder
from app.models.mock_gst import MockGST


def seed_gst_data():
    db = SessionLocal()

    try:
        bidders = db.query(Bidder).all()

        if not bidders:
            print("No bidders found. Create bidders first.")
            return

        gst_records = [
            {
                "bidder_index": 0,
                "gstin": "DEMO-GST-001",
                "legal_name": bidders[0].company_name,
                "registration_status": "ACTIVE",
                "return_filing_status": "REGULAR",
                "remarks": "GST registration verified in mock government database."
            },
            {
                "bidder_index": 1,
                "gstin": "DEMO-GST-002",
                "legal_name": bidders[1].company_name,
                "registration_status": "ACTIVE",
                "return_filing_status": "REGULAR",
                "remarks": "GST registration verified in mock government database."
            },
            {
                "bidder_index": 2,
                "gstin": "DEMO-GST-003",
                "legal_name": bidders[2].company_name,
                "registration_status": "CANCELLED",
                "return_filing_status": "IRREGULAR",
                "remarks": "GST registration is correctly marked as cancelled."
            },
        ]

        for record in gst_records:
            bidder = bidders[record["bidder_index"]]

            existing = (
                db.query(MockGST)
                .filter(MockGST.gstin == record["gstin"])
                .first()
            )

            if existing:
                print(f"{record['gstin']} already exists. Skipping.")
                continue

            gst_record = MockGST(
                bidder_id=bidder.bidder_id,
                gstin=record["gstin"],
                legal_name=record["legal_name"],
                registration_status=record["registration_status"],
                return_filing_status=record["return_filing_status"],
                last_return_filed=datetime.now(timezone.utc),
                registration_date=datetime.now(timezone.utc),
                remarks=record["remarks"],
            )

            db.add(gst_record)

        db.commit()
        print("GST ground-truth data seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_gst_data()