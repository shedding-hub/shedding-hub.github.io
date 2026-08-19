---
layout: default
title: Team - Shedding Hub
---
<section class="hero is-light">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <h1 class="title is-size-1 mb-4">Team</h1>
      <p class="subtitle is-size-4">
        The people who build the pipeline, curate the data, and check it against the papers.
      </p>
    </div>
  </div>
</section>

{%- comment -%}
  Sections come from the `group` field in _data/team.yaml, so moving somebody
  between them is a one-word edit rather than moving markup. Current members get
  a full entry; alumni get a compact card, which keeps the page from growing
  without bound as people pass through.
{%- endcomment -%}
{% assign sections = "leadership,staff,student" | split: "," %}
{% assign headings = "Leadership,Staff,Students" | split: "," %}
{% assign blurbs = "Direction and technical vision.,Project management and research support.,Curating datasets and building the analysis." | split: "," %}

{% for section in sections %}
{% assign members = "" | split: "" %}
{% for person_hash in site.data.team %}
  {% if person_hash[1].group == section %}
    {% assign members = members | push: person_hash %}
  {% endif %}
{% endfor %}

{% if members.size > 0 %}
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">{{ headings[forloop.index0] }}</span>
    <h2 class="title is-3 mb-2">{{ headings[forloop.index0] }}</h2>
    <p class="subtitle is-6 mb-5">{{ blurbs[forloop.index0] }}</p>

    {% for person_hash in members %}
    {% assign person = person_hash[1] %}
    <article class="member" id="{{ person_hash[0] }}">
      <figure class="member-photo">
        <img src="/assets/team/{{ person_hash[0] }}.jpg"
             alt="" loading="lazy">
      </figure>
      <div class="member-body">
        <h3 class="title is-5 member-name">{{ person.first }} {{ person.last }}</h3>
        <p class="member-role is-data">
          {{ person.job }}{% if person.institution %} &middot; {{ person.institution }}{% endif %}
        </p>
        <div class="content member-text">
          {{ person.description | markdownify }}
        </div>
        <p class="member-links">
          {% if person.profile %}
          <a href="{{ person.profile }}" target="_blank" rel="noopener">
            <span class="icon"><i class="fa-solid fa-building-columns"></i></span> Profile
          </a>
          {% endif %}
          {% if person.website %}
          <a href="{{ person.website }}" target="_blank" rel="noopener">
            <span class="icon"><i class="fa-solid fa-globe"></i></span> Website
          </a>
          {% endif %}
          {% if person.github %}
          <a href="https://github.com/{{ person.github }}" target="_blank" rel="noopener">
            <span class="icon"><i class="fab fa-github"></i></span> {{ person.github }}
          </a>
          {% endif %}
        </p>
      </div>
    </article>
    {% endfor %}
  </div>
</section>

<hr class="lod-rule">
{% endif %}
{% endfor %}

{%- comment -%} Alumni: compact, so the page stays readable as the list grows. {%- endcomment -%}
{% assign alumni = "" | split: "" %}
{% for person_hash in site.data.team %}
  {% if person_hash[1].group == "alumni" %}
    {% assign alumni = alumni | push: person_hash %}
  {% endif %}
{% endfor %}

{% if alumni.size > 0 %}
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">Alumni</span>
    <h2 class="title is-3 mb-2">Previously on the team</h2>
    <p class="subtitle is-6 mb-5">
      Contributors who have since graduated. The datasets they curated are still here.
    </p>
    <div class="alumni-grid">
      {% for person_hash in alumni %}
      {% assign person = person_hash[1] %}
      <div class="alumnus" id="{{ person_hash[0] }}">
        <img class="alumnus-photo" src="/assets/team/{{ person_hash[0] }}.jpg" alt="" loading="lazy">
        <div>
          <p class="alumnus-name">{{ person.first }} {{ person.last }}</p>
          <p class="alumnus-role is-data">{{ person.job }}</p>
          {% if person.github %}
          <a class="alumnus-link" href="https://github.com/{{ person.github }}" target="_blank" rel="noopener">
            <span class="icon"><i class="fab fa-github"></i></span>{{ person.github }}
          </a>
          {% endif %}
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<hr class="lod-rule">
{% endif %}

<!-- Advisors -->
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">Advisors</span>
    <h2 class="title is-3 mb-2">Scientific advisors</h2>
    <p class="subtitle is-6 mb-5">Guidance on the science the repository has to serve.</p>
    <div class="alumni-grid">
      {% for advisor in site.data.advisors %}
      <div class="alumnus">
        <img class="alumnus-photo" src="/assets/team/{{ advisor.key }}.jpg" alt="" loading="lazy">
        <div>
          <p class="alumnus-name">{{ advisor.name }}</p>
          <p class="alumnus-role is-data">{{ advisor.institution }}</p>
          <a class="alumnus-link" href="{{ advisor.url }}" target="_blank" rel="noopener">
            <span class="icon"><i class="fa-solid fa-building-columns"></i></span>Profile
          </a>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<hr class="lod-rule">

<!-- Join -->
<section class="section">
  <div class="container is-max-desktop">
    <span class="eyebrow">Join us</span>
    <h2 class="title is-3 mb-4">Work on this with us</h2>
    <div class="content">
      <p>
        Students at Emory curate datasets, build the extraction and review agents, and
        check what the agents produce against the source papers. If that sounds like
        your kind of work, get in touch.
      </p>
    </div>
    <a class="button is-primary"
       href="mailto:sheddinghub@emory.edu?subject=Joining%20the%20Shedding%20Hub%20team&body=Programme%20and%20year%3A%0AWhat%20you%20would%20like%20to%20work%20on%3A%0ARelevant%20experience%3A%0A">
      <span class="icon"><i class="fa-solid fa-envelope"></i></span>
      <span>Get in touch</span>
    </a>
  </div>
</section>

<style>
/* Current members: photo beside a full entry. */
.member {
  display: grid;
  grid-template-columns: 8rem 1fr;
  gap: 1.75rem;
  padding: 1.75rem 0;
  border-top: 1px solid var(--border-color);
}

.member:last-of-type {
  border-bottom: 1px solid var(--border-color);
}

.member-photo {
  margin: 0;
}

.member-photo img {
  width: 8rem;
  height: 8rem;
  object-fit: cover;
  border-radius: 50%;
  display: block;
}

.member-name {
  margin-bottom: 0.3rem;
}

.member-role {
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-light);
  margin-bottom: 0.9rem;
}

.member-text p {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.member-links {
  margin-top: 0.9rem;
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
  font-size: 0.85rem;
}

.member-links .icon {
  margin-right: 0.3rem;
}

@media screen and (max-width: 640px) {
  .member {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .member-photo img {
    width: 6rem;
    height: 6rem;
  }
}

/* Alumni and advisors: compact, several to a row. */
.alumni-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(17rem, 1fr));
  gap: 1rem;
}

.alumnus {
  display: flex;
  gap: 1rem;
  align-items: center;
  padding: 1rem;
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 4px;
}

.alumnus-photo {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 50%;
  object-fit: cover;
  flex: none;
}

.alumnus-name {
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.95rem;
  line-height: 1.3;
}

.alumnus-role {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-light);
  margin-top: 0.2rem;
}

.alumnus-link {
  display: inline-block;
  margin-top: 0.4rem;
  font-size: 0.78rem;
}

.alumnus-link .icon {
  margin-right: 0.25rem;
}
</style>
