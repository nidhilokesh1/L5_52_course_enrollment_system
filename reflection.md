# Lab 5: Static Code Analysis — Reflection

**Student Name:** NIDHI L  
**SRN:** PES1UG24CS298  
**Repository:** `L5_52_course_enrollment_system`  
**Date:** October 28, 2026  

---

### 1. What is the purpose and scope of static code analysis, and how is it different from testing?

Static code analysis involves inspecting and analyzing source code without executing it. Its scope encompasses catching security vulnerabilities, logical flaws, architectural anti-patterns, maintainability issues, and adherence to programming style standards (such as PEP 8).

In contrast, software testing (dynamic analysis) verifies system behavior during execution by supplying concrete inputs and asserting observed runtime outputs against expected outcomes. While unit and integration tests verify *whether the program delivers expected functional results*, static analysis evaluates *how safe, clean, and maintainable the implementation is*.

In this lab, executing `course_enrollment_system.py` initially completed with zero runtime exceptions and produced seemingly normal outputs (`Is CS101 open: True`, `Scholarship Fee: 450.0`, etc.). Traditional black-box testing would have passed completely. However, static analysis immediately uncovered critical vulnerabilities—such as arbitrary code execution via `eval()`, command injection via `os.system()`, cryptographically broken hashing (MD5), insecure OTP randomness, and mutable default arguments—which remain hidden during standard happy-path testing until attacked or triggered in production.

---

### 2. Which finding was the most severe, and why did you prioritize it?

The most critical findings were the **High-severity security vulnerabilities flagged by Bandit**:
1. **Dynamic Code Execution via `eval()` (B307 / CWE-78)**: In `calculateScholarshipTuition()`, the script evaluated a raw expression string `eval(discount_expr)`. In real-world applications where discount rules or coupons are supplied by users or web endpoints, this creates a catastrophic Remote Code Execution (RCE) vector that allows attackers to execute arbitrary system commands or compromise the hosting environment.
2. **OS Shell Injection via `os.system()` (B605 / CWE-78)**: In `exportCourseRoster()`, filename strings were concatenated directly into a shell command (`"echo ... " + filename`). Supplying filenames with shell command delimiters (`&&`, `;`, `|`) allows arbitrary command execution with the privileges of the running application.
3. **Broken Cryptographic Hash Algorithm (MD5) (B324 / CWE-327)**: Using MD5 for student identifier hashing introduces collision risks and violates security compliance standards.

Per lab instructions and industry secure development lifecycles (SDL), security defects were prioritized first because vulnerabilities represent direct threats to user data integrity and application safety.

---

### 3. How did your fixes improve code quality, security, and maintainability?

- **Security Improvements:**
  - Removed all dynamic evaluation (`eval`) in favor of direct arithmetic calculation with strict input validation.
  - Eliminated shell-level process execution (`os.system`), replacing it with standard Python string output.
  - Upgraded hashing from weak MD5 to SHA-256 (`hashlib.sha256`) with explicit UTF-8 character encoding.
  - Switched OTP generation from PRNG `random.randint` to cryptographically secure `secrets.randbelow()`.
  - Replaced plaintext hardcoded administrative credentials with dynamic environment variable retrieval (`os.getenv`), preventing secret leakage in source control.

- **Code Quality Improvements:**
  - Resolved the infamous Python mutable default argument bug (`audit_trail=[]`), initializing fresh list instances inside `enroll_student` so student registration history is isolated per invocation.
  - Eliminated dangerous bare `except:` statements that silently suppressed program crashes, replacing them with specific `KeyError` handling and user-facing warnings.
  - Encapsulated mutable global state into structured module data (`TUITION_LEDGER`), eliminating the `global` keyword.
  - Enforced Pythonic identity checks (`is None`) and cleaned up redundant conditional logic.

- **Maintainability & Style:**
  - Raised the Pylint code rating from **4.00/10 to a perfect 10.00/10**.
  - Reduced Flake8 style and formatting warnings from 12 down to **0**.
  - Adopted standard PEP 8 naming conventions (`snake_case` functions, `UPPER_CASE` constants), added comprehensive docstrings for the module and all functions, wrapped line lengths strictly within 79 characters, and safely managed file I/O using `with` context managers.

---

### 4. What are the limitations of these tools? Did you see any false positives or things they missed?

Static analysis tools rely on AST inspection, pattern matching, and rule heuristics. Consequently, they possess inherent limitations:

1. **Context and Semantic Unawareness:**
   - Bandit flags `hashlib.md5()` regardless of whether the hash is used for cryptographic security or merely as a simple non-security identifier or checksum.
   - Bandit flags any variable named `*_token` or `*_secret` as a potential hardcoded credential (heuristic matching), even if it is a harmless placeholder or mock in unit tests.

2. **Style vs. Correctness Trade-offs:**
   - Pylint and Flake8 enforce strict syntactic rules (e.g., maximum line length of 79 characters, `snake_case` naming). While these rules enhance readability, renaming functions like `enrollStudent` to `enroll_student` can break public API consumers unless all calling code is updated simultaneously.

3. **Inability to Detect Business Logic Bugs:**
   - Static analysis tools completely missed the logical flaw in `drop_course("CS202")`. Course `CS202` originally started with `0` seats and was marked `is_closed: True`. Dropping an enrollment automatically incremented seats to `1` and set `is_closed: False`, artificially expanding the catalog without verifying if the course had ever been enrolled in the first place.
   - The tools also do not verify arithmetic correctness or edge cases like integer overflow or negative fee amounts.

**Conclusion:** Static analysis is an indispensable first line of defense in modern CI/CD pipelines to enforce code health, consistency, and baseline security, but it must be paired with thorough unit testing, integration testing, and human peer review.
