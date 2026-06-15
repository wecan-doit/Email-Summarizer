# ☁️ Google Cloud Setup Guide (B.L.A.S.T. Implementation)

This guide provides the precise steps to configure Google Cloud for the Email Summarizer project. Use this for onboarding new users/students.

---

## 🛠️ Step 1: Create a Google Cloud Project
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Select a Project** > **New Project**.
3. Name it `B-L-A-S-T-Email-Digest` and click **Create**.

## 🔑 Step 2: Enable APIs
You must enable the following three APIs:
1. **Gmail API**
2. **Google Docs API**
3. **Google Drive API** (Required for metadata/permissions)

*Search for each in the Library and click **Enable**.*

## 👤 Step 3: Configure OAuth Consent Screen
This is the most common failure point.
1. Click **APIs & Services** > **OAuth consent screen**.
2. Select **External** and click **Create**.
3. **App Information**: Enter a name (e.g., "Email Digest") and your email.
4. **Developer Contact**: Enter your email.
5. **Scopes**: Click "Add or Remove Scopes". Manually add:
   - `.../auth/gmail.modify`
   - `.../auth/documents`
6. **Test Users**: Add your own email address as a test user. **CRITICAL: If you skip this, your authentication will fail.**

## 💳 Step 4: Create Credentials
1. Click **APIs & Services** > **Credentials**.
2. Click **Create Credentials** > **OAuth client ID**.
3. **Application type**: Select **Desktop app**.
4. **Name**: `B.L.A.S.T. Local Client`.
5. Click **Create**, then click the **Download JSON** icon for the client you just created.
6. Rename the downloaded file to `credentials.json` and move it to your project root.

---

## 🚀 Step 5: Initial Authentication
1. Ensure `credentials.json` is in the same folder as your code.
2. Run your link test script:
   ```powershell
   python tools/link_test.py
   ```
3. A browser window will open. Select your Google account and click "Advanced" > "Go to Email Digest (unsafe)" to grant permissions.
4. Once completed, a `token.json` file will appear in your folder. **This is your persistent key.**

---

## 🛡️ Common Troubleshooting
- **Error: "Project not configured for OAuth"**: Ensure you added your email to "Test Users" in Step 3.
- **Error: "Scope Mismatch"**: Delete `token.json` and re-run the script if you changed permissions in your code.
