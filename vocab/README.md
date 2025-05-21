# Shedding Hub Vocabulary

[![DOI](https://img.shields.io/static/v1?label=DOI&message=pending&color=blue)](https://github.com/shedding-hub/vocab)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://spdx.org/licenses/MIT.html)
![Version](https://img.shields.io/badge/Version-0.1.0-green)

A controlled vocabulary for studies with pathogen and biomarker shedding information. The ontology is published at [BioPortal](https://bioportal.bioontology.org/ontologies/SHEDDING-HUB).

## Overview

The Shedding Hub Vocabulary (SHV) is a SKOS-based controlled vocabulary designed to standardize terminology for studies involving pathogen and biomarker shedding. It provides a structured framework for describing:

- Analytes (biomarkers and pathogens)
- Specimen types
- Units of measurement
- Reference events
- Participant attributes
- Sample measurements

## Namespace

The namespace for the Shedding Hub Vocabulary is:

```
@prefix shv: <https://shedding-hub.github.io/vocab#>
```

## Top Concepts

The vocabulary is organized around five top-level concepts:

1. **Analyte**: Biomarkers, pathogens, and related measurement parameters
2. **DOI**: Digital object identifiers for source publications or repositories
3. **Participants**: Study subjects and their attributes
4. **Title**: Titles of source publications or repositories
5. **URL**: Access URLs for source publications or repositories

## Key Features

- **SKOS-based**: Follows the Simple Knowledge Organization System standard
- **Domain-specific**: Focused on pathogen and biomarker shedding studies
- **Hierarchical**: Well-structured concept relationships
- **Extensible**: Designed to be expanded as needed

## Example Usage

Here's a simple example of how to use the vocabulary in Turtle format:

```turtle
@prefix shv: <https://shedding-hub.github.io/vocab#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://example.org/study/1> 
  shv:title "SARS-CoV-2 shedding in stool samples" ;
  shv:doi "10.1234/example.12345" ;
  shv:url <https://example.org/study/1> .

<https://example.org/study/1/participant/1> 
  a shv:participants ;
  shv:age "35"^^xsd:integer ;
  shv:sex shv:male .

<https://example.org/study/1/measurement/1> 
  shv:biomarker shv:SARS-CoV-2 ;
  shv:specimen shv:stool ;
  shv:reference_event shv:symptom_onset ;
  shv:time "3"^^xsd:integer ;
  shv:unit shv:gc_wet_gram ;
  shv:value "1.2E5"^^xsd:double .
```

## Vocabulary Structure

The vocabulary includes concepts for:

- **Biomarkers/Pathogens**: SARS-CoV-2, Influenza, PMMoV, etc.
- **Specimen Types**: Stool, Nasopharyngeal swab, Plasma, etc.
- **Measurement Units**: Cycle threshold, gene copies/mL, etc.
- **Reference Events**: Symptom onset, Hospital admission, etc.
- **Participant Attributes**: Age, Sex, Ethnicity, Race, etc.

## Documentation

Full documentation is available at:
- [https://shedding-hub.github.io/vocab/](https://shedding-hub.github.io/vocab/)

## License

This vocabulary is released under the [MIT License](https://spdx.org/licenses/MIT.html).

## Citation

Please cite this vocabulary as:

```
Shedding Hub Vocabulary. (2025). Shedding Hub Project. https://shedding-hub.github.io/vocab
```

## Contact

For questions, suggestions, or contributions, please [open an issue](https://github.com/shedding-hub/vocab/issues) on our GitHub repository or contact the maintainer at [yuke_dot_wang_at_emory_dot_edu](mailto:yuke.wang@emory.edu).
