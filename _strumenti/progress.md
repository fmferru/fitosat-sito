# SDD ledger — plan: /home/claude/docs/plans/2026-11-19-prima-schermata.md
Ruling: no git repo in this workspace — checkpoints are file copies, task-start/task-done scripts not used — cost if wrong: no commit history, recoverable from checkpoint copies.
Pre-flight: T2 consumes T1 webp (1600x1000) ok; T3 consumes navTone inContent + T2 progress z — both defined in T2/existing code.
Task 1: complete (check_bg.py → PASS; orbit 17KB, country 58KB, rows 49KB)
Task 2: Ruling: removed old blurred JPEG and repurposed .intro-veil as a bottom gradient behind the slogan; slogan block fixed at top 52%/bottom 2.5% with h1 clamp(1.45rem, min(5vw,4.6vh), 3.4rem) to fit 375x667 — cost if wrong: slogan slightly smaller than before on desktop.
Task 2: complete (check_intro.js → PASS on 390x844, 1440x900, 375x667, 1366x768 + reduced motion)
Task 3: Ruling: tucking disabled via CSS override + navTone no longer adds class; intro wordmark hidden (visibility) after handoff at z>=0.3, symbol+tagline fade over z 0-0.2; reduced motion shows brandBar and hides intro wordmark — cost if wrong: duplicate/missing wordmark only in reduced-motion mode.
Task 3: complete (check_bar.js → PASS at 320/390/1440 light + 390 dark; check_intro.js → PASS)
Task 4: Ruling: added full-width translucent bar background (#barBg) inside content instead of a pill behind the wordmark — page text showed through around the pill — cost if wrong: header band takes ~66px of screen inside content.
Task 4: complete (gen_en.py → no untranslated; check_intro/check_bar → PASS on IT and EN; previews sent)
Final review: fresh reviewer (opus) — 0 critical, 2 important, 5 minor
Final: fixed handoff miss after height-only resize — check_fix.js RED→GREEN, suite 3/3 IT + EN
Final: fixed invisible #brandBar focusable — check_fix.js RED→GREEN, suite 3/3 IT + EN
Final: minor (deferred): wordmark dips briefly at handoff (instant hide vs 0.25s fade)
Final: minor (deferred): white wordmark less legible over light countryside fields (z 0.3–0.6)
Final: minor (deferred): countryside image slightly soft on 2560px screens
Final: minor (deferred): leftover unused code (p, logoTarget, --slogan-top, pastIntro/lastY, .tucked CSS)
Final: minor (deferred): intro CTA focusable while slogan invisible (pre-existing)
Final: published (deploy 6afe50d4) with cleanup + slogan 'Radici nella terra, occhi dal cielo'
Final: published HD intro orbit→rows (deploy 6aff5b1e)
