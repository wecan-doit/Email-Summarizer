# 📖 SOP 03: visual Delivery

## 🎯 Goal
Present the intelligence digest in a professional, easy-to-scan Google Doc with a clear visual hierarchy.

## 📥 Inputs
- Summarized items (from SOP 02).
- `templates/doc_schema.html`: (Optional) Structural reference.

## ⚙️ Logic
1. **Header Generation**: Insert H1 with the current date.
2. **TL;DR Block**: Insert a high-level executive summary of all news at the top.
3. **Item Appending**: For each item, append:
    - H2: Source Name
    - Body: Key Points (Bullet list)
    - **Bold**: "So What?" section
    - Hyperlink: "Source"
4. **Post-Processing**: Mark all successfully processed emails as "READ" in Gmail to clear the queue.

## ⚠️ Edge Cases
- **API Quota limits**: If appending many items, use `batchUpdate` to reduce calls.
- **Network failure**: If delivery fails, log the state in `.tmp/` so it can be resumed without re-summarizing (saving Gemini tokens).

## 🛠️ Tooling
- `tools/append_to_doc()`: Google Docs API interaction.
- `tools/mark_as_read()`: Gmail API cleanup.
