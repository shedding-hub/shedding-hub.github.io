# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based GitHub Pages website for the Shedding Hub, a platform for data and statistical models for biomarker shedding. The site displays datasets, tutorials, team information, and controlled vocabulary for pathogen and biomarker shedding studies.

## Build and Development

### Building the Site Locally

```bash
bundle install
bundle exec jekyll serve
```

### Dataset Management

The site uses a Makefile to fetch and process dataset YAML files from the main shedding-hub repository:

```bash
# Download dataset YAMLs, figures, and the fitted-parameter catalog
make ^_datasets-yaml

# Convert YAML files to markdown for Jekyll collection
make _datasets

# Clean generated files
make clean
```

The `_datasets/%.md` rule builds front matter with `printf`, not `echo`. Only some
shells expand `\n` in `echo`; the ones that do not (Git Bash, for one) write a
literal `---\n`, which Jekyll reads as malformed front matter and then drops every
dataset from the collection **silently** — a site that builds cleanly with an empty
catalog. If the dataset count ever renders as zero, check that first.

By default, datasets are fetched from the `main` branch. To use a different branch:

```bash
make ^_datasets-yaml DATA_REF=your-branch-name
```

### GitHub Actions Workflow

The site automatically builds and deploys via `.github/workflows/jekyll-gh-pages.yml`:
1. Fetches dataset YAMLs from shedding-hub/shedding-hub repository
2. Converts them to markdown files
3. Builds the Jekyll site
4. Deploys to GitHub Pages

The workflow triggers on:
- Push to main branch
- Pull requests to main
- Manual workflow dispatch
- Repository dispatch events from the main shedding-hub repository

## Architecture

### Jekyll Configuration

- **Collections**: Uses a `datasets` collection configured in `_config.yml` with auto-generated output and a default `dataset` layout
- **Strict Front Matter**: Enabled to catch YAML parsing errors early

### Site Structure

- `index.md`: Homepage. Every catalog figure it shows (studies, participants, measurements, pathogens, specimen types) is computed in Liquid from `site.datasets` at build time, so pushing datasets updates the page with no edits.
- `team.md`: Team member profiles pulled from `_data/team.yaml`
- `model.md`: Shedding models and tutorials (Bayesian workflows, time-course modeling)
- `datasets.html`: The catalog. Cards are rendered for every dataset and then filtered and paginated **in the browser** (`DatasetsFilter` in the default layout, 24 per page). Pagination is deliberately not server-side: the search and biomarker/specimen filters must cover every dataset, not just the page being viewed. Any filter change resets to page one, since a narrower result set can have fewer pages than the one on screen.
- `fits.html`: One row per fitted analyte, from `_data/shedding_catalog.yaml`, with client-side filtering and column sorting.
- `curation.html`: AI curation pipeline
- `vocab/`: Controlled vocabulary for shedding studies (SKOS-based ontology published at BioPortal)

### Derived Counts

Manual biocuration closed at a fixed number of studies; everything curated since is
AI-assisted. `manual_curated_count` in `_config.yml` holds that constant, and both
`index.md` and `curation.html` derive the AI-curated count as
`site.datasets | size | minus: site.manual_curated_count`. Do not hardcode either
number in a page — bump the constant only if the manual benchmark itself changes.

### Two Sources of Fit Data

There are two, they disagree, and that is expected:

- `_data/figures.json` — the figure index, rebuilt whenever datasets land, so it
  **leads**. Counts fitted curve images. Has no parameters. Use it for headline
  counts of how much is fitted.
- `_data/shedding_catalog.yaml` — the catalog the Python package ships, rebuilt at
  each package release, so it **lags**. The only source of fit parameters (peak,
  sigma, censoring limit, AIC, subject and measurement counts).

At the time of writing the index held 197 curves across 68 studies while the catalog
held 144 fits across 48 studies. `fits.html` states both rather than picking one, so
neither the coverage nor the parameter table misrepresents the other. Do not "fix"
the gap by making one number match the other.

**The gap is not staleness.** The catalog is rebuilt in the same commit as a data
drop. The figures are rendered from the concentration catalog *and* a
cycle-threshold catalog, and Ct analytes are deliberately excluded from the shipped
package because their peak is measured in cycles below a reference rather than as a
log10 concentration. 45 studies are concentration-only, 20 Ct-only, 3 have both.

