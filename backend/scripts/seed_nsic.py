from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.bidder import Bidder
from app.models.mock_nsic import MockNSIC


def seed_nsic_data():
    db = SessionLocal()

    try:
        bidders = db.query(Bidder).all()

        if len(bidders) < 3:
            print("At least 3 bidders are required. Create bidders first.")
            return

        nsic_records = [
            {
                "bidder_index": 0,
                "nsic_number": "DEMO-NSIC-001",
                "registration_status": "ACTIVE",
                "remarks": "NSIC registration verified in mock government database."
            },
            {
                "bidder_index": 1,
                "nsic_number": "DEMO-NSIC-002",
                "registration_status": "ACTIVE",
                "remarks": "NSIC registration verified in mock government database."
            },
            {
                "bidder_index": 2,
                "nsic_number": "DEMO-NSIC-003",
                "registration_status": "EXPIRED",
                "remarks": "NSIC registration is correctly marked as expired."
            },
        ]

        for record in nsic_records:
            bidder = bidders[record["bidder_index"]]

            existing = (
                db.query(MockNSIC)
                .filter(
                    MockNSIC.nsic_number == record["nsic_number"]
                )
                .first()
            )

            if existing:
                print(
                    f"{record['nsic_number']} already exists. Skipping."
                )
                continue

            nsic_record = MockNSIC(
                bidder_id=bidder.bidder_id,
                nsic_number=record["nsic_number"],
                enterprise_name=bidder.company_name,
                registration_status=record["registration_status"],
                registration_date=datetime.now(timezone.utc),
                valid_until=datetime.now(timezone.utc),
                remarks=record["remarks"],
            )

            db.add(nsic_record)

        db.commit()

        print("NSIC ground-truth data seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_nsic_data()