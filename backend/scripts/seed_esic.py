from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.bidder import Bidder
from app.models.mock_esic import MockESIC


def seed_esic_data():
    db = SessionLocal()

    try:
        bidders = db.query(Bidder).all()

        if len(bidders) < 3:
            print("At least 3 bidders are required. Create bidders first.")
            return

        esic_records = [
            {
                "bidder_index": 0,
                "esic_number": "DEMO-ESIC-001",
                "compliance_status": "COMPLIANT",
                "remarks": "ESIC compliance verified in mock government database."
            },
            {
                "bidder_index": 1,
                "esic_number": "DEMO-ESIC-002",
                "compliance_status": "COMPLIANT",
                "remarks": "ESIC compliance verified in mock government database."
            },
            {
                "bidder_index": 2,
                "esic_number": "DEMO-ESIC-003",
                "compliance_status": "NON_COMPLIANT",
                "remarks": "ESIC compliance is correctly marked as non-compliant."
            },
        ]

        for record in esic_records:
            bidder = bidders[record["bidder_index"]]

            existing = (
                db.query(MockESIC)
                .filter(
                    MockESIC.esic_number == record["esic_number"]
                )
                .first()
            )

            if existing:
                print(
                    f"{record['esic_number']} already exists. Skipping."
                )
                continue

            esic_record = MockESIC(
                bidder_id=bidder.bidder_id,
                esic_number=record["esic_number"],
                employer_name=bidder.company_name,
                compliance_status=record["compliance_status"],
                last_contribution_date=datetime.now(timezone.utc),
                registration_date=datetime.now(timezone.utc),
                remarks=record["remarks"],
            )

            db.add(esic_record)

        db.commit()

        print("ESIC ground-truth data seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_esic_data()