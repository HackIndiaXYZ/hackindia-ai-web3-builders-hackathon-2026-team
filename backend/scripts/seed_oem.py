from datetime import datetime, timedelta, timezone

from app.core.database import SessionLocal
from app.models.bidder import Bidder
from app.models.mock_oem import MockOEM


def seed_oem_data():
    db = SessionLocal()

    try:
        bidders = db.query(Bidder).order_by(Bidder.bidder_id).all()

        if len(bidders) < 3:
            print("At least 3 bidders are required. Create bidders first.")
            return

        valid_until = datetime.now(timezone.utc) + timedelta(days=365)

        oem_records = [
            {
                "bidder_index": 0,
                "authorization_number": "DEMO-OEM-001",
                "oem_name": "Atlas Copco (India) Private Limited",
                "authorization_status": "AUTHORIZED",
                "remarks": (
                    "OEM authorization verified in mock government database."
                ),
            },
            {
                "bidder_index": 1,
                "authorization_number": "DEMO-OEM-002",
                "oem_name": "Atlas Copco (India) Private Limited",
                "authorization_status": "AUTHORIZED",
                "remarks": (
                    "OEM authorization verified in mock government database."
                ),
            },
            {
                "bidder_index": 2,
                "authorization_number": "DEMO-OEM-003",
                "oem_name": "Atlas Copco (India) Private Limited",
                "authorization_status": "NOT_AUTHORIZED",
                "remarks": (
                    "OEM authorization status is correctly marked "
                    "as not authorized."
                ),
            },
        ]

        for record in oem_records:
            bidder = bidders[record["bidder_index"]]

            existing = (
                db.query(MockOEM)
                .filter(
                    MockOEM.authorization_number
                    == record["authorization_number"]
                )
                .first()
            )

            if existing:
                print(
                    f"{record['authorization_number']} already exists. "
                    "Skipping."
                )
                continue

            oem_record = MockOEM(
                bidder_id=bidder.bidder_id,
                authorization_number=record["authorization_number"],
                oem_name=record["oem_name"],
                authorization_status=record["authorization_status"],
                valid_until=valid_until,
                remarks=record["remarks"],
            )

            db.add(oem_record)

        db.commit()

        print("OEM ground-truth data seeded successfully!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_oem_data()