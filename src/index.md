---
toc: false
sql:
  article: ./data/article.parquet
  entity: ./data/entity.parquet
  article_entity: data/article-entity.parquet
---
```js
import { version, make_articles_query }  from './components/queries.js';
import { download_button, PROQUEST_URL } from './components/download.js';

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

<div class="card grid-colspan-1">


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


const z_option_ctrl = Inputs.select(["publication", "entity"], {
  multiple: false,
  label: "Colour by"
});

const z_option = view(z_option_ctrl);


function set_z_option(value) {
  // this is so that it can be switched back to publications when there are
  // no entities selected
  z_option_ctrl.value = value;
  z_option_ctrl.dispatchEvent(new Event("input"));
};


const normalise = view(Inputs.select(new Map([
  [ "% of all articles", "all" ],
  [ "% of human rights articles", "human_rights" ],
  [ "Raw article counts", "raw"]
  ]), {
  multiple: false,
  label: "y axis"
}));


```



```js

if( pick_entities.length < 1 ) {
  if( z_option === "entity" ) {
    display(htl.html`<p><b>Note</b>: select one or more entities</p>`);
  } else {
    if( normalise === "human_rights" ) {
      display(htl.html`<p><b>Note</b>: when normalised to articles containing 'human rights', all values will be 100% until an entity is selected</p>`);
    } else {
      display(htl.html`<p></p>`);
    } 
  }
}

```

</div>

<div class="card grid-colspan-1">

<h3>Geo entities</h3>

```js

const geo_search = view(Inputs.text({placeholder: "Search entities"}))

```


```js

const geo_entities = await sql([`SELECT
    eid, type, name, freq 
FROM
    entity
WHERE
    freq > ${FREQ_CUTOFF} 
    AND (name != 'xhtml1' AND name LIKE '%${geo_search}%')
    and type = 'geo'
ORDER BY freq DESC
`]);


const geo_pick = view(Inputs.table(geo_entities, { 
  columns: [ "name", "freq" ],
  required: false,
  multiple: true,
}));

```
</div>

<div class="card grid-colspan-1">

<h3>Org entities</h3>

```js

const org_search = view(Inputs.text({placeholder: "Search entities"}))

```

```js

const org_entities = await sql([`SELECT
    eid, type, name, freq 
FROM
    entity
WHERE
    freq > ${FREQ_CUTOFF} 
    AND ( name != 'xhtml1' and name LIKE '%${org_search}%' )
    AND type = 'org' 
ORDER BY freq DESC
`]);


const org_pick = view(Inputs.table(org_entities, { 
  columns: [ "name", "freq" ],
  required: false,
  multiple: true,
}));


```

</div>
</div>

```js


const pick_entities = [...geo_pick, ...org_pick];

// if( pick_entities.length < 1 ) {
//   set_z_option("publication");
// }

const date_start = `${Math.floor(slider_start)}-01-01`;
const date_end = `${Math.floor(slider_end)}-12-31`;

const articles_query = make_articles_query(
   date_start, date_end, pick_pubs, pick_entities
);

const articles = await sql([articles_query]);


const make_y_label = () => {
  if( normalise === "raw") {
    return { label: "article count", grid: true};
  } else {
    return { label: "percent",
//      tickFormat: ".3f",
      grid: true };
  }
};


```

```js

const normalise_binned = (values, extent) => { 
  const yyyy = String(extent.x1.getFullYear());
  const basis = z_option === 'publication' ? extent.z : 'total';
  if( normalise === "raw" ) {
    return values.length;
  } else {
    const counts = article_counts[basis];
    if( counts ) {
      const all_articles = counts[yyyy][normalise];
      if( all_articles > 0 ) {
        return 100 * values.length / all_articles;
      } else {
        return null;
      }
    } else {
      return  null;
    }
  }
}

```


  <div class="card grid-colspan-3">


```js

// the datum for the tips is an array with all of the articles for
// that mark

const no_graph = pick_entities.length < 1 && z_option === "entity";

const selected = no_graph ? [] : view(Plot.plot({
      title: "Articles",
      width: 1000,
      marginLeft: 45,
      y: make_y_label(),
      x: { domain: [ new Date(date_start), new Date(date_end )]},
      color: { legend: true },
      marks: [
        Plot.lineY(
          articles,
          Plot.binX(
            {y: normalise_binned, filter: null},
            {
              x: "date",
              stroke: z_option,
              interval: "year",
            } 
          )),
        Plot.dot(
          articles,
          Plot.pointer(
          Plot.binX(
            {y: normalise_binned, filter: null},
            {
              x: "date",
              stroke: z_option,
              fill: "red",
              interval: "year",
              channels: {
                articles: {
                  value: (d) => d.length,
                  label: "article count",
                },
                date: (d) => {
                  const y = d.map((a) => a.date );
                  return (new Date(y[0])).getFullYear().toString();
                },
              },
              tip: {
                fontSize: 14,
              }
            }
          ))),
        Plot.ruleY([0])
        ]
      }));

```
  </div>





```js

  const nice_dates = d3.utcFormat("%Y-%m-%d");

  const selected_nice = selected ? selected.map((r) => {
  	return {
		aid: r.aid,
		date: nice_dates(new Date(r.date)),
		title: r.title
	};
  }) : articles ;

  const dl_button = selected ? download_button(selected_nice, "articles.csv") : "";

```

<div class="grid grid-colspan-3">

```js


  display(Inputs.table(selected_nice, {
    sort: "date",
    columns: [ "aid", "date", "title" ],
    format: {
      aid: (d) => htl.html`<a href="${PROQUEST_URL}${d}" target="_blank">PQ</a>`,
    },
    width: {
      aid: 20,
      date: 80,
      title: 500
    },
    rows: 10
  }));


```
  ${dl_button}


  </div>

</div>




<style>

h1 {
  font-family: sans-serif
}

.hero h2 {
}


</style>
