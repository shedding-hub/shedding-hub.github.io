---
layout: default
title: Shedding Hub
---

{%- comment -%}
  Catalog figures, computed from the dataset collection at build time so every
  number on this page reflects whatever was last pushed to the data repository.
{%- endcomment -%}
{% assign num_measurements = 0 %}
{% assign num_participants = 0 %}
{% for dataset in site.datasets %}
  {% assign temp = dataset.participants | size %}
  {% assign num_participants = num_participants | plus: temp %}
  {% for participant in dataset.participants %}
    {% assign temp = participant.measurements | size %}
    {% assign num_measurements = num_measurements | plus: temp %}
  {% endfor %}
{% endfor %}
{% assign num_studies = site.datasets | size %}
{% assign num_ai = num_studies | minus: site.manual_curated_count %}
{% capture raw_biomarkers %}{% for dataset in site.datasets %}{% for analyte in dataset.analytes %}{{ analyte[1].biomarker }},{% endfor %}{% endfor %}{% endcapture %}
{% assign biomarkers = raw_biomarkers | split: ',' | uniq | sort %}
{% assign num_biomarkers = biomarkers | size %}
{% capture raw_specimens %}{% for dataset in site.datasets %}{% for analyte in dataset.analytes %}{% if analyte[1].specimen.first %}{% for spec in analyte[1].specimen %}{{ spec }},{% endfor %}{% else %}{{ analyte[1].specimen }},{% endif %}{% endfor %}{% endfor %}{% endcapture %}
{% assign specimens = raw_specimens | split: ',' | uniq %}
{% assign num_specimens = specimens | size %}
{%- comment -%}
  Fitted shedding curves, counted from the figure index the data repository builds.
  Guarded: a DATA_REF predating the figures leaves site.data.figures absent, and the
  card falls back to naming the models without a count rather than printing zero.
{%- endcomment -%}
{% assign num_fits = 0 %}
{% assign num_fitted_analytes = 0 %}
{% if site.data.figures %}
  {%- comment -%}
    where_exp does the per-figure filtering inside Ruby. Counting the innermost
    level with a third nested Liquid for-loop segfaulted the renderer here.
  {%- endcomment -%}
  {% for entry in site.data.figures %}
    {% for analyte in entry[1].analytes %}
      {% assign fitted = analyte.figures | where_exp: "figure", "figure.model != 'observations'" %}
      {% assign analyte_fits = fitted | size %}
      {% assign num_fits = num_fits | plus: analyte_fits %}
      {% if analyte_fits > 0 %}
        {% assign num_fitted_analytes = num_fitted_analytes | plus: 1 %}
      {% endif %}
    {% endfor %}
  {% endfor %}
{% endif %}

<section class="hero is-light hero-brand">
  {%- assign trace = site.data.hero_trace -%}
  <svg class="hero-plot" viewBox="0 0 {{ trace.width }} {{ trace.height }}"
       preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">
    {%- for line in trace.traces %}
    <polyline class="hero-trace" points="{{ line.points }}" style="--trace-index: {{ forloop.index }}" />
    {%- endfor %}
    {%- for point in trace.dots %}
    <circle class="hero-dot" cx="{{ point.x }}" cy="{{ point.y }}" r="4" />
    {%- endfor %}
    {%- for point in trace.censored %}
    <circle class="hero-censored" cx="{{ point.x }}" cy="{{ point.y }}" r="5" />
    {%- endfor %}
    <line class="hero-loq" x1="0" y1="{{ trace.loq_y }}" x2="{{ trace.width }}" y2="{{ trace.loq_y }}" />
  </svg>

  <div class="hero-body">
    <div class="container is-max-desktop has-text-centered">
      <h1 class="hero-logo">
        <span class="hero-logo-lockup" aria-hidden="true"></span>
        <span class="is-sr-only">Shedding Hub</span>
      </h1>
      <p class="subtitle is-size-4 hero-lede">
        Every published measurement of how much pathogen a person sheds, and when &mdash;
        standardized, versioned, and ready to model.
      </p>
      <div class="hero-actions">
        <a href="/datasets.html" class="button is-primary is-medium">
          <span class="icon"><i class="fa-solid fa-database"></i></span>
          <span>Browse datasets</span>
        </a>
        <button type="button" class="button is-medium copy-chip"
                data-copy="pip install shedding-hub" aria-label="Copy install command">
          <span class="is-data">pip install shedding-hub</span>
          <span class="icon copy-chip-idle"><i class="fa-regular fa-copy"></i></span>
          <span class="icon copy-chip-done"><i class="fa-solid fa-check"></i></span>
        </button>
      </div>
    </div>
  </div>
