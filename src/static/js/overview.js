
$(document).ready(function ($) {
    let generateButton = $("#generate");
    generateButton.off("click");
    generateButton.click(function () {
        let year = $('#yearOverview').val();
        window.location = '/overview?year=' + year;
    });

    addOverviewYears();
});

function addOverviewYears(){
    let options = document.getElementById("yearOverview");
    let today = new Date();
    for(let i = 2019; i<=today.getFullYear(); i++){
        let option = document.createElement("option");
        let newYear = i + 1;
        let academicYear = i.toString() + "-" + newYear.toString();
        option.innerText = academicYear;
        option.value = academicYear;
        options.appendChild(option);
    }
    $('#yearOverview').selectpicker();
}

