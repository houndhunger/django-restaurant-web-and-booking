/* global flatpickr */
"use strict";

document.addEventListener('DOMContentLoaded', function () {
    const flatpickrInstance = flatpickr("#id_reservation_date", {
        enableTime: true,
        dateFormat: "Y/m/d H:i",
        time_24hr: true,
        minuteIncrement: 0, // Custom for resetting
        allowInput: true, // Allow manual input
        onChange: function (selectedDates, dateStr, instance) {
            const selectedDate = selectedDates[0];

            // Custom validation for 15-minute increments
            const minutes = selectedDate.getMinutes();
            if (minutes % 15 !== 0) {
                // Reset minutes to 0 if not a 15-minute increment
                selectedDate.setMinutes(0);
                instance.setDate(selectedDate, true); // Update the input value
            }
        },
    });

    // Function to adjust minutes when up or down is clicked
    function adjustMinutes(delta) {
        const currentDate = flatpickrInstance.selectedDates[0];

        if (currentDate) {
            let newMinutes = currentDate.getMinutes() + delta;

            // Ensure minutes stay within bounds (0-59) and align with 15-minute increments
            if (newMinutes >= 60) {
                newMinutes = 0; // Reset to 0 if above 59
            } else if (newMinutes < 0) {
                newMinutes = 45; // Set to 45 if below 0
            }

            currentDate.setMinutes(newMinutes);
            flatpickrInstance.setDate(currentDate, true); // Update Flatpickr instance
        }
    }

    // Detect clicks on up and down arrows within Flatpickr
    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("arrowUp")) {
            adjustMinutes(15); // Increment by 15 minutes
        } else if (e.target.classList.contains("arrowDown")) {
            adjustMinutes(-15); // Decrement by 15 minutes
        }
    });
});
