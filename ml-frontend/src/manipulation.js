


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
    }).then(response => response.text()).then(
        data => {
            
            const csvData = data;
            
            const tableHTML = convertToHTML(csvData);
            dropButton.innerHTML = tableHTML;
        }
    ).catch(error => console.log(error))
};

function convertToHTML(csvData){
    const rows = csvData.split("\r\n");
    let htmlTable = '<table>'
    var col = true;
    rows.forEach(row => {
        htmlTable += '<tr>';
        const eles = row.split(",");
        // if (eles.indexOf("\r") !== -1) {
        //     eles = eles.replace("", '');
        // }
        eles.forEach(cell => {
            if(cell != ''){
            htmlTable += '<td>'+cell+'</td>';}
            else if(cell == '' && col){
                cell = 'S.no';
                htmlTable += '<td>'+cell+'</td>';
            }
            else{
                cell = 'null';
                htmlTable += '<td>'+cell+'</td>';
            }
        });
        col = false;
        htmlTable += '</tr>';
    });
    htmlTable += '</table>';
    return htmlTable;
}