---
toc: false
sql:
  article: ./data/article.parquet
  entity: ./data/entity.parquet
  article_entity: data/article-entity.parquet
---

```js
import { version }  from './components/queries.js';

const article_counts = await FileAttachment("data/counts.json").json();


```
<div class="hero">
  <h1>Human Rights in News Articles</h1>
  <h2>${version}</h2>

</div>

<div class="grid grid-cols-3">

<div class="card grid-colspan-2">


```js

const entities = await sql([`

  SELECT
    entity.eid as eid,
    any_value(entity.name) as entity_name,
    count(article) as articles,
    date_part('year', article.date) as year,
    article.publication as publication
    FROM
        article
    JOIN article_entity ON (article.aid = article_entity.aid)
    JOIN entity ON (entity.eid = article_entity.eid)
    GROUP BY publication, year, entity.eid
    ORDER BY year, articles DESC
    `
]);

const e_array = [...entities].filter((d) => d.articles > 100);

display(e_array);

// const totals = {};

// e_array.forEach((e) => {
//   if( e.entity_name in totals ) {
//     totals[e.entity_name] += e.articles;    
//   } else {
//     totals[e.entity_name] = 0;    
//   }
// });


```

</div>



<div class="card">



</div>


</div>



</div>



  <div class="card">

```js

// try sorting them by centroid



display(Plot.plot({
  margin: 100,
  width: 1000,
  x: {
    axis: "both",
    tickRotate: 90,
    grid: true,
    tickFormat: (d) => `${d}`
  },
  y: {
    axis: "both",
    tickRotate: -30,
    grid: true
  },
  color: { scheme: "YlGnBu", legend: true},
  marks: [
    Plot.cell(
      e_array,
      {
        x: "year",
        y: "entity_name",
        fx: "publication",
        channels: {
          articles: (d) => d.articles,
          counts: (d) => article_counts[d.publication][d.year],
          normalised: (d) => 100 * d.articles / article_counts[d.publication][d.year],
        },
        fill: (d) => 100 * d.articles / article_counts[d.publication][d.year],
        tip: true,
        sort: {
          y: "articles", reduce: "sum", order: "descending"
        }
      })
  ]
}));



  // display(Plot.plot({
  //     title: "Articles",
  //     y: { label: "count", grid: true },
  //     color: {
  //       type: "categorical",
  //       legend: true,
  //     },
  //     marks: [
  //       Plot.line(
  //         entities,
  //         {
  //           x: "year", y: "hits", stroke: "entity_name", tip: true
  //         }
  //       )
  //     ]
  //   }));




```



  </div>

<style>

h1 {
  font-family: sans-serif
}

.hero h2 {
}


</style>
