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
        src="https://shedding-hub-dashboard-demo.onrender.com"
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
      <h2 class="title is-3 has-text-centered">Why Focus on Shedding Data?</h2>
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

<!-- Data Curation Section -->
<section class="section has-background-light">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered mb-5">Our Approach for Data Curation</h2>
    <div class="content">
      <p>
        Shedding Hub provides high-quality, curated pathogen shedding data extracted from published scientific literature.
        Since May 2024, our team of human biocurators has meticulously extracted biomarker shedding data from peer-reviewed
        studies, with rigorous quality assurance and quality control processes ensuring data accuracy and consistency.
      </p>
      <p>
        Beginning in June 2025, we enhanced our curation pipeline by integrating large language models (LLMs) to power
        the data discovery and extraction process. This AI-assisted approach allows us to scale our efforts significantly
        while maintaining the high quality standards established by our human curation workflow. All LLM-extracted data
        undergoes expert review to ensure reliability and completeness.
      </p>
    </div>
  </div>
</section>

<!-- Get Started Section -->
<section class="section">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered mb-5">Get Started</h2>
    <div class="content">
      <p class="has-text-centered mb-5">
        Access and analyze Shedding Hub data in just a few lines of Python code.
        Watch this quick tutorial to see how easy it is to get started.
      </p>

      <div class="video-container">
        <video autoplay muted loop controls playsinline preload="auto" style="width: 100%; max-width: 1280px; display: block; margin: 0 auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
          <source src="/assets/videos/SheddingHubQuickStart.mp4" type="video/mp4">
          Your browser does not support the video tag.
        </video>
      </div>

      <div class="has-text-centered mt-5">
        <a href="/package.html" class="button is-primary is-medium">
          <span class="icon">
            <i class="fa-solid fa-book"></i>
          </span>
          <span>View Full Documentation</span>
        </a>
      </div>
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
                <p class="subtitle is-6">Co-founder</p>
                <p class="subtitle is-6">{{ site.data.team.andrew.job }}, {{ site.data.team.andrew.institution }}</p>
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
                <p class="subtitle is-6">Co-founder</p>
                <p class="subtitle is-6">{{ site.data.team.till.job }}, {{ site.data.team.till.institution }}</p>
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
    <div class="columns is-multiline">
      <div class="column is-6">
        <div class="card" style="height: 100%;">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-128x128">
                  <img src="/assets/team/ChristineMoe.jpg" alt="Dr. Christine Moe" style="border-radius: 50%;">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">Dr. Christine Moe</p>
                <p class="subtitle is-6">Eugene J. Gangarosa Professor of Safe Water and Sanitation, Hubert Department of Global Health, Rollins School of Public Health, Emory University</p>
              </div>
            </div>
            <div class="content">
              <a href="https://sph.emory.edu/profile/faculty/christine-moe">View profile</a>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-6">
        <div class="card" style="height: 100%;">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-128x128">
                  <img src="/assets/team/PeterTeunis.jpg" alt="Dr. Peter Teunis" style="border-radius: 50%;">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">Dr. Peter Teunis</p>
                <p class="subtitle is-6">Visiting Professor, Hubert Department of Global Health, Rollins School of Public Health, Emory University</p>
              </div>
            </div>
            <div class="content">
              <a href="https://sph.emory.edu/profile/faculty/peter-teunis">View profile</a>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-6">
        <div class="card" style="height: 100%;">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-128x128">
                  <img src="/assets/team/BenLopman.jpg" alt="Dr. Benjamin Lopman" style="border-radius: 50%;">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">Dr. Benjamin Lopman</p>
                <p class="subtitle is-6">Professor, Department of Epidemiology, Rollins School of Public Health, Emory University, Director and Co-Principal Investigator, CIDMATH</p>
              </div>
            </div>
            <div class="content">
              <a href="https://sph.emory.edu/profile/faculty/benjamin-lopman">View profile</a>
            </div>
          </div>
        </div>
      </div>
      <div class="column is-6">
        <div class="card" style="height: 100%;">
          <div class="card-content">
            <div class="media">
              <div class="media-left">
                <figure class="image is-128x128">
                  <img src="/assets/team/KatiaKoelle.jpg" alt="Dr. Katia Koelle" style="border-radius: 50%;">
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-5">Dr. Katia Koelle</p>
                <p class="subtitle is-6">Professor, Department of Biology, College of Arts and Sciences, Emory University, Director of Scientific Initiatives and Co-Principal Investigator, CIDMATH</p>
              </div>
            </div>
            <div class="content">
              <a href="https://biology.emory.edu/people/bios/faculty/koelle-katia.html">View profile</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Contribute Data Section -->
<section class="section">
  <div class="container is-max-desktop">
    <h2 class="title is-3 has-text-centered mb-5">Contribute Data</h2>
    <div class="content has-text-centered">
      <p class="mb-5">
        Help expand the Shedding Hub database by contributing your pathogen shedding datasets.
        We welcome data on biomarker shedding dynamics across various pathogens,
        specimen types, and populations. Our team will work with you to ensure proper data formatting
        and integration into the platform.
      </p>
      <p class="mb-5">
        Whether you have data from a single subject or multiple studies, we're here to help.
        Contributions undergo quality review and are credited appropriately in our database.
      </p>
      <a href="mailto:sheddinghub@gmail.com?subject=Dataset Contribution Inquiry" class="button is-primary is-large">
        <span class="icon">
          <i class="fa-solid fa-envelope"></i>
        </span>
        <span>Contact Us to Contribute</span>
      </a>
    </div>
  </div>
</section>

<!-- Funding Acknowledgment Section -->
<section class="section has-background-light">
  <div class="container is-max-desktop">
    <div class="content has-text-centered">
      <h2 class="title is-4 mb-4">Funding</h2>
      <p class="mb-4">
        The Shedding Hub was made possible by the Insight Net cooperative agreement CDC-RFA-FT-23-0069 from the CDC’s Center for Forecasting and Outbreak Analytics. Its contents are solely the responsibility of the authors and do not necessarily represent the official views of the Centers for Disease Control and Prevention. Support for the Shedding Hub is provided by the Emory Center for Infectious Disease Modeling and Analytics & Training Hub (CIDMATH).
      </p>
      <a href="https://cidmath.org/" target="_blank" rel="noopener noreferrer">
        <img src="/assets/logo/logo_emory_cidmath_dark_blue_2_no-tagline.svg"
             alt="CIDMATH - Center for Infectious Disease Modeling and Analysis"
             style="max-width: 400px; width: 100%; height: auto;">
      </a>
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
  height: 1000px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  background: var(--bg-card);
  display: block;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

/* Tablet breakpoint */
@media screen and (max-width: 1024px) {
  #dash-dashboard {
    height: 850px;
  }
}

/* Mobile breakpoint */
@media screen and (max-width: 768px) {
  #dash-dashboard {
    height: 700px;
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
