---
layout: default
title: Models - Shedding Hub
---
<section class="hero is-light">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <h1 class="title is-size-1 mb-4">Models</h1>
      <p class="subtitle is-size-4">
        The shedding curves fitted across the repository, and worked examples of
        fitting your own.
      </p>
    </div>
  </div>
</section>

<!-- The three curve families -->
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">The curves</span>
    <h2 class="title is-3 mb-2">Three shapes, fitted to every analyte with enough data</h2>
    <p class="subtitle is-6 mb-5">
      All three are fitted on the log<sub>10</sub> scale by censored maximum likelihood.
    </p>

    <div class="curve">
      <div class="curve-head">
        <h3 class="title is-6">Exponential</h3>
        <code class="curve-form">c(t) = c₀ · e<sup>−a₀t</sup></code>
      </div>
      <p>
        Pure decay from the reference event. It assumes shedding is already at its peak
        when the clock starts, which is often true when the clock starts at symptom onset
        and the study caught people late.
      </p>
    </div>

    <div class="curve">
      <div class="curve-head">
        <h3 class="title is-6">Gamma</h3>
        <code class="curve-form">c(t) = c₀ · t<sup>b₀</sup> · e<sup>−a₀t</sup></code>
      </div>
      <p>
        A rise to a peak at <code>t = b₀/a₀</code>, then decay. It needs observations
        after the reference event to see the rise, and its curve is undefined at
        <code>t ≤ 0</code>, so those readings are discarded.
      </p>
    </div>

    <div class="curve">
      <div class="curve-head">
        <h3 class="title is-6">Gamma shifted</h3>
        <code class="curve-form">c(t) = c₀ · (t−t₀)<sup>b₀</sup> · e<sup>−a₀(t−t₀)</sup></code>
      </div>
      <p>
        The same shape with shedding starting at <code>t₀</code> rather than at the
        reference event. It exists because the reference event is not the same event
        across studies &mdash; symptom onset, enrollment, confirmation, vaccination and
        hospital admission all appear &mdash; and because the plain gamma was discarding
        tens of thousands of detected measurements recorded at exactly <code>t = 0</code>.
        Its <code>t₀</code> is what makes those reference events commensurable.
      </p>
    </div>

    <div class="content mt-5">
      <p>
        Across all three, <code>a₀</code> is the decay rate, giving a half-life of
        <code>ln(2)/a₀</code>; <code>b₀</code> governs the rise; <code>t₀</code> is the
        onset of shedding.
      </p>
    </div>

    <div class="caution">
      <span class="eyebrow">Read this before comparing them</span>
      <p>
        <strong>Choosing between the three is not an AIC comparison.</strong> They are
        fitted to different observation sets &mdash; gamma drops every reading at
        <code>t ≤ 0</code> and gamma-shifted keeps the detected ones &mdash; and AIC only
        compares models fitted to the same data. Check the measurement count before
        reading anything into the AIC.
      </p>
    </div>

    <div class="content mt-5">
      <p>
        <a href="/fits.html">See every fitted curve and its parameters &rarr;</a><br>
        <a href="https://shedding-hub.readthedocs.io/en/latest/modeling-methods/">Read the
        full modelling methods, including where the estimates should not be trusted &rarr;</a>
      </p>
    </div>
  </div>
</section>

<hr class="lod-rule">

<!-- Censoring -->
<section class="section">
  <div class="container is-max-desktop">
    <div class="columns is-variable is-8">
      <div class="column is-6">
        <span class="eyebrow">How they are fitted</span>
        <h2 class="title is-4">Non-detects are data</h2>
        <div class="content">
          <p>
            Roughly a third of the measurements in the repository are reported negative.
            They enter the likelihood as left-censored observations &mdash; carrying the
            information that the concentration was below the limit &mdash; rather than
            being dropped or replaced with a substituted value.
          </p>
          <p>
            Dropping them biases decay rates slow and inflates simulated late-phase
            shedding, which is exactly the quantity a wastewater or transmission model
            is most sensitive to.
          </p>
        </div>
      </div>
      <div class="column is-6">
        <span class="eyebrow">If you just want numbers</span>
        <h2 class="title is-4">You do not have to fit anything</h2>
        <div class="content">
          <p>
            The fitted parameters ship with the Python package, so a transmission or
            wastewater model can consume them directly without refitting: load a
            study, take its curve, and simulate a cohort that carries
            inter-individual variability rather than tracing one average.
          </p>
          <p>
            <a href="/package.html">See what the package does &rarr;</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</section>

