---
toc: false
sql:
  article: ./data/article.parquet
  entity: ./data/entity.parquet
  article_entity: data/article-entity.parquet
---

```js
import { version, make_articles_query }  from './components/queries.js';
```

<div class="hero">
  <h1>Human Rights in News Articles</h1>
  <h2>${version}</h2>

</div>

```js


const FREQ_CUTOFF = 10;
const missing = await FileAttachment("data/missing.csv").csv();
const ui_preload = await FileAttachment("data/types.json").json();
const date_range = ui_preload["dates"];
const pubs = ui_preload["publications"];


```
<div class="grid grid-cols-3">

<div class="card grid-colspan-1">


```js

const slider_start = view(Inputs.range(date_range,
  {label: "Start", value: date_range[0], step:1}
  ));

const slider_end = view(Inputs.range(date_range,
  {label: "End", value: date_range[1], step:1}
  ));



```
</div>

<div class="card grid-colspan-2">

<p>Total articles in the NRE parquet</p>


</div>
</div>

```js


const year_start = Math.floor(slider_start);
const year_end = Math.floor(slider_end);


```

  <div class="grid grid-colspan-3">

  <div class="card">

```js

const selected = view(Plot.plot({
      title: "Articles",
      y: "Count",
      x: { domain: [ new Date("1923-01-01"), new Date("2023-01-01")]},
      color: { legend: true },
      marks: [
        Plot.lineY(
          missing,
          Plot.binX(
            {y: "count", filter: null},
            {
              x: "date",
              stroke: "db",
              interval: "year",
            } 
          )),
        Plot.ruleY([0])
        ]
      }));        

```
  </div>

</div>




<style>

h1 {
  font-family: sans-serif
}

.hero h2 {
}


</style>
