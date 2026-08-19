---
layout: default
title: Datasets - Shedding Hub
---
<section class="hero is-light">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <h1 class="title is-size-1 mb-4">Datasets</h1>
      <p class="subtitle is-size-4">
        Every curated study, with its participants, measurements, and fitted shedding curves.
      </p>
    </div>
  </div>
</section>

<!-- How to use this page -->
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">How to use this page</span>
    <div class="columns is-variable is-6 mt-2">
      <div class="column">
        <h3 class="title is-6">1. Narrow the list</h3>
        <p class="is-size-7">
          Search by study identifier or title, or filter by pathogen and specimen type.
          Filters apply across every dataset, not just the page you are on.
        </p>
      </div>
      <div class="column">
        <h3 class="title is-6">2. Read the card</h3>
        <p class="is-size-7">
          Each card shows the study identifier, how many participants and measurements it
          holds, and which pathogens it covers.
        </p>
      </div>
      <div class="column">
        <h3 class="title is-6">3. Open a study</h3>
        <p class="is-size-7">
          <strong>Explore</strong> opens the study page, where every analyte's
          fitted shedding curve is plotted against its measurements.
          <strong>Source</strong> goes to the original paper.
        </p>
      </div>
    </div>
  </div>
</section>

<!-- The filter bar sticks only while the list it controls is on screen: its
     containing block ends with this wrapper, so it releases before the sections
     below rather than floating over them. -->
<div class="datasets-browse">

<!-- Search and Filter Controls -->
<section class="filter-controls">
  <div class="container is-max-desktop">
    <!-- Same three-column grid as the how-to block above, so the controls line
         up with it exactly rather than each sizing to its own content. -->
    <div class="columns is-variable is-6 mb-0">
      <div class="column">
        <div class="control has-icons-left">
          <input class="input" type="search" id="search-input" placeholder="Search datasets...">
          <span class="icon is-left">
            <i class="fas fa-search"></i>
          </span>
        </div>
      </div>

      <div class="column">
        <div class="select is-fullwidth">
          <select id="biomarker-filter">
            <option value="">All Biomarkers</option>
            <!-- Populated by JavaScript -->
          </select>
        </div>
      </div>

      <div class="column">
        <div class="select is-fullwidth">
          <select id="specimen-filter">
            <option value="">All Specimens</option>
            <!-- Populated by JavaScript -->
          </select>
        </div>
      </div>
    </div>
    <p class="filter-count">
      <strong><span id="results-count">{{ site.datasets | size }}</span> datasets</strong>
    </p>
  </div>
</section>

<section class="section pt-4">
  <div class="container is-max-desktop">
    <div class="dataset-grid" id="datasets-container">
      {% for dataset in site.datasets %}
      {% capture biomarkers %}{% for analyte in dataset.analytes %}{{analyte[1].biomarker}}{% unless forloop.last %},{% endunless %}{% endfor %}{% endcapture %}
      {% capture specimens %}{% for analyte in dataset.analytes %}{% if analyte[1].specimen.first %}{% for spec in analyte[1].specimen %}{{spec}}{% unless forloop.last %},{% endunless %}{% endfor %}{% else %}{{analyte[1].specimen}}{% endif %}{% unless forloop.last %},{% endunless %}{% endfor %}{% endcapture %}
      {% assign num_measurements = 0 %}
      {% for participant in dataset.participants %}
      {% assign temp = participant.measurements | size %}
      {% assign num_measurements = num_measurements | plus: temp %}
      {% endfor %}
      <article class="card dataset-card" data-biomarkers="{{ biomarkers }}" data-specimens="{{ specimens }}" data-slug="{{ dataset.slug }}">
        <div class="card-content">
          <h3 class="title is-6 dataset-title">{{ dataset.title }}</h3>
          <p class="dataset-slug is-data">{{ dataset.slug }}</p>

          <div class="dataset-stats">
            <span>
              <span class="icon"><i class="fas fa-people-group"></i></span>
              <span class="separate-thousands">{{ dataset.participants | size }}</span>
              participants
            </span>
            <span>
              <span class="icon"><i class="fa-solid fa-vial-circle-check"></i></span>
              <span class="separate-thousands">{{ num_measurements }}</span>
              measurements
            </span>
          </div>

          <div class="dataset-tags">
            {% assign uniq_biomarkers = biomarkers | split: ',' | uniq %}
            {% for biomarker in uniq_biomarkers %}
            <span class="tag pathogen-tag pathogen-{{ biomarker | slugify }}">{{ biomarker }}</span>
            {% endfor %}
          </div>
        </div>
        <footer class="card-footer">
          {% if dataset.doi %}
          {% assign url = "https://doi.org/" | append: dataset.doi %}
          {% else %}
          {% assign url = dataset.source_url %}
          {% endif %}
          <a href="{{ url }}" class="card-footer-item" title="Open the source paper">
            <span class="icon"><i class="fa-solid fa-file-lines"></i></span>
            <span>Source</span>
          </a>
          {% assign dataset_key = dataset.path | split: "/" | last | split: "." | first %}
          <a href="https://github.com/shedding-hub/shedding-hub/blob/main/data/{{ dataset_key }}/{{ dataset_key }}.yaml"
             class="card-footer-item" title="View the dataset YAML on GitHub">
            <span class="icon"><i class="fab fa-github"></i></span>
            <span>YAML</span>
          </a>
          <a href="{{ dataset.url }}" class="card-footer-item is-explore" title="Open the study page with its fitted curves">
            <span class="icon"><i class="fa-solid fa-chart-line"></i></span>
            <span>Explore</span>
          </a>
        </footer>
      </article>
      {% endfor %}
    </div>

    <p id="datasets-empty" class="notification is-light" hidden>
      No datasets match that search. Clear a filter to widen it.
    </p>

    <nav class="pager" id="datasets-pager" aria-label="Dataset pages">
      <button type="button" class="button pager-prev" id="pager-prev">
        <span class="icon"><i class="fa-solid fa-arrow-left"></i></span>
        <span>Previous</span>
      </button>
      <div class="pager-pages" id="pager-pages"></div>
      <button type="button" class="button pager-next" id="pager-next">
        <span>Next</span>
        <span class="icon"><i class="fa-solid fa-arrow-right"></i></span>
      </button>
    </nav>
  </div>
