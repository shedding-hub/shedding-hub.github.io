---
layout: default
title: Shedding Hub
---
<section class="hero is-light">
  <!-- calculate the number of measurements, participants, and studies -->
  {% assign num_measurements = 0 %}
  {% assign num_participants = 0 %}
  {% for dataset_hash in site.data.datasets %}
  {% assign dataset = dataset_hash[1] %}
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
        <span class="has-text-primary has-text-weight-bold separate-thousands">{{ site.data.datasets | size }}</span>
        studies. And counting.
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop">
    {% for dataset_hash in site.data.datasets %}
    {% assign dataset = dataset_hash[1] %}
    <div class="card">
      <div class="card-content">
        <p class="title">
          {% if dataset.url %}
          {% assign url = dataset.url %}
          {% else %}
          {% assign url = "https://doi.org/" | append: dataset.doi %}
          {% endif %}
          <a href="{{ url }}">{{dataset.title}}</a>
        </p>
        <div class="grid">
          <div class="cell has-text-centered">
            <div>
              <p class="heading">Participants</p>
              <span class="icon-text">
                <span class="icon">
                  <i class="fas fa-user"></i>
                </span>
                <span>{{ dataset.participants | size }}</span>
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
                <span>{{ num_measurements }}</span>
              </span>
            </div>
          </div>
          <div class="cell has-text-centered">
            <div>
              <p class="heading">Biomarkers</p>
              {% capture biomarkers %}{% for analyte in dataset.analytes %}{{analyte[1].biomarker}};{% endfor %}{%
              endcapture %}
              {% assign uniq_biomarkers = biomarkers | split: ';' | uniq %}
              {% for biomarker in uniq_biomarkers %}
              <span class="tag">{{ biomarker }}</span>
              {% endfor %}
            </div>
          </div>
        </div>
        <p>{{ dataset.description | markdownify }}</p>

      </div>
      <footer class="card-footer">
        <a href="https://github.com/shedding-hub/shedding-hub/blob/main/data/{{dataset_hash[0]}}.yaml"
          class="card-footer-item">
          <span class="icon-text">
            <span class="icon">
              <i class="fab fa-github-alt"></i>
            </span>
            <span>View on GitHub</span>
          </span>
        </a>
      </footer>
    </div>
    {% endfor %}
  </div>
</section>