</section>

<p class="hero-caption">
  Above: SARS-CoV-2 stool shedding for eight patients from
  <a href="/datasets/woelfel2020virological.html"><code>woelfel2020virological</code></a>.
  Every vertex is a measurement; points on the dashed line fell below the
  limit of quantification.
</p>

<!-- What's New -->
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">Recently</span>
    <h2 class="title is-3 mb-5">What&rsquo;s new</h2>
    <div class="columns">
      <div class="column">
        <a class="news-card" href="/curation.html">
          <p class="news-figure is-data">{{ num_ai }}</p>
          <h3 class="title is-5">studies curated by AI</h3>
          <p>
            A multi-agent pipeline now finds, extracts, and cross-checks studies, and a
            human curator reviews every one before it lands.
          </p>
          <span class="news-link">How the pipeline works <i class="fa-solid fa-arrow-right"></i></span>
        </a>
      </div>
      <div class="column">
        <a class="news-card" href="/fits.html">
          {% if num_fits > 0 %}
          <p class="news-figure is-data">{{ num_fits }}</p>
          <h3 class="title is-5">fitted shedding curves</h3>
          <p>
            Every analyte with enough data is fitted three ways &mdash; exponential,
            gamma, and gamma-shifted &mdash; covering {{ num_fitted_analytes }} analytes.
            Each fit is plotted on its dataset page.
          </p>
          {% else %}
          <p class="news-figure is-data">3</p>
          <h3 class="title is-5">shedding curve models</h3>
          <p>
            Analytes with enough data are fitted three ways &mdash; exponential, gamma,
            and gamma-shifted &mdash; and each fit is plotted on its dataset page.
          </p>
          {% endif %}
          <span class="news-link">See the fits <i class="fa-solid fa-arrow-right"></i></span>
        </a>
      </div>
      <div class="column">
        <a class="news-card" href="/package.html">
          <p class="news-figure is-data">pip</p>
          <h3 class="title is-5">install shedding-hub</h3>
          <p>
            Load any study, fit rise-and-decay curves that handle non-detects properly,
            and simulate cohorts. Published on PyPI with full documentation.
          </p>
          <span class="news-link">Read the docs <i class="fa-solid fa-arrow-right"></i></span>
        </a>
      </div>
    </div>
  </div>
</section>

<hr class="lod-rule">

<!-- At a Glance -->
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">At a glance</span>
    <h2 class="title is-3 mb-5">What&rsquo;s in the repository</h2>
    <div class="stat-grid">
      <div class="stat">
        <p class="stat-value is-data separate-thousands">{{ num_measurements }}</p>
        <p class="stat-label">Measurements</p>
      </div>
      <div class="stat">
        <p class="stat-value is-data separate-thousands">{{ num_participants }}</p>
        <p class="stat-label">Participants</p>
      </div>
      <div class="stat">
        <p class="stat-value is-data separate-thousands">{{ num_studies }}</p>
        <p class="stat-label">Studies</p>
      </div>
      <div class="stat">
        <p class="stat-value is-data">{{ num_biomarkers }}</p>
        <p class="stat-label">Pathogens</p>
      </div>
      <div class="stat">
        <p class="stat-value is-data">{{ num_specimens }}</p>
        <p class="stat-label">Specimen types</p>
      </div>
    </div>
    <div class="biomarker-tags">
      {%- comment -%}
        Carries the pathogen through as a query parameter so the datasets page opens
        already filtered to it, rather than dropping the reader into all 84 studies.
      {%- endcomment -%}
      {% for biomarker in biomarkers %}<a class="tag pathogen-tag pathogen-{{ biomarker | slugify }}" href="/datasets.html?biomarker={{ biomarker | uri_escape }}" title="Show {{ biomarker }} datasets">{{ biomarker }}</a>{% endfor %}
    </div>
  </div>
