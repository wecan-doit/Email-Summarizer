# 🏗️ B.L.A.S.T. Task Plan: AI Newsletter Digest

## Phase 1: Blueprint (Vision & Logic)
- [x] Complete Phase 1 Discovery (User Confirmation Pending).
- [x] Define JSON Data Schema in `gemini.md`.
- [x] Research helpful resources/libraries (google-api-python-client, etc.)
- [x] Approve Blueprint

## Phase 2: Link (Connectivity)
- [x] Create `.env` for `GEMINI_API_KEY`
- [x] Obtain `credentials.json` for Google Cloud OAuth
- [x] Build `tools/link_test.py`
- [x] Verify Gmail API Connectivity
- [x] Verify Google Docs API Connectivity
- [x] Verify Gemini API Connectivity

## Phase 3: Architect (The 3-Layer Build)
- [x] Create `architecture/` SOPs
- [x] Define `whitelist.txt`
- [ ] Define `keywords.md` (Optional - currently using whitelist)
- [x] Develop `tools/fetch_unread()`
- [x] Develop `tools/batch_summarize()`
- [x] Develop `tools/append_to_doc()`
- [x] Build `tools/pilot_main.py` (Navigation Layer)
- [x] **New:** Implement 48-hour fetch filter (`newer_than:2d`)

## Phase 4: Stylize (Refinement & UI)
- [x] Refine Output Schema (TL;DR, "So What?", Citations)
- [x] Implement Rich Console UI (Progress bars, etc.)
- [x] Final visual polish of Google Doc output
- [x] **New:** Create High-Aesthetic Visual Dashboard for non-developers


## Phase 5: Trigger (Deployment)
- [ ] Set up daily execution trigger (Local Task Scheduler/Cron)
- [x] Implement "Mark as Read" post-processing
- [ ] Finalize Maintenance Log in `gemini.md`

## Additional Recommended Features to Add for the optimalism of the project.
- [ ] improving the web scraper. As we discussed, the current
  implementation is brittle, and I recommend replacing it with the more powerful trafilatura library.