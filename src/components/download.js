
import * as d3 from "d3-dsv";

const PROQUEST_URL = "https://www.proquest.com/docview/";

function download(value, name = "untitled", label = "Save") {
  const a = document.createElement("a");
  const b = a.appendChild(document.createElement("button"));
  b.textContent = label;
  a.download = name;

  async function reset() {
    await new Promise(requestAnimationFrame);
    URL.revokeObjectURL(a.href);
    a.removeAttribute("href");
    b.textContent = label;
    b.disabled = false;
  }

  a.onclick = async event => {
    b.disabled = true;
    if (a.href) return reset(); // Already saved.
    b.textContent = "Saving…";
    try {
      const object = await (typeof value === "function" ? value() : value);
      b.textContent = "Download";
      a.href = URL.createObjectURL(object); // eslint-disable-line require-atomic-updates
    } catch (ignore) {
      b.textContent = label;
    }
    if (event.eventPhase) return reset(); // Already downloaded.
    b.disabled = false;
  };

  return a;
}


// This assumes that the data is an array of
//  {
//  	aid: "23948293842"
//  	title: "Article title"
//  	date: "1998-02-01"
//  }

const download_button = (data, filename="data.csv") => {
  // add URLs based on aid
  data.forEach((r) => r.url = `${PROQUEST_URL}${r.aid}`); 
  const downloadData = new Blob([d3.csvFormat(data, ['aid', 'url', 'date', 'title'])], { type: "text/csv" });
  const size = (downloadData.size / 1024).toFixed(0);
  const button = download(
    downloadData,
    filename,
    `Download ${filename} (~${size.toLocaleString("en-US")} KB)`
  );
  return button;
}


export {download_button, PROQUEST_URL}