</section>

<!-- Interactive Data Explorer -->
<section class="section has-background-light">
  <div class="container is-fluid">
    <div class="container is-max-desktop">
      <span class="eyebrow">Explore</span>
      <h2 class="title is-3 mb-4">Interactive data explorer</h2>
      <div class="content mb-5">
        <p>
          Plot time courses, compare studies, and inspect shedding dynamics without writing code.
        </p>
      </div>
    </div>
    <div class="dashboard-container" id="dashboard-container">
      <button type="button" class="dashboard-launch" id="dashboard-launch">
        <span class="icon is-large"><i class="fa-solid fa-circle-play fa-2x"></i></span>
        <span class="dashboard-launch-label">Load the dashboard</span>
        <span class="dashboard-launch-note">Opens in place</span>
      </button>
    </div>
  </div>
</section>

<hr class="lod-rule">

<!-- Why -->
<section class="section">
  <div class="container is-max-desktop">
    <div class="columns is-variable is-8">
      <div class="column is-6">
        <span class="eyebrow">Why this exists</span>
        <h2 class="title is-4">Shedding data is scattered by default</h2>
        <div class="content">
          <p>
            How much pathogen a person sheds, and for how long, drives biomedical research,
            transmission models, wastewater surveillance, and public health policy. Yet the
            measurements sit in supplementary spreadsheets, in figures and tables with various
            formats, and in lab methods and units that differ from one paper to the next.
          </p>
          <p>
            Shedding Hub puts them in one schema, under version control, with the source
            paper attached to every study. Nothing here is a number you have to take on faith.
          </p>
        </div>
      </div>
      <div class="column is-6">
        <span class="eyebrow">How it gets curated</span>
        <h2 class="title is-4">Curated by people, scaled by machines</h2>
        <div class="content">
          <p>
            From May 2024, human biocurators extracted every study by hand, building the
            {{ site.manual_curated_count }}-study benchmark the rest of the pipeline is
            measured against.
          </p>
          <p>
            Since June 2025, large language models do the first pass on discovery and
            extraction, and a second model checks the first. Expert review still gates
            what gets published, so scale never comes at the cost of the benchmark.
          </p>
          <p><a href="/curation.html">Read how the curation pipeline works &rarr;</a></p>
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="lod-rule">

<!-- Get Started -->
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">Get started</span>
    <h2 class="title is-3 mb-5">From install to first plot in a few lines</h2>
    <div class="video-container">
      <video muted loop controls playsinline preload="metadata" poster="/assets/logo/og-image.png"
             style="width: 100%; max-width: 1280px; display: block; margin: 0 auto; border-radius: 6px; box-shadow: 0 4px 12px var(--shadow);">
        <source src="/assets/videos/SheddingHubQuickStart.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>
    <div class="has-text-centered mt-5">
      <a href="https://shedding-hub.readthedocs.io/" class="button is-primary is-medium" target="_blank" rel="noopener">
        <span class="icon"><i class="fa-solid fa-book"></i></span>
        <span>Read the documentation</span>
      </a>
    </div>
  </div>
</section>

<hr class="lod-rule">

