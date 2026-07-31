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

<div class="grid grid-cols-3">

<div class="card grid-colspan-3">



```js

const metadata = await FileAttachment("data/merged/article_metadata.csv").csv();

const selected = view(Inputs.table(metadata));

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
