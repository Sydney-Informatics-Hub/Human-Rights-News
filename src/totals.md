---
toc: false
sql:
  article: ./data/article.parquet
  entity: ./data/entity.parquet
  article_entity: data/article-entity.parquet
---
```js

import { version }  from './components/queries.js';

```
<div class="hero">
  <h1>Human Rights in News Articles</h1>
  <h2>${version}</h2>

</div>

```js

import { make_articles_query }  from './components/queries.js';

const FREQ_CUTOFF = 10;
const tabular_counts = await FileAttachment("data/table_counts.json").json();
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

const pick_pub = view(Inputs.select(pubs, { 
  label: "Newspaper",
  format: (d) => d.name,
  multiple: false
}));


```
</div>

<div class="card grid-colspan-2">

<p>This visualisation shows a breakdown of the total article counts used to normalise the visualisations on the front page. The main visualisation is normalised against the count of articles with the type 'Articles - All Types'.</p>


</div>
</div>

```js


const year_start = Math.floor(slider_start);
const year_end = Math.floor(slider_end);


```

  <div class="grid grid-colspan-3">

  <div class="card">

```js

  display(Inputs.table(tabular_counts));

  // display(Plot.plot({
  //     title: "Totals",
  //     y: { label: "count",  grid: true },
  //     x: { domain: [ year_start, year_end ]},
  //     color: { legend: true },
  //     clip: true,
  //     marks: [
  //       Plot.lineY(
  //         tabular_counts[pick_pub.name],
  //         {
  //           x: "year", y: "count", stroke: "article_type", tip: true
  //         } 
  //         ),
  //       Plot.ruleY([0])
  //       ]
  //   }));

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
