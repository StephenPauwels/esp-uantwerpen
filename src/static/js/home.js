let editor;
let nl_data;
let en_data;


Dropzone.options.dropzone = {
    init: function () {

        this.on("success", function (file, msg) {
            add_editable_document(msg['file_location'])
        });

        this.on("complete", function (file) {
            this.removeFile(file);
        });

        this.on("error", function (file, msg) {
            this.removeFile(file);
            alert(msg);
        });
    }
};

/**
 * MAIN FUNCTION
 */
$(function() {

    editor = CKEDITOR.replace("editor");
    editor.config.allowedContent = true;

    $.ajax({
        url: '/get-home-data',
        method: 'get',
        success: function (data) {
            nl_data = data["nl"];
            en_data = data["en"];
            editor.setData(en_data);

            for (const document of data['documents']) {
                add_editable_document(document);
            }
        }
    });


    $('#description-toggle').change(function () {
        const english = $(this).prop('checked');

        if (english) {
            nl_data = editor.getData();
            editor.setData(en_data);
        } else {
            en_data = editor.getData();
            editor.setData(nl_data);
        }
    });

    $('#submitbtn').click(function() {

        const english = $("#description-toggle").prop('checked');

        if (english) {
            en_data = editor.getData();
        } else {
            nl_data = editor.getData();
        }

        $.ajax({
            url: "save-home",
            method: 'post',
            data: {
                homepagedataNL: nl_data,
                homepagedataEN: en_data
            },
            success: function () {
                window.location.href = "/";
            },
            error: function (msg) {
                alert(`Error occurred: ${JSON.stringify(msg)}`)
            }
        });
    });
});

/**
 * This function adds a document to the document list.
 * @param {item} document document to be added
 */
function add_editable_document(document) {
    $("#documents-list").append(
        $(`<span class="badge type-bg-color mr-1">
                <a class="type-bg-color" href="/get-document/${document}">${document}</a> 
                &nbsp;
                <span onclick="remove_document(this)" style="cursor: pointer;">x</span>
            </span>`)
    );
}

/**
 * This function removes a certain document/
 * @param {item} elem to be removed document
 */
function remove_document(elem) {
    elem = $(elem);

    // Extract file location
    let text = elem.parent().children().first().attr("href");
    text = text.substring(text.lastIndexOf('/') + 1);


    $.ajax({
        url: 'remove-document/' + text,
        method: 'post',
        success: function () {
            elem.parent().remove();
        }
    })
}

