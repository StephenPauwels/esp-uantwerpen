/**
 * This function serves as a cookie handler
 */
window.addEventListener("load", function () {
        window.cookieconsent.initialise({
        "palette": {
            "popup": {
                "background": "#edeff5",
                "text": "#838391"
            },
            "button": {
                "background": "transparent",
                "text": "#4b81e8",
                "border": "#4b81e8"
            }
        },
        "type": "opt-in",
        "content": {
            "message": text_notification,
            "allow": text_allow,
            "deny": text_deny
        },
        onInitialise: function (status) {
            var type = this.options.type;
            var didConsent = this.hasConsented();
            if (type === 'opt-in' && didConsent) {
                // enable cookies
                if (getCookie("sessionAction") !== "active") {
                    $.ajax({
                        url: "/new_session",
                        success: function (result) {
                            if (result !== "false"){
                                document.cookie = "sessionAction=active";
                                document.cookie = "session_id="+result;
                            }

                        }
                    });
                    //alert(document.cookie);
                }
            }
            if (type === 'opt-out' && !didConsent) {
                // disable cookies
            }
        },

        onStatusChange: function (status, chosenBefore) {
            var type = this.options.type;
            var didConsent = this.hasConsented();
            if (type === 'opt-in' && didConsent && getCookie("sessionAction") !== "active") {
                var temp;
                $.ajax({
                    url: "new_session",
                    success: function (result) {
                        if (result !== "false"){
                                document.cookie = "sessionAction=active";
                                document.cookie = "session_id="+result;
                            }
                    }
                });

                /*$.ajax({
                    url: "/~/allow_cookies",
                    success: function (result) {
                    }
                });*/
                //alert(document.cookie);
            }
            if (type === 'opt-out' && !didConsent) {
                // disable cookies
            }
        },

        onRevokeChoice: function () {
            var type = this.options.type;
            if (type === 'opt-in') {
                document.cookie = "sessionAction=;expires=Thu, 01 Jan 1970 00:00:01 GMT";
                document.cookie = "session_id=;expires=Thu, 01 Jan 1970 00:00:01 GMT";
            }
            if (type === 'opt-out') {
                // enable cookies
            }
        },
    })
});

/**
 * This function fetches a certain cookie.
 * @param {number} cname cookie name
 * @returns {string} cookie
 */
function getCookie(cname) { //source: www.w3schools.com
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
