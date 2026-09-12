from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.bidder import Bidder
from app.models.mock_startup import MockStartup


def seed_startup_data():
    db = SessionLocal()

    try:
        bidders = db.query(Bidder).all()

        if len(bidders) < 3:
            print("At least 3 bidders are required. Create bidders first.")
            return

        startup_records = [
            {
                "bidder_index": 0,
                "recognition_number": "DEMO-DPIIT-001",
                "recognition_status": "RECOGNIZED",
                "remarks": "DPIIT startup recognition verified in mock government database."
            },
            {
                "bidder_index": 1,
                "recognition_number": "DEMO-DPIIT-002",
                "recognition_status": "RECOGNIZED",
                "remarks": "DPIIT startup recognition verified in mock government database."
            },
            {
                "bidder_index": 2,
                "recognition_number": "DEMO-DPIIT-003",
                "recognition_status": "NOT_RECOGNIZED",
                "remarks": "Startup recognition status is correctly marked as not recognized."
            },
        ]

        for record in startup_records:
            bidder = bidders[record["bidder_index"]]

            existing = (
                db.query(MockStartup)
                .filter(
                    MockStartup.recognition_number
                    == record["recognition_number"]
                )
                .first()
            )

            if existing:
                print(
                    f"{record['recognition_number']} already exists. Skipping."
                )
                continue

            startup_record = MockStartup(
                bidder_id=bidder.bidder_id,
                recognition_number=record["recognition_number"],
                startup_name=bidder.company_name,
                recognition_status=record["recognition_status"],
                recognition_date=datetime.now(timezone.utc),
                valid_until=datetime.now(timezone.utc),
                remarks=record["remarks"],
            )

            db.add(startup_record)

        db.commit()

        print("Startup/DPIIT ground-truth data seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_startup_data()