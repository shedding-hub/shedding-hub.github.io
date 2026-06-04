# Terms of Use Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Terms of Use page to the Shedding Hub website and link it from the footer.

**Architecture:** Create one new Jekyll page (`terms.md`) using the existing `default` layout, then add a "Terms of Use" link to the footer in `_layouts/default.html`. No new layouts, styles, or data files are needed.

**Tech Stack:** Jekyll, Bulma CSS, Liquid templating, HTML

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `terms.md` | Create | Terms of Use page content |
| `_layouts/default.html` | Modify (footer only) | Add link to `/terms.html` |

---

### Task 1: Create the Terms of Use page

**Files:**
- Create: `terms.md`

- [ ] **Step 1: Create `terms.md` with the following content**

```markdown
---
layout: default
title: Terms of Use
---

<section class="section">
  <div class="container is-max-desktop">
    <h1 class="title">Terms of Use</h1>
    <p class="subtitle has-text-grey">Last updated: June 4, 2026</p>

    <div class="content">

      <h2>Acceptance of Terms</h2>
      <p>
        By accessing or using the Shedding Hub website ("the Site"), you agree to be bound by
        these Terms of Use. If you do not agree, please do not use the Site.
      </p>

      <h2>Data and Attribution</h2>
      <p>
        All datasets and content provided by the Shedding Hub are made available under the
        <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener">
        Creative Commons Attribution 4.0 International (CC BY 4.0)</a> license. You are free
        to share and adapt the material for any purpose, including commercial use, provided
        that you give appropriate credit.
      </p>
      <p>
        When using data from Shedding Hub, please cite both the Shedding Hub platform and
        the original published study from which the data were extracted. A suggested citation
        for the platform:
      </p>
      <blockquote>
        Wang, Y., Hoffmann, T., et al. Shedding Hub: A curated platform for biomarker
        shedding data. <a href="https://shedding-hub.github.io">https://shedding-hub.github.io</a>
      </blockquote>
      <p>
        Each dataset page lists the original publication DOI; please also cite that source.
      </p>

      <h2>Third-Party Content</h2>
      <p>
        The datasets hosted on Shedding Hub are derived from peer-reviewed scientific
        publications. The Shedding Hub project does not claim ownership of the underlying
        data. Users are responsible for complying with any terms or licenses associated with
        the original publications.
      </p>

      <h2>Disclaimer</h2>
      <p>
        All data and content are provided "as is" without warranty of any kind, express or
        implied. The Shedding Hub project makes no representations about the accuracy,
        completeness, or suitability of the data for any particular purpose. Use of the
        data is at your own risk.
      </p>

      <h2>Contact</h2>
      <p>
        Questions about these Terms of Use? Contact us at
        <a href="mailto:sheddinghub@gmail.com">sheddinghub@gmail.com</a>.
      </p>

    </div>
  </div>
</section>
```

- [ ] **Step 2: Commit**

```bash
git add terms.md
git commit -m "Add Terms of Use page"
```

---

### Task 2: Add Terms of Use link to the footer

**Files:**
- Modify: `_layouts/default.html` (footer section, around line 120–122)

- [ ] **Step 1: Locate the footer in `_layouts/default.html`**

The current footer reads:

```html
  <footer class="footer" style="padding: 1.5rem; text-align: center; background-color: var(--bg-secondary); border-top: 1px solid var(--border-color); color: var(--text-light);">
    <p>&copy; Copyright 2026. Emory CIDMATH. All Rights Reserved.</p>
  </footer>
```

- [ ] **Step 2: Replace the footer with the updated version that includes the Terms of Use link**

Replace the entire `<footer>` block with:

```html
  <footer class="footer" style="padding: 1.5rem; text-align: center; background-color: var(--bg-secondary); border-top: 1px solid var(--border-color); color: var(--text-light);">
    <p>&copy; Copyright 2026. Emory CIDMATH. All Rights Reserved.</p>
    <p style="margin-top: 0.5rem; font-size: 0.875rem;">
      <a href="/terms.html" style="color: var(--text-light);">Terms of Use</a>
    </p>
  </footer>
```

- [ ] **Step 3: Verify the site builds without errors**

Run:
```bash
bundle exec jekyll build
```
Expected: `Build complete!` with no errors or warnings about front matter.

- [ ] **Step 4: Verify the pages render correctly**

Run:
```bash
bundle exec jekyll serve
```

Then check:
- `http://localhost:4000/terms.html` — page loads, all five sections visible, CC BY link works, mailto link correct
- `http://localhost:4000/` — footer now shows "Terms of Use" link below the copyright line
- Click the "Terms of Use" link in the footer — navigates to `/terms.html` correctly
- Toggle dark mode — footer link color uses `var(--text-light)` and renders legibly in both themes

- [ ] **Step 5: Commit**

```bash
git add _layouts/default.html
git commit -m "Add Terms of Use link to footer"
```
