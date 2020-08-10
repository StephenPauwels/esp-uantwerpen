function restoreFilters() {
    let params = getURLParams();
    if (params.get('available')) {
        $("#full-filter").prop('checked', params.get('available') === 'true');
    }
    if (params.get('liked')) {
        $("#liked-filter").prop('checked', params.get('liked') === 'true');
    }
    if (params.get('employee')) {
        $("#search_promotor").val(params.get('employee'));
    }
}

/**
 * @returns {number} the page, default value 0
 */
function getPage() {
    let urlParam = $.urlParam('page');
    if (urlParam) {
        return parseInt(urlParam[0]);
    } else {
        return 0;
    }
}

/**
 * This function pushes a new page to the browser, based on a new page index.
 * @param {number} number index for the next page
 */
function setPage(number) {
    let projectsPerPage = getProjectsPerPage();
    if (projectsPerPage === 1000) {
        projectsPerPage = "All";
    }
    setParam('page', number);
    setParam('amount', projectsPerPage);
    setParam('edit', inEditMode());
    setParam('search', getSearch());
    // window.history.pushState('Projects', "Projects - ESP", GLOBAL.root + `/projects?page=${number}&amount=${projectsPerPage}&edit=${inEditMode()}&search=${getSearch()}`);
}

/**
 * This function retrieves the search query from the url.
 * @return {string} query
 */
function getSearch() {
    const query = $.urlParam("search");
    if (query) {
        return query;
    } else {
        return "";
    }
}

/**
 * This function pushes a new page to the browser, based on a search query
 * @param {string} query
 */
function setSearch(query) {
    setParam('search', query);
    // window.history.pushState('Projects', "Projects - ESP", GLOBAL.root + `/projects?page=${getPage()}&amount=${getProjectsPerPage()}&edit=${inEditMode()}&search=${query}`);
}

/**
 * @returns {number} projects per page, default value 50
 */
function getProjectsPerPage() {
    let urlParam = parseURLParams(window.location.href)['amount'];
    if (!urlParam) {
        return 50;
    }

    let amount = urlParam[0];
    if (amount === "All") {
        return 1000;
    } else {
        return parseInt(amount);
    }
}

/**
 * This function pushes a new page to the browser, based on a new amount of projects per page
 * @param {number} number the new project count per page
 */
function setProjectsPerPage(number) {
    if (number === 1000) {
        number = "All";
    }
    setParam('amount', number);
    // window.history.pushState('Projects', "Projects - ESP", GLOBAL.root + `/projects?page=${getPage()}&amount=${number}&edit=${inEditMode()}&search=${getSearch()}`);
}

/**
 * This function retrieves the amount of pages.
 * @return {number} page count
 */
function getPages() {
    return Math.ceil(PROJECTS.length / getProjectsPerPage());
}


/**
 * Save scrolling position
 */
function saveScrollingPosition() {
    var pathName = document.location.pathname;
    window.onbeforeunload = function () {
        var scrollPosition = $(document).scrollTop();
        sessionStorage.setItem("scrollPosition_" + pathName, scrollPosition.toString());
    };
}

function restoreScrollingPosition() {
    var pathName = document.location.pathname;
    if (sessionStorage["scrollPosition_" + pathName]) {
        $(document).scrollTop(sessionStorage.getItem("scrollPosition_" + pathName));
    }
}