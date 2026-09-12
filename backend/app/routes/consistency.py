from fastapi import APIRouter, Depends
from app.core.auth import get_current_user
from app.models.user import User
from app.services.consistency_service import check_identity_consistency

router = APIRouter(
    prefix="/consistency",
    tags=["Consistency Verification"]
)


@router.post("/identity")
def verify_identity_consistency(
    bidder_name: str,
    gst_name: str | None = None,
    pan_name: str | None = None,
    udyam_name: str | None = None,
    current_user: User = Depends(get_current_user)
):
    return check_identity_consistency(
        bidder_name=bidder_name,
        gst_name=gst_name,
        pan_name=pan_name,
        udyam_name=udyam_name
    )