<hr class="lod-rule">

<!-- Tutorials -->
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">Worked examples</span>
    <h2 class="title is-3 mb-2">Fitting shedding curves yourself</h2>
    <p class="subtitle is-6 mb-5">
      Both work through
      <a href="/datasets/woelfel2020virological.html"><code>woelfel2020virological</code></a>,
      so they can be read against each other.
    </p>

    <div class="columns">
      <div class="column is-6">
        <a class="tutorial-card" href="/tutorials/Bayesian-workflow-Rstan.html">
          <p class="tutorial-tool is-data">R &middot; Stan</p>
          <h3 class="title is-5">A Bayesian workflow for shedding dynamics</h3>
          <p>
            Builds the decay phase up as a Bayesian workflow: prior predictive checks,
            fitting, diagnostics, and comparison of an exponential against a gamma model.
          </p>
          <p class="tutorial-authors">
            Yuke Wang &middot; Till Hoffmann
          </p>
          <span class="tutorial-link">Open the tutorial <i class="fa-solid fa-arrow-right"></i></span>
        </a>
      </div>

      <div class="column is-6">
        <a class="tutorial-card" href="/tutorials/Time-course-of-fecal-shedding-using-JAGS_Teunis/shed-mod.html">
          <p class="tutorial-tool is-data">R &middot; JAGS</p>
          <h3 class="title is-5">Time course of fecal shedding</h3>
          <p>
            Models the whole time course rather than the decay alone &mdash; an initial
            rise to a peak, then a decline to undetectable &mdash; with the model written
            out in JAGS and checked against the data.
          </p>
          <p class="tutorial-authors">
            Peter F. M. Teunis
          </p>
          <span class="tutorial-link">Open the tutorial <i class="fa-solid fa-arrow-right"></i></span>
        </a>
      </div>
    </div>

    <div class="content mt-5">
      <p class="is-size-7 has-text-grey">
        Have a modelling notebook that uses Shedding Hub data?
        <a href="mailto:sheddinghub@emory.edu?subject=A%20modelling%20tutorial%20for%20Shedding%20Hub&body=What%20it%20demonstrates%3A%0ASoftware%20it%20uses%3A%0AWhere%20it%20lives%20now%3A%0A%0AYour%20name%20and%20institution%3A%0A">Send
        it to us</a> and we will host it here alongside these.
      </p>
    </div>
  </div>
</section>

<style>
/* Curve definitions: the formula sits beside the name, so the three shapes can be
   compared down the column without reading the prose. */
.curve {
  padding: 1.25rem 0;
  border-top: 1px solid var(--border-color);
}

.curve:last-of-type {
  border-bottom: 1px solid var(--border-color);
}

.curve-head {
  display: flex;
  align-items: baseline;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 0.5rem;
}

.curve-head .title {
  margin-bottom: 0;
  min-width: 8rem;
}

.curve-form {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.85rem;
  white-space: nowrap;
}

.curve p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  max-width: 46rem;
}

/* Dashed, like every other not-the-main-path marker on the site. */
.caution {
  margin-top: 2rem;
  padding: 1.25rem 1.5rem;
  border: 1px dashed var(--border-color);
  border-radius: 4px;
  background: var(--bg-secondary);
}

.caution p {
  color: var(--text-secondary);
  font-size: 0.9rem;
  margin: 0;
}

/* Tutorial cards, matching the news cards on the homepage. */
.tutorial-card {
  display: block;
  height: 100%;
  padding: 1.75rem;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-top: 3px solid var(--primary-color);
  border-radius: 4px;
  color: var(--text-primary);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.tutorial-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 0.4rem 1.2rem var(--shadow);
  color: var(--text-primary);
}

.tutorial-tool {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: var(--text-light);
  margin-bottom: 0.4rem;
}

.tutorial-card p:not(.tutorial-tool):not(.tutorial-authors) {
  color: var(--text-secondary);
  font-size: 0.92rem;
}

.tutorial-authors {
  margin-top: 0.9rem;
  font-size: 0.8rem;
  color: var(--text-light);
}

.tutorial-link {
  display: inline-block;
  margin-top: 1rem;
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--primary-color);
}

.tutorial-link i {
  margin-left: 0.35rem;
  transition: transform 0.2s ease;
}

.tutorial-card:hover .tutorial-link i {
  transform: translateX(3px);
}
</style>
