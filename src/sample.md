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

<div class="grid grid-cols-2">

<div class="card grid-colspan-2">

```js

const ui_preload = await FileAttachment("data/types.json").json();
const date_range = ui_preload["dates"];


const search = view(Inputs.text({ label: "Title search", placeholder: "Search titles..."}));

const slider_start = view(Inputs.range(date_range,
  {label: "Start", value: date_range[0], step:1}
  ));

const slider_end = view(Inputs.range(date_range,
  {label: "End", value: date_range[1], step:1}
  ));



```


```js

const matcher = `%${search}%`;

const articles = await sql`
SELECT
    article.aid as aid,
    article.title as title,
    article.publication as publication,
    article.date as date 
FROM
    article
WHERE title ILIKE ${matcher}
`;


const selected = view(Inputs.table(articles, {
    sort: "date",
    layout: "auto",
    format: {
      aid: (d) => htl.html`<a href="https://www.proquest.com/docview/${d}" target="_blank">${d}</a>`
    },
    required: false
  }));

```

</div>

<div class="card grid-colspan-2">

## Entities

```js

// NOTE: not using an sql` ... ` template because placeholders don't support
// array arguments in duckdb-wasm
// See https://github.com/duckdb/duckdb-wasm/issues/447

const aids = selected.map((d) => `'${d.aid}'`).join(',');

const all_query = `
SELECT
    article.title as title,
    entity.name as entity,
    entity.eid as eid,
    entity.freq as freq
FROM
    article
JOIN article_entity ON (article.aid = article_entity.aid)
JOIN entity ON (entity.eid = article_entity.eid)
WHERE
    article.aid IN (${aids})
ORDER BY freq DESC
`;

if( selected.length > 0 ) {
  display(Inputs.table(await sql([all_query])));
} else {
  display(htl.html`Select one or more articles to see lists of entities detected in those articles`)
}


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
