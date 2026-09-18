"""
Build _data/citations.yaml so each dataset card can offer a real citation.

The datasets carry a title and a DOI and nothing else -- no authors, journal,
year or volume anywhere in the schema -- so a citation cannot be assembled from
the repository alone. This resolves each DOI against doi.org's content
negotiation, which returns both a formatted string and the structured CSL JSON
behind it, and caches the result.

Cached, not fetched at render time, for three reasons: the site build has no
network budget for 144 sequential resolutions, publishers rate-limit and drop
connections under exactly that pattern, and a citation that silently disappears
when a publisher has a bad minute is worse than one that is a week stale.

Deliberately outside the site build, matching `hero-trace` and `vocab`: CI has
no Python, and the output is committed. Run `make citations` when datasets are
added. Existing entries are reused unless --refresh is given, so a normal run
costs one request per *new* dataset rather than 144.

What it stores per study:
  apa      a formatted string, for display and for the copy button
  bibtex   for reference managers
  year, journal, authors_short   for a compact inline credit line

Failures are recorded rather than skipped. A dataset whose DOI does not resolve
keeps an `error` field, so the template can fall back to the DOI link and the
gap is visible in the data file instead of silently absent from the page.
"""

import argparse
import pathlib
import sys
import time
import urllib.error
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_data" / "citations.yaml"

# Publishers drop connections under a long sequential crawl; this is the same
# failure the data repository's own DOI check retries around.
RETRIES = 3
BACKOFF = 2.0
TIMEOUT = 30
# Courtesy gap between resolutions. doi.org is fine with this rate; the
# publishers it redirects to are the ones that complain.
DELAY = 0.5


def negotiate(doi: str, accept: str) -> str:
    """One content-negotiated GET against doi.org, retrying transport failures."""
    request = urllib.request.Request(
        f"https://doi.org/{doi}",
        headers={
            "Accept": accept,
            # doi.org asks for a contactable agent on automated use.
            "User-Agent": "shedding-hub-site/1.0 (mailto:sheddinghub@emory.edu)",
        },
    )
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                return response.read().decode("utf-8", errors="replace").strip()
        except urllib.error.HTTPError:
            # A real status is an answer: the DOI does not resolve, or the
            # publisher will not serve this format. Retrying will not change it.
            raise
        except Exception:
            if attempt == RETRIES - 1:
                raise
            time.sleep(BACKOFF * (attempt + 1))
    return ""


