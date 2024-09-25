# Restaurant Booking System

## Purpose of the Project

Restaurant Booking System is a Django web application created for Dino Bar and Restaurant designed to manage restaurant reservations. The application provides features for customers and staff to handle reservations, manage tables, and ensure a smooth dining experience.

![Restaurant booknig Mockup](docs/images/mockup-image-restaurant.jpg)

## Project Management - Kanban Board

For efficient project management, a **Kanban Board** is used to track progress, manage tasks, and ensure the project stays on schedule.

The Kanban board includes the following columns:
- **To Do**: Tasks that are planned but not yet started.
- **In Progress**: Tasks currently being worked on.
- **Done**: Completed tasks.

You can view the live Kanban board here: [Project Kanban Board](https://github.com/users/houndhunger/projects/2/views/1?layout=board).

This helped me to visualize the workflow, organize tasks, and maintain clarity on project goals.

## - Technologies Used
### - Languages
- **Python**: The core language used for backend logic in Django.
- **HTML5**: Used for structuring the web pages.
- **CSS3**: Used for styling the web pages and making them responsive.
- **JavaScript**: Used for interactive features and form validation.

### Frameworks, Libraries, and Tools
- **Django 4.2**: The main web framework used to build the project.
- **Bootstrap 5**: Used for responsive design and layout.
- **Django Allauth**: For user authentication and email verification.
- **Django Summernote**: For rich text editing within forms.
- **PostgreSQL**: The database used for storing reservation and user data.
- **Gunicorn**: The Python WSGI HTTP Server used for deployment.
- **Heroku**: For hosting the live version of the application.
- **Git**: Version control system for tracking changes in the project.
- **GitHub**: For hosting the project repository.
- **Cloudinary**: For managing static and media files in production.
- **Whitenoise**: For serving static files in production.
- **Google Fonts**: For custom fonts on the website.
- **Font Awesome**: For icons used in the navigation bar and footer.

## - UPDATE IMAGE - Supported screens and browsers
The website was developed and tested on Google Chrome. It's working correctly for Small screen sizes, like Galaxy Fold, as well as for large screens.
![Responsive design](docs/images/responsive-design.png)
*Image was generated using this [techsini.com website](https://techsini.com/multi-mockup/index.php)

## Installation
### Prerequisites
- Python 3.8 or later
- Django 4.2 or later
- PostgreSQL or another supported database
- Email service for sending confirmation emails

### Steps to Set Up
- **Clone the Repository**
 ```bash
  git clone https://github.com/houndhunger/django-restaurant-web-and-booking.git
  cd django-restaurant-web-and-booking
 ```
## Deployment
The Restaurant Booking System can be hosted on a web server to provide online access. It is designed for easy integration into existing websites or platforms used by restaurants. This allows restaurants to seamlessly add booking functionality to their operations and manage reservations effectively.

### Via Gitpod
1. Upon starting the Gitpod online workspace,
2. I initiated a Python web server using the command: ```"python3 manage.py runserver"```
3. Gitpod prompted me to open the website within its environment.
4. After making updates and saving them on Gitpod,
5. I refreshed the website to reflect the changes.

### Via Heroku
- The website repository is hosted at [Restaruant booking system repository](https://github.com/houndhunger/django-restaurant-web-and-booking/)
- The project is deployed to Heroku and is publicly accessible. [Restaruant booknig system app](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/)

To deploy the project, follow these steps:

1. Ensure that you have configured your environment variables in the Heroku dashboard.
2. Push your code to the Heroku remote repository: ```"git push"```
3. Deploy the app on Heroku either by manually deploying through the Heroku dashboard or by enabling automatic deployment for the main branch.
## Features

### Existing Features
- **User Features**
  - **Make Reservations**: Users can book tables for their desired time and date.
  - **View Reservations**: Users can view and manage their existing reservations.
  - **Update Reservations**: Users can update their reservation details if necessary.
  - **Cancel Reservations**: Users can cancel their reservations if plans change.
  - **Receive Email Notifications**: Users will receive automatic email confirmations after making, editing, or cancelling reservations.
  - **Automate Preferences**: The system will automatically reserve suitable tables based on guest preferences and notify guests if their preferences cannot be fully met.

- **Staff Features**
  - **Manage Reservations**: Staff can view and manage all reservations made by users through the admin interface.
  - **View Table Availability**: Staff can check table availability for any given time slot via the admin interface.
  - **Manage Tables**: Staff can add, update, or remove tables and their details using the admin interface.
  - **Custom Reservation Times**: Apply custom reservation times based on party size and buffer/service time.

### Future Enhancements
- **User Features**
  - **Update Profile Information**: Users will have the ability to manage their personal information, including name, password, and email address, for better reservation details through a dedicated profile page.
  - **Receive Email Notifications and Reminders**: Users will receive automatic email reminders a day before the booking and notifications about upcoming reservations on the morning of their reservation day at a preferred time.
  - **View Reservation Statistics**: Admins will generate reports to analyze trends such as peak hours and busy days, enabling data-driven decision-making.
  - **Availability Indicators**: Users will see real-time availability (0-49% available, 50-79% busy, 80-99% almost full, and 100% full) when selecting reservation dates and times.
  - **Calendar View of Availability**: Users will have a calendar view displaying available slots for different dates and times for easier booking.

### Future Enhancements
- **Staff Features**: 
  - **Manage Reservations - non-admin interface**: View and manage all reservations made by users through a non-admin user custom interface.
  - **View Table Availability - non-admin interface**: Check table availability for any given time slot through a non-admin user custom interface.
  - **Manage Tables - non-admin interface**: Add, update, or remove tables and their details through a non-admin user custom interface.
  - **Enhanced management of Reservations**: Staff will have enhanced tools to efficiently view, approve, and modify reservations made by users through an intuitive admin interface.
  - **View Reservation Statistics**: Staff will be able to generate detailed reports on reservation patterns, helping to identify peak times and improve service efficiency.
  - **Communication Tools**: Staff will have access to communication tools to directly notify users about their reservation status, changes, or special promotions.
  - **Restaurant Table Plan Layout**: Manage the restaurant's table reservations for efficient reservation handling and table assignments.

## Structure
### Interaction Design
- **Navigation Bar**
  - The fully responsive navigation bar is present on all pages, providing links to Home, and Menu. For signed-in users, the navigation bar shows links to Make a Reservation, My Reservations, Contact, Profile and Sign out. For those not signed in user navigation bar shows links to Sign in, Sign up and Make Reservation which leads to Sign in.
Profile and Log out. It ensures easy navigation across devices and maintains a consistent user experience.

 ![Nav Bar](docs/images/navigation-bar-image.png)

- **Reservation Management**
  - Customers can make, view, update, and cancel reservations through a user-friendly interface. This feature helps users to manage their dining plans effectively and receive confirmation emails for their bookings.

 ![Reservation Management](docs/images/docs/images/my-reservations-page.png)

- **Admin Dashboard**
  - The staff dashboard allows users to view and manage all reservations, including adding or updating table information. It provides an overview of current bookings and table availability to assist staff in daily operations.

 ![Admin Dashboard](docs/images/admin-dashboard-page.png)

- **Custom Signup and Login**
  - Users can sign up with email verification to ensure valid accounts. The custom signup form is designed to collect essential user details and facilitate secure login and registration processes.

 ![Custom Signup](docs/images/sign-up-page.png)

- **Email Notifications**
  - Automated email notifications are sent to users upon reservation creation, update, or cancellation. This feature ensures that users receive timely updates and confirmations about their reservations.

 ![Email Notifications](docs/images/email-notifications-image.png)

- **Footer**
  - The footer includes links to social media profiles and contact information. It encourages users to stay connected and provides easy access to additional resources.
  - For development purposes, phone numbers and email address links use fake or reserved domains to prevent accidental emails or real interactions (e.g., info@example.com).

 ![Footer](docs/images/footer-image.png)

### Information Design

- **Entity-Relationship Diagram (ERD)**  
  - The following ERD outlines the relationships between models in the system:

 ![Email Notifications](docs/images/erd.png)
  
## Development Process
The development process for this project involved several stages, each addressing different aspects of functionality and user experience:

- **Initial Setup**: 
  - Created the project and booking app, including the setup of essential configurations and initial database deployment.
  - Deployed the application to Heroku and set up secret keys for deployment.

- **Core Functionality Development**: 
  - Implemented the core features of the reservation system, including creating and editing reservations.
  - Developed the table model and incorporated it into the reservation system.
  - Updated the `Reservation` model and `MakeReservationView` to ensure basic booking functionality.

- **Enhancements and Fixes**: 
  - Enhanced the user interface with CSS updates and improvements to user experience.
  - Added and configured the `debug_toolbar` for development purposes.
  - Integrated Allauth for user authentication, replacing native Django forms to ensure a streamlined authentication process.
  - Added Gmail email notification functionality.

- **Advanced Features**: 
  - Improved reservation logic in `BaseReservationView` and `reservation_utils.py` to ensure accurate data handling and table assignment.

- **Ongoing Refinements**: 
  - Continued working on improving the table reservation logic and fixing logical errors.
  - Added staff role management for reservations, allowing staff to effectively manage and oversee reservations within the system.
  - Enhancing the guest experience by making it easier to identify available reservations based on busy days and guest preferences.

## User Stories
- **As a user, I want to be able to register an account**:
  - **Problem:** Users need a way to create an account with verified email addresses to ensure security and validity.
  - **Action:** Implement an account registration system that includes email verification as part of the process.
  - **Outcome:** Users can successfully create an account with a verified email address, ensuring that only valid emails are used.

| | | |
|:-|:-|:-|
| User opens the Home page | User clicks Sign up link in the navigation menu or on the home page, which leads user to Sign Up page | Fills the Sign up page |
| ![Home page](docs/images/home-page.png) | ![Sign up](docs/images/sign-up-page.png) | ![Fill Sign up](docs/images/sign-up-filled-page.png) |
| Submits the Sign up page by clicking "Sign up" button, which leads user to Verify Your Email Address page | User will receive a notification email, with activation link | By clicking on the notification link, the user will open the Confirm Email Address page |
| ![Verify Your Email Address](docs/images/verify-your-email-address-page.png) | ![blank](docs/images/email-notifications-image-2.png) | ![Confirm Email Address](docs/images/confirm-email-address-page.png) |
| By clicking on the "Confirm" button, the user will finish sign up process landing on the Home page |  |  |
| ![blank](docs/images/home-page.png) | ![blank](docs/images/blank.png) | ![blank](docs/images/blank.png) |

- **As a user, I want to log in and log out securely**
  - **Problem:** Users need to securely log in and out of the system to access and manage their reservations.
  - **Action:** Users log in using their email and password and can log out when done.
  - **Outcome:** After successful authentication, users are redirected to their dashboard. On logout, they are redirected to the homepage.

| | | |
|:-|:-|:-|
| User opens the Home page | User clicks on Sign in the navigation menu, which leads user to Sign In page | Fills the Sign in page 
| ![Home page](docs/images/home-page.png) | ![Sign up](docs/images/sign-up-page.png) | ![Fill Sign up](docs/images/sign-in-filled-page.png) |
| By clicking on the Sign In button, the user will finish up securely sign-in process landing on the Home page showing navigation menu for authenticated user | User clicks on Sign out in navigation menu, which leads user to Sign Out page | By clicking on "Sign Out" button, the user will finish the secured Sign Out process landing on the Home page |
 ![Home page - logged in](docs/images/home-authenticated-page.png) | ![Home page](docs/images/sign-out-page.png) | ![Home page](docs/images/home-page.png) |

- **As a user, I want to book a table**
  - **Problem:** Users want to reserve a table for a specific date, time, and party size.
  - **Action:** Users fill out a reservation form, selecting a date, time, guest count, and seating preferences (e.g., quiet, outside seating).
  - **Outcome:** If available, the reservation is confirmed, and a confirmation message is displayed to the user.

| | | |
|:-|:-|:-|
| User opens the Home page | User clicks on Make a Reservation in the navigation menu, which leads user to Make a Reservation page | Fills the Make a Reservation page |
| ![Home page](docs/images/home-page.png) | ![Make a Reservation](docs/images/make-a-reservation-full-page.png) | ![Fill Make a Reservation](docs/images/make-a-reservation-full-filled-page.png) |
| By clicking on Submit button, user will submit Reservation and landing on Reservation Preview | User clicks on My Reservation button, which leads user to Sign Out page |  |
| ![Home page - logged in](docs/images/reservation-preview-page.png) | ![My Reservations](docs/images/my-reservations-page.png) |  |

- **As a user, I want to view and manage my reservations**
  - **Problem:** Users need the ability to manage their existing reservations, including making changes or cancellations.
  - **Action:** Users view their reservations on the "My Reservations" page, where they can edit or cancel them as needed.
  - **Outcome:** Users can modify or cancel their bookings with immediate feedback on changes.

| | | |
|:-|:-|:-|
| User clicks on "My Reservations" in the navigation menu, which leads to user's reservations | "My Reservations" page is paginated, user can click "NEXT »" at the bottom of the page, which leads user to next page | User clicks "Amend" Reservation for relevant reservation, which leads user to "Edit Reservation" page |
| ![My Reservations](docs/images/my-reservations-page-full.png) | ![My Reservations next page](docs/images/my-reservations-page-next.png) | ![Edit reservation](docs/images/edit-a-reservation-full-page.png) |git add
| User can edit reservation and submit it by clicking on "Submit" button | Alternatively user in "My Reservations" can "Delete Reservation" by clicking on "Delete Reservation" button, which leads user to "Delete Reservation" page. Here user can confirm the deletion by clicking on "Yes, Delete" button. | Then the user is redirected to the My Reservations page |
| ![Reservation preview](docs/images/reservation-preview-page2.png) | ![](docs/images/delete-reservation-page.png) | ![](docs/images/my-reservations-page-after-delete.png) |

- **As a user, I want to interact with the website on different devices**
  - **Problem:** Users need to access and navigate the booking system from various devices, such as desktops, tablets, and smartphones.
  - **Action:** The website is designed to be responsive, adjusting layouts and components based on the device's screen size by Bootstrap front-end framework.
  - **Outcome:** Users have a seamless experience across all devices, ensuring easy reservation management on the go.

| | | |
|:-|:-|:-|
 | XXL - Larger desktops - 1400px and above (1920px)| Extra large (XL) - Large desktops  - 1200px - 1399px (1390px) | Large (LG) - Desktops - 992px - 1199px (1180px) |
| ![XXL Larger desktops](docs/images/make-a-reservation-full-page.png) | ![Extra large (XL) Large desktops](docs/images/my-reservations-page-full-1390px.png) | ![Large (LG)Large (LG) Desktops](docs/images/my-reservations-page-full-1180px.png) |
| ![XXL Larger desktops](docs/images/make-a-reservation-full-page.png) | ![Extra large (XL) Large desktops](docs/images/make-a-reservation-full-page-1180px.png) | ![Large (LG)Large (LG) Desktops](docs/images/make-a-reservation-full-page-1390px.png) |
| Medium (MD) -Tablets - 768px - 991px (980px)| Small (SM) - Phones (landscape)  - 576px - 767px (760px) | Extra small (XS) - Phones (portrait) col - 0px - 575px (570px) |
| ![Medium (MD) -Tablet](docs/images/my-reservations-page-full-980px.png) | ![Small (SM) - Phones](docs/images/my-reservations-page-full-760px.png) | ![Extra small (XS) - Phones (portrait) col](docs/images/my-reservations-page-full-570px.png) |
| ![Medium (MD) -Tablet](docs/images/make-a-reservation-full-page-980px.png) | ![Small (SM) - Phones](docs/images/make-a-reservation-full-page-760px.png) | ![Extra small (XS) - Phones (portrait) col](docs/images/make-a-reservation-full-page-570px.png) |

- **As an admin, I want to manage reservations**
  - **Problem:** Admin need to edit or cancel reservations to manage the restaurant's capacity efficiently.
  - **Action:** Admin can access the dashboard to handle all reservations and modify them as necessary.
  - **Outcome:** The restaurant's reservation system is kept organized, allowing smooth operation and customer satisfaction.

| | | |
|:-|:-|:-|
| Admin dashobard leads to | Booking - Reservations | Editing reservation (f.e. top reservation) |
| ![Admin home](docs/images/admin-dashboard-page.png) | ![Table page](docs/images/admin-reservations.png) | ![Small device](docs/images/admin-reservation1.png) |
| Staff with admin can proceed with changes, f.e. changing reservation "Status" to "Deleted" | Or change "Assigned Tables" (f.e. reservation second form the top) |  |
| ![Status changed to deleted](docs/images/admin-reservations-mark-deleted.png) | ![Table changed](docs/images/admin-reservations-table-changed.png) | ![blank](docs/images/blank.png) |

## Bugs and Issues
### Solved Bugs
- **Problem with mixing native Django forms and Allauth forms**  
  - **Problem**: There was a conflict when using both native Django forms and Allauth forms in the same project. This caused authentication and form validation issues, such as failing to log in users or improper form handling.  
  - **Solution**: The problem was resolved by exclusively using Allauth forms for user authentication, registration, and account management. This ensured consistent handling of user sessions and authentication processes across the app.

- **Gmail Email Notifications**  
  - **Problem**: Gmail email notifications were not working as expected.  
  - **Issue**: The issue was due to an incorrect definition in `env.py`.  
  - **Solution**: Corrected the definition in `env.py` to properly set the environment variables for email configuration. This adjustment resolved the email notification issue.

- **Reverse for 'edit_reservation' with no arguments not found**  
  - **Problem**: When trying to render the reservation preview page, Django couldn't reverse the URL for `edit_reservation`.  
  - **Issue**: The URL tag in the template was missing the required `pk` argument.  
  - **Solution**: Passed the correct `pk` argument in the URL tag to ensure Django could resolve the route. Updated the URL in the template as `{% url 'edit_reservation' reservation.pk %}`.

- **Form cleaned data issue in `ReservationUpdateView`**  
  - **Problem**: During form submission, reservation data was not being saved properly, and no tables were being assigned.  
  - **Issue**: The reservation logic was not handling form validation and saving correctly.  
  - **Solution**: Improved reservation logic by handling form validation and saving the reservation correctly if tables were available. Redirected to the `reservation_preview` after successful submission.

- **NoReverseMatch for 'reservation_preview'**  
  - **Problem**: After submitting the reservation form, there was a `NoReverseMatch` error due to the wrong view name in the redirect call.  
  - **Issue**: The `reservation_preview` view was not correctly set up in the URL patterns.  
  - **Solution**: Created the `reservation_preview` view and linked it properly in the URL patterns. Fixed the redirect by ensuring the correct path and `pk` argument were passed.

- **Bootstrap Content Off-Center**
  - **Problem**: Some content of the website is off-centre on screens larger than 1200px.
  - **Issue**: This misalignment can lead to an unprofessional appearance and negatively affect user experience.
  - **Solution**: Bad css styling with fixed width. Removing the fixed width on a specific class div solved the issue.

- **Table reservation: Works with logical errors, needs checking**  
  - **Problem:** The table reservation system logic is overcomplicated and prone to logical errors, requiring simplification and validation.  
  - **Issue:** Complex logic involving table assignment, zones, and advanced features has led to inconsistent behaviour, especially with overlapping reservations or large group bookings.  
  - **Solution:** The logic was stripped down to a simpler approach, assigning tables one by one in sequence. Advanced features such as zone management and other priorities were reintroduced incrementally, ensuring the system remains functional with a clear foundation.

- **Improper form error handling on table unavailability**  
  - **Problem:** When no tables are available for a given reservation, the error message does not clearly indicate the specific issue. It shows a generic error.  
  - **Issue:** Users receive a vague response when their reservation cannot be processed due to unavailable tables, leading to confusion and poor user experience.  
  - **Solution:** Customized error messages are now implemented, providing clear and specific feedback when tables are unavailable, depending on the issue (e.g., fully booked, out of opening hours).  

- **Handling simultaneous reservations with the same table**
  - **Problem:** Previously, there was no mechanism to prevent two users from reserving the same table at the same time.
  - **Action:** The view logic was updated to filter only available tables for the selected reservation time, preventing double bookings.
  - **Outcome:** The system now efficiently handles simultaneous reservation requests, ensuring no table is double-booked during overlapping time slots.

### REVISIT - Unsolved Bugs
   **Flatpickr is too large for small screens**  
  - **Problem**: The Flatpickr date picker appears oversized and doesn't fit well on smaller screens, making the user experience cumbersome.  
  - **Issue**: The cause is likely due to Flatpickr’s default styling, which isn’t fully responsive out of the box.  
  - **Solution**: Future plans include implementing responsive adjustments or integrating a mobile-friendly date picker.

  - **Advanced booking - Preferences**
  - **Problem**: The system doesn't consistently accommodate all guest preferences (e.g., quiet area, outdoor seating, etc.).
  - **Issue**: Some preferences are ignored or incorrectly applied during table assignment, leading to unsatisfactory guest experiences.
  - **Solution**: Implement more complex booking logic that ensures preferences are properly respected, along with extensive testing to verify correct behaviour.

- **Flatpickr doesn't pop up warning message**  
  - **Problem**: The Flatpickr widget doesn't consistently pop up a warning message when invalid input is entered for the minutes field, particularly when the input does not follow the 5-minute increment rule.  
  - **Issue**: Flatpickr allows manual input if allowInput: true is set, but it doesn't automatically enforce validation or display warnings for values that don't align with the defined minute Increment. Without additional validation logic, the widget may not always catch invalid inputs.
  - **Solution**: Implement custom validation using Flatpickr's onClose or onValueUpdate events to manually validate time inputs. Ensure that invalid entries outside the allowed 5-minute increments trigger a warning message consistently. Alternatively, handle input validation via the form's submission logic or create an inline error display mechanism.
  
## Testing
### Code validation 
- **HTML**: The following paths have been validated and no errors were found when passing through the [W3C validator](https://validator.w3.org/).
  - [app/](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/)
  - [app/menu/](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/menu/)  
  - [app/reservation/make/](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/reservation/make/)  
  - [app/reservations/](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/reservations/)  
  - [app/open/](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/open/)  
  - [app/contact/](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/contact/)  
  - [app/accounts/logout/](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/accounts/logout/)  
  - [app/accounts/login/](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/accounts/login/)  
  - [app/reservation/make/](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/reservation/make/)  
  - app/reservation/###/edit/ 
  - app/reservation/###/preview/
  - app/delete-reservation/###/

- **CSS**: The following file has been validated and no errors were found when passing through the [Jigsaw validator](https://jigsaw.w3.org/css-validator/).
  - [static/css/style.css](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/static/css/style.css)

- **JavaScript**: The following file has been validated and no errors were found when passing through the [jshint.com](https://jshint.com/). New JavaScript features (ES6) settings are turned on. Results show no errors.
[static/css/style.css](https://django-restaurant-web-and-book-565ecd4fe61b.herokuapp.com/static/js/flatpickr.js)

- **Python**: Code passes [pep8ci](https://pep8ci.herokuapp.com/) validation with 100% success validating following files:
  - [booking/reservation_utils.py](booking/utils/reservation_utils.py)  
  - [booking/admin.py](booking/admin.py)  
  - [booking/forms.py](booking/forms.py)  
  - [booking/urls.py](booking/urls.py)  
  - [booking/views.py](booking/views.py)  
  - [codestar/settings.py](codestar/settings.py)  
  - [codestar/urls.py](codestar/urls.py)  
  - [codestar/views.py](codestar/views.py)

### Test Cases
#### Manual Testing
Here are the key manual tests performed on the reservation booking system:

1. **Make a Reservation**
    - **Test**: Create a new reservation with valid data.
    - **Expected Result**: Reservation is created and visible under "My Reservations".
    - **Steps**: 

| | | | |
|:-|:-|:-|:-|
| 1. Log in to the system. | 2. Navigate to "Make a Reservation". | 3. Fill in reservation details (date & time, guest count, note, preferences). | 4. Submit and check if the reservation is successfully saved. |
| ![Sign in](docs/images/sign-in-page.png) | ![Make reservation](docs/images/make-a-reservation-full-page.png) | ![Fill in reservation details](docs/images/make-a-reservation-full-filled-page.png) | ![My reservations](docs/images/my-reservations-page.png) |

2. **Edit Reservation**
    - **Test**: Edit an existing reservation.
    - **Expected Result**: Updated details are saved and displayed correctly.
    - **Steps**:

| | | | |
|:-|:-|:-|:-|
|  1. Go to "My Reservations". | 2. Select an existing reservation | 3. Modify reservation details (e.g., guest count) | 4. Submit and verify the changes. |
| ![My Reservations](docs/images/my-reservations-page-full.png) | ![My Reservations next page](docs/images/my-reservations-page-next.png) | ![Edit reservation](docs/images/edit-a-reservation-full-page.png) | ![Reservation preview](docs/images/reservation-preview-page2.png) |



3. **Delete Reservation**
    - **Test**: Delete an existing reservation.
    - **Expected Result**: Reservation is deleted and no longer visible in "My Reservations".
    - **Steps**:

| | | | |
|:-|:-|:-|:-|
|   1. Access "My Reservations". | 2. "Amend Reservaton". |3. Choose "Delete" and confirm the action. | 4. User is redirected to "My Reservations". |
| ![My Reservations](docs/images/my-reservations-page-full.png) | ![My Reservations next page](docs/images/my-reservations-page-next.png) | ![Edit reservation](docs/images/delete-reservation-page.png) | ![Reservation preview](docs/images/my-reservations-page-after-delete.png) |



4. **Reservation Overlap Check**
   - **Test**: Attempt to book a reservation that overlaps with an existing one.
   - **Steps**:
     1. Try to book a reservation that conflicts with a current reservation.
     2. Submit the form.
   - **Expected Result**: Error message is displayed about overlapping reservations.

5. **Reservation Time Outside Operating Hours**
   - **Test**: Attempt to make a reservation outside the restaurant's opening hours.
   - **Steps**:
     1. Select a time before opening or after closing hours.
     2. Submit the form.
   - **Expected Result**: Error message indicating that the reservation is outside operating hours.

6. **Guest Count Limit**
   - **Test**: Attempt to book a reservation exceeding the maximum guest limit.
   - **Steps**:
     1. Select a large guest count beyond the allowed limit.
     2. Submit the form.
   - **Expected Result**: Error message that the guest count exceeds the limit.

7. **Reservation Confirmation Email**
   - **Test**: Verify if a confirmation email is sent after booking.
   - **Steps**:
     1. Create a reservation.
     2. Check the email inbox for a confirmation message.
   - **Expected Result**: Confirmation email is received with reservation details.

#### Manual Testing (Handling Invalid Inputs)
1. **Invalid Reservation Date**
   - **Test**: Attempt to book a reservation with an invalid or past date.
   - **Steps**: 
     1. Select a date in the past or an invalid date (e.g., 31st February).
     2. Submit the form.
   - **Expected Result**: Error message indicating that the selected date is invalid or cannot be in the past.

2. **Invalid Reservation Time**
   - **Test**: Try to book a reservation with a time outside the restaurant's operating hours.
   - **Steps**:
     1. Select a time that is either too early or too late (before midnight or after 23:59).
     2. Submit the form.
   - **Expected Result**: Error message indicating that the reservation time is outside the allowed hours.

3. **Exceed Maximum Guest Limit**
   - **Test**: Input a guest count exceeding the maximum allowed capacity.
   - **Steps**:
     1. Enter a guest count larger than the allowed maximum.
     2. Submit the form.
   - **Expected Result**: Error message indicating the guest count exceeds the restaurant's capacity.

4. **Empty Required Fields**
   - **Test**: Leave required fields (date, time, guest count) empty.
   - **Steps**:
     1. Try to submit the reservation form without filling in any required fields.
   - **Expected Result**: Form validation error for each missing field.

5. **Non-Numeric Guest Count**
   - **Test**: Enter a non-numeric value for the guest count field.
   - **Steps**:
     1. Enter text or symbols in the guest count field.
     2. Submit the form.
   - **Expected Result**: Error message indicating that the guest count must be a number.

6. **Overlapping Reservations**
   - **Test**: Try to book a reservation that conflicts with an existing one.
   - **Steps**:
     1. Book a reservation at the same time and for the same table as an existing reservation.
     2. Submit the form.
   - **Expected Result**: Error message indicating the reservation overlaps with an existing one.

7. **SQL Injection Attempt**
   - **Test**: Try injecting SQL commands into input fields to test for security vulnerabilities.
   - **Steps**:
     1. Enter an SQL query (e.g., `'; DROP TABLE reservations; --`) into any text input field.
     2. Submit the form.
   - **Expected Result**: Input is sanitized, and no SQL injection occurs.
   - **Explanation**: Django's ORM uses parameterized queries to escape user inputs, treating them as plain text. This prevents any SQL commands from executing, ensuring that no damage occurs to the database.















## Credits
- **Mentor**: Thanks to my mentor for his guidance and support throughout the development of this project.
- **Code Institute Tutor Service**: Special thanks to the Code Institute Tutor Service for their assistance and valuable feedback.
- **ChatGPT Service**: Appreciation to ChatGPT for providing helpful advice and code suggestions during the project development.


## License
This project is open-source and available under the MIT License. Feel free to fork, modify, and distribute the code for educational or commercial purposes.

---

Happy coding!