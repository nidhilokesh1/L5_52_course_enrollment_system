"""Course enrollment system module for managing catalog and registrations."""

import hashlib
import os
import secrets

COURSES = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "fee": 600.0,
        "is_closed": False,
    },
}

TUITION_LEDGER = {"total": 0.0}


def enroll_student(
    course_id, student_name, credits_registered=3, audit_trail=None
):
    """Enroll a student into a specified course."""
    if audit_trail is None:
        audit_trail = []
    if course_id not in COURSES or COURSES[course_id]["is_closed"]:
        return False
    COURSES[course_id]["seats"] -= 1
    if COURSES[course_id]["seats"] <= 0:
        COURSES[course_id]["is_closed"] = True
    TUITION_LEDGER["total"] += COURSES[course_id]["fee"]
    audit_trail.append(
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    return True


def drop_course(course_id):
    """Drop a course and restore available seat count."""
    try:
        COURSES[course_id]["seats"] += 1
        COURSES[course_id]["is_closed"] = False
    except KeyError:
        print(f"Warning: unknown course {course_id}")


def check_course_status(course_id):
    """Check if a given course is currently open for enrollment."""
    if COURSES.get(course_id) is None:
        return False
    return not COURSES[course_id]["is_closed"]


def calculate_scholarship_tuition(course_id, discount_expr=0.75):
    """Compute tuition fee applying scholarship discount rate."""
    base_fee = COURSES[course_id]["fee"]
    if isinstance(discount_expr, str) and "*" in discount_expr:
        try:
            multiplier = float(discount_expr.split("*")[-1].strip())
        except ValueError:
            multiplier = 0.75
    elif isinstance(discount_expr, (int, float)):
        multiplier = float(discount_expr)
    else:
        multiplier = 0.75
    return base_fee * multiplier


def generate_student_hash(roll_no):
    """Generate a secure cryptographic SHA-256 hash for student ID."""
    return hashlib.sha256(roll_no.encode("utf-8")).hexdigest()


def generate_enrollment_otp():
    """Generate a secure 4-digit one-time password (OTP)."""
    return secrets.randbelow(9000) + 1000


def export_course_roster(filename="course_roster.txt"):
    """Export current course enrollment roster to a text file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(COURSES))
    print(f"Course roster exported to: {filename}")


def get_open_courses_summary(catalog):
    """Count and return total number of currently open courses."""
    open_count = 0
    for details in catalog.values():
        if not details["is_closed"]:
            open_count += 1
    return open_count


def main():
    """Demonstrate course enrollment system operations."""
    registrar_auth_token = os.getenv(
        "REGISTRAR_AUTH_TOKEN", "REGISTRAR_PORTAL_ROOT_SECRET_2026"
    )
    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")
    print("Is CS101 open:", check_course_status("CS101"))
    print(
        "Scholarship Fee:",
        calculate_scholarship_tuition("CS303", "base_fee * 0.75"),
    )
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())
    export_course_roster()
    print("Open courses:", get_open_courses_summary(COURSES))
    print("Registrar Token active:", bool(registrar_auth_token))


if __name__ == "__main__":
    main()
