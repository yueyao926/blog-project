from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.dependencies import get_current_admin, get_db
from app.models.site_setting import SiteSetting
from app.models.user import User
from app.schemas.site_setting import SiteSettingOut


router = APIRouter(prefix="/site-settings", tags=["Site settings"])

ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}
MAX_IMAGE_BYTES = 10 * 1024 * 1024


@router.get("", response_model=SiteSettingOut)
def get_site_settings(db: Session = Depends(get_db)):
    settings = db.query(SiteSetting).filter(SiteSetting.id == 1).first()
    return settings or SiteSettingOut()


@router.put("/hero-image", response_model=SiteSettingOut)
async def update_hero_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    extension = ALLOWED_IMAGE_TYPES.get(file.content_type or "")
    if not extension:
        raise HTTPException(status_code=400, detail="仅支持 JPG、PNG、WebP 或 GIF 图片")

    content = await file.read(MAX_IMAGE_BYTES + 1)
    if len(content) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="图片大小不能超过 10 MB")

    uploads = Path("uploads")
    uploads.mkdir(parents=True, exist_ok=True)
    filename = f"hero-{uuid4().hex}{extension}"
    (uploads / filename).write_bytes(content)

    settings = db.query(SiteSetting).filter(SiteSetting.id == 1).first()
    if settings is None:
        settings = SiteSetting(id=1)
        db.add(settings)

    settings.hero_image = f"/uploads/{filename}"
    db.commit()
    db.refresh(settings)
    return settings
