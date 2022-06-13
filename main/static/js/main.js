$(document).ready(function () {
    $('#textarea').on('input', function (e) {
        this.style.height = '0px';
        this.style.height = (this.scrollHeight + 6) + 'px';
    });
    var csrf_token = $("input[name=csrfmiddlewaretoken]")
    $("body").on("click", ".Delete", function () {
        var delete_button = $(this)
        $.ajax({
            url: '/delete/' + $(this).closest('div').attr('id'),
            type: 'POST',
            data: {
                id: $(this).closest('div').attr('id'),
                csrfmiddlewaretoken: csrf_token.val(),
                func: $(this).text()
            },
            success: function (response) {
                delete_button.parents('div').remove()
            }
        });

    });
    $("body").on("click", ".Done", function () {
        var done_button = $(this)
        $.ajax({
            url: '/delete/' + $(this).closest('div').attr('id'),
            type: 'POST',
            data: {
                id: $(this).closest('div').attr('id'),
                csrfmiddlewaretoken: csrf_token.val(),
                func: $(this).text()
            },
            success: function (response) {
                if (response.completed) {
                    done_button.parents('div').find('h2').addClass('stroked_h')
                    done_button.text("Return")
                }
                else {
                    done_button.parents('div').find('h2').removeClass('stroked_h')
                    done_button.text("Done")
                }

            }
        });

    });
    $(".create_task").click(function () {
        if (isNullOrWhitespace($(".title").val())) {

        }
        else {
            var create_div = $(this).parents('div').eq(1)
            $.ajax({
                url: '',
                type: 'POST',
                data: {
                    title: $(".title").val(),
                    csrfmiddlewaretoken: csrf_token.val(),
                },
                success: function (response) {
                    console.log(response.title)
                    $("<div class='mx-auto' style=' max-width: 50rem; overflow-wrap: break-word; border: 1px solid black; border-radius: 7px; padding:20px;\
                margin-top:20px'>\
                <h2 class='text-dark'>"+ response.title + "</h2>\
    <div style='display: flex; justify-content: flex-end;' id='"+ response.id + "'>\
        <button type='submit' class='btn btn-outline-dark my_button Done' name='Done'>Done</button>\
        <button type='submit' class='btn btn-outline-dark ml-3 my_button Delete' name='Delete'>Delete</button>\
    </div>").insertAfter(create_div)

                }
            });
        }


    });
    function isNullOrWhitespace(input) {
        return !input || !input.trim();
    }
});