<!-- Using Shedding Hub -->
<section class="section has-background-light">
  <div class="container is-max-desktop">
    <span class="eyebrow">Community</span>
    <h2 class="title is-3 mb-5">Using Shedding Hub?</h2>
    <div class="columns">
      <div class="column is-6">
        <div class="box" style="height: 100%;">
          <h3 class="title is-5">Tell us what you built</h3>
          <p class="mb-4">
            We want to know which studies you pulled, what you modeled, and what the data
            could not answer. It shapes what gets curated next, and we would like to credit
            the work on this site.
          </p>
          <a class="button is-primary"
             href="mailto:sheddinghub@emory.edu?subject=How%20I%20use%20Shedding%20Hub&body=Institution%3A%0AWhat%20I%27m%20working%20on%3A%0ADatasets%20I%20used%3A%0AWhat%20I%20wish%20existed%3A%0A">
            <span class="icon"><i class="fa-solid fa-comment-dots"></i></span>
            <span>Share your use case</span>
          </a>
        </div>
      </div>
      <div class="column is-6">
        <div class="box" style="height: 100%;">
          <h3 class="title is-5">Get release notes</h3>
          <p class="mb-4">
            An occasional email when a batch of datasets lands, the schema changes, or the
            package ships something that affects your analysis. No other mail.
          </p>
          <a class="button"
             href="mailto:sheddinghub@emory.edu?subject=Subscribe%20to%20Shedding%20Hub%20updates&body=Please%20add%20me%20to%20the%20Shedding%20Hub%20update%20list.%0A%0AName%3A%0AInstitution%3A%0A">
            <span class="icon"><i class="fa-solid fa-envelope"></i></span>
            <span>Subscribe to updates</span>
          </a>
        </div>
      </div>
    </div>

    <div class="box cite-box">
      <span class="eyebrow">How to cite</span>
      <p class="mb-3">Citing Shedding Hub in a paper? Use this, and tell us so we can link the work here.</p>
      {%- comment -%}
        The concept DOI, not a version DOI: it always resolves to the current
        release, so this citation cannot go stale the way the Terms page's did —
        that one still pointed at v1.0.0 from 2025.
      {%- endcomment -%}
      <div class="cite-row">
        <code class="cite-text" id="cite-text">Wang, Y., Hoffmann, T., Xiao, W., Hu, Y., Chen, Z., Zhang, H., Shen, L., &amp; Zhai, S. (2026). Shedding Hub [Software]. Zenodo. https://doi.org/10.5281/zenodo.15052772</code>
        <button type="button" class="button is-small copy-chip" data-copy="Wang, Y., Hoffmann, T., Xiao, W., Hu, Y., Chen, Z., Zhang, H., Shen, L., &amp; Zhai, S. (2026). Shedding Hub [Software]. Zenodo. https://doi.org/10.5281/zenodo.15052772">
          <span class="icon copy-chip-idle"><i class="fa-regular fa-copy"></i></span>
          <span class="icon copy-chip-done"><i class="fa-solid fa-check"></i></span>
          <span class="copy-chip-idle">Copy</span>
          <span class="copy-chip-done">Copied</span>
        </button>
      </div>
      <p class="is-size-7 mt-3 has-text-grey">
        That DOI covers all versions and resolves to the current release. To cite the exact
        version an analysis used, take its version DOI from the
        <a href="https://doi.org/10.5281/zenodo.15052772" target="_blank" rel="noopener">Zenodo
        record</a>. Individual datasets should also cite their source study, linked from every
        dataset page.
      </p>
    </div>
  </div>
</section>

<hr class="lod-rule">

<!-- Contribute -->
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">Contribute</span>
    <h2 class="title is-3 mb-4">Have shedding data?</h2>
    <div class="content">
      <p>
        We take data from a single participant or an entire cohort, published or not. Our
        curators handle the schema work and the quality review, and contributors are credited
        on the dataset. If a study of yours is already in here and the extraction looks wrong,
        we especially want to hear that.
      </p>
    </div>
    <div class="buttons">
      <a href="mailto:sheddinghub@emory.edu?subject=Contributing%20a%20dataset&body=What%20the%20data%20measures%20%28pathogen%2C%20specimen%29%3A%0AStudy%20or%20cohort%20it%20comes%20from%3A%0APublished%3F%20DOI%20or%20PMID%2C%20or%20say%20unpublished%3A%0ARoughly%20how%20many%20participants%20and%20measurements%3A%0AWhat%20form%20it%20is%20in%20%28spreadsheet%2C%20database%20export%2C%20figures%20only%29%3A%0AAnything%20unusual%20about%20how%20it%20was%20collected%20or%20reported%3A%0A%0AYour%20name%20and%20institution%3A%0A" class="button is-primary is-medium">
        <span class="icon"><i class="fa-solid fa-envelope"></i></span>
        <span>Contribute a dataset</span>
      </a>
      <a href="https://github.com/shedding-hub/shedding-hub/issues" class="button is-medium" target="_blank" rel="noopener">
        <span class="icon"><i class="fa-solid fa-flag"></i></span>
        <span>Report a data issue</span>
      </a>
    </div>
  </div>
</section>

<hr class="lod-rule">

