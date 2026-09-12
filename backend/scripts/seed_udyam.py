from datetime import datetime, timezone

from app.core.database import SessionLocal
from app.models.bidder import Bidder
from app.models.mock_udyam import MockUdyam


def seed_udyam_data():
    db = SessionLocal()

    try:
        bidders = db.query(Bidder).all()

        if len(bidders) < 3:
            print("At least 3 bidders are required. Create bidders first.")
            return

        udyam_records = [
            {
                "bidder_index": 0,
                "udyam_number": "DEMO-UDYAM-001",
                "enterprise_type": "SMALL",
                "registration_status": "ACTIVE",
                "remarks": "Udyam registration verified in mock government database."
            },
            {
                "bidder_index": 1,
                "udyam_number": "DEMO-UDYAM-002",
                "enterprise_type": "MICRO",
                "registration_status": "ACTIVE",
                "remarks": "Udyam registration verified in mock government database."
            },
            {
                "bidder_index": 2,
                "udyam_number": "DEMO-UDYAM-003",
                "enterprise_type": "MEDIUM",
                "registration_status": "EXPIRED",
                "remarks": "Udyam record is correctly marked as expired."
            },
        ]

        for record in udyam_records:
            bidder = bidders[record["bidder_index"]]

            existing = (
                db.query(MockUdyam)
                .filter(
                    MockUdyam.udyam_number == record["udyam_number"]
                )
                .first()
            )

            if existing:
                print(
                    f"{record['udyam_number']} already exists. Skipping."
                )
                continue

            udyam_record = MockUdyam(
                bidder_id=bidder.bidder_id,
                udyam_number=record["udyam_number"],
                enterprise_name=bidder.company_name,
                enterprise_type=record["enterprise_type"],
                registration_status=record["registration_status"],
                registration_date=datetime.now(timezone.utc),
                valid_until=datetime.now(timezone.utc),
                remarks=record["remarks"],
            )

            db.add(udyam_record)

        db.commit()

        print("Udyam ground-truth data seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_udyam_data()