# FitForge Development Notes

## Superuser Credentials
- Username: admin
- Email: admin@fitforge.com
- Password: Set during initial setup

## Database Information
- Development: SQLite3
- Production: PostgreSQL (planned)

## All Migrations Applied
- All apps have migrations applied successfully
- Database schema is up to date

## Models Created
### Classes App
- ClassCategory
- FitnessClass
- ClassSchedule

### Memberships App
- MembershipTier
- UserMembership

### Bookings App
- Booking

### Products App
- ProductCategory
- Product

### Profiles App
- UserProfile (with auto-creation signals)

## Admin Access
- Admin panel: http://127.0.0.1:8080/admin/
- All models registered in admin with appropriate displays and filters
