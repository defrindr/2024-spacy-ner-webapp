"use strict";

/**
 * @author Defri Indra Mahardika
 * @since 2024
 * Converter CSV to Table HTML
 */
class Csv2Table {
  _elementId = null;
  _source = null;
  _withHeader = true;
  _tableClass = "table table-hover table-striped";
  _containerClass = "table-responsive";

  /**
   * Constructor of class
   * Parameter id is container for table (html id attribute)
   * @param {any} params {
      id,
      source = '',
      withHeader = true,
      tableClass = "table table-hover table-striped",
      containerClass = "table-responsive"
    }
   */
  constructor(params) {
    if (params.id === undefined) throw new Error("Parameter id is required");
    if (params.source === undefined)
      throw new Error("Parameter source is required");

    if (params.withHeader !== undefined) {
      this._withHeader = params.withHeader;
    }

    if (params.tableClass !== undefined) {
      this._tableClass = params.tableClass;
    }

    if (params.containerClass !== undefined) {
      this.__containerClass = params.containerClass;
    }

    this._elementId = document.getElementById(params.id);
    this._source = params.source;

    // build table if source not empty
    if (params.source !== "") {
      this._build();
    }
  }

  /**
   * Update source instance
   * @param {any} params {source}
   */
  update(params) {
    if (params.source !== "") {
      this._source = params.source;
      this._build();
    }
  }

  /**
   * Fetch and build HTML Element
   */
  _build() {
    // Clean HTML Element
    this._elementId.innerHTML = "";

    this._fetchSource()
      .then((papa) => {
        this._elementId.innerHTML = this._makeHtml(papa.data);
      })
      .catch((err) => console.error(err));
  }

  /**
   * Fetch and parse CSV
   * @returns
   */
  _fetchSource() {
    const promiseFetch = new Promise((resolve, reject) => {
      fetch(this._source)
        .then((response) => response.text())
        .then((v) => resolve(Papa.parse(v)))
        .catch((err) => reject(err));
    });

    return promiseFetch;
  }

  /**
   * Generate HTML Element
   * @param {*} sources 
   * @returns string of html element
   */
  _makeHtml(sources) {
    let header = "";
    if (this._withHeader) {
      let titles = sources.shift();

      let ths = [];

      for (let titleIndex = 0; titleIndex < titles.length; titleIndex++) {
        ths.push(`<th>${titles[titleIndex]}</th>`);
      }

      header = `<thead>${ths.join("")}</thead>`;
    }

    let body = "";
    let rows = [];

    for (let rowIndex = 0; rowIndex < sources.length; rowIndex++) {
      let columns = [];
      let source = sources[rowIndex];

      for (let columnIndex = 0; columnIndex < source.length; columnIndex++) {
        let contentTd = source[columnIndex];
        if (contentTd.length > 250)
          contentTd = contentTd.substring(0, 250) + "...";
        columns.push(`<td>${contentTd}</td>`);
      }

      rows.push(`<tr>${columns.join("")}</tr>`);
    }

    body = `<tbody>${rows.join("")}</tbody>`;

    let table = `<table class="${this._tableClass}">${header}${body}</table>`;

    return `<div class="${this._containerClass}">${table}</div>`;
  }
}