</section>

</div><!-- /.datasets-browse -->

<!-- Example fit -->
<section class="section has-background-light">
  <div class="container is-max-desktop">
    <span class="eyebrow">What a study page shows</span>
    <h2 class="title is-4 mb-4">Every analyte gets a fitted curve</h2>
    <div class="columns is-variable is-6">
      <div class="column is-7">
        <figure class="example-fit">
          <img src="/assets/figures/woelfel2020virological/stool__gamma.png"
               alt="Gamma model fitted to SARS-CoV-2 stool shedding from woelfel2020virological, plotted against the observed measurements"
               loading="lazy">
        </figure>
      </div>
      <div class="column is-5">
        <div class="content">
          <p>
            This is the gamma fit for SARS-CoV-2 in stool from
            <a href="/datasets/woelfel2020virological.html"><code>woelfel2020virological</code></a>,
            plotted over the measurements it was fitted to. Non-detects are handled as
            censored observations rather than dropped.
          </p>
          <p>
            Open any study with <strong>Explore</strong> to see its own curves, or
            compare the fitted parameters across every study in one table.
          </p>
          <a href="/fits.html" class="button is-primary">
            <span class="icon"><i class="fa-solid fa-table"></i></span>
            <span>Browse the fits catalog</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
/* Three across on desktop, one on a phone. Cards are uniform height so the grid
   does not ripple as titles wrap to different line counts. */
.dataset-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  align-items: stretch;
}

@media screen and (max-width: 1023px) {
  .dataset-grid { grid-template-columns: repeat(2, 1fr); }
}

@media screen and (max-width: 640px) {
  .dataset-grid { grid-template-columns: 1fr; }
}

.dataset-card {
  display: flex;
  flex-direction: column;
  border-radius: 4px;
}

.dataset-card .card-content {
  flex: 1 1 auto;
  padding: 1.25rem;
}

.dataset-title {
  line-height: 1.35;
  margin-bottom: 0.5rem;
}

.dataset-slug {
  font-size: 0.72rem;
  color: var(--text-light);
  margin-bottom: 0.9rem;
  word-break: break-all;
}

.dataset-stats {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
  margin-bottom: 0.9rem;
}

.dataset-stats .icon {
  color: var(--primary-color);
  margin-right: 0.35rem;
}

.dataset-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.dataset-tags .tag {
  background-color: var(--bg-secondary);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  font-size: 0.68rem;
}

.dataset-card .card-footer {
  border-top: 1px solid var(--border-color);
}

.dataset-card .card-footer-item {
  font-size: 0.75rem;
  padding: 0.6rem 0.35rem;
  color: var(--text-secondary);
  border-color: var(--border-color);
  flex-direction: column;
  gap: 0.2rem;
  /* Column flex centres the label as a block; without this its text still sets
     ragged-left whenever it wraps to a second line. */
  text-align: center;
}

.dataset-card .card-footer-item .icon {
  font-size: 0.8rem;
}

.dataset-card .card-footer-item:hover {
  color: var(--primary-color);
  background-color: var(--bg-secondary);
}

.dataset-card .card-footer-item.is-explore {
  color: var(--primary-color);
  font-weight: 600;
}

/* Pager */
.pager {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-top: 2.5rem;
  flex-wrap: wrap;
}

.pager-pages {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.pager-page {
  min-width: 2.25rem;
  height: 2.25rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background-color: var(--bg-card);
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-size: 0.8rem;
  cursor: pointer;
}

.pager-page:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.pager-page[aria-current="page"] {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: var(--text-inverse);
  font-weight: 600;
}

[data-theme="dark"] .pager-page[aria-current="page"] {
  color: var(--bg-primary);
}

.pager-ellipsis {
  align-self: center;
  color: var(--text-light);
  padding: 0 0.25rem;
}

.pager button:disabled {
  opacity: 0.4;
  cursor: default;
}

.example-fit img {
  display: block;
  width: 100%;
  height: auto;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  background: #fff;
}
</style>
