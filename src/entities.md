---
toc: false
sql:
  article: ./data/article.parquet
  entity: ./data/entity.parquet
  article_entity: data/article-entity.parquet
---
```js

import { version, make_articles_query }  from './components/queries.js';

const FREQ_CUTOFF = 10;
const ui_preload = await FileAttachment("data/types.json").json();
const date_range = ui_preload["dates"];
const pubs = ui_preload["publications"];
const article_counts = await FileAttachment("data/counts.json").json();
```
<div class="hero">
  <h1>Human Rights in News Articles</h1>
  <h2>${version}</h2>

</div>

<div class="grid grid-cols-3">

<div class="card grid-colspan-2">


```js

const slider_start = view(Inputs.range(date_range,
  {label: "Start", value: date_range[0], step:1}
  ));

const slider_end = view(Inputs.range(date_range,
  {label: "End", value: date_range[1], step:1}
  ));

const pick_pubs = view(Inputs.select(pubs, { 
  label: "Newspaper",
  format: (d) => d.name,
  multiple: true,
  value: pubs.slice(0,10)
}));

display(html`<br/>`);

const ent_search = view(Inputs.text({ placeholder: "Search for entities..."}));

```

```js
const ent_match = `%${ent_search}%`;
const entities = await sql([`SELECT
    eid, type, name, freq 
FROM
    entity
WHERE
    freq > ${FREQ_CUTOFF}
    AND name != 'xhtml1'
    AND name ILIKE '${ent_match}'
ORDER BY freq DESC
`]);

const entity_set = view(Inputs.table(entities, {
   columns: [ "name", "freq" ],
   required: false,
}));

```

</div>



<div class="card">

```js

// The Mutable and set_eids / set_label function are so that groups can 
// be updated when the user clicks the "add" / "remove" buttons, not whenever
// the input views update reactively. 

const groups = Mutable({});

const current_eids = Mutable([]);
const current_label = Mutable("");

const add_group = ( ) => {
  const l = current_label.value;
  if( l !== '' && current_eids.value.length > 0 ) {
    groups.value[l] = current_eids.value;
  }
};

const remove_group = ( ) => {
  const labels = Object.keys(groups.value);
  console.log(labels);
  console.log(groups.value);
  if( labels.length > 0 ) {
    console.log(`Removing group ${labels[0]}`);
    delete(groups.value[labels[0]]);
  }
}

const clear_groups = () => {
  groups.value = {};
}

const set_eids = ( eids ) => { current_eids.value = eids };

const set_label = ( label ) => { current_label.value = label; };

```


```js
const label = view(Inputs.text({placeholder: "Enter a label...", label: 'Group'}));
const trigger_add = view(Inputs.button('Add selected'));
const trigger_remove = view(Inputs.button('Remove'));
const trigger_clear = view(Inputs.button('Clear all'));
```

<ul>

```js
const trig1 = trigger_add + trigger_clear + trigger_remove;

if( Object.keys(groups).length > 0 ) {
  Object.keys(groups).forEach((label) => {
    const elist = groups[label].map((e) => html`<li>${e.name}</li>`);
    display(html`<li><b>${label}</b><ul>${elist}</ul></li>`);
  });
} else {
    display(html`<p>Select entities from the list and add them to a group</p>`);
}


```

</ul>

```js
trigger_add;
add_group();
```


```js
trigger_remove;
remove_group();
```

```js
trigger_clear;
clear_groups();
```

```js
set_eids(entity_set);
set_label(label);


```




</div>


</div>

```js
const trig2 = trigger_add + trigger_remove + trigger_clear;

const date_start = `${Math.floor(slider_start)}-01-01`;
const date_end = `${Math.floor(slider_end)}-12-31`;

const all_entities = [].concat(...Object.values(groups));

const query = make_articles_query(
  date_start, date_end, pick_pubs, all_entities
);

const articles = await sql([query]);


articles;

```


</div>


  <div class="grid grid-cols-2">

  <div class="card">

```js

  articles;

  const ent_groups = {};

  Object.keys(groups).forEach((l) => {
    groups[l].forEach((e) => ent_groups[e.eid] = l)
  });

  display(Plot.plot({
      title: "Articles",
      y: { label: "count", tickFormat: ".0p", grid: true },
      x: { domain: [ new Date(date_start), new Date(date_end )]},
      color: {
        type: "categorical",
        legend: true,
      },
      marks: [
        Plot.lineY(
          articles,
          Plot.binX(
            {
              y: (values, extent) => { 
                const yyyy = String(extent.x1.getFullYear());
                const basis = 'total';
                const counts = article_counts[basis];
                if( counts ) {
                  const all_articles = counts[yyyy];
                  if( all_articles > 0 ) {
                    return values.length / all_articles;
                  } else {
                    return null;
                  }
                } else {
                  return  null;
                }
              },
              filter: null,
            },
            {
              x: "date", stroke: (d) => ent_groups[d.eid],
              group: "year", tip: true
            }
          )
        ),
        Plot.ruleY([0])
      ]
    }))





```
  </div>

  <div class="card">

```js
  display(Inputs.table(articles, {
    sort: "date",
    format: {
      aid: (d) => htl.html`<a href="https://www.proquest.com/docview/${d}" target="_blank">${d}</a>`
    }
  }))
  
// } else {
//   display(html`  `);
// }
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