`_data/shedding_catalog_ct.yaml` is copied by `make ^_datasets-yaml` when the data
repository publishes one. It is gitignored *there* today, so the file is normally
absent and the fits page shows concentration fits with no value-type filter. When it
appears, the filter turns on by itself and defaults to concentration — a Ct peak and
a concentration peak share the Peak column but not its meaning, so they must never be
mixed without the reader asking. The Ct rows read their peak from `peak_cycles`
rather than `peak_log10`.

### Homepage Hero

The hero plots real measurements from a reference dataset rather than decorative
artwork. `tools/make_hero_trace.py` reads one study out of `_datasets/` and writes
normalized SVG coordinates to `_data/hero_trace.yaml`, which `index.md` renders as
paths. The output is committed because CI builds with Ruby only and has no Python;
regenerate with `make hero-trace` after `make ^_datasets-yaml`, and only when
changing the featured study or the plot geometry.

### Curation Growth Curve

`curation.html`'s "Where it stands" section carries a step chart of how the catalog
actually grew, so the claim that the agents changed the slope is shown rather than
asserted. The homepage's AI-curation card links straight to it (`/curation.html#growth`).

**Nothing generates it here.** The shape is read out of the *data* repository's commit
history, which this site never receives — `_datasets/` is unpacked from an archive with
no git attached, and CI is Ruby only. So `scripts/build_curation_growth.py` builds it
there, `refresh-figures.yaml` republishes it on every data change, and
`make ^_datasets-yaml` copies `curation_growth.yaml` out of the same archive it already
downloads, exactly like `figures.json` and `shedding_catalog.yaml`. `_data/curation_growth.yaml`
is therefore gitignored and generated, not edited.

Tolerated when absent, like the figures: a `DATA_REF` predating it still builds, and
`{%- if growth -%}` makes the section read as it did before the figure existed.

The published file carries normalized SVG coordinates rather than counts — Liquid has no
arithmetic worth the name, so ticks, label positions and the path are all resolved
upstream. To change the geometry, change the script in the data repository.

The caption prints the figure's `as_of` date while the stat grid above comes from
`site.datasets`. Both now refresh on the same deploy, so they should agree; the `as_of`
line stays because it dates the *history*, and it is the tell if a refresh ever fails.

One trap, guarded upstream but worth knowing here: the curve is built from `git log`, so
a shallow clone silently collapses it to a single point. The data repository checks out
with `fetch-depth: 0` and its script refuses fewer than 20 `data/` commits.

### Design Tokens

`_layouts/default.html` defines the palette, typography, and theme variables for the
whole site. Two things there are easy to break:

- Bulma 1.x derives `is-primary` and `is-link` components from its own
  `--bulma-*-h/s/l` variables, so retuning `--primary-color` alone does not move
  buttons or tags off Bulma's stock hue. Both sets are defined together.
- `--bulma-link-text` and the primary button text colors are pinned explicitly.
  Bulma's automatic derivations produced link and button contrast below the WCAG AA
  4.5:1 threshold against this palette.

Light-theme rules that override a `[data-theme="dark"]` rule must be scoped
`:root:not([data-theme="dark"])`. At equal specificity with matching `!important`,
source order alone decides the winner and the dark theme silently loses.

### Layouts

- `_layouts/default.html`: Base layout with Bulma CSS framework, navigation, Font Awesome icons, and JavaScript for thousand separators and mobile menu
- `_layouts/dataset.html`: Dataset detail page showing analytes, participants, measurements, and biomarker information with computed statistics using Liquid

### Data Flow

1. Dataset YAML files are downloaded from the main shedding-hub repository
2. Makefile converts YAML to markdown with front matter, transforming `url:` to `source_url:` to avoid conflicts with Jekyll's built-in `url` field
3. Jekyll processes these as collection items with the dataset layout
4. Liquid templates calculate statistics (participant counts, measurement counts, biomarker types) dynamically

### Key Data Structures

Dataset YAML files contain:
- `title`, `description`, `doi`, `source_url`
- `analytes`: Hash of analyte configurations (biomarker, specimen, unit, limits of detection/quantification)
- `participants`: Array of participant objects with `measurements` arrays containing `analyte`, `time`, `value`, etc.

### External Resources

- CSS: Bulma 1.0.2 via CDN
- Icons: Font Awesome 6.6.0 via CDN
- Vocabulary: SKOS-based controlled vocabulary namespace `https://shedding-hub.github.io/vocab#`

## Important Notes

- Dataset markdown files in `_datasets/` are auto-generated from YAML - do not edit them manually
- The site relies on data from the external shedding-hub/shedding-hub repository
- Liquid template logic in layouts performs extensive on-the-fly calculations for statistics
- The vocabulary is published separately at BioPortal as a controlled ontology
