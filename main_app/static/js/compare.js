// Script to handle selection of data from drop-downs for comparing two locations

document.getElementById("left-location-select").addEventListener("change", updateComparison);
document.getElementById("right-location-select").addEventListener("change", updateComparison);

document.getElementById("left-location-select").addEventListener("change", () => filterLocations('left', 'right'));
document.getElementById("right-location-select").addEventListener("change", () => filterLocations('right', 'left'));

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
            const leftValue = parseFloat(entry[variable]);

            const rightEntry = rightComparison[year].find(e => Object.keys(e)[0] == variable);
            const rightValue = parseFloat(rightEntry[variable]);

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
            leftValueCell.textContent = leftValue == 0 ? '-' : leftValue;

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
                rightValueCell.textContent = rightValue == 0 ? '-' : rightValue;

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