Implement following tasks.

# IMPLEMENTATION PART-1: Add Classes in './app/models.py'

All classes must inherit from the `BaseModel` class. Update `forms.py`, `routes.py`, and relevant templates as needed.

## Task 1: Add `Contact` Model
- `user_id`: ForeignKey to `User.id`, unique
- `mobile`: 12-digit integer
- `whatsapp`: 12-digit integer
- `email`: String, with email validator

## Task 2: Add `HomeAddress` Model
- `user_id`: ForeignKey to `User.id`, unique
- `country_id`: ForeignKey to `Countries.id`, required
- `state_id`: ForeignKey to `States.id` (related to `Countries.id`), required
- `city_id`: ForeignKey to `Cities.id` (related to `States.id`), required
- `area`: String (max 32 chars), optional
- `zip`: String (max 32 chars), optional

## Task 3: Add `ResidentAddress` Model
- Same fields and constraints as `HomeAddress`, but for the resident address

## Task 4: Add `OtherDetail` Model
- `user_id`: ForeignKey to `User.id`, unique
- `education`: String (max 32 chars), required
- `profession`: String (max 32 chars), required
- `visa_status`: String (max 32 chars), optional
- `citizenship`: String (max 32 chars), optional
- `spouse`: Integer (single digit), optional
- `son`: Integer (single digit), optional
- `daughter`: Integer (single digit), optional

## Task 5: Add `ProgressRecord` Model
- `user_id`: ForeignKey to `User.id`, duplicates allowed
- `note`: Text (paragraph)

## Task 6: Add `AttendanceStatusLookup` Model
- `status`: Single alphabetic character

## Task 7: Add `ClassSession` Model
- `class_date`: Date
- `class_batch_id`: ForeignKey to `ClassBatch.id`
- `teacher_id`: ForeignKey to `User.id` (where the user's role is 'Ustad')
- Unique constraint on (`class_date`, `class_batch_id`)

## Task 8: Add `UserAttendance` Model
- `user_id`: ForeignKey to `User.id`
- `class_session_id`: ForeignKey to `ClassSession.id`
- `attendance_status`: ForeignKey to `AttendanceStatusLookup.status`
- `note`: Text (paragraph)
- `late_by_min`: Integer, optional
- `left_early_by_min`: Integer, optional
- Unique constraint on (`user_id`, `class_session_id`)

## Task 9: Add `TemperamentLookup` Model
- `user_id`: ForeignKey to `User.id`, duplicates allowed
- `temperament`: String (max 32 chars)

## Task 10: Add `UserTemperament` Model
- `user_id`: ForeignKey to `User.id`, duplicates allowed
- `temperament_id`: ForeignKey to `TemperamentLookup.id`, duplicates allowed
- `note`: Text (paragraph)

## Task 11: Add `RegStatusLookup` Model
- `status`: String (max 16 chars)

## Task 12: Add `UserRegStatus` Model
- `user_id`: ForeignKey to `User.id`, duplicates allowed
- `status_id`: ForeignKey to `RegStatusLookup.id`
- On status change, append notes to `ProgressRecord.note`

## Task 13: Add `CallOutTime` Model
- `user_id`: ForeignKey to `User.id`, duplicates allowed
- `hours`: Time
- `timezone`: String (max 16 chars)

## Task 14: Add `Photo` Model
- `user_id`: ForeignKey to `User.id`, unique
- `picture`: Large binary data

## Task 15: Add `TestSession` Model
- `test_date`: Date
- `class_batch_id`: ForeignKey to `ClassBatch.id`
- `max_score`: Integer (0–999)
- Unique constraint on (`test_date`, `class_batch_id`)

## Task 16: Add `TestSessionScore` Model (inherits `BaseModel`)
- `test_session_id`: ForeignKey to `TestSession.id`
- `user_id`: ForeignKey to `User.id`
- `score`: Integer (0 to `TestSession.max_score`)
- `note`: String (optional, single line)

## Task 17: Add `Task` Model
- `name`: String (max 64 chars)
- `description`: Rich text (3 paragraphs)
- `class_batch_id`: ForeignKey to `ClassBatch.id`
- `due_date`: Date

## Task 18: Add `UserTask` Model
- `user_id`: ForeignKey to `User.id`
- `task_id`: ForeignKey to `Task.id`
- `status`: Boolean (0 or 1)
- `note`: String (single line)
- Unique constraint on (`user_id`, `task_id`)

## Task 19: Add `SkillLookup` Model
- `skill`: String (max 32 chars)

## Task 20: Add `UserSkill` Model
- `user_id`: ForeignKey to `User.id`, duplicates allowed
- `skill_id`: ForeignKey to `SkillLookup.id`, duplicates allowed
- `skill_detail`: String (optional, single line)

## Task 21: Add `DuaCatLookup` Model
- `dua`: String (max 32 chars)

## Task 22: Add `UserDua` Model
- `user_id`: ForeignKey to `User.id`, duplicates allowed
- `dua_cat_id`: ForeignKey to `DuaCatLookup.id`, duplicates allowed
- `class_session_id`: ForeignKey to `ClassSession.id`
- `dua_detail`: String (single line)

## Task 23: Add `Aaamal` Model
- `user_id`: ForeignKey to `User.id`, duplicates allowed
- `fazar_ba_jamat`: Integer (single digit)
- `roza`: Integer (single digit)
- `zikr`: Integer (single digit)
- `tahajjud`: Integer (single digit)
- `sadka`: Integer (single digit)

---

# IMPLEMENTATION PART-2: Update `User` Class

- Remove `email` attribute (now in `Contact`)
- Add relationships to new models: `contact`, `gender` (choices from `Config.GENDERS`), `home_address`, `resident_address`, `other_details`, `progress_record`, `attendance`, `attendance_feedback`, `user_registration_status`, `callout_time`, `photo`, `test_session_score`, `user_task`, `user_dua`, `aamal`, `user_temperament`, `user_skill`

---

# IMPLEMENTATION PART-3: Update Login Method

- Update forms, routes and templates to use `Contact.email` instead of `User.email`

---

# IMPLEMENTATION PART-4: Additional Features & Improvements

- Ensure all models use appropriate indexes and constraints for efficiency and data integrity
- Use SQLAlchemy validators and types for security (e.g., `EmailType`, `LargeBinary`, `Text`)
- Use `nullable=False` for required fields
- Use `unique=True` and composite unique constraints as specified
- Add `__repr__` methods for better debugging
- Suggest: Use SQLAlchemy relationships for easier joins and cascading deletes where appropriate