<!-- Leadership -->
<section class="section">
  <div class="container is-max-desktop">
    <div class="carousel-head">
      <div>
        <span class="eyebrow">People</span>
        <h2 class="title is-3">Leadership</h2>
      </div>
      <div class="carousel-controls">
        <button type="button" class="carousel-button" id="people-prev" aria-label="Show previous people">
          <span class="icon"><i class="fa-solid fa-arrow-left"></i></span>
        </button>
        <button type="button" class="carousel-button" id="people-next" aria-label="Show next people">
          <span class="icon"><i class="fa-solid fa-arrow-right"></i></span>
        </button>
      </div>
    </div>

    <ul class="people-track" id="people-track" tabindex="0" aria-label="Project leadership and scientific advisors">
      {%- comment -%}
        Built like the advisor cards below: the same markup, and an outward link
        to the person's own profile rather than back into this site. Falls back
        to the personal site for anyone without an institutional page.
      {%- endcomment -%}
      {% assign founder_keys = "andrew,till" | split: "," %}
      {% for key in founder_keys %}
      {% assign person = site.data.team[key] %}
      {% assign founder_url = person.profile | default: person.website %}
      <li class="person-card">
        <a href="{{ founder_url }}" target="_blank" rel="noopener">
          <img class="person-photo" src="/assets/team/{{ key }}.jpg" alt="" loading="lazy">
          <p class="person-name">Dr. {{ person.first }} {{ person.last }}</p>
          <p class="person-role">Co-founder</p>
          <p class="person-affil">{{ person.institution }}</p>
        </a>
      </li>
      {% endfor %}
      {% for advisor in site.data.advisors %}
      <li class="person-card">
        <a href="{{ advisor.url }}" target="_blank" rel="noopener">
          <img class="person-photo" src="/assets/team/{{ advisor.key }}.jpg" alt="" loading="lazy">
          <p class="person-name">{{ advisor.name }}</p>
          <p class="person-role">Scientific advisor</p>
          <p class="person-affil">{{ advisor.institution }}</p>
        </a>
      </li>
      {% endfor %}
    </ul>

    <p class="mt-5">
      <a href="/team.html">Meet the full team, including our students and curators &rarr;</a>
    </p>
  </div>
</section>

<!-- Funding -->
<section class="section has-background-light">
  <div class="container is-max-desktop has-text-centered">
    <span class="eyebrow">Funding</span>
    <div class="content">
      <p class="is-size-7 has-text-grey">
        The Shedding Hub was made possible by the Insight Net cooperative agreement
        CDC-RFA-FT-23-0069 from the CDC&rsquo;s Center for Forecasting and Outbreak Analytics.
        Its contents are solely the responsibility of the authors and do not necessarily
        represent the official views of the Centers for Disease Control and Prevention.
        Support for the Shedding Hub is provided by the Emory Center for Infectious Disease
        Modeling and Analytics &amp; Training Hub (CIDMATH).
      </p>
    </div>
    <a href="https://cidmath.org/" target="_blank" rel="noopener noreferrer">
      <img src="/assets/logo/logo_emory_cidmath_dark_blue_2_no-tagline.svg"
           alt="CIDMATH - Center for Infectious Disease Modeling and Analysis"
           style="max-width: 320px; width: 100%; height: auto;">
    </a>
  </div>
</section>

<style>
/* ---------------------------------------------------------------------------
   Hero: the lockup sits on clean paper, and real shedding trajectories from the
   repository emerge underneath it. The plot's limit-of-quantification line lands
   at the hero's bottom edge, where it becomes the first section divider.
   --------------------------------------------------------------------------- */
.hero-brand {
  position: relative;
  overflow: hidden;
}

.hero-brand .hero-body {
  position: relative;
  z-index: 1;
  padding-top: 4.5rem;
  /* Leaves the lower band of the plot, and the quantification line at its floor,
     visible below the buttons. */
  padding-bottom: 8rem;
}

