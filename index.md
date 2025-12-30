---
layout: default
title: Shedding Hub
---

<section class="hero is-light">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <h1 class="title is-size-1 mb-4">Shedding Hub</h1>
      <p class="subtitle is-size-4">
        To support global efforts to understand and model pathogen shedding dynamics, we provide curated data,
        statistical models, and interactive tools for researchers and public health professionals.
      </p>
    </div>
  </div>
</section>

<!-- Highlights Section -->
<section class="section has-background-light">
  <div class="container is-max-desktop">
    <div class="columns">
      <div class="column">
        <div class="box" style="height: 100%;">
          <h3 class="title is-5">
            <span class="icon-text">
              <span class="icon has-text-primary">
                <i class="fa-solid fa-database"></i>
              </span>
              <span>Curated Datasets</span>
            </span>
          </h3>
          <p>Access standardized biomarker shedding data from published studies, spanning multiple pathogens and specimen types.</p>
        </div>
      </div>
      <div class="column">
        <div class="box" style="height: 100%;">
          <h3 class="title is-5">
            <span class="icon-text">
              <span class="icon has-text-primary">
                <i class="fa-solid fa-chart-line"></i>
              </span>
              <span>Statistical Models</span>
            </span>
          </h3>
          <p>Bayesian workflows and tutorials for modeling shedding dynamics, including time-course analysis and decay models.</p>
        </div>
      </div>
      <div class="column">
        <div class="box" style="height: 100%;">
          <h3 class="title is-5">
            <span class="icon-text">
              <span class="icon has-text-primary">
                <i class="fa-solid fa-code"></i>
              </span>
              <span>Python Tools</span>
            </span>
          </h3>
          <p>Programmatic access to data and analysis tools through our open-source Python package and interactive visualizations.</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- At a Glance Section -->
<section class="section">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered mb-5">At a Glance</h2>
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
    <div class="content has-text-centered">
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

<!-- Interactive Data Explorer Section -->
<section class="section has-background-light">
  <div class="container is-fluid">
    <h2 class="title is-3 has-text-centered mb-4">Interactive Data Explorer</h2>
    <div class="container is-max-desktop content has-text-centered mb-5">
      <p>
        Explore biomarker shedding data interactively through our dashboard. Visualize time-course patterns,
        compare across studies, and analyze shedding dynamics.
      </p>
    </div>
    <div class="dashboard-container">
      <iframe
        id="dash-dashboard"
        src="PLACEHOLDER_DASH_URL"
        frameborder="0"
        loading="lazy"
        title="Shedding Hub Interactive Dashboard">
      </iframe>
    </div>
  </div>
</section>

<!-- Why Section -->
<section class="section">
  <div class="container is-max-desktop">
    <div class="content">
      <h2 class="title is-3">Why Focus on Shedding Data?</h2>
      <p>
        Understanding pathogen shedding dynamics is critical for infectious disease transmission modeling,
        wastewater-based epidemiology, and public health surveillance. However, shedding data is often
        scattered across publications, stored in heterogeneous formats, and difficult to access for
        meta-analysis and model development.
      </p>
      <p>
        Shedding Hub addresses these challenges by providing a centralized platform with standardized data,
        statistical modeling resources, and interactive tools. Our platform enables researchers to explore
        shedding patterns across studies, develop and validate models, and generate insights for
        evidence-informed public health decision-making.
      </p>
    </div>
  </div>
</section>

<!-- Leadership Section -->
<section class="section has-background-light">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered mb-6">Leadership</h2>

    <!-- Core Team -->
    <h3 class="title is-4 has-text-centered mb-4">Core Team</h3>
    <div class="columns">
      <div class="column is-6">
        <div class="card">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-128x128">
                  <img src="/assets/team/andrew.jpg" alt="Yuke (Andrew) Wang" style="border-radius: 50%;">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">Yuke (Andrew) Wang</p>
                <p class="subtitle is-6">{{ site.data.team.andrew.job }}</p>
                <p class="subtitle is-6">{{ site.data.team.andrew.institution }}</p>
              </div>
            </div>
            <div class="content">
              <p>{{ site.data.team.andrew.bio | truncatewords: 50 }}</p>
              <a href="/team.html#andrew">View profile</a>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-6">
        <div class="card">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-128x128">
                  <img src="/assets/team/till.jpg" alt="Till Hoffmann" style="border-radius: 50%;">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">Till Hoffmann</p>
                <p class="subtitle is-6">{{ site.data.team.till.job }}</p>
                <p class="subtitle is-6">{{ site.data.team.till.institution }}</p>
              </div>
            </div>
            <div class="content">
              <p>{{ site.data.team.till.bio | truncatewords: 50 }}</p>
              <a href="/team.html#till">View profile</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Scientific Advisors -->
    <h3 class="title is-4 has-text-centered mb-4 mt-6">Scientific Advisors</h3>
    <div class="columns">
      <div class="column is-6">
        <div class="card">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-128x128">
                  <img src="/assets/team/ChristineMoe.jpg" alt="Dr. Christine Moe" style="border-radius: 50%;">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">Dr. Christine Moe</p>
                <p class="subtitle is-6">Professor</p>
                <p class="subtitle is-6">Rollins School of Public Health, Emory University</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-6">
        <div class="card">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-128x128">
                  <img src="/assets/team/PeterTeunis.jpg" alt="Dr. Peter Teunis" style="border-radius: 50%;">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">Dr. Peter Teunis</p>
                <p class="subtitle is-6">Visiting Professor</p>
                <p class="subtitle is-6">Rollins School of Public Health, Emory University</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<style>
/* Dashboard container */
.dashboard-container {
  position: relative;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  background: var(--bg-secondary);
  border-radius: 6px;
  transition: background-color 0.3s ease;
}

.dashboard-container::before {
  content: 'Loading dashboard...';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: var(--text-light);
  font-size: 1.2rem;
  z-index: -1;
}

/* Responsive iframe sizing */
#dash-dashboard {
  width: 100%;
  height: 800px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-card);
  display: block;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

/* Tablet breakpoint */
@media screen and (max-width: 1024px) {
  #dash-dashboard {
    height: 700px;
  }
}

/* Mobile breakpoint */
@media screen and (max-width: 768px) {
  #dash-dashboard {
    height: 600px;
  }

  .dashboard-container {
    margin: 0 -1rem;
    border-radius: 0;
  }
}

/* Loading spinner animation */
.dashboard-container.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 50px;
  height: 50px;
  margin: -25px 0 0 -25px;
  border: 4px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const container = document.querySelector('.dashboard-container');
  const iframe = document.getElementById('dash-dashboard');

  // Add loading state
  container.classList.add('loading');

  // Handle successful load
  iframe.addEventListener('load', function() {
    container.classList.remove('loading');
    console.log('Dashboard loaded successfully');
  });

  // Handle load errors
  iframe.addEventListener('error', function() {
    container.classList.remove('loading');
    container.innerHTML = `
      <div class="notification is-warning">
        <p><strong>Dashboard temporarily unavailable</strong></p>
        <p>The interactive dashboard could not be loaded. Please try refreshing the page or visit the <a href="/datasets.html">Datasets page</a> to browse data.</p>
      </div>
    `;
  });

  // Timeout fallback (30 seconds)
  setTimeout(function() {
    if (container.classList.contains('loading')) {
      console.warn('Dashboard load timeout');
      container.classList.remove('loading');
    }
  }, 30000);
});
</script>
