// Script to handle selection of data from drop-downs for comparing two locations
// Can take preset locations from query parameters:
// /compare?left=location1.id&right=location2.id

document.getElementById("left-location-select").addEventListener("change", updateComparison);
document.getElementById("right-location-select").addEventListener("change", updateComparison);

document.getElementById("left-location-select").addEventListener("change", () => filterLocations('left', 'right'));
document.getElementById("right-location-select").addEventListener("change", () => filterLocations('right', 'left'));

// Check if location IDs are passed as URL parameters and set the selectors
document.addEventListener("DOMContentLoaded", function() {
    const leftLocationId = getUrlParameter('left');
    const rightLocationId = getUrlParameter('right');

    // Only select locations if IDs are passed in URL parameters
    if (leftLocationId) {
        document.getElementById("left-location-select").value = leftLocationId;
    } else {
        document.getElementById("left-location-select").value = "";
    }

    if (rightLocationId) {
        document.getElementById("right-location-select").value = rightLocationId;
    } else {
        document.getElementById("right-location-select").value = "";
    }

    // Filter initial dropdowns to avoid duplicate locations
    filterLocations('left', 'right');
    filterLocations('right', 'left');

    if (leftLocationId && rightLocationId) {
        updateComparison();
    }
});


function formatWithCommas(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function getUrlParameter(name) {
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

function filterLocations(source, target) {
    const sourceSelect = document.getElementById(`${source}-location-select`);
    const targetSelect = document.getElementById(`${target}-location-select`);
    const selectedLocationId = sourceSelect.value;
    const currentTargetSelected = targetSelect.value;

    // Save the current options except the selected one
    let optionsHtml = '<option value="" disabled>Select a location</option>';
    locations_j.forEach(location => {
        if (location.pk.toString() !== selectedLocationId) {
            optionsHtml += `<option value="${location.pk}"${location.pk.toString() === currentTargetSelected ? ' selected' : ''}>${location.fields.name}</option>`;
        }
    });

    // Update the options of the target dropdown
    targetSelect.innerHTML = optionsHtml;
    
    // Ensure that if there is no location selected, the 'Select a location' option remains selected
    if (!currentTargetSelected) {
        targetSelect.value = "";
    }
}
    
function updateComparison() {
    const leftLocationId = document.getElementById("left-location-select").value;
    const rightLocationId = document.getElementById("right-location-select").value;

    const leftLocation = locations_j.find(location => location.pk == leftLocationId);
    const rightLocation = locations_j.find(location => location.pk == rightLocationId);

    const leftComparison = leftLocation.fields.location.comparison;
    const rightComparison = rightLocation.fields.location.comparison;

    const leftTableBody = document.getElementById("left-location-data");
    const rightTableBody = document.getElementById("right-location-data");

    leftTableBody.innerHTML = '';
    rightTableBody.innerHTML = '';

    const years = Object.keys(leftComparison).sort((a, b) => b - a);
    years.forEach(year => {
        leftComparison[year].forEach(entry => {
            const variable = Object.keys(entry)[0];
            let leftRawValue = entry[variable];
            let leftValue = (leftRawValue && variable !== 'date') ? parseFloat(leftRawValue) : leftRawValue;

            const rightEntry = rightComparison[year].find(e => Object.keys(e)[0] == variable);
            let rightRawValue = (rightEntry ? rightEntry[variable] : null);
            let rightValue = (rightRawValue && variable !== 'date') ? parseFloat(rightRawValue) : rightRawValue;

            const leftRow = document.createElement("tr");

            if (variable === 'date') {
                leftRow.style.setProperty("--bs-table-bg", "#C89933");
            }

            const leftVariableCell = document.createElement("td");
            const leftValueCell = document.createElement("td");
            const leftArrowCell = document.createElement("td");

            leftVariableCell.classList.add("text-center")
            leftValueCell.classList.add("text-center")
            leftArrowCell.classList.add("text-center")

            leftVariableCell.textContent = names[variable];


            if (leftValue > rightValue) {
                leftArrowCell.innerHTML = '<span style="color:green">▲</span>';
            } else if (leftValue < rightValue) {
                leftArrowCell.innerHTML = '<span style="color:red">▼</span>';
            }

            leftRow.appendChild(leftVariableCell);
            leftRow.appendChild(leftValueCell);
            leftRow.appendChild(leftArrowCell);
            leftTableBody.appendChild(leftRow);

            if (rightEntry) {
                const rightRow = document.createElement("tr");

                if (variable === 'date') {
                rightRow.style.setProperty("--bs-table-bg", "#C89933");
                }

                const rightArrowCell = document.createElement("td");
                const rightValueCell = document.createElement("td");
                const rightVariableCell = document.createElement("td");

                rightVariableCell.classList.add("text-center")
                rightValueCell.classList.add("text-center")
                rightArrowCell.classList.add("text-center")

                rightVariableCell.textContent = names[variable];

                if (variable === 'date') {
                    leftValueCell.textContent = leftValue;
                    rightValueCell.textContent = rightValue;
                } else {
                    leftValueCell.textContent = (!leftRawValue || isNaN(leftValue)) ? '-' : formatWithCommas(leftValue);
                    if (rightEntry) {
                        rightValueCell.textContent = (!rightRawValue || isNaN(rightValue)) ? '-' : formatWithCommas(rightValue);
                    }
                }

                if (rightValue > leftValue) {
                    rightArrowCell.innerHTML = '<span style="color:green">▲</span>';
                } else if (rightValue < leftValue) {
                    rightArrowCell.innerHTML = '<span style="color:red">▼</span>';
                }

                rightRow.appendChild(rightArrowCell);
                rightRow.appendChild(rightValueCell);
                rightRow.appendChild(rightVariableCell);
                rightTableBody.appendChild(rightRow);
            }
        });
    });
}

updateComparison();