let ALL_PROJECTS = null;
let PROJECTS = null;
let TYPES = [];
let EMPLOYEES = [];
let GROUPS = [];


// Enum used in the function addEditEntry
const ENTRY_TYPE = {ADD_EMPLOYEE: 1, REMOVE_EMPLOYEE: 2, TAG: 3, TYPE: 4};


$(function () {

    // Reset modal info span when closing
    $('#editModal').on('hidden.bs.modal', function (e) {
        $("#modal-info").text("");
    });

    setupButtons();
    setupModal();
    saveScrollingPosition();

    // Set the value of the selector to the value in the URL parameters
    $("#amount-selector").val(getProjectsPerPage() === 1000 ? "All" : getProjectsPerPage());

    if ($.urlParam("search")) {
        $("#search_text").val($.urlParam("search"));
        search();
    } else {
        refreshProjectsData(restoreScrollingPosition);
    }

    $.ajax({
        url: "projects-page-additional",
        success: function (result) {
            EMPLOYEES = result["employees"];
            TYPES = result["types"];
            GROUPS = result["groups"];
            init_type_select();
            init_research_select();
            init_employee_filter();
            setModalGroupSelector();
        }
    });

});



/**
 * Refreshes the projects and navigation when the back button is pressed
 */
window.addEventListener('popstate', function (event) {
    refreshProjects();
    refreshNavigation();
    setActiveNavElement(getPage());
    $("#amount-selector").val(getProjectsPerPage() === 1000 ? "All" : getProjectsPerPage());
}, false);


/**
 * This function initializes all buttons, checkboxes and selectors and gives them the correct starting values.
 */
function setupButtons() {
    let editModalButton = $("#editModalButton");
    let selectAllButton = $("#selectAllButton");
    let showDescriptionsButton = $("#showDescriptionsButton");

    editModalButton.click(function () {
        let checkedProjects = getCheckedProjects();

        $("#modal-title").text(checkedProjects.length + (checkedProjects.length === 1 ? " project" : " projects") + " selected");

        let saveChangesButton = $("#saveChangesButton");
        saveChangesButton.off("click");
        saveChangesButton.click(function () {
            sendEditingChanges(checkedProjects);
        });
    });
    selectAllButton.click(function () {
        let allCheckBoxes = $(".custom-control-input");

        // Check if all checkboxes are checked
        let allChecked = true;
        allCheckBoxes.each(function () {
            if (!$(this).is(":checked")) {
                allChecked = false;
            }
        });

        if (allChecked) {
            allCheckBoxes.prop('checked', false);
        } else {
            allCheckBoxes.prop('checked', true);
        }
    });
    showDescriptionsButton.click(function () {
        let allCards = $('[id^="card-collapse"]');
        let allExpanded = true;
        allCards.each(function () {
            if (!$(this).hasClass('show')) {
                allExpanded = false;
            }
        });

        if (allExpanded) {
            allCards.collapse('hide');
        } else {
            allCards.collapse('show');
        }
    });


    if (inEditMode()) {
        editModalButton.show();
        selectAllButton.show();
        setProjectsPerPage(1000);
    } else {
        selectAllButton.hide();
        editModalButton.hide();
    }
}



