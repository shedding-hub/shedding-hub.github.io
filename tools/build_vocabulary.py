"""
Bring vocab/shedding-hub.ttl up to date with the data schema.

The vocabulary had drifted sixteen months behind: 7 biomarkers published
against 28 in the schema, 11 specimens against 31. Hand-maintaining a second
copy of a list that changes with every data batch is what produced that, so the
four enum lists are generated from `data/.schema.yaml` instead. The schema is
the authority for *which terms exist*; everything else in the file stays as
written.

This edits the existing graph rather than regenerating the file, and the
distinction is load-bearing. The vocabulary is published at a resolvable
namespace and submitted to BioPortal, so a local name is a public identifier. A
first draft of this script rebuilt the file from scratch and would have renamed
`shv:SARS-CoV-2` to `shv:SARS_CoV_2` and dropped thirty authored concepts --
the participant attributes, the measurement fields, the detection limits -- none
of which appear in any enum. Starting from the existing graph makes that class
of mistake impossible: a term already present keeps its identifier and its
definition, and only genuinely new terms are minted.

What changes on a run:
  - terms in the schema but not the vocabulary are added under their field
  - terms in the vocabulary but no longer in the schema are reported, not
    deleted, because something may already cite them
  - the field's skos:narrower list is rebuilt to match
  - dct:modified, owl:versionInfo and owl:versionIRI are updated

Deliberately not part of the site build, matching `hero-trace`: CI has no
Python, and this is a versioned artifact that should change when a person
decides it changes, not silently on a deploy. Run `make vocab`, then commit.
"""

import argparse
import datetime as dt
import pathlib
import re
import sys

try:
    import rdflib
    from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS
except ImportError:  # pragma: no cover
    sys.exit("rdflib is required: pip install rdflib pyyaml")

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://shedding-hub.github.io/vocab"
SCHEME = rdflib.URIRef(BASE)
SHV = rdflib.Namespace(BASE + "#")

ENUM_FIELDS = ("biomarker", "specimen", "unit", "reference_event")


def local_name(term: str) -> str:
    """
    Mint a local name for a term new to the vocabulary.

    Hyphens are kept: Turtle allows them in a prefixed name, the published file
    already relies on that for `shv:SARS-CoV-2`, and collapsing them would make
    two different identifiers for one concept. Everything else a local name
    cannot carry -- spaces, slashes -- becomes an underscore, which is the style
    already used for `gc_wet_gram` and `symptom_onset`.
    """
    s = re.sub(r"[^\w-]+", "_", term.strip())
    return re.sub(r"_+", "_", s).strip("_")


def enum_values(node, defs) -> list:
    """Collect an enum, following $ref and anyOf/oneOf, preserving order."""
    if "enum" in node:
        return list(node["enum"])
    for key in ("anyOf", "oneOf"):
        if key in node:
            out = []
            for sub in node[key]:
                for v in enum_values(sub, defs):
                    if v not in out:
                        out.append(v)
            return out
    if "$ref" in node:
        return enum_values(defs[node["$ref"].split("/")[-1]], defs)
    if node.get("type") == "array" and "items" in node:
        return enum_values(node["items"], defs)
    return []


