document.addEventListener("DOMContentLoaded", () => {
    var dropColDropdown = document.getElementById("drop-column-dropdown");
    var dropSelectDropDown = document.getElementById("drop-column-select");
    // dropSelectDropDown.addEventListener("" ,() => {
        let column = getColumns();
        column.forEach(col => {
            var option = document.createElement("option");
            option.text = col;
            dropSelectDropDown.appendChild(option);
        });
        dropSelectDropDown.style.display = "block";

    // });

});

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