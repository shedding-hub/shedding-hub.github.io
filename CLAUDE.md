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
# Download dataset YAML files from shedding-hub repository
make ^_datasets-yaml

# Convert YAML files to markdown for Jekyll collection
make _datasets

# Clean generated files
make clean
```

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

- `index.md`: Homepage displaying all datasets with summary statistics (measurements, participants, studies)
- `team.md`: Team member profiles pulled from `_data/team.yaml`
- `model.md`: Shedding models and tutorials (Bayesian workflows, time-course modeling)
- `vocab/`: Controlled vocabulary for shedding studies (SKOS-based ontology published at BioPortal)

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
