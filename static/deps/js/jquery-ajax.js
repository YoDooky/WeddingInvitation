// Waiting document load
$(document).ready(function () {
    // Get notification by id for ajax notifications
    let successMessage = $("#jq-notification");
    let warningMessage = $("#jq-warning");


    // Event for <Approve> button to show registration form
    $(document).on("click", ".show-approve-invitation", function (e) {
        e.preventDefault();
        // Hide button
        this.style.display = "none";
        // Show register form
        let registerForm = document.getElementById('invitationApproveDivBlock');
        registerForm.style.display = "";
        // // Get href for django controller
        // let indexURL = $(this).attr("href");
        // // Make GET request
        // $.ajax({
        //     type: "GET",
        //     url: indexURL,
        //     data: {
        //         action: 'show_register_form'
        //     },
        //     success: function (data) {
        //         // Add register form via changing content
        //         let invitationDiv = $("#invitationApproveDivBlock");
        //         invitationDiv.html(data.register_container);
        //     },
        //     error: function (data) {
        //         console.log("Cant load register form");
        //     },
        // });
    });


    // Event for <Approve> button to approve registration
    $(document).on("click", ".accept-invitation", function (e) {
        e.preventDefault();
        // Get form HTML data
        let formHTML = document.getElementById("invitationForm")
        // Get usefull data from form
        let formFirstName = "";
        let formLastName = "";
        for (let htmlElement of formHTML.elements) {
            if (htmlElement.id === "first_name_input1") {
                formFirstName = htmlElement.value
            }
            if (htmlElement.id === "last_name_input2") {
                formLastName = htmlElement.value
            }
        }
        // Get href for django controller
        let indexURL = $(this).attr("href");
        // Make post req using ajax without page reload
        $.ajax({
            type: "POST",
            url: indexURL,
            data: {
                action: 'register',
                first_name: formFirstName,
                last_name: formLastName,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Alert or success message
                if (data.alert) {
                    warningMessage.html(data.alert);
                    warningMessage.fadeIn(400);
                    setTimeout(function () {
                        warningMessage.fadeOut(400);
                    }, 7000);
                } else {
                    successMessage.html(data.message);
                    successMessage.fadeIn(400);
                    setTimeout(function () {
                        successMessage.fadeOut(400);
                    }, 7000);
                    // Hide registration form
                    let registerForm = document.getElementById('invitationApproveDivBlock');
                    registerForm.style.display = "none";
                    // Check form radiobuttons (that was selected and saved to db)
                    if (data.questions) {
                        for (let radioButton of data.questions) {
                            let radioButtonElement = document.getElementById(radioButton);
                            radioButtonElement.checked = true;
                        }
                    }
                    // Show survey form
                    let surveyForm = document.getElementById('surveyApproveDivBlock');
                    surveyForm.style.display = "";
                }
            },
            error: function (data) {
                console.log("Error while register user");
            },
        });
    });


    // Event for <Approve> button to approve survey
    $(document).on("click", ".approve-survey", function (e) {
        e.preventDefault();
        // Get form HTML data
        let formHTML = document.getElementById("surveyForm")
        // Get usefull data from form
        let formData = {};
        let dictIndex = 0
        for (let htmlElement of formHTML.elements) {
            if (htmlElement.tagName !== "INPUT") {
                continue
            }
            if (!htmlElement.tagName) {
                continue
            }
            if (htmlElement.tagName === "csrfmiddlewaretoken") {
                continue
            }
            if (!htmlElement.checked) {
                continue
            }
            formData[dictIndex] = htmlElement.id
            dictIndex += 1
        }
        // Get usefull data from registration form
        let registrationFormHTML = document.getElementById("invitationForm")
        let formFirstName = "";
        let formLastName = "";
        for (let htmlElement of registrationFormHTML.elements) {
            if (htmlElement.id === "first_name_input1") {
                formFirstName = htmlElement.value
            }
            if (htmlElement.id === "last_name_input2") {
                formLastName = htmlElement.value
            }
        }
        // Get href for django controller
        let indexURL = $(this).attr("href");
        // Make post req using ajax without page reload
        $.ajax({
            type: "POST",
            url: indexURL,
            data: {
                action: 'survey',
                first_name: formFirstName,
                last_name: formLastName,
                form_data: formData,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                if (data.alert) {
                    warningMessage.html(data.alert);
                    warningMessage.fadeIn(400);
                    setTimeout(function () {
                        warningMessage.fadeOut(400);
                    }, 7000);
                } else {
                    // Success message
                    successMessage.html(data.message);
                    successMessage.fadeIn(400);
                    setTimeout(function () {
                        successMessage.fadeOut(400);
                    }, 7000);
                    // Show survey form
                    let surveyForm = document.getElementById('surveyApproveDivBlock');
                    surveyForm.style.display = "none";
                }
            },
            error: function (data) {
                console.log("Error while sending survey data");
            },
        });
    });
});