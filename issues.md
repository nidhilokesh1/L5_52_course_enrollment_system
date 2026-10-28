# Lab 5: Static Code Analysis — Issues Log

**Student Name:** NIDHI L  
**SRN:** PES1UG24CS298  
**Course:** Software Engineering / Software Testing & Automation (SETA)  
**Assigned Repository:** `L5_52_course_enrollment_system`  
**File Analyzed:** `course_enrollment_system.py`  

---

## Static Analysis Summary

| Tool | Initial Status | Final Status |
|---|---|---|
| **Pylint** | 4.00 / 10.00 | **10.00 / 10.00** |
| **Bandit** | 6 issues (2 High, 1 Medium, 3 Low) | **0 issues (Clean)** |
| **Flake8** | 12 style & formatting warnings | **0 warnings (Clean)** |

---

## Documented Issues Table

| Issue | Type | Line(s) (Original) | Description | Fix Approach |
|---|---|---|---|---|
| **Weak MD5 Hash Algorithm (B324)** | Security / Bandit (High) | 52 | `hashlib.md5()` was used to generate student identification hashes. MD5 is cryptographically broken and vulnerable to collision and preimage attacks. | Replaced `hashlib.md5` with cryptographically secure `hashlib.sha256(roll_no.encode("utf-8")).hexdigest()`. |
| **Command Shell Injection (B605)** | Security / Bandit (High) | 63 | `os.system("echo Course roster exported to: " + filename)` executes shell commands using string concatenation. If `filename` contains unvalidated characters, an attacker can execute arbitrary system commands. | Removed `os.system` invocation completely; replaced with safe, native Python output: `print(f"Course roster exported to: {filename}")`. |
| **Unsafe `eval()` Execution (B307, Pylint W0123)** | Security / Bug (Medium) | 45–47 | `eval(discount_expr)` parses and evaluates arbitrary Python expressions dynamically. Supplying malicious strings enables Remote Code Execution (RCE), and it also masked usage of `base_fee`. | Replaced dynamic `eval()` with safe arithmetic computation. Safely parsed numeric multipliers from the discount rate and computed `base_fee * multiplier` directly. |
| **Mutable Default Argument (Pylint W0102)** | Bug / Logic | 15 | `def enrollStudent(..., audit_trail=[])` binds the default empty list at function definition time. The same list object is shared across successive function calls, leaking registration state between students. | Changed parameter default to `audit_trail=None` and initialized `if audit_trail is None: audit_trail = []` inside the function body to guarantee a fresh instance per call. |
| **Bare `except` & Silent Pass (Bandit B110, Pylint W0702, Flake8 E722)** | Quality / Security / Style | 27–32 | `try ... except: pass` catches all exceptions indiscriminately (including `KeyboardInterrupt` and `SystemExit`) and suppresses errors silently, masking non-existent course ID bugs. | Specified the exact exception `except KeyError:` and added informative console feedback: `print(f"Warning: unknown course {course_id}")`. |
| **Predictable PRNG for Security Token (Bandit B311)** | Security / Bandit (Low) | 55–56 | `random.randint(1000, 9999)` uses the Mersenne Twister PRNG, whose internal state can be determined from observed outputs, making enrollment OTPs guessable. | Imported standard library `secrets` module and used `secrets.randbelow(9000) + 1000` to produce cryptographically secure, unpredictable OTPs. |
| **Hardcoded Secret String (Bandit B105)** | Security / Bandit (Low) | 75 | `registrar_auth_token = "REGISTRAR_PORTAL_ROOT_SECRET_2026"` hardcoded administrative credentials in plain source code and exposed them in standard console logs. | Retrieved token dynamically from environment via `os.getenv("REGISTRAR_AUTH_TOKEN", ...)` and printed only a boolean existence indicator `bool(registrar_auth_token)` rather than the plain secret. |
| **Global State Mutation (Pylint W0603, C0103)** | Code Quality / Architecture | 12, 16 | `global total_tuition` mutates a global scalar variable inside `enrollStudent()`. Global mutable state violates modularity and prevents thread safety. | Encapsulated tuition totals into an uppercase module constant structure `TUITION_LEDGER = {"total": 0.0}`, updating `TUITION_LEDGER["total"] += fee` without `global`. |
| **Singleton Comparison & Simplifiable Logic (Pylint C0121, R1703, R1705; Flake8 E711)** | Style / Quality | 36–42 | `courses.get(course_id) == None` compared singletons with `==` rather than `is`; redundant `if ... return True else return False`; unused `lab_fee = 45.0`. | Replaced with `is None`, removed dead variable `lab_fee`, and simplified return to direct boolean `return not COURSES[course_id]["is_closed"]`. |
| **Unmanaged File Resource & Missing Encoding (Pylint W1514, R1732)** | Reliability / Quality | 60–62 | `f = open(filename, "w")` was opened without a context manager or explicit encoding, risking file descriptor leakage on exceptions and platform encoding discrepancies. | Refactored to context manager with UTF-8 encoding: `with open(filename, "w", encoding="utf-8") as roster_file:`. |
| **PEP 8 Formatting & Style Bundle (Flake8 E501, F401, W292; Pylint C0114, C0116, C0103, W0611, W0621)** | Style / Maintainability | Multiple | Line lengths exceeding 79 columns; unused `import math`; missing module and function docstrings; non-standard camelCase names; outer scope name shadowing (`courses`). | Formatted all lines to ≤79 columns, removed unused imports, added descriptive docstrings across all functions and module header, renamed to idiomatic `snake_case`, and guarded entry with `if __name__ == "__main__":`. |

---

## Verification Results

- **Pylint Score:** 10.00 / 10.00
- **Bandit Analysis:** 0 issues identified
- **Flake8 Compliance:** 0 warnings (100% PEP 8 compliant)
- **Functional Validation:** Program runs cleanly and produces all expected outputs accurately.
