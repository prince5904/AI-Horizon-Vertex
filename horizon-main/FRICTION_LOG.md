# Project Friction Log

This document records the key challenges, investigations, and resolutions encountered during the development of the AI Recruiter Copilot.

---

## **Entry 1: The Composio SDK Version Conflict**

- **Date:** October 21-22, 2025
- **Status:** **Resolved**

### 1. Problem Description

A collaborator (and potential judge) was unable to run the project after a fresh installation. The pipeline failed immediately with an `ImportError`, specifically:

```
ImportError: cannot import name 'ComposioToolSet' from 'composio'
```

This was a critical issue, as it meant the project was not easily reproducible, which could lead to immediate disqualification or failure during a technical review.

### 2. Investigation & Troubleshooting Steps

Our initial assumption was that the local code was incorrect. This led to a series of steps that initially worsened the problem before revealing the true cause.

1.  **Initial "Fix" Attempt:** Based on the error, we assumed `ComposioToolSet` was deprecated. We updated all 5 core files to import and use the `Composio` class instead.

2.  **New Error Emerges:** This change resolved the `ImportError` but introduced a new, deeper runtime error:
    ```
    AttributeError: 'Composio' object has no attribute 'execute_action'
    ```

3.  **Root Cause Analysis:** The `AttributeError` was the key. It signaled a **major breaking change** in the Composio SDK's API. The method for executing tools had changed from `execute_action(...)` to a new `tools.execute(...)` pattern.

4.  **Version Verification:**
    - We checked our working environment's installed version using `pip show composio`, which confirmed we were using `v0.8.20`.
    - We checked the collaborator's environment and realized they had installed a newer version (`v1.0+`) by simply running `pip install composio`.

5.  **Conclusion:** The friction was caused by a mismatch between the project's code (written for SDK `v0.8.20`) and the collaborator's environment (which had SDK `v1.0+`). The project's `requirements.txt` file was correct, but the collaborator had not used it.

### 3. Resolution

Instead of migrating the entire project to the new, unfamiliar v1.0 API under a tight deadline, we focused on ensuring **reproducibility**.

1.  **Code Reversion:** We reverted all changes, restoring the code to use the stable and working `ComposioToolSet` and `execute_action` methods, consistent with version `0.8.20`.

2.  **Dependency Lockdown:** We confirmed that `requirements.txt` correctly pinned the version: `composio==0.8.20`.

3.  **Documentation Enhancement (The Key Solution):** We realized the installation process was the weak link. To prevent this from happening with judges, we created robust documentation:
    -   **`INSTALLATION.md`:** A new, detailed, step-by-step guide was created. It explicitly warns about the version sensitivity and provides exact commands for setting up the virtual environment and installing dependencies from `requirements.txt`.
    -   **Troubleshooting Section:** Added a "Common Issues" section to `INSTALLATION.md` and `README.md` that directly addresses the `ImportError` and `AttributeError`, with the clear solution: `pip install composio==0.8.20 --force-reinstall`.
    -   **`README.md` Update:** Added a prominent warning box at the top of the `README.md`, directing users to read `INSTALLATION.md` *before* starting.

### 4. Key Takeaways

-   **Dependency Pinning is Crucial:** Never assume `pip install <package>` is sufficient. A `requirements.txt` file with pinned versions (`==`) is essential for reproducibility.
-   **Documentation is as Important as Code:** A clear, explicit installation guide can prevent 99% of environment-related issues.
-   **Breaking Changes are Inevitable:** When an SDK error appears, the first step should be to check for version mismatches and consult the library's changelog or documentation.

---
