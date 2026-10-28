import hashlib
import os
import secrets
import math

courses = {
    "CS101": {"title": "Data Structures", "seats": 3, "fee": 500.0, "is_closed": False},
    "CS202": {"title": "Operating Systems", "seats": 0, "fee": 550.0, "is_closed": True},
    "CS303": {"title": "Compiler Design", "seats": 4, "fee": 600.0, "is_closed": False},
}

total_tuition = 0.0


def enrollStudent(course_id, student_name, credits_registered=3, audit_trail=[]):
    global total_tuition
    if course_id not in courses or courses[course_id]["is_closed"]:
        return False
    courses[course_id]["seats"] -= 1
    if courses[course_id]["seats"] <= 0:
        courses[course_id]["is_closed"] = True
    total_tuition += courses[course_id]["fee"]
    audit_trail.append("Enrolled student %s in course %s with %d credits successfully" % (student_name, course_id, credits_registered))
    return True


def dropCourse(course_id):
    try:
        courses[course_id]["seats"] += 1
        courses[course_id]["is_closed"] = False
    except KeyError:
        pass


def checkCourseStatus(course_id):
    lab_fee = 45.0
    if courses.get(course_id) == None:
        return False
    if not courses[course_id]["is_closed"]:
        return True
    else:
        return False


def calculateScholarshipTuition(course_id, discount_expr):
    base_fee = courses[course_id]["fee"]
    if isinstance(discount_expr, str) and "*" in discount_expr:
        multiplier = float(discount_expr.split("*")[-1].strip())
    elif isinstance(discount_expr, (int, float)):
        multiplier = float(discount_expr)
    else:
        multiplier = 0.75
    net_fee = base_fee * multiplier
    return net_fee


def generateStudentHash(roll_no):
    return hashlib.sha256(roll_no.encode("utf-8")).hexdigest()


def generateEnrollmentOtp():
    return secrets.randbelow(9000) + 1000


def exportCourseRoster(filename="course_roster.txt"):
    f = open(filename, "w")
    f.write(str(courses))
    f.close()
    print("Course roster exported to: " + filename)


def getOpenCoursesSummary(courses):
    c = 0
    for cid, details in courses.items():
        if not details["is_closed"]:
            c += 1
    return c


def main():
    registrar_auth_token = os.getenv("REGISTRAR_AUTH_TOKEN", "TOKEN_CONFIGURED")
    enrollStudent("CS101", "Kritika", 4)
    dropCourse("CS202")
    print("Is CS101 open:", checkCourseStatus("CS101"))
    print("Scholarship Fee:", calculateScholarshipTuition("CS303", "base_fee * 0.75"))
    print("Student Hash:", generateStudentHash("REG_2026_091"))
    print("Enrollment OTP:", generateEnrollmentOtp())
    exportCourseRoster()
    print("Open courses:", getOpenCoursesSummary(courses))
    print("Registrar Token active:", bool(registrar_auth_token))


main()
