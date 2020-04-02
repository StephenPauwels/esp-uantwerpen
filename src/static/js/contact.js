/**
 * This function sends an email.
 */
$(window).ready(function () {

    let status = $("#status");

    document.getElementById("send-button").onclick = function () {

        status.text("Sending message...");

        data = {
            "first-name": $("#first-name").val(),
            "last-name": $("#last-name").val(),
            "role": $("#role").val(),
            "message": $("#message").val()
        };

        $.ajax({
            type: "POST",
            url: "mail",
            data: JSON.stringify(data, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {
                status.text("Message sent!");
            },
            error: function (result) {
                status.text("Error occurred!");
            }
        });
    }
});


