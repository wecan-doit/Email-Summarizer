# 🔍 Research & Findings

## Initial Discoveries
- Project initiated based on **B.L.A.S.T. Master System Prompt**.
- Primary objective: Automated AI Newsletter Digest.
- Tech Stack identified: Gmail API, Google Docs API, Gemini API, Python.

## Constraints
- Must use OAuth 2.0 for Google Services.
- Whitelist-based filtering required.
- Output must be a daily Google Doc.

## Newsletter Structure Discovery
- **Observation:** User noted that newsletters (Flipboard, Quora) often contain headlines with "Read More" links that direct to external websites.
- **Implication:** The system may need to scrape/crawl the linked URLs to obtain the full context for summarization, rather than relying solely on the email body text.
- **Requirement:** Add web scraping capability (e.g., `requests` + `BeautifulSoup`) to the extraction layer.

## Pilot Run Results (2026-05-07)
- **Success:** The 5-email limit was successfully applied, resulting in a concise digest.
- **Quality:** Summaries include clear TL;DR, bulleted key points, and a professional "So What?" analysis.
- **CLI Issue:** Encountered a persistent model-access loop (`gemini-3-flash-preview` access error) when using the CLI's internal `WebFetch` tool to read the Google Doc.
- **Workaround:** Created `tools/read_doc.py` to fetch Google Doc content via API, which works reliably and bypasses the CLI bug.

## Journey Log & Educational Insights
- **Key Lesson:** The "Link" phase (Phase 2) is the most volatile. Authentication loops are common and require the pilot to be prepared to reset the state (delete tokens).
- **Architecture over CLI:** Relying on Layer 3 tools (Python) rather than CLI built-ins (WebFetch) provides more stability and control over regional model-access errors.
- **Teaching Tip:** When teaching students, emphasize the **OAuth Consent Screen** "Test Users" step, as it is the #1 cause of silent authentication failures.

## New Requirements (2026-05-08)
- **Observation:** User requested a specific time window for fetching newsletters to ensure freshness and avoid backlog processing.
- **Requirement:** Implement a hard filter to only fetch emails from the last 48 hours (`newer_than:2d` in Gmail query). This has been added to Rule #5 in the Constitution.


