# Unsecure PWA — Security Audit & Patch

A security assessment of an intentionally vulnerable Flask progressive web application,
completed as part of Year 12 Software Design & Development at Inner Sydney High School.

The application was evaluated during its testing and debugging phase. Five vulnerabilities
were identified through manual code review and penetration testing. One instance of each
vulnerability was patched to demonstrate understanding of the fix — the intentionally
vulnerable code is preserved elsewhere in the repo for reference.

---

## Vulnerabilities Identified & Patched

### 1. Broken Authentication
**How it existed:** No password strength requirements, no rate limiting on the login route,
a narrow timing delay (80–90ms) that enabled username enumeration, and passwords stored
as plain text with no hashing or salt.

**Fixes applied:**
- Added `pattern` attribute to signup form enforcing minimum 8 characters, uppercase,
  lowercase and a number
- Added rate limiting via `Flask-Limiter` — 5 login attempts per minute per IP
- Widened timing delay from 10ms range to 150ms range (50–200ms) to prevent timing-based
  username enumeration
- Implemented `bcrypt` password hashing and salting before database storage

---

### 2. Cross-Site Scripting (XSS) — Stored
**How it existed:** Feedback submitted through the form was written directly into
`success_feedback.html` via an f-string in `listFeedback()` with no encoding applied.
Any HTML or JavaScript submitted as feedback was rendered as live markup in every user's
browser.

**Fix applied:**
- Imported Python's built-in `html` module and wrapped feedback output with `html.escape()`
  before writing to file, converting characters like `<` and `>` into safe HTML entities

---

### 3. Cross-Site Request Forgery (CSRF)
**How it existed:** No CSRF token validation on any form. Flask processed POST requests
based solely on the presence of form fields, with no origin verification. A forged request
from a malicious page would be accepted without question.

**Fix applied:**
- Installed `flask-wtf` and initialised `CSRFProtect(app)` with a `SECRET_KEY` generated
  via `os.urandom(32)`
- Added a hidden `{{ csrf_token() }}` field to each HTML form so Flask validates token
  on every POST

---

### 4. Invalid Forwarding and Redirecting (Open Redirect)
**How it existed:** Three route handlers (`home()`, `signup()`, `addFeedback()`) each read
a `url` parameter from the GET query string and passed it directly to `redirect()` with no
validation. An attacker could append `?url=https://evilsite.com` to any of these routes.

**Fix applied:**
- Removed all three unvalidated redirect blocks entirely, as they served no essential
  purpose in the application's core logic
- Documented the correct implementation using an allowlist of permitted internal paths
  for cases where redirects are genuinely required

---

### 5. SQL Injection
**How it existed:** The login query in `user_management.py` was constructed using
f-string concatenation, directly embedding user input into the SQL. Entering
`hi' or '1'='1` as a password bypassed authentication entirely.

**Fix applied:**
- Replaced string concatenation with parameterised queries using `?` placeholders,
  preventing user input from ever being interpreted as SQL

---

### Bonus: Malicious Third-Party Script Inclusion
**Identified in appendix:** A script tag in `layout.html` was loading JavaScript from
an unrecognised external domain unrelated to Bootstrap. Because `layout.html` is the base
template, this would execute on every page for every user.

**Fix applied:** Removed the script tag entirely.

---

## Scope Note

This project patches **one instance of each vulnerability** to demonstrate understanding
of the fix. The remaining vulnerable code is intentionally left in place — this is a
learning and assessment exercise, not a production hardening effort.

---

## What I Learned

- How to identify vulnerabilities through both manual code review and dynamic testing (DAST)
- The difference between stored and reflected XSS, and why sanitising at retrieval matters
  as much as at input
- Why parameterised queries eliminate SQL injection at the driver level
- How CSRF tokens work and why session cookies alone are not sufficient
- How timing side-channels can leak information even without direct data exposure
- The value of security by design — retrofitting fixes is harder and riskier than
  building securely from the start

---

## Tools & Libraries Used

- Python / Flask
- flask-wtf (CSRF protection)
- flask-limiter (rate limiting)
- bcrypt (password hashing)
- SQLite
- Python `html` module (XSS escaping)

---

## Report

The full security assessment report is available in [this repository](https://github.com/Squ1dddy/Unsecure_PWA/blob/main/SECURITY%20FUNDAMENTALS%20AND%20ASSESSMENT%20REPORT%20BEAU%20-%20SW%20AT2.pdf). It covers each. It covers each
vulnerability in detail including business risk, technical description, identification
method, and fix with code evidence. It also covers broader concepts including
cryptography, sandboxing, security by design, privacy by design, and defensive data
input handling.

> Adapted from the Australian Signals Directorate's Australian Cyber Security Centre
> framework (2022).
