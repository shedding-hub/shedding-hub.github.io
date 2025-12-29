---
layout: default
title: Shedding Hub
---

<section class="hero is-light">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <h1 class="title is-size-1">Shedding Hub</h1>
      <p class="subtitle is-size-4">
        Data and statistical models for biomarker shedding
      </p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop">
    <div class="content">
      <p>
        Shedding Hub is a comprehensive platform for biomarker shedding data and statistical models.
        We provide curated datasets from published studies, interactive visualization tools, and
        statistical modeling tutorials to advance research in pathogen shedding dynamics.
      </p>
      <p>
        Our platform supports researchers, public health professionals, and data scientists working
        on infectious disease transmission, wastewater-based epidemiology, and pathogen shedding patterns.
        Explore our interactive dashboard below to visualize shedding data, or browse our
        <a href="/datasets.html">datasets collection</a> and <a href="/model.html">modeling tutorials</a>.
      </p>
    </div>
  </div>
</section>

<!-- Dash Dashboard Section -->
<section class="section">
  <div class="container is-fluid">
    <h2 class="title has-text-centered">Interactive Data Explorer</h2>
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

<!-- Python Package Section -->
<section class="section">
  <div class="container is-max-desktop">
    <h2 class="title">Python Package</h2>
    <div class="content">
      <p>
        Access and analyze Shedding Hub data programmatically with our Python package,
        available on PyPI. The <code>shedding-hub</code> package provides tools for loading datasets,
        performing statistical analyses, and creating visualizations.
      </p>

      <h3>Installation</h3>
      <pre><code>pip install shedding-hub</code></pre>

      <h3>Quick Start</h3>
      <pre><code>import shedding_hub

# Load a dataset
data = shedding_hub.load_dataset('woelfel2020virological')

# Analyze shedding patterns
analysis = shedding_hub.analyze(data)
print(analysis.summary())</code></pre>

      <h3>Features</h3>
      <ul>
        <li>Load datasets directly from the Shedding Hub repository</li>
        <li>Parse YAML data into Python objects</li>
        <li>Statistical analysis tools for shedding dynamics</li>
        <li>Visualization utilities</li>
        <li>Export to common formats (CSV, JSON, pandas DataFrame)</li>
      </ul>

      <div class="buttons">
        <a class="button is-primary" href="https://pypi.org/project/shedding-hub/" target="_blank" rel="noopener">
          <span class="icon">
            <i class="fab fa-python"></i>
          </span>
          <span>View on PyPI</span>
        </a>
        <a class="button is-link" href="https://github.com/shedding-hub/shedding-hub" target="_blank" rel="noopener">
          <span class="icon">
            <i class="fab fa-github"></i>
          </span>
          <span>Documentation</span>
        </a>
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
  background: #f5f5f5;
  border-radius: 6px;
}

.dashboard-container::before {
  content: 'Loading dashboard...';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #7a7a7a;
  font-size: 1.2rem;
  z-index: -1;
}

/* Responsive iframe sizing */
#dash-dashboard {
  width: 100%;
  height: 800px;
  border: 1px solid #dbdbdb;
  border-radius: 6px;
  background: white;
  display: block;
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
  border: 4px solid #dbdbdb;
  border-top-color: #485fc7;
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
