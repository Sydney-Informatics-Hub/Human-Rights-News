// See https://observablehq.com/framework/config for documentation.
export default {
  // The app’s title; used in the sidebar and webpage titles.
  title: "Human Rights in News Articles",

  head: '<link rel="icon" href="observable.png" type="image/png" sizes="32x32">',

  // The path to the source root.
  root: "src",

  pages : [
    { name: "Grouped entities", path: "/entities.html"},
    { name: "Heatmap", path: "/heatmap.html"},
    { name: "Inspect articles", path: "/sample.html"},
    { name: "Metadata", path: "/metadata.html"},
    { name: "Counts", path: "/counts.html"},
    { name: "Methods", path: "/methods.html"},
  ]

};
