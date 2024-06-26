import * as XLSX from "xlsx";

export const CSVDownloader = (
  totalData,
  actualHeaderKey,
  headerToShow,
  fileName
) => {
  let data = totalData || null;
  if (data == null || !data.length) {
    return null;
  }
  let columnDelimiter = ",";
  let lineDelimiter = "\n";
  let keys = headerToShow;
  let result = "";
  result += keys.join(columnDelimiter);
  result += lineDelimiter;
  data.forEach(function (item) {
    let ctr = 0;
    actualHeaderKey.forEach(function (key) {
      if (ctr > 0) result += columnDelimiter;
      if (Array.isArray(item[key])) {
        let arrayItem =
          item[key] && item[key].length > 0
            ? '"' + item[key].join(",") + '"'
            : "-";
        result += arrayItem;
      } else if (typeof item[key] == "string") {
        let strItem = item[key] ? '"' + item[key] + '"' : "-";
        result += strItem ? strItem.replace(/\s{2,}/g, " ") : strItem;
      } else {
        let strItem = item[key] + "";
        result += strItem ? strItem.replace(/,/g, "") : strItem;
      }

      ctr++;
    });
    result += lineDelimiter;
  });

  if (result == null) return;

  var blob = new Blob([result]);
  if (navigator.msSaveBlob) {
    // IE 10+
    navigator.msSaveBlob(blob, exportedFilenmae);
  } else if (navigator.userAgent.match(/iPhone|iPad|iPod/i)) {
    var hiddenElement = window.document.createElement("a");
    hiddenElement.href = "data:text/csv;charset=utf-8," + encodeURI(result);
    hiddenElement.target = "_blank";
    hiddenElement.download = fileName;
    hiddenElement.click();
  } else {
    let link = document.createElement("a");
    if (link.download !== undefined) {
      // Browsers that support HTML5 download attribute
      var url = URL.createObjectURL(blob);
      link.setAttribute("href", url);
      link.setAttribute("download", fileName);
      link.style.visibility = "hidden";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }
};

export const XLSXDownloader = (totalData, headerToShow, fileName) => {
  let data = totalData || null;
  if (data == null || !data.length) {
    return null;
  }

  // Convert list of objects to a 2D array
  const arr = data.map((obj) => Object.values(obj));
  const data_arr = [headerToShow, ...arr];

  // Create a new workbook
  const wb = XLSX.utils.book_new();

  // Add a worksheet to the workbook
  const ws = XLSX.utils.aoa_to_sheet(data_arr);
  // Set bold font for header row
  const headerStyle = { font: { bold: true } };
  // Append worksheet to the workbook
  XLSX.utils.book_append_sheet(wb, ws, "Sheet1");

  // Export the workbook to an XLSX file
  XLSX.writeFile(wb, fileName);
};
