from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.bidder import Bidder
from app.models.mock_pan import MockPAN


def seed_pan_data():
    db = SessionLocal()

    try:
        bidders = db.query(Bidder).all()

        if len(bidders) < 3:
            print("At least 3 bidders are required. Create bidders first.")
            return

        pan_records = [
            {
                "bidder_index": 0,
                "pan": "DEMO-PAN-001",
                "pan_status": "ACTIVE",
                "income_tax_status": "COMPLIANT",
                "remarks": "PAN and income-tax status verified in mock government database."
            },
            {
                "bidder_index": 1,
                "pan": "DEMO-PAN-002",
                "pan_status": "ACTIVE",
                "income_tax_status": "COMPLIANT",
                "remarks": "PAN and income-tax status verified in mock government database."
            },
            {
                "bidder_index": 2,
                "pan": "DEMO-PAN-003",
                "pan_status": "ACTIVE",
                "income_tax_status": "NON_COMPLIANT",
                "remarks": "PAN is active, but income-tax compliance is correctly marked as non-compliant."
            },
        ]

        for record in pan_records:
            bidder = bidders[record["bidder_index"]]

            existing = (
                db.query(MockPAN)
                .filter(MockPAN.pan == record["pan"])
                .first()
            )

            if existing:
                print(f"{record['pan']} already exists. Skipping.")
                continue

            pan_record = MockPAN(
                bidder_id=bidder.bidder_id,
                pan=record["pan"],
                legal_name=bidder.company_name,
                pan_status=record["pan_status"],
                income_tax_status=record["income_tax_status"],
                last_return_filed=datetime.now(timezone.utc),
                remarks=record["remarks"],
            )

            db.add(pan_record)

        db.commit()

        print("PAN ground-truth data seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_pan_data()