---
toc: false
---
```js
import { version }  from './components/queries.js';

```
<div class="hero">
  <h1>Human Rights in News Articles</h1>
  <h2>${version}</h2>

</div>

<div class="grid grid-cols-1">

<div class="card">





```mermaid
---
title: Data flow
---
graph TD;
  
  pq_database@{ shape: database, label: "ProQuest DB" };
  pq_search@{ shape: rect, label: "Search: 'human rights'" };
  pq_dataset@{ shape: docs, label: "Articles mentioning 'human rights'" };
  pq_dataset_all@{ shape: docs, label: "All articles" };
  ner_notebook@{ shape: subprocess, label: "Named entity recognition", type: "SoftwareSourceCode" };
  collate_notebook@{ shape: subprocess, label: "Collate results" };
  count_notebook@{ shape: subprocess, label: "Count articles" };
  preprocess@{ shape: subprocess, label: "Merge and deduplicate articles" };
  preprocess_counts@{ shape: subprocess, label: "Merge article counts" };
  counts_by_year@{ shape: rect, label: "Article counts CSV" };
  articles_metadata@{ shape: rect, label: "Article metadata CSV" };
  articles_parquet@{ shape: rect, label: "Articles Parquet" };
  entities_json@{ shape: docs, label: "Entities JSON" };
  open_refine@{ shape: subprocess, label: "OpenRefine data cleaning" };
  open_refine_csv@{ shape: docs, label: "Cleaned entities CSV" };
  deduplicate@{ shape: subprocess, label: "Deduplicate entities" };
  entities_csv@{ shape: docs, label: "Cleaned entities CSV" };
  articles_loader@{ shape: subprocess, label: "Articles data loader" };
  entities_loader@{ shape: subprocess, label: "Entities data loader" };
  join_loader@{ shape: subprocess, label: "Junction data loader" };
  articles_frontend@{ shape: rect, label: "Articles" };
  entities_frontend@{ shape: rect, label: "Entities" };
  articles_entities_frontend@{ shape: rect, label: "Articles-Entities" };
  articles_basis@{ shape: rect, label: "Article counts JSON"};
  web@{ shape: doc, label: "This website" }

  subgraph TDM Studio
    pq_database-->pq_search;
    pq_search-->pq_dataset;
    pq_database-->pq_dataset_all;
    pq_dataset-->ner_notebook
    ner_notebook-->collate_notebook;
    ner_notebook-->entities_json;
    pq_search-->articles_metadata;
    pq_dataset_all-->count_notebook;
    count_notebook-->counts_by_year;
  end

  articles_metadata-->articles_loader;
  
  collate_notebook-->preprocess;
  preprocess-->articles_parquet;
  articles_parquet-->articles_loader;
  counts_by_year-->preprocess_counts;
  preprocess_counts-->articles_basis;
  entities_json-->open_refine;
  open_refine-->open_refine_csv;
  open_refine_csv-->deduplicate;
  deduplicate-->entities_csv;


  subgraph Observable Build
    articles_loader-->articles_frontend;
    articles_parquet-->entities_loader; 
    entities_csv-->entities_loader;
    entities_loader-->entities_frontend;
    articles_parquet-->join_loader;
    entities_csv-->join_loader; 
    join_loader-->articles_entities_frontend;
    articles_frontend-->web;
    entities_frontend-->web;
    articles_entities_frontend-->web;
    articles_basis-->web;
  end

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
