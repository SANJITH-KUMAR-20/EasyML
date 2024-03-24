document.addEventListener("DOMContentLoaded", function() {
    // Get elements
    var startButton = document.getElementById("start-button");
    var uploadContainer = document.getElementById("upload-container");
    var startContent = document.getElementById("para1");
    var introContent = document.getElementsByClassName("header");
    var fileInput = document.getElementById("file-input");
    var uploadButton = document.getElementById("upload-button");

    // Add event listener for start button click
    startButton.addEventListener("click", function() {
        startButton.style.display = "none";
        uploadContainer.style.display = "block";
        startContent.style.display = "block";
    });

    // Add event listener for upload button click
    uploadButton.addEventListener("click", function() {
        var file = fileInput.files[0];
        if (file) {
            if (file.name.endsWith('.csv')) {
                var formData = new FormData();
                formData.append("file", file);

                fetch("http://localhost:8000/upload_csv", {
                    method: "POST",
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error("Failed to upload CSV file.");
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data.message); // Success message from backend
                    // Add code for further actions after successful upload
                })
                .catch(error => {
                    console.error("Error:", error);
                });
            } else {
                alert("Please select a CSV file.");
            }
        } else {
            alert("Please select a file.");
        }
    });
});
