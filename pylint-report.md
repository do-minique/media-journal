
# Pylint report

Pylint gives the following report:


```bash
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:31:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:73:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:97:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:103:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:123:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:167:11: W0718: Catching too general exception Exception (broad-exception-caught)
app.py:123:0: R0911: Too many return statements (7/6) (too-many-return-statements)
app.py:171:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:171:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:222:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:222:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:242:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:308:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:337:15: W0718: Catching too general exception Exception (broad-exception-caught)
app.py:308:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:343:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:369:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:369:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:394:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:394:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:414:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:445:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:465:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:471:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module dbfunctions
dbfunctions.py:1:0: C0114: Missing module docstring (missing-module-docstring)
dbfunctions.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:36:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:61:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:72:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:76:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:81:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:87:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:152:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:192:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:212:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:234:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:243:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:251:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:268:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:277:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:286:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:295:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:299:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:310:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:315:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:323:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:323:0: R0913: Too many arguments (6/5) (too-many-arguments)
dbfunctions.py:341:0: C0116: Missing function or method docstring (missing-function-docstring)
dbfunctions.py:350:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:14:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:15:0: C0103: Constant name "media_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:16:0: C0103: Constant name "review_count" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 8.55/10 (previous run: 8.53/10, +0.02)
```

## Docstring warnings

```bash
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
```
Most of the report’s messages concern missing docstring comments. A conscious decision has been made in the application not to use them.

## Exception warnings

```bash
app.py:167:11: W0718: Catching too general exception Exception (broad-exception-caught)
```
These Pylint warnings indicate that the code is catching the very general Exception class instead of handling more specific, expected exceptions.

Left as-is intentionally because this is a top-level safeguard that catches any unexpected errors and logs the issue instead of crashing the application.

## Missing return values

```bash
app.py:171:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```
This warning means that some code paths in the function return a value while others return nothing (None), leading to inconsistent return behavior.

This is due to some functions using the GET and POST methods, where a return value is not defined for other cases. These cases are impossible however, as the decorator requires the method to be either GET or POST.

## Constant naming

```bash
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```
This warning means that some constant(s) does not follow the expected naming convention, which requires constants to be written in UPPER_CASE (e.g., SECRET_KEY).

Pylint interprets some variables as constants, but in this application variable names are intentionally written in lowercase.

## Too many return statements

```bash
app.py:123:0: R0911: Too many return statements (7/6) (too-many-return-statements)
```
This warning means that the function contains more return statements than the recommended limit (7 instead of 56. Using more return statements in this application is intentional.

## Too many arguments

```bash
dbfunctions.py:323:0: R0913: Too many arguments (6/5) (too-many-arguments)
```
This warning means that the function takes more arguments than the recommended limit (6 instead of 5). Using more arguments is intentional, because some functions need all these separate values.