.hero-plot {
  position: absolute;
  inset: auto 0 0 0;
  width: 100%;
  height: 78%;
  z-index: 0;
  /* Clear a hole through the middle where the lockup, lede and buttons sit, so
     the plot never sits behind body text. It reappears toward the edges and the
     bottom, where the quantification line meets the first section divider. */
  -webkit-mask-image: radial-gradient(ellipse 62% 58% at 50% 34%,
      transparent 0%, transparent 42%, rgba(0, 0, 0, 0.55) 74%, #000 100%);
  mask-image: radial-gradient(ellipse 62% 58% at 50% 34%,
      transparent 0%, transparent 42%, rgba(0, 0, 0, 0.55) 74%, #000 100%);
}

/* Straight segments between observations, never a spline: the plot must not
   suggest peaks that were never measured. */
.hero-trace {
  fill: none;
  stroke: var(--primary-color);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  opacity: 0.28;
  stroke-dasharray: 4000;
  stroke-dashoffset: 4000;
  animation: hero-trace-in 2s cubic-bezier(0.22, 0.8, 0.3, 1) forwards;
  animation-delay: calc(var(--trace-index) * 0.12s + 0.3s);
}

[data-theme="dark"] .hero-trace {
  opacity: 0.38;
}

@keyframes hero-trace-in {
  to { stroke-dashoffset: 0; }
}

.hero-dot,
.hero-censored {
  opacity: 0;
  animation: hero-point-in 0.5s ease forwards;
  animation-delay: 2.1s;
}

.hero-dot {
  fill: var(--primary-color);
}

/* Censored results are drawn hollow: the measurement happened, the quantity did
   not clear the limit. */
.hero-censored {
  fill: var(--bg-hero);
  stroke: var(--primary-color);
  stroke-width: 2;
}

@keyframes hero-point-in {
  to { opacity: 0.55; }
}

[data-theme="dark"] .hero-dot,
[data-theme="dark"] .hero-censored {
  animation-name: hero-point-in-dark;
}

@keyframes hero-point-in-dark {
  to { opacity: 0.7; }
}

.hero-loq {
  stroke: var(--text-light);
  stroke-width: 1.5;
  stroke-dasharray: 7 7;
  opacity: 0.7;
}

.hero-logo {
  margin: 0 0 1.75rem;
}

/* The lockup is the heading: the h1 keeps its text for assistive tech and search,
   while the visible mark + wordmark come from a single alpha mask tinted with
   --logo-ink, so one file serves both themes. */
.hero-logo-lockup {
  display: block;
  width: min(34rem, 84vw);
  aspect-ratio: 1200 / 616;
  margin: 0 auto;
  animation: hero-logo-trace 1.2s cubic-bezier(0.22, 0.8, 0.3, 1) both;
}

@supports ((-webkit-mask-image: url("")) or (mask-image: url(""))) {
  .hero-logo-lockup {
    background-color: var(--logo-ink);
    -webkit-mask: url("/assets/logo/shedding-hub-lockup-mask.png") center / contain no-repeat;
    mask: url("/assets/logo/shedding-hub-lockup-mask.png") center / contain no-repeat;
  }
}

@keyframes hero-logo-trace {
  from {
    clip-path: inset(0 100% 0 0);
    opacity: 0.35;
  }
  to {
    clip-path: inset(0 0 0 0);
    opacity: 1;
  }
}

.hero-lede {
  max-width: 44rem;
  margin-left: auto;
  margin-right: auto;
  color: var(--text-secondary);
}

.hero-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 2rem;
}

/* Sits under the hero, below the quantification line, where a figure caption
   belongs relative to its plot. */
.hero-caption {
  max-width: 44rem;
  margin: 0 auto;
  padding: 1.25rem 1.5rem 0;
  text-align: center;
  font-size: 0.8rem;
  line-height: 1.6;
  color: var(--text-secondary);
}

.hero-caption code {
  background: none;
  padding: 0;
  color: inherit;
  font-size: 0.95em;
}

/* Copy-to-clipboard chip, used for the install line and the citation. */
.copy-chip {
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  cursor: pointer;
}

.copy-chip:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.copy-chip.is-copied {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

/* Both states ship in the markup and are swapped by class. Font Awesome's JS
   build rewrites every <i> into an <svg>, so anything that reaches for the icon
   element itself breaks; these wrapper spans are ours and stay put. */
.copy-chip .copy-chip-done {
  display: none;
}

.copy-chip.is-copied .copy-chip-idle {
  display: none;
}

.copy-chip.is-copied span.copy-chip-done {
  display: inline;
}

.copy-chip.is-copied .icon.copy-chip-done {
  display: inline-flex;
}

.copy-chip .icon {
  margin-left: 0.5rem;
}

.copy-chip .icon:first-child {
  margin-left: 0;
  margin-right: 0.35rem;
}

/* ---------------------------------------------------------------------------
   What's new
   --------------------------------------------------------------------------- */
.news-card {
  display: block;
  height: 100%;
  padding: 1.75rem;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-top: 3px solid var(--primary-color);
  border-radius: 4px;
  color: var(--text-primary);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.news-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 0.4rem 1.2rem var(--shadow);
  color: var(--text-primary);
}

.news-figure {
  font-size: 2.75rem;
  font-weight: 600;
  line-height: 1;
  /* Mono puts a full character width around the thousands comma; pulling the
     tracking in closes that gap without giving up the tabular alignment. */
  letter-spacing: -0.055em;
  color: var(--primary-color);
  margin-bottom: 0.35rem;
}

.news-card .title {
  margin-bottom: 0.75rem;
}

.news-card p:not(.news-figure) {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.news-link {
  display: inline-block;
  margin-top: 1rem;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--primary-color);
}

.news-card:hover .news-link i {
  transform: translateX(3px);
}

.news-link i {
  margin-left: 0.35rem;
  transition: transform 0.2s ease;
}

/* ---------------------------------------------------------------------------
   At a glance
   --------------------------------------------------------------------------- */
/* .stat-grid and its parts now live in the shared layout, since three pages use them. */

.biomarker-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
  margin-top: 1.5rem;
}

.biomarker-tags .tag {
  background-color: var(--bg-secondary);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  font-family: var(--font-mono);
  font-size: 0.72rem;
}

.biomarker-tags .tag:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

/* ---------------------------------------------------------------------------
   Dashboard: loaded on demand so a cold start on the free instance never blocks
   the page, and the iframe is not fetched for readers who never open it.
   --------------------------------------------------------------------------- */
.dashboard-container {
  position: relative;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  overflow: hidden;
}

.dashboard-launch {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  min-height: 13rem;
  padding: 2rem;
  background: none;
  border: 0;
  cursor: pointer;
  color: var(--text-secondary);
  font-family: inherit;
}

.dashboard-launch:hover {
  background-color: var(--bg-secondary);
  color: var(--primary-color);
}

.dashboard-launch-label {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1.15rem;
}

.dashboard-launch-note {
  font-size: 0.8rem;
  color: var(--text-light);
}

#dash-dashboard {
  width: 100%;
  height: 1000px;
  border: 0;
  background: var(--bg-card);
  display: block;
}

