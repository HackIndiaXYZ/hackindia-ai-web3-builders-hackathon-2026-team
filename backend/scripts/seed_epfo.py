from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.bidder import Bidder
from app.models.mock_epfo import MockEPFO


def seed_epfo_data():
    db = SessionLocal()

    try:
        bidders = db.query(Bidder).all()

        if len(bidders) < 3:
            print("At least 3 bidders are required. Create bidders first.")
            return

        epfo_records = [
            {
                "bidder_index": 0,
                "epfo_number": "DEMO-EPFO-001",
                "compliance_status": "COMPLIANT",
                "remarks": "EPFO compliance verified in mock government database."
            },
            {
                "bidder_index": 1,
                "epfo_number": "DEMO-EPFO-002",
                "compliance_status": "COMPLIANT",
                "remarks": "EPFO compliance verified in mock government database."
            },
            {
                "bidder_index": 2,
                "epfo_number": "DEMO-EPFO-003",
                "compliance_status": "NON_COMPLIANT",
                "remarks": "EPFO compliance is correctly marked as non-compliant."
            },
        ]

        for record in epfo_records:
            bidder = bidders[record["bidder_index"]]

            existing = (
                db.query(MockEPFO)
                .filter(
                    MockEPFO.epfo_number == record["epfo_number"]
                )
                .first()
            )

            if existing:
                print(
                    f"{record['epfo_number']} already exists. Skipping."
                )
                continue

            epfo_record = MockEPFO(
                bidder_id=bidder.bidder_id,
                epfo_number=record["epfo_number"],
                establishment_name=bidder.company_name,
                compliance_status=record["compliance_status"],
                last_contribution_date=datetime.now(timezone.utc),
                registration_date=datetime.now(timezone.utc),
                remarks=record["remarks"],
            )

            db.add(epfo_record)

        db.commit()

        print("EPFO ground-truth data seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_epfo_data()