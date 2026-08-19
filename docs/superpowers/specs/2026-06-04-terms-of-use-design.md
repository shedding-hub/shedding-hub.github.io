# Terms of Use — Design Spec

**Date:** 2026-06-04
**Status:** Approved

## Summary

Add a Terms of Use page to the Shedding Hub website. The page is concise, plain-language, and appropriate for an academic open-data research platform.

## Decisions

- **Legal entity:** The Shedding Hub project (not Emory University or CIDMATH specifically)
- **License:** CC BY — free for any use including commercial, with attribution required
- **Contact:** sheddinghub@emory.edu
- **Approach:** Minimal (~300 words), plain-language, no legal jargon

## Page Structure

File: `terms.md` at the repo root, using `layout: default` and `title: Terms of Use`.

Five sections:

1. **Acceptance** — Using the site constitutes acceptance of these terms.
2. **Data & Attribution (CC BY)** — Data freely available for any purpose. Users must credit original published studies and cite Shedding Hub. Include a suggested citation format.
3. **Third-Party Content** — Datasets are derived from peer-reviewed publications; Shedding Hub does not own the underlying data. Users should also comply with original publication terms.
4. **Disclaimer** — Data provided "as is" without warranty of accuracy or completeness.
5. **Contact** — Questions to sheddinghub@emory.edu.

## Navigation

- Add a "Terms of Use" link to the **footer** in `_layouts/default.html`.
- Do NOT add it to the navbar (it is a meta/legal page, not primary navigation).

## Styling

- Use `<section class="section">` with Bulma's `.content` class for readable prose.
- Matches the styling pattern of `team.md` and `model.md`.
- No custom CSS or special components needed.

## Files to Create/Modify

| File | Action |
|---|---|
| `terms.md` | Create — new Terms of Use page |
| `_layouts/default.html` | Modify — add footer link to `/terms.html` |
