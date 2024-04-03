


document.addEventListener("DOMContentLoaded", () => {
        var dropButton = document.getElementById("drop-column-button");
        var imputeButton = document.getElementById("impute-column-button");
        var dropColDropdown = document.getElementById("drop-column-dropdown");
        var imputeDropDown = document.getElementById("impute-column-dropdown");
        // var csvContainers = document.getElementsByClassName("csv-container");
        // var dropSelectDropDown = document.getElementById("drop-column-select");
        const columnDropDown = document.getElementById("columnDropdown");
        const multiSelectBox = document.getElementById("multiSelectDropdown");
        
        dropButton.addEventListener("click", () => {
            dropColDropdown.style.display = "block";
            var finalizeDrop = document.getElementById("finalize-drop-button");
            finalizeDrop.addEventListener("click", () => {
                var dropedResultantCSV = document.getElementById("drop-csv-res");
                displayCSV(dropedResultantCSV);
            })
            
        });
        multiSelectBox.addEventListener("click" ,() => {
            let column = getColumns();
            column.forEach(col => {
                const listItem = document.createElement("li");
                const label = document.createElement("label");
                const checkbox = document.createElement("input");
                checkbox.type = "checkbox";
                checkbox.value = col;
                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(col));
                listItem.appendChild(label);
                columnDropDown.appendChild(listItem);
            });
            columnDropDown.style.display = "block";

        });
        imputeButton.addEventListener("click", () => {
            imputeDropDown.style.display = "block";
        });
});

// function selectedColumns(column, SelectDropDown, dropDown){
//     SelectDropDown.innerHTML = "";
//     column.forEach(col => {
//         var option = document.createElement("option");
//         option.text = col;
//         option.value = col;
//         SelectDropDown.appendChild(option);
//     });
    
//     console.log(SelectDropDown.innerHTML)
// }
function getColumns(){
    var column = [];
    fetch("http://localhost:8000/get_columns",
    {
        method:"GET"
    }).then(response => response.text()).then(data =>{
        let columns = data.split(",");
        columns.forEach(col => column.push(col));
    });
    return column;
}

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