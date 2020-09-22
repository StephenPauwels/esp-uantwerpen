
/**
 * This function provides sets group selector html content.
 */
function setModalGroupSelector() {
    $("#edit-group-selector").html(
        `<option value="Don't change">Don't change</option>` +
        GROUPS.map(function (group) {
            return `<option value=${group}>${group}</option>`
        }).join("")
    ).selectpicker("refresh");
}

/**
 * Sets the on click functions for the modal, so that edit entries can be added
 */
function setupModal() {
    // Have to make my own function, the standard JQuery one does not work for dropdowns in a modal
    function toggleDropdown(dropdown) {
        if (dropdown.is(":visible")) {
            dropdown.hide();
        } else {
            dropdown.show();
        }
    }

    // ADD SECTION
    let addMenu = $("#add-selector-menu");
    $("#add-selector").click(() => toggleDropdown(addMenu));

    addMenu.children().click(function () {
        addMenu.hide();
        let entries = $("#add-entries");
        let selectedValue = $(this).text();
        if (selectedValue === "Employee" || selectedValue === "Werknemer") {
            entries.append(createEditEntry(ENTRY_TYPE.ADD_EMPLOYEE));
        } else if (selectedValue === "Type") {
            entries.append(createEditEntry(ENTRY_TYPE.TYPE));
        } else if (selectedValue === "Tag") {
            entries.append(createEditEntry(ENTRY_TYPE.TAG));
        }
    });

    // REMOVE SECTION
    let removeMenu = $("#remove-selector-menu");
    $("#remove-selector").click(() => toggleDropdown(removeMenu));

    removeMenu.children().click(function () {
        removeMenu.hide();
        let entries = $("#remove-entries");
        let selectedValue = $(this).text();
        if (selectedValue === "Employee" || selectedValue === "Werknemer") {
            entries.append(createEditEntry(ENTRY_TYPE.REMOVE_EMPLOYEE));
        } else if (selectedValue === "Type") {
            entries.append(createEditEntry(ENTRY_TYPE.TYPE));
        } else if (selectedValue === "Tag") {
            entries.append(createEditEntry(ENTRY_TYPE.TAG));
        }
    });

    // Close the dropdowns when clicking anywhere
    $(document).click(function () {
        addMenu.hide();
        removeMenu.hide();
    });
}

/**
 * Creates an element to be added in the editing modal
 * @param {ENTRY_TYPE} type the type of the element
 * @returns {*|jQuery|HTMLElement}
 */
function createEditEntry(type) {
    if (type === ENTRY_TYPE.TYPE) {
        return createTypeEditEntry();
    }

    let className;
    let middleColumn;
    let placeholder;

    if (type === ENTRY_TYPE.ADD_EMPLOYEE) {
        className = "employee-entry";
        middleColumn = `
            <select class="form-control">
                <option value="Promotor">Promotor</option>
                <option value="Co-Promotor">Co-Promotor</option>
                <option value="Mentor">Mentor</option>
            </select>`;
        placeholder = "Name";
    } else if (type === ENTRY_TYPE.REMOVE_EMPLOYEE) {
        className = "employee-entry";
        middleColumn = `<span>Employee</span>`;
        placeholder = "Name";
    } else if (type === ENTRY_TYPE.TAG) {
        className = "tag-entry";
        middleColumn = `<span style="color: var(--placeholdercolor)">Tag</span>`;
        placeholder = "Tag";
    }

    let element = `
        <div class="form-row ${className} align-items-center">
            <div class="col-md-6">
                <input type="text" class="form-control" placeholder="${placeholder}">
            </div>
            
            <div class="col-md-4 text-center">
                ${middleColumn}
            </div>
            
            <div class="col-md-2">
                <button class="btn bg-light btn-sm" type="button" onclick="removeEntry(this);">
                    <span style="color: var(--placeholdercolor); font-size: 20px !important;">
                        <b>×</b>
                    </span>
                </button>
            </div>
        </div>`;

    let dom = $(element);

    // Add autocomplete for employees
    if (type === ENTRY_TYPE.ADD_EMPLOYEE || type === ENTRY_TYPE.REMOVE_EMPLOYEE) {
        autocomplete(dom.find("input")[0], EMPLOYEES);
    }

    return dom;
}

/**
 * This function provides html content to change/modify types.
 * @return jQuery element for static html
 */
