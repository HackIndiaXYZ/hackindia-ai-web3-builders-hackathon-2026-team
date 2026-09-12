from datetime import datetime, timedelta, timezone

from app.core.database import SessionLocal
from app.models.bidder import Bidder
from app.models.mock_blacklist import MockBlacklist


def seed_blacklist_data():
    db = SessionLocal()

    try:
        bidders = db.query(Bidder).order_by(Bidder.bidder_id).all()

        if len(bidders) < 3:
            print("At least 3 bidders are required. Create bidders first.")
            return

        valid_until = datetime.now(timezone.utc) + timedelta(days=365)

        blacklist_records = [
            {
                "company_name": bidders[0].company_name,
                "status": "NOT_BLACKLISTED",
                "authority": "Mock Government Procurement Database",
                "remarks": "No active blacklisting record found.",
            },
            {
                "company_name": bidders[1].company_name,
                "status": "NOT_BLACKLISTED",
                "authority": "Mock Government Procurement Database",
                "remarks": "No active blacklisting record found.",
            },
            {
                "company_name": bidders[2].company_name,
                "status": "BLACKLISTED",
                "authority": "Mock Government Procurement Database",
                "remarks": "Active blacklisting record exists in the mock database.",
            },
        ]

        for record in blacklist_records:
            existing = (
                db.query(MockBlacklist)
                .filter(
                    MockBlacklist.company_name == record["company_name"]
                )
                .first()
            )

            if existing:
                print(
                    f"{record['company_name']} already exists. Skipping."
                )
                continue

            blacklist_record = MockBlacklist(
                company_name=record["company_name"],
                status=record["status"],
                authority=record["authority"],
                valid_until=valid_until,
                remarks=record["remarks"],
            )

            db.add(blacklist_record)

        db.commit()

        print("Blacklist ground-truth data seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_blacklist_data()