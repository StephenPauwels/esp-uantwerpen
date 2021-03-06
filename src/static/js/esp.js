/**
 * This function fetches parameters from a url.
 * @param {string} url to be converted
 * @returns {list} parameter list
 */
// https://stackoverflow.com/questions/814613/how-to-read-get-data-from-a-url-using-javascript
function parseURLParams(url) {
    var queryStart = url.indexOf("?") + 1,
        queryEnd = url.indexOf("#") + 1 || url.length + 1,
        query = url.slice(queryStart, queryEnd - 1),
        pairs = query.replace(/\+/g, " ").split("&"),
        parms = {}, i, n, v, nv;

    if (query === url || query === "") return {};

    for (i = 0; i < pairs.length; i++) {
        nv = pairs[i].split("=", 2);
        n = decodeURIComponent(nv[0]);
        v = decodeURIComponent(nv[1]);

        if (!parms.hasOwnProperty(n)) parms[n] = [];
        parms[n].push(nv.length === 2 ? v : null);
    }
    return parms;
}

/**
 * This function fetches url parameters
 * @param {string} name desired parameter
 * @returns {string} decoded parameter
 */
$.urlParam = function (name) {
    const results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results == null) {
       return null;
    }
    return decodeURI(results[1]) || 0;
};


function getURLParams() {
    const queryString = window.location.search;
    return new URLSearchParams(queryString);
}

function setParam(key, value) {
    let params = getURLParams();
    params.set(key, value);
    window.history.replaceState({}, '', `${location.pathname}?${params}`);
}


/**
 * This function extends the jQuery functionality with an easy to use get request (which only requires a url parameter).
 * @returns {json} result items requested
 */
jQuery.extend({
    getValues: function (url) {
        let result = null;
        $.ajax({
            url: url,
            type: 'get',
            dataType: 'json',
            async: false,
            success: function (data) {
                result = data;
            },
            error: function () {
                result = null;
            }
        });
        return result;
    }
});

/**
 * This function extends the jQuery functionality with an easy to use post request (which requires a url parameter and a json data object).
 */
jQuery.extend({
    returnValues: function (url, data) {
        $.ajax({
            url: url,
            type: 'post',
            dataType: 'json',
            data: {data: data},
        });
    }
});

$(document).ready(function ($) {
    $(".clickable-table").click(function () {
        window.location = $(this).find("a").attr("href");
    });

    $("#my-profile").click(function () {
        editProfileModal();
    });

    $("#my-csv").click(function () {
        getCSVModal();
        addCsvYears();
    });

/*    $("#extension-confirmation").click(function () {
        $("#extension-confirmation-modal").modal("toggle");
    })*/
});

/**
 * Populates the notification tab with all the open registrations and projects that need to be extended.
 * @param {string} user The employee user id.
 * @param {string} registration_title The title to be displayed when new registration is detected.
 * @param {string} extension_title The title to be displayed when new registration is detected.
 * @param {string} language Current language
 */
function notifications(user, registration_title, extension_title, language) {
    let data = $.getValues("get-guides-project-info/" + user);
    let notification_count = 0;
    notification_count += get_open_registrations(data, registration_title);
    let badge = document.getElementById("notification-count");
    if (notification_count > 0) {
        badge.innerHTML = "" + notification_count;
    } else if (notification_count === 0) {
        if (language === 'en') {
            document.getElementById("notifications").innerHTML = "No new notifications!";
        } else if (language === 'nl') {
            document.getElementById("notifications").innerHTML = "Geen nieuwe meldingen!";
        }
    }
}

/**
 * Collects and constructs all the open registration notifications.
 * @param {array} data The pending registrations.
 * @param {string} title The title to be displayed when new registration is detected.
 * @return {number} The number of notifications constructed.
 */
function get_open_registrations(data, title) {
    let nr_of_notifications = 0;
    let base = document.getElementById("notifications");
    //Loop all the projects
    for (let i = 0; i < data.length; i++) {
        //Loop all the registrations of that project
        if (data[i]['registrations'].length > 0) {
            for (let j = 0; j < data[i]['registrations'].length; j++) {
                base.appendChild(make_notification_item(title, data[i]['registrations'][j]['name'] + " (" + data[i]['registrations'][j]['type'] + ")",
                    data[i]["title"], "project-page?project_id=" + data[i]['project_id'],
                    "static/images/registration.svg", data[i]['registrations'][j]['date']));
                nr_of_notifications += 1;
            }
        }
    }
    return nr_of_notifications;
}