function createTypeEditEntry() {
    let options = "";
    for (let type of TYPES) {
        options += `<option value="${type}">${type}</option>`;
    }

    let element = `
        <div class="form-row type-entry align-items-center">
            <div class="col-md-6">
                <select class="form-control">
                    ${options}
                </select>
            </div>
            
            <div class="col-md-4 text-center">
                <span style="color: var(--placeholdercolor)">Type</span>
            </div>
            
            <div class="col-md-2">
                <button class="btn bg-light btn-sm" type="button" onclick="removeEntry(this);">
                    <span style="color: var(--placeholdercolor); font-size: 20px !important;">
                        <b>×</b>
                    </span>
                </button>
            </div>
        </div>`;

    return $(element);
}

/**
 * Only used in entries for the editing function (see createEditEntry())
 * @param element the 'remove button'
 */
function removeEntry(element) {
    $(element).parent().parent().remove();
}


/**
 * Only used in entries for the editing function (see createEditEntry())
 * @param {array} projects to be be edited
 */
function sendEditingChanges(projects) {
    let json = {
        projects: projects,
        entries: []
    };


    let addEntries = $("#add-entries").children();
    for (let entry of addEntries) {
        // Convert to JQuery object
        entry = $(entry);

        if (entry.hasClass("employee-entry")) {
            let employee = entry.find("input").val();
            if (!EMPLOYEES.includes(employee)) {
                $("#modal-info").text("Employee " + employee + " does not exist");
                return;
            }
            let guidance = entry.find("select").val();

            json.entries.push({
                entry_type: "add-employee",
                name: employee,
                guidance: guidance
            });
        } else if (entry.hasClass("tag-entry")) {
            let tag = entry.find("input").val();
            json.entries.push({
                entry_type: "add-tag",
                tag: tag
            });
        } else if (entry.hasClass("type-entry")) {
            let type = entry.find("select").val();
            json.entries.push({
                entry_type: "add-type",
                type: type
            });
        }
    }

    let removeEntries = $("#remove-entries").children();
    for (let entry of removeEntries) {
        // Convert to JQuery object
        entry = $(entry);

        if (entry.hasClass("employee-entry")) {
            let employee = entry.find("input").val();
            if (!EMPLOYEES.includes(employee)) {
                $("#modal-info").text("Employee " + employee + " does not exist");
                return;
            }

            json.entries.push({
                entry_type: "remove-employee",
                name: employee,
            });
        } else if (entry.hasClass("tag-entry")) {
            let tag = entry.find("input").val();
            json.entries.push({
                entry_type: "remove-tag",
                tag: tag
            });
        } else if (entry.hasClass("type-entry")) {
            let type = entry.find("select").val();
            json.entries.push({
                entry_type: "remove-type",
                type: type
            });
        }
    }

    let replaceResearchGroup = $("#edit-group-selector").val();
    if (replaceResearchGroup !== "Don't change") {
        json.entries.push({
            entry_type: "replace-group",
            group: replaceResearchGroup
        });
    }

    let activeStatus = $("#active-status-selector").val();
    if (activeStatus !== "Don't change" && activeStatus !== "Verander niet") {
        json.entries.push({
            entry_type: "replace-active",
            active: activeStatus === "Active" || activeStatus === "Actief"
        });
    }

    // Send the data
    $.ajax({
        url: "projects",
        type: "POST",
        data: JSON.stringify(json),
        contentType: 'application/json',
        success: function () {
            $("#modal-info").text("Successfully saved!");
            setLoading(true);
            refreshProjectsData();
        },
        error: function (message) {
            $("#modal-info").text("Error occurred: " + message["responseJSON"]["message"])
        }
    });
}



/**
 * This function checks if the page is being viewed in edit mode.
 * @return {boolean}
 */
function inEditMode() {
    let urlParam = parseURLParams(window.location.href)['edit'];
    if (urlParam) {
        return urlParam[0] === "true";
    } else {
        return false;
    }
}



/**
 * Retrieves the projects with a checked checkbox
 * @returns {Array} of project ID's
 */
function getCheckedProjects() {
    let i = 0;
    let currentCheckbox = $("#checkbox0");
    let checkedProjects = [];

    // Checks if current checkbox exists
    while (currentCheckbox.length) {

        if (currentCheckbox.is(":checked")) {
            checkedProjects.push(getProjectAtCard(i)['project_id']);
        }

        // Go to the next one
        i++;
        currentCheckbox = $(`#checkbox${i}`)
    }

    return checkedProjects;
}