def match_key(text: str) -> str:
    """Loose key for deciding whether a schema term is already a concept."""
    return re.sub(r"[^a-z0-9]+", "", str(text).lower())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--schema",
        type=pathlib.Path,
        default=ROOT / "tmp" / "shedding-hub-main" / "data" / ".schema.yaml",
        help="data/.schema.yaml from the shedding-hub archive (see `make ^_datasets-yaml`).",
    )
    parser.add_argument("--ttl", type=pathlib.Path, default=ROOT / "vocab" / "shedding-hub.ttl")
    parser.add_argument("--version", default=None, help="New owl:versionInfo, e.g. 0.2.0")
    parser.add_argument("--check", action="store_true", help="Report drift; write nothing.")
    args = parser.parse_args()

    if not args.schema.is_file():
        sys.exit(f"schema not found at {args.schema}\nRun `make ^_datasets-yaml` first.")

    schema = yaml.safe_load(args.schema.read_text(encoding="utf-8"))
    defs = schema["$defs"]
    spec = defs["analyte_specification"]["properties"]
    terms = {f: enum_values(spec[f], defs) for f in ENUM_FIELDS}

    graph = rdflib.Graph()
    graph.parse(str(args.ttl), format="turtle")

    existing = {}
    for subject in set(graph.subjects(RDF.type, SKOS.Concept)):
        name = str(subject).split("#")[-1]
        existing[match_key(name)] = subject
        for label in graph.objects(subject, SKOS.prefLabel):
            existing.setdefault(match_key(label), subject)

    added, stale = [], []
    for field, values in terms.items():
        parent = SHV[field]
        children = []
        for value in values:
            subject = existing.get(match_key(value))
            if subject is None:
                subject = SHV[local_name(value)]
                graph.add((subject, RDF.type, SKOS.Concept))
                graph.add((subject, SKOS.prefLabel, rdflib.Literal(value, lang="en")))
                graph.add((subject, RDFS.label, rdflib.Literal(value, lang="en")))
                graph.add((subject, SKOS.inScheme, SCHEME))
                graph.add((subject, DCTERMS.created,
                           rdflib.Literal(dt.date.today().isoformat(),
                                          datatype=rdflib.XSD.date)))
                added.append((field, value, str(subject).split("#")[-1]))
                existing[match_key(value)] = subject
            graph.add((subject, SKOS.broader, parent))
            children.append(subject)

        # Terms the vocabulary lists that the schema no longer has. Reported,
        # never deleted: the namespace resolves, so something may cite them.
        for old in list(graph.objects(parent, SKOS.narrower)):
            if old not in children:
                stale.append((field, str(old).split("#")[-1]))

        graph.remove((parent, SKOS.narrower, None))
        for child in children:
            graph.add((parent, SKOS.narrower, child))

    if args.check:
        for field, value, name in added:
            print(f"MISSING  {field}: {value!r} (would mint shv:{name})")
        for field, name in stale:
            print(f"STALE    {field}: shv:{name} is no longer in the schema")
        if not added and not stale:
            print("vocabulary is current with the schema.")
            return 0
        print(f"\n{len(added)} to add, {len(stale)} stale. Run `make vocab`.")
        return 1

    version = args.version
    if version is None:
        current = graph.value(SCHEME, OWL.versionInfo)
        parts = str(current or "0.1.0").split(".")
        parts[1] = str(int(parts[1]) + 1)
        parts[2] = "0"
        version = ".".join(parts)

    graph.remove((SCHEME, OWL.versionInfo, None))
    graph.remove((SCHEME, OWL.versionIRI, None))
    graph.remove((SCHEME, DCTERMS.modified, None))
    graph.add((SCHEME, OWL.versionInfo, rdflib.Literal(version)))
    graph.add((SCHEME, OWL.versionIRI, rdflib.URIRef(f"{BASE}/{version}")))
    graph.add((SCHEME, DCTERMS.modified,
               rdflib.Literal(dt.date.today().isoformat(), datatype=rdflib.XSD.date)))

    graph.bind("shv", SHV)
    graph.bind("skos", SKOS)
    graph.bind("dct", DCTERMS)
    graph.bind("owl", OWL)
    args.ttl.write_text(graph.serialize(format="turtle"), encoding="utf-8")

    print(f"wrote {args.ttl} — version {version}, {len(graph)} triples")
    print(f"  added {len(added)} concept(s):")
    for field, value, name in added:
        print(f"    {field:16s} {value!r} -> shv:{name}")
    if stale:
        print(f"  {len(stale)} stale term(s) kept, not deleted:")
        for field, name in stale:
            print(f"    {field:16s} shv:{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
