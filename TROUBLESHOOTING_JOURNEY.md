# 🛡️ B.L.A.S.T. Battle Scars & Troubleshooting Guide

This document captures the real-world challenges, bugs, and "gotchas" encountered during the implementation of the AI Newsletter Digest. Use this to teach others and to skip the pain points.

---

## 🛑 1. The "Model Access Loop" (Gemini CLI Bug)
**Symptoms:** 
- CLI asks to switch models repeatedly.
- Error: `It seems like you don't have access to gemini-3-flash-preview`.
- Selecting "Switch to gemini-2.5-pro" results in the same window/error.

**The Cause:** 
The Gemini CLI's internal `WebFetch` tool defaults to a specific preview model (e.g., `gemini-3-flash-preview`) that may not be available on all accounts or in all regions.

**The Fix/Workaround:**
- **Avoid built-in WebFetch:** Do not rely on the CLI's automatic URL fetching for sensitive tasks like reading Google Docs.
- **Custom Scripting:** Use a dedicated Python script (e.g., `tools/read_doc.py`) using the official `google-api-python-client` to fetch content. This bypasses the CLI's internal model checks.

---

## 🔑 2. The `RefreshError` (Scope Change Conflict)
**Symptoms:**
- `google.auth.exceptions.RefreshError: ('invalid_scope: Bad Request', ...)`
- Script crashes during token refresh.

**The Cause:**
You upgraded the scopes (e.g., changed `gmail.readonly` to `gmail.modify` in your code), but your existing `token.json` was authorized only for the old, narrower scope. Google refuses to refresh a token into a broader scope.

**The Fix:**
1. **Delete the Token:** Manually delete `token.json` in your project root.
2. **Re-Authenticate:** Run your `link_test.py` script again. A browser window will open, and you can grant the new permissions.

---

## 📋 3. Google Workspace Setup Precautions
**Symptoms:**
- 403 Forbidden or 401 Unauthorized errors.

**Guidelines for New Users:**
- **Project Type:** Ensure your Google Cloud project is configured as a "Desktop App" in the OAuth Consent Screen.
- **Scopes:** Always define the *minimum* required scopes first, but be prepared to delete `token.json` if you ever need to add a new permission (like "Mark as Read").
- **Credentials:** Your `credentials.json` must be in the root folder, but **NEVER** commit it to GitHub. Add it to `.gitignore` immediately.

---

## 📈 4. The "42-Page Document" Problem (Efficiency)
**Symptoms:**
- The pilot run generates a massive document that costs too many tokens to process.

**The Fix:**
- **Implement a Hard Limit:** Always add `maxResults` to your API calls (e.g., `service.users().messages().list(..., maxResults=5)`).
- **Curation First:** Rely on the `whitelist.txt` to prevent non-essential emails from even being scanned.

---

## 🚀 How to Teach This (Step-by-Step)
1. **The Sandbox:** Start with `link_test.py` to prove connectivity.
2. **The Constitution:** Fill out `gemini.md` before writing a single line of logic.
3. **The Pilot:** Run a "Pilot" with only 1-2 items to verify the style.
4. **The Trigger:** Only automate (Cron/Task Scheduler) once the Pilot is 100% deterministic.