/**
 * Makes a notification item.
 * @param subject The subject of the notification.
 * @param info The info of the notification.
 * @param project The project the notification is referring to.
 * @param link The link when clicking on the notification.
 * @param image_link The link for the notification image.
 * @param date Date of the notification.
 * @return {HTMLLIElement} List item HTML element.
 */
function make_notification_item(subject, info, project, link, image_link, date) {
    let item = document.createElement("li");
    //Create the table (notification element)
    let table = document.createElement("table");
    item.appendChild(table);
    table.setAttribute("class", "clickable-table");
    //Make link to the related project
    let ref = document.createElement("a");
    ref.setAttribute("href", link);
    table.appendChild(ref);
    //The table exists of only one big row
    let main_row = document.createElement("tr");
    table.appendChild(main_row);
    //That row is divided into 3 columns: 1 for image
    let main_col1 = document.createElement("tb");
    main_row.appendChild(main_col1);
    main_col1.setAttribute("class", "col-3");
    //Create dummy row to place the image in de the center row
    let dummy_row = document.createElement("tr");
    main_col1.appendChild(dummy_row);
    let image_row = document.createElement("tr");
    main_col1.appendChild(image_row);
    //1 row for the text
    let main_col2 = document.createElement("tb");
    main_row.appendChild(main_col2);
    main_col2.setAttribute("class", "col-8");
    ///Subject row
    let content_row1 = document.createElement("tr");
    main_col2.appendChild(content_row1);
    ///Info row
    let content_row2 = document.createElement("tr");
    main_col2.appendChild(content_row2);
    ///Project title row
    let content_row3 = document.createElement("tr");
    main_col2.appendChild(content_row3);

    //1 row for the date
    let main_col3 = document.createElement("tb");
    main_row.appendChild(main_col3);
    main_col3.setAttribute("class", "col-1");
    ///Subject row
    let date_row1 = document.createElement("tr");
    main_col3.appendChild(date_row1);
    date_row1.innerHTML = date['day'] + "/" + date['month'];

    //Create the image for the notification and put it in the table
    let image = document.createElement("img");
    image_row.appendChild(image);
    image.src = image_link;
    image.width = 40;
    image.height = 30;

    //Populate text rows
    content_row1.innerHTML = "<tb><b>" + subject + "</b></tb>";
    content_row2.innerHTML = "<tb>" + info + "</tb>";
    content_row3.innerHTML = "<tb><i>" + project.substring(0, 30) + "...</i></tb>";

    return item;
}

/**
 * This function fetches the html content for editing an employee.
 * @returns {string} html content
 */
function getEditEmployeeHTML(researchGroups) {
    // Add the research groups to the select
    let options = "<option value=\"\">None</option>";
    for (let group of researchGroups) {
        options += `<option value="${group.name}">${group.name}</option>`
    }
    return `
            <div class="row">
                <div class="col">
                    Name
                </div>
                <div class="col">
                    <input id="my-profile-name-input" class="form-control-sm">
                </div>
            </div>
            <div class="row">
                <div class="col">
                    Email
                </div>
                <div class="col">
                    <input id="my-profile-email-input" class="form-control-sm">
                </div>
            </div>
            <div class="row">
                <div class="col">
                    Office
                </div>
                <div class="col">
                    <input id="my-profile-office-input" class="form-control-sm">
                </div>
            </div>
            <div class="row">
                <div class="col">
                    Extra Info
                </div>
                <div class="col">
                    <input id="my-profile-extra-info-input" class="form-control-sm">         
               </div>
            </div>
            <div class="row">
                <div class="col">
                    Research Group
                </div>
                <div class="col">
                    <select style='width: 100%; max-width: 150px;' id="my-profile-research-group-input">
                        ${options}   
                    </select>                
                </div>
            </div>
            <div class="row">
                <div class="col">
                    Title
                </div>
                <div class="col">
                    <select id="my-profile-title-input">
                        <option value="">None</option>
                        <option value="PhD">PhD</option>
                        <option value="Professor">Professor</option>
                    </select>            
               </div>
            </div>
            <div class="row">
                <div class="col">
                    Profile Picture
                </div>
            </div>
            <br>
            <div class="row">
                <div class="col">
                    <img id="profile-pic" width="75" height="75"/>
                </div>
                <div class="col">
                    <br>
                    <button class="btn btn-light" id="profile-pic-random">Random</button>
                </div>
            </div>            
        `;
}

