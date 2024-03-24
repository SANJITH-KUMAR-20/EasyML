


document.addEventListener("DOMContentLoaded", () => {
        var dropButton = document.getElementById("drop-column-button");
        var imputeButton = document.getElementById("impute-column-button");
        var dropColDropdown = document.getElementById("drop-column-dropdown");
        var imputeDropDown = document.getElementById("impute-column-dropdown");
        var csvContainers = document.getElementsByClassName("csv-container");
        
        dropButton.addEventListener("click", () => {
            dropColDropdown.style.display = "block";
            var finalizeDrop = document.getElementById("finalize-drop-button");
            finalizeDrop.addEventListener("click", () => {
                var dropedResultantCSV = document.getElementById("drop-csv-res");
                displayCSV(dropedResultantCSV);
            })
            
        });
        imputeButton.addEventListener("click", () => {
            imputeDropDown.style.display = "block";
        });
});

function displayCSV(dropButton){

    fetch("http://localhost:8000/get_csv",
    {
        method : "GET"
    }).then(response => response.json()).then(
        data => {
            console.log(data)
            const csvData = JSON.parse(data);
            console.log(csvData)
            const tableHTML = "<table>" +
                    csvData.map(row => {
                        return "<tr>" +
                            row.map(cell => {
                                return "<td>" + cell + "</td>";
                            }).join("") +
                            "</tr>";
                    }).join("") +
                    "</table>";
            console.log(tableHTML)
            dropedResultantCSV.innerHTML = tableHTML;
        }
    ).catch(error => console.log(error))
};