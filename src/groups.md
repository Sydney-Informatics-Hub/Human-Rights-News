---
toc: false
---

<div class="hero">
  <h1>Human Rights in News Articles</h1>
  <h2>rel 0.2.7</h2>

</div>

<div class="grid">


<div class="card">

```js

const articles = [
  { "date": "1910-01-01", "eid": 1 },
  { "date": "1910-01-01", "eid": 2 },
  { "date": "1910-01-01", "eid": 3 },
  { "date": "1911-01-01", "eid": 2 },
  { "date": "1911-01-01", "eid": 3 },
  { "date": "1911-01-01", "eid": 4 },
  { "date": "1911-01-01", "eid": 5 },
  { "date": "1912-01-01", "eid": 1 },
  { "date": "1912-01-01", "eid": 2 },
  { "date": "1912-01-01", "eid": 3 },
  { "date": "1913-01-01", "eid": 1 },
  { "date": "1913-01-01", "eid": 3 },
  { "date": "1913-01-01", "eid": 4 },
  { "date": "1913-01-01", "eid": 5 },
  { "date": "1913-01-01", "eid": 6 },
  { "date": "1914-01-01", "eid": 2 },
  { "date": "1914-01-01", "eid": 3 },
  { "date": "1914-01-01", "eid": 4 },
  { "date": "1914-01-01", "eid": 3 },
  { "date": "1915-01-01", "eid": 6 },
  { "date": "1915-01-01", "eid": 1 },
  { "date": "1915-01-01", "eid": 2 },
  { "date": "1915-01-01", "eid": 3 },
  { "date": "1915-01-01", "eid": 4 },
  { "date": "1915-01-01", "eid": 4 },
  { "date": "1916-01-01", "eid": 6 },
  { "date": "1916-01-01", "eid": 3 },
  { "date": "1916-01-01", "eid": 4 },
];

const groups = {
  1: "Group A",
  2: "Group A",
  3: "Group A",
  4: "Group C",
  5: "Group C",
  6: "Group C"
}

const counts = {
  1910: 20,
  1911: 21,
  1912: 22,
  1913: 23,
  1914: 24,
  1915: 25,
  1916: 26,
};

  const date_start = "1910-01-01";
  const date_end = "1916-12-31";


  display(Plot.plot({
      title: "Articles",
      y: { label: "count", grid: true },
      x: { domain: [ new Date(date_start), new Date(date_end )] },
      color: { legend: true, type: "categorical" },
      marks: [
        Plot.lineY(
          articles,
          Plot.binX(
            {
              y: (values, extent) => { 
                const yyyy = String(extent.x1.getFullYear());
                console.log(yyyy);
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
              x: "date", stroke: (d) => groups[d.eid],
              interval: "year", tip: true
            } 
            
          )),
          Plot.ruleY([0])
        ]
      }
    ));


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