@media screen and (max-width: 1024px) {
  #dash-dashboard { height: 850px; }
}

@media screen and (max-width: 768px) {
  #dash-dashboard { height: 700px; }
}

/* ---------------------------------------------------------------------------
   Citation
   --------------------------------------------------------------------------- */
.cite-box {
  margin-top: 1.5rem;
}

.cite-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.cite-text {
  flex: 1 1 20rem;
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  padding: 0.6rem 0.8rem;
  border-radius: 4px;
  font-size: 0.82rem;
  word-break: break-word;
}

/* ---------------------------------------------------------------------------
   People carousel
   --------------------------------------------------------------------------- */
.carousel-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.carousel-head .title {
  margin-bottom: 0;
}

.carousel-controls {
  display: flex;
  gap: 0.5rem;
  flex: none;
}

.carousel-button {
  width: 2.5rem;
  height: 2.5rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--border-color);
  border-radius: 50%;
  background-color: var(--bg-card);
  color: var(--text-primary);
  cursor: pointer;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.carousel-button:hover:not(:disabled) {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.carousel-button:disabled {
  opacity: 0.35;
  cursor: default;
}

.people-track {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: calc((100% - 3rem) / 4);
  gap: 1rem;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
  list-style: none;
  margin: 0;
  padding: 0.25rem;
  scrollbar-width: none;
}

.people-track::-webkit-scrollbar {
  display: none;
}

.person-card {
  scroll-snap-align: start;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 4px;
  padding: 1.5rem 1rem;
  text-align: center;
  transition: border-color 0.2s ease;
}

.person-card:hover {
  border-color: var(--primary-color);
}

.person-card a {
  color: inherit;
  display: block;
}

.person-photo {
  width: 5.5rem;
  height: 5.5rem;
  border-radius: 50%;
  object-fit: cover;
  margin: 0 auto 1rem;
  display: block;
}

.person-name {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.95rem;
  line-height: 1.3;
}

.person-role {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--primary-color);
  margin-top: 0.35rem;
}

