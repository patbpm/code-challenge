/* TODO: Flesh this out to connect the form to the API and render results
   in the #address-results div. */
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const addressResults = document.getElementById("address-results");
  const parseType = document.getElementById("parse-type");
  const resultsTable = addressResults.querySelector("tbody");
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const address = document.getElementById("address").value;

    fetch(`/api/parse/?address=${encodeURIComponent(address)}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          // error message
          addressResults.style.display = "block";
          addressResults.innerHTML = `<div class="alert alert-danger">${data.detail}</div>`;
        } else {
          // successful results
          addressResults.style.display = "block";
          parseType.textContent = data.address_type;

          resultsTable.innerHTML = "";

          // Populate table with address components
          for (const [part, tag] of Object.entries(data.address_components)) {
            const row = resultsTable.insertRow();
            const cellPart = row.insertCell(0);
            const cellTag = row.insertCell(1);
            cellPart.textContent = tag;
            cellTag.textContent = part;
          }
        }
      })
      .catch((error) => {
        addressResults.style.display = "block";
        addressResults.innerHTML = `<div class="alert alert-danger">An error occurred: ${error.message}</div>`;
      });
  });
});
