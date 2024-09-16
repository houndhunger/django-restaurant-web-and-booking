$(document).ready(function () {
    $("#id_reservation_date").change(function () {
        var selectedDate = $(this).val();
        console.log("Selected date: ", selectedDate);  // Debugging

        if (selectedDate) {
            $.ajax({
                url: getAvailableTablesUrl,
                type: 'POST',
                data: JSON.stringify({
                    'date': selectedDate
                }),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                success: function (data) {
                    console.log("AJAX response data: ", data);  // Debugging
                    var tables = data.tables;
                    var html = "<p>Available tables for " + selectedDate + ":</p><ul>";
                    if (tables.length > 0) {
                        for (var i = 0; i < tables.length; i++) {
                            html += "<li>Table " + tables[i].number + "</li>";
                        }
                    } else {
                        html += "<li>No available tables</li>";
                    }
                    html += "</ul>";
                    $("#available-tables").html(html).show();
                },
                error: function (xhr, status, error) {
                    console.error("AJAX request failed:", status, error);  // Debugging
                }
            });
        } else {
            $("#available-tables").hide();
        }
    });
});