/**
 * This function provides functionality for editing your own profile.
 */
function editProfileModal() {
    let modalBody = $("#my-profile-body");
    $("#my-profile-title").text("Edit my profile");
    $("#my-profile-modal").modal("toggle");
    $("#my-profile-info").text("");


    let spinner = $("#my-profile-loading");
    spinner.show();
    let data = $.getValues("get-edit-profile-data/" + name);
    spinner.hide();

    if (data === null) {
        modalBody.text("Employee name from LDAP not found in database");
        return;
    }
    let employee = data["employee"];
    let researchGroups = data["groups"];

    modalBody.html(getEditEmployeeHTML(researchGroups));

    $("#my-profile-name-input").val(employee["name"]);
    $("#my-profile-email-input").val(employee["email"]);
    $("#my-profile-office-input").val(employee["office"]);
    $("#my-profile-research-group-input").val(employee["research_group"]);
    $("#my-profile-title-input").val(employee["title"] ? employee["title"] : "");
    $("#my-profile-extra-info-input").val(employee["extra_info"]);
    $("#profile-pic").attr("src", employee["picture_location"]);

    let profilePicRandom = $("#profile-pic-random");
    profilePicRandom.off("click");
    profilePicRandom.click(function () {
        $.ajax({
            url: "random-profile-picture",
            success: function (response) {
                employee["picture_location"] = response["location"];
                document.getElementById('profile-pic').src = employee["picture_location"];
            },
            error: function (message) {
                $("#my-profile-info").text("Randomize failed")
            }
        });
    });

    let saveChangesButton = $("#saveChangesMyProfile");
    saveChangesButton.off("click");
    saveChangesButton.click(function () {
        $("#my-profile-info").text("Saving...");
        let data = {};
        data["object"] = "employee";
        data["key"] = employee["e_id"];
        data["is_active"] = employee["is_active"];
        data["name"] = $("#my-profile-name-input").val();
        data["email"] = $("#my-profile-email-input").val();
        data["office"] = $("#my-profile-office-input").val();
        data["research_group"] = $("#my-profile-research-group-input").val();
        data["is_external"] = "FALSE";
        data["picture_location"] = employee["picture_location"];
        data["title"] = $("#my-profile-title-input").val();
        data["extra_info"] = $("#my-profile-extra-info-input").val();
        $.ajax({
            url: "update-profile",
            method: "POST",
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function (message) {
                $("#my-profile-info").text("Successfully saved!");
            },
            error: function (message) {
                $("#my-profile-info").text("Error occurred: " + message["responseJSON"]["message"])
            }
        });
    });

}

/**
 * This function provides functionality for downloading the csv file.
 */
function getCSVModal() {
    let modalBody = $("#my-csv-body");
    $("#my-csv-title").text("Download Report");
    $("#my-csv-modal").modal("toggle");

    modalBody.html(`
            <div class="row">
                <div class="col">
                    Generates a csv file with data for all project registrations on active projects from given academic year.
                </div>
            </div>            
        `);

    let downloadButton = $("#download-csv");
    downloadButton.off("click");
    downloadButton.click(function () {
        let years = $('#yearSelector').val();
        window.location = '/csv-data?years=' + years.join('+');
    });
}

/**
 * This function converts a timestamp into a string
 * @param {integer} stamp timestamp to be converted
 */
function timestampToString(stamp) {
    const date = new Date(stamp * 1000);
    const options = { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' };
    return date.toLocaleDateString("en-US", options);
}

function addCsvYears(){
    let options = document.getElementById("yearSelector");
    let today = new Date();
    for(let i = today.getFullYear(); i >= 2019; i--){
        let option = document.createElement("option");
        let newYear = i + 1;
        let academicYear = i.toString() + "-" + newYear.toString();
        option.innerText = academicYear;
        option.value = academicYear;
        options.appendChild(option);
    }
    $('#yearSelector').selectpicker();
}