# 📖 SOP 01: Intelligent Extraction

## 🎯 Goal
Extract clean, relevant text from whitelisted newsletters and follow external "Read More" links to ensure a complete context for summarization.

## 📥 Inputs
- `whitelist.txt`: List of authorized sender emails.
- Gmail API: Source of unread messages.

## ⚙️ Logic
1. **Fetch Unread**: Query Gmail for `is:unread` messages from senders in `whitelist.txt`.
2. **Raw Extraction**: Extract the body text (preferring `text/plain`, falling back to `text/html` and stripping tags).
3. **Link Detection**: Scan for "Read More" or "Full Story" links if the snippet is less than 500 characters.
4. **Web Scrape (Conditional)**: If a "Read More" link is found, follow it using `requests` and extract the primary article content.
5. **Payload Generation**: Format the data into the JSON schema defined in `gemini.md`.

## ⚠️ Edge Cases
- **No unread emails**: System logs "No updates" and terminates gracefully.
- **Broken links**: If "Read More" fails, proceed with the existing email snippet and log a warning.
- **Paywalls**: If the external link hits a paywall, extract what is visible.

## 🛠️ Tooling
- `tools/fetch_unread()`: Gmail interaction.
- `tools/web_extractor()`: Scraping external content.
