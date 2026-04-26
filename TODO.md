# Cloudinary Removal & Static Files Fix

## Steps
- [x] Remove `cloudinary` and `django-cloudinary-storage` from `requirements.txt`
- [x] Add `src.apps.logo` to `INSTALLED_APPS` in `config/settings.py`
- [x] Regenerate `team` migration (remove CloudinaryField references)
- [x] Create `logo` initial migration
- [x] Delete leftover `staticfiles/cloudinary/` directory
- [ ] Run `makemigrations` and `migrate` to verify (needs `.env` env vars)