.person-affil {
  font-size: 0.78rem;
  color: var(--text-light);
  margin-top: 0.5rem;
  line-height: 1.4;
}

@media screen and (max-width: 1023px) {
  .people-track { grid-auto-columns: calc((100% - 1rem) / 2); }
}

@media screen and (max-width: 640px) {
  .people-track { grid-auto-columns: 78%; }

  .hero-brand .hero-body {
    padding-top: 3rem;
    padding-bottom: 5rem;
  }

  .hero-logo { margin-bottom: 1.25rem; }
}

@media (prefers-reduced-motion: reduce) {
  .hero-logo-lockup,
  .hero-trace,
  .hero-dot,
  .hero-censored {
    animation: none;
  }

  .hero-trace { stroke-dashoffset: 0; }

  .hero-dot,
  .hero-censored { opacity: 0.55; }

  .people-track { scroll-behavior: auto; }

  .news-card:hover { transform: none; }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function () {
  // Copy chips: install line and citation.
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      // Falls through to the legacy path when the async API rejects, not only
      // when it is missing: it also refuses on an unfocused document and under
      // some permissions policies.
      return navigator.clipboard.writeText(text).catch(function () {
        return legacyCopy(text);
      });
    }
    return legacyCopy(text);
  }

  function legacyCopy(text) {
    return new Promise(function (resolve, reject) {
      const field = document.createElement('textarea');
      field.value = text;
      field.setAttribute('readonly', '');
      field.style.position = 'fixed';
      field.style.top = '-1000px';
      document.body.appendChild(field);
      field.select();
      const ok = document.execCommand('copy');
      field.remove();
      ok ? resolve() : reject(new Error('copy command rejected'));
    });
  }

  document.querySelectorAll('.copy-chip').forEach(function (chip) {
    chip.addEventListener('click', function () {
      copyText(chip.dataset.copy).then(function () {
        chip.classList.add('is-copied');
        clearTimeout(chip.resetTimer);
        chip.resetTimer = setTimeout(function () {
          chip.classList.remove('is-copied');
        }, 1800);
      }).catch(function () {
        // Leave the chip untouched rather than claiming a copy that never happened.
        console.warn('Could not copy to the clipboard');
      });
    });
  });

  // Dashboard loads only when asked for, so a cold start never blocks the page.
  const launch = document.getElementById('dashboard-launch');
  if (launch) {
    launch.addEventListener('click', function () {
      const container = document.getElementById('dashboard-container');
      const frame = document.createElement('iframe');
      frame.id = 'dash-dashboard';
      frame.src = 'https://shedding-hub-dashboard-demo.onrender.com';
      frame.title = 'Shedding Hub interactive dashboard';
      container.replaceChildren(frame);
    });
  }

  // People carousel: one viewport of cards per press.
  const track = document.getElementById('people-track');
  const prev = document.getElementById('people-prev');
  const next = document.getElementById('people-next');

  if (track && prev && next) {
    const syncButtons = function () {
      const maxScroll = track.scrollWidth - track.clientWidth;
      prev.disabled = track.scrollLeft < 8;
      next.disabled = track.scrollLeft >= maxScroll - 8;
    };

    const page = function (direction) {
      const card = track.querySelector('.person-card');
      const step = card ? card.getBoundingClientRect().width + 16 : track.clientWidth;
      track.scrollBy({ left: direction * step, behavior: 'smooth' });
    };

    prev.addEventListener('click', function () { page(-1); });
    next.addEventListener('click', function () { page(1); });
    track.addEventListener('scroll', syncButtons, { passive: true });
    window.addEventListener('resize', syncButtons);
    syncButtons();
  }
});
</script>
