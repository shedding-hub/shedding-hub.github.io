---
layout: default
title: Team - Shedding Hub
---
<section class="hero is-light">
  <div class="hero-body">
    <div class="container is-max-desktop">
      <h1 class="title is-size-1 mb-4">Team</h1>
      <p class="subtitle is-size-4">
        Meet the researchers and contributors behind the Shedding Hub platform.
      </p>
    </div>
  </div>
</section>

<section class="section">
  <div class="container is-max-desktop content">
    {% for person_hash in site.data.team %}
    {% assign person = person_hash[1] %}
    <div class="box">
      <div class="media">
        <div class="media-left">
          <figure class="image is-128x128">
            <img class="is-rounded" src="/assets/team/{{person_hash[0]}}.jpg"
              alt="Photo of {{person.first}} {{person.last}}" />
          </figure>
        </div>
        <div class="media-content">
          <p id="{{person_hash[0]}}" class="title is-4">{{person.first}} {{person.last}}</p>
          <p class="subtitle is-6">
          <ul style="list-style: none; margin: 0; padding: 0;">
            {% if person.job %}
            <li>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-briefcase"></i>
                </span>
                <span>{{person.job}}</span>
              </span>
            </li>
            {% endif %}
            {% if person.institution %}
            <li>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-building-columns"></i>
                </span>
                <span>{{person.institution}}</span>
              </span>
            </li>
            {% endif %}
            {% if person.website %}
            <li>
              <span class="icon-text">
                <span class="icon">
                  <i class="fa-solid fa-globe"></i>
                </span>
                <span><a href="{{person.website}}">{{person.website}}</a></span>
              </span>
            </li>
            {% endif %}
            {% if person.github %}
            <li>
              <span class="icon-text">
                <span class="icon">
                  <i class="fab fa-github"></i>
                </span>
                <span><a href="https://github.com/{{person.github}}">@{{person.github}}</a></span>
              </span>
            </li>
            {% endif %}
          </ul>
          </p>
          <p>{{person.description | markdownify}}</p>
        </div>
      </div>
    </div>
    {% endfor %}
  </div>
</section>