def short_authors(csl: dict) -> str:
    """`Surname et al.` / `A and B` / `A` -- a credit line, not a full list."""
    authors = csl.get("author") or []
    names = [a.get("family") or a.get("literal") or "" for a in authors]
    names = [n for n in names if n]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return f"{names[0]} et al."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--datasets",
        type=pathlib.Path,
        default=ROOT / "tmp" / "shedding-hub-main" / "data",
        help="data/ from the shedding-hub archive (see `make ^_datasets-yaml`).",
    )
    parser.add_argument(
        "--hub-doi",
        default="10.5281/zenodo.15052772",
        help=(
            "Zenodo CONCEPT doi for the Shedding Hub itself, stored under the reserved "
            "key `_shedding_hub`. The concept doi deliberately, not a version doi: it "
            "resolves to whatever the latest release is, so a card citing 146 datasets "
            "does not point readers at the March 2025 snapshot. 10.5281/zenodo.15052773 "
            "is the v1.0.0 version doi and would do exactly that."
        ),
    )
    parser.add_argument("--refresh", action="store_true", help="Re-fetch every entry.")
    parser.add_argument("--limit", type=int, default=0, help="Stop after N fetches.")
    args = parser.parse_args()

    if not args.datasets.is_dir():
        sys.exit(f"datasets not found at {args.datasets}\nRun `make ^_datasets-yaml` first.")

    import json

    cached = {}
    if OUT.is_file() and not args.refresh:
        cached = yaml.safe_load(OUT.read_text(encoding="utf-8")) or {}

    out, fetched, reused, failed = {}, 0, 0, 0
    paths = sorted(args.datasets.glob("*/*.yaml"))
    for path in paths:
        study = path.parent.name
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        doi = (data.get("doi") or "").strip()

        if study in cached and not cached[study].get("error") and not args.refresh:
            out[study] = cached[study]
            reused += 1
            continue

        if not doi:
            # Two datasets carry a url instead. Nothing to negotiate against.
            out[study] = {"url": data.get("url", ""), "error": "no doi"}
            failed += 1
            continue

        if args.limit and fetched >= args.limit:
            out[study] = cached.get(study, {"doi": doi, "error": "not fetched"})
            continue

        def attempt(accept, label):
            """One format, failing alone. Registrars differ in what they serve:
            JaLC refuses BibTeX with a 406 and redirects the formatted string,
            while serving CSL JSON perfectly well. Treating one refusal as total
            loses a citation that was entirely obtainable."""
            try:
                value = negotiate(doi, accept)
                time.sleep(DELAY)
                return value
            except Exception as error:  # noqa: BLE001
                print(f"  {study}: {label} unavailable ({error})", file=sys.stderr)
                return ""

        try:
            apa = attempt("text/x-bibliography; style=apa", "apa")
            bibtex = attempt("application/x-bibtex", "bibtex")
            raw = attempt("application/vnd.citationstyles.csl+json", "csl")
            csl = json.loads(raw) if raw else {}
            if not csl and not apa:
                raise RuntimeError("no format served")
            issued = (csl.get("issued") or {}).get("date-parts") or [[None]]
            if not apa and csl:
                # Reconstructed, not fetched. Enough to credit the study
                # properly; the DOI on the card remains authoritative.
                who = short_authors(csl)
                year = issued[0][0] or "n.d."
                title = csl.get("title") or ""
                journal = csl.get("container-title") or ""
                apa = f"{who} ({year}). {title}. {journal}. https://doi.org/{doi}".replace(" . ", " ")
            out[study] = {
                "doi": doi,
                "apa": apa,
                "bibtex": bibtex,
                "year": issued[0][0],
                "journal": csl.get("container-title") or "",
                "authors_short": short_authors(csl),
            }
            fetched += 1
            print(f"  {study}: {out[study]['authors_short']} ({out[study]['year']})")
        except Exception as error:  # noqa: BLE001
            out[study] = {"doi": doi, "error": f"{type(error).__name__}: {error}"}
            failed += 1
            print(f"  {study}: FAILED — {error}", file=sys.stderr)

    # The resource's own citation, fetched once and reused like any other.
    if args.hub_doi and (args.refresh or not cached.get("_shedding_hub", {}).get("apa")):
        try:
            doi = args.hub_doi
            hub_apa = negotiate(doi, "text/x-bibliography; style=apa")
            time.sleep(DELAY)
            hub_bib = negotiate(doi, "application/x-bibtex")
            out["_shedding_hub"] = {"doi": doi, "apa": hub_apa, "bibtex": hub_bib}
            print(f"  _shedding_hub: {doi}")
        except Exception as error:  # noqa: BLE001
            out["_shedding_hub"] = {"doi": args.hub_doi, "error": str(error)}
            print(f"  _shedding_hub: FAILED - {error}", file=sys.stderr)
    elif cached.get("_shedding_hub"):
        out["_shedding_hub"] = cached["_shedding_hub"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        "# Generated by tools/fetch_citations.py from each dataset's DOI.\n"
        "# Run `make citations` after adding datasets. Do not edit by hand.\n"
        + yaml.safe_dump(out, allow_unicode=True, sort_keys=True, width=100),
        encoding="utf-8",
    )
    print(f"\nwrote {OUT}: {len(out)} entries — {fetched} fetched, {reused} reused, {failed} failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
