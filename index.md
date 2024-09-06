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

<section class="section">
  <div class="container is-max-desktop">
    {% for dataset in site.datasets %}
    <div class="card">
      <div class="card-content">
        <p class="title has-text-primary">{{dataset.title}}</p>
        <div class="grid">
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
              {% capture biomarkers %}{% for analyte in dataset.analytes %}{{analyte[1].biomarker}};{% endfor %}{%
              endcapture %}
              {% assign uniq_biomarkers = biomarkers | split: ';' | uniq %}
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
        <!-- TODO: `url` automatically created by the collection overwrites the `url` field in the data. -->
        {% assign url = dataset.url %}
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
              <i class="fab fa-github-alt"></i>
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
