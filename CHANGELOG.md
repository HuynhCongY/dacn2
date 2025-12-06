# Changelog

## [Unreleased] - 2025-12-06

### Fixed
- Event display now shows complete information for all events
  - Events with both location AND reminder now display both fields (previously one might be hidden)
  - Fixed icon consistency: 🕐 for time, 📍 for location, ⏰ for reminder, 📝 for description
  - Preview section after adding events now shows all fields with proper icons
  - Events with `reminder_minutes = 0` no longer show "Nhắc trước: 0 phút"

### Changed
- Improved code maintainability:
  - Extracted datetime format to `DATETIME_FORMAT` constant
  - Extracted icon definitions to constants (ICON_TIME, ICON_LOCATION, ICON_REMINDER, ICON_DESCRIPTION)
  - Created helper function `should_show_reminder()` to eliminate code duplication
  - Replaced wildcard import with explicit imports for better clarity
  - Made year range selection dynamic (current year ± 5 years) instead of hardcoded 2020-2030

### Technical Details

**Files Modified:**
- `app.py`: Updated `show_event_card()` and `show_add_event_page()` functions
- `utils/constants.py`: Added display format constants and icon definitions

**Test Results:**
- ✅ All test cases pass
- ✅ Event with both location AND reminder - shows BOTH
- ✅ Event with only location - shows only location
- ✅ Event with only reminder - shows only reminder
- ✅ Event with neither - shows only time
- ✅ Edge case: reminder_minutes = 0 is correctly hidden
- ✅ CodeQL security scan: No alerts found

**Display Consistency:**
The fix ensures consistent display across ALL views:
- Calendar tab (day/week/month views)
- Search results
- Preview after adding event (both NLP and manual)
