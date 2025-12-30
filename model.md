---
layout: default
title: Models - Shedding Hub
---
<section class="hero is-light">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <h1 class="title is-size-1 mb-4">Models</h1>
      <p class="subtitle is-size-4">
        Statistical models and tutorials for analyzing pathogen shedding dynamics.
      </p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop content">
    <div class="card">
      <div class="card-content">
        <a class="title has-text-primary" href="https://shedding-hub.github.io/tutorials/Bayesian-workflow-Rstan.html">Bayesian Workflow for Modeling Shedding Dynamics using Rstan</a>
        <div class="media-content" style="margin-top: 20px;">
          <ul style="list-style: none; margin: 0; padding: 0;">
            <li>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-user"></i>
                </span>
                <span style="font-family:'Courier New'">Yuke Wang, <a href="https://github.com/YWAN446">@YWAN446</a></span> 
              </span>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-building-columns"></i>
                </span>
                <span style="font-family:'Courier New'">Hubert Department of Global Health, Rollins School of Public Health, Emory University</span>
              </span>
            </li>
            <li>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-user"></i>
                </span>
                <span style="font-family:'Courier New'">Till Hoffmann, <a href="https://github.com/tillahoffmann">@tillahoffmann</a></span> 
              </span>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-building-columns"></i>
                </span>
                <span style="font-family:'Courier New'">Department of Biostatistics, Harvard T.H. Chan School of Public Health, Harvard University</span>
              </span>
            </li>
          </ul>
        </div>
        <div class="content" style="margin-top: 20px;">
          <p> The current tutorial demonstrates the Bayesian workflow to model shedding data using Rstan. We use the longitudinal SARS-CoV-2 fecal shedding data from <a href="https://doi.org/10.1038/s41586-020-2196-x">Wölfel et al. (2020)</a>. The data includes observations of SARS-CoV-2 RNA concentration in 82 stool samples from 9 patients. As most samples collected in shedding studies are several days after symptom onset when the number of pathogens shed is decreasing. In this tutorial, we focus on modeling the decay phase of the shedding dynamics. We consider two classical models, exponential decay model and gamma model.</p>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-content">
        <a class="title has-text-primary" href="https://github.com/shedding-hub/shedding-hub.github.io/blob/main/tutorials/Time-course-of-fecal-shedding-using-JAGS_Teunis/shed-mod.md">Time Course of Fecal Shedding</a>
        <div class="media-content" style="margin-top: 20px;">
          <ul style="list-style: none; margin: 0; padding: 0;">
            <li>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-user"></i>
                </span>
                <span style="font-family:'Courier New'">Peter FM Teunis,</span> 
              </span>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-building-columns"></i>
                </span>
                <span style="font-family:'Courier New'">Center for Global Safe WASH, Rollins School of Public Health, Emory University</span>
              </span>
            </li>
          </ul>
        </div>
        <div class="content" style="margin-top: 20px;">
          <p> We develop a realistic model of the time course of virus shedding which includes an initial increase in virus concentration, followed by a decrease to undetectable levels. In this tutoiral, we apply the model to the longitudinal SARS-CoV-2 fecal shedding data from <a href="https://doi.org/10.1038/s41586-020-2196-x">Wölfel et al. (2020)</a> using JAGS. The data includes observations of SARS-CoV-2 RNA concentration in 82 stool samples from 9 patients.</p>
        </div>
      </div>
    </div>
  </div>
</section>