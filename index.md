---
layout: default
title: Shedding Hub
---
<section class="hero is-light">
  <!-- calculate the number of measurements, participants, and studies -->
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
  <div class="container is-max-desktop">
    <div class="hero-body">
      <div class="is-size-1">
        <span class="has-text-primary has-text-weight-bold separate-thousands">{{ num_measurements }}</span>
        biomarker measurements for
        <span class="has-text-primary has-text-weight-bold separate-thousands">{{ num_participants }}</span>
        participants from
        <span class="has-text-primary has-text-weight-bold separate-thousands">{{ site.datasets | size }}</span>
        studies. And counting.
      </div>
    </div>
  </div>
</section>

<!-- Search and Filter Controls -->
<section class="filter-controls">
  <div class="container is-max-desktop">
    <div class="field is-horizontal">
      <!-- Search input -->
      <div class="control has-icons-left">
        <input class="input" type="search" id="search-input" placeholder="Search datasets...">
        <span class="icon is-left">
          <i class="fas fa-search"></i>
        </span>
      </div>

      <!-- Biomarker filter -->
      <div class="control">
        <div class="select">
          <select id="biomarker-filter">
            <option value="">All Biomarkers</option>
            <!-- Populated by JavaScript -->
          </select>
        </div>
      </div>

      <!-- Specimen filter -->
      <div class="control">
        <div class="select">
          <select id="specimen-filter">
            <option value="">All Specimens</option>
            <!-- Populated by JavaScript -->
          </select>
        </div>
      </div>

      <!-- Results count -->
      <div class="control">
        <p class="help">
          <strong><span id="results-count">{{ site.datasets | size }}</span> datasets</strong>
        </p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop" id="datasets-container">
    {% for dataset in site.datasets %}
    {% capture biomarkers %}{% for analyte in dataset.analytes %}{{analyte[1].biomarker}}{% unless forloop.last %},{% endunless %}{% endfor %}{% endcapture %}
    {% capture specimens %}{% for analyte in dataset.analytes %}{% if analyte[1].specimen.first %}{% for spec in analyte[1].specimen %}{{spec}}{% unless forloop.last %},{% endunless %}{% endfor %}{% else %}{{analyte[1].specimen}}{% endif %}{% unless forloop.last %},{% endunless %}{% endfor %}{% endcapture %}
    <div class="card dataset-card mb-5" data-biomarkers="{{ biomarkers }}" data-specimens="{{ specimens }}" data-slug="{{ dataset.slug }}">
      <div class="card-content">
        <p class="title has-text-primary">{{dataset.title}}</p>
        <div class="grid">
          <div class="cell has-text-centered">
            <div>
              <p class="heading">Identifier</p>
              <span class="icon-text">
                <span class="icon">
                  <i class="fas fa-barcode"></i>
                </span>
                <code>{{ dataset.slug }}</code>
              </span>
            </div>
          </div>
          <div class="cell has-text-centered">
            <div>
              <p class="heading">Participants</p>
              <span class="icon-text">
                <span class="icon">
                  <i class="fas fa-people-group"></i>
                </span>
                <span class="separate-thousands">{{ dataset.participants | size }}</span>
              </span>
            </div>
          </div>
          <div class="cell has-text-centered">
            <div>
              {% assign num_measurements = 0 %}
              {% for participant in dataset.participants %}
              {% assign temp = participant.measurements | size %}
              {% assign num_measurements = num_measurements | plus: temp %}
              {% endfor %}
              <p class="heading">Measurements</p>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-vial-circle-check"></i>
                </span>
                <span class="separate-thousands">{{ num_measurements }}</span>
              </span>
            </div>
          </div>
          <div class="cell has-text-centered">
            <div>
              <p class="heading">Biomarkers</p>
              {% assign uniq_biomarkers = biomarkers | split: ',' | uniq %}
              {% for biomarker in uniq_biomarkers %}
              <span class="tag">{{ biomarker }}</span>
              {% endfor %}
            </div>
          </div>
        </div>
        <div class="content">{{ dataset.description | markdownify }}</div>
      </div>
      <footer class="card-footer">
        {% if dataset.doi %}
        {% assign url = "https://doi.org/" | append: dataset.doi %}
        {% else %}
        {% assign url = dataset.source_url %}
        {% endif %}
        <a href="{{ url }}" class="card-footer-item">
          <span class="icon-text">
            <span class="icon">
              <i class="fa-solid fa-file-lines"></i>
            </span>
            <span>View Source</span>
          </span>
        </a>
        {% assign dataset_key = dataset.path | split: "/" | last | split: "." | first%}
        <a href="https://github.com/shedding-hub/shedding-hub/blob/main/data/{{ dataset_key }}/{{ dataset_key }}.yaml"
          class="card-footer-item">
          <span class="icon-text">
            <span class="icon">
              <i class="fab fa-github"></i>
            </span>
            <span>View on GitHub</span>
          </span>
        </a>
        <a href="{{ dataset.url }}" class="card-footer-item">
          <span class="icon-text">
            <span class="icon">
              <i class="fa-solid fa-chart-line"></i>
            </span>
            <span>Explore Dataset</span>
          </span>
        </a>
      </footer>
    </div>
    {% endfor %}
  </div>
</section>
