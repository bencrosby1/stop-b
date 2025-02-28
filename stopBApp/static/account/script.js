document.addEventListener("DOMContentLoaded", function () {
    const inputs = document.querySelectorAll(".input-container input");
    const saveBtn = document.getElementById("save-btn");
    const deleteAccountBtn = document.getElementById("delete-account-btn");
    const deleteModal = document.getElementById("delete-modal");
    const closeDeleteModalBtn = document.getElementById("close-delete-modal");
    const passwordModal = document.getElementById("password-modal");
    const closePasswordModalBtn = document.getElementById("close-modal");

    inputs.forEach(input => {
        input.dataset.originalValue = input.value;
    });

    // Function to enable editing for fields
    window.enableEdit = function (fieldId) {
        let input = document.getElementById(fieldId);
        input.removeAttribute("readonly");
        input.style.backgroundColor = "#ffffff"; // Make it white when editable
        input.style.cursor = "text";
        saveBtn.style.display = "block";
    };

    // Ensure modals do NOT open automatically
    passwordModal.style.display = "none";
    deleteModal.style.display = "none";

    // Open Password Modal
    document.getElementById("password-group").addEventListener("click", function(event) {
        event.preventDefault();
        passwordModal.style.display = "flex";
    });

    // Close Password Modal
    closePasswordModalBtn.addEventListener("click", function() {
        passwordModal.style.display = "none";
    });

    // Open Delete Account Modal
    deleteAccountBtn.addEventListener("click", function(event) {
        event.preventDefault();
        deleteModal.style.display = "flex";
    });

    // Close Delete Account Modal
    closeDeleteModalBtn.addEventListener("click", function() {
        deleteModal.style.display = "none";
    });

    window.addEventListener("click", function(event) {
        if (event.target === deleteModal) {
            deleteModal.style.display = "none";
        }
        if (event.target === passwordModal) {
            passwordModal.style.display = "none";
        }
    });
});
