const version = 'rel 0.2.11';


function make_articles_query (date_start, date_end, pubs, entities) {

  const pubs_sql = pubs.map((d) => `'${d.name}'`).join(",");
  const entities_sql = entities.map((d) => `'${d.eid}'`).join(",")

  if( entities.length < 1 || entities.map((d) => d.name).includes("all") ) {
    return `SELECT
        article.aid as aid,
        article.title as title,
        article.publication as publication,
        article.date as date,
    FROM
        article
    WHERE
        date >= TIMESTAMP '${date_start}'
        AND date <= TIMESTAMP '${date_end}'
        AND publication in (${pubs_sql})
    `;

  } else {
    return `SELECT
        article.aid as aid,
        article.title as title,
        article.publication as publication,
        article.date as date,
        entity.eid as eid,
        entity.name as entity
    FROM
        article
    JOIN article_entity ON (article.aid = article_entity.aid)
    JOIN entity ON (entity.eid = article_entity.eid)
    WHERE
        date >= TIMESTAMP '${date_start}'
        AND date <= TIMESTAMP '${date_end}'
        AND publication in (${pubs_sql})
        AND entity.eid in (${entities_sql}) 
    `;
  }
}


export { version, make_articles_query }

