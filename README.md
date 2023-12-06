# SELLINF: THE PLATFORM FOR PUBLISHING CONTENT

## Project description

Sellinf is an innovative platform designed for creating, publishing and viewing content. At the center of Sellinf's
concept is the desire to provide users with a two-tiered experience - free and premium content.

On the platform, each user can easily register by providing a minimal amount of personal information (phone number and
username) to gain access to the platform.

For viewing premium content there is a one-time subscription with the help of Stripe payment service.
SELLINF creates a convenient space for interaction between creators and audience, facilitating creative exchange of
information!
> README WAS TRANSLATED IN ENGLISH BY DEEPL. THERE ARE MAY BE GRAMMATICAL MISTAKES.

## Project Features

1. **Registration by Phone Number**: Provides the option of registering on the platform through phone number, providing
   a
   convenient and quick process.
   This is the primary and only method of user authentication, increasing account security.
2. **Types of content**: The platform supports multiple types of content for all users - paid and free. This helps to
   create a diverse and engaging experience for all users. By supporting different types of content, sellinf provides
   flexibility of choice and allows the audience to enjoy quality content according to their preferences.
3. **Subscription system**: A one-time subscription payment provides ease of use and access to premium content
   forever.
4. **Content Moderation**: While going through the moderation process, the content is securely protected from
   objectionable material. Moderators ensure a high level of quality and compliance of content with platform standards.
5. **Security and Privacy**: Measures are taken to ensure the security of user data and privacy of personal information.
   Data encryption and authentication measures protect accounts.

## Requirement for setup and startup

1. **Creating an .env file**: Create a file named .env in the root directory of your project. In the .env file, fill in
   ```text
   SECRET_KEY=
   DEBUG=
   POSTGRES_DB=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_HOST=
   POSTGRES_PORT=
   PGDATA=
   LANGUAGE_CODE=
   TIME_ZONE=
   USE_I18N=
   USE_TZ=
   MEDIA_URL=
   MEDIA_ROOT=
   ADMIN_PHONE_NUMBER=
   CELERY_TIMEZONE=
   CELERY_TASK_TRACK_STARTED=
   CELERY_TASK_TIME_LIMIT=
   CELERY_BROKER_URL=
   CELERY_RESULT_BACKEND=
   STRIPE_PUBLIC_KEY=
   STRIPE_SECRET_KEY=
   PAYMENT_SUCCESS_URL=
   PAYMENT_CANCEL_URL=
   CACHE_LOCATION=
   ```

2. **Build Containers**: Now run the following command to build containers:
   ```commandline
   docker-compose build
   ```

### PROJECT STARTUP

1. **Starting the project**: To start the project, after successfully building the containers, enter the following
   command:
   ```commandline
   docker-compose up
   ```
2. **Using the project**: Open a web browser and navigate to the address specified in the console
   (usual **http://127.0.0.1:8000/**).
   > Test the various functionalities of your project to make sure they are working as
   expected.

## ROLE ASSIGNMENT

1. **User**: a role intended for regular registered users who can view free content and edit their own profile.
   > The user group is assigned to a user after registration
2. **Upgraded_user**: a role reserved for users who have paid a one-time subscription. They can view premium
   information,
   create their own content and subscribe to authors.
   > The upgraded_user group is assigned to a user after they have paid for a subscription
3. **Moderator**: a role that ensures the control and quality of content on the platform. Moderators have the ability to
   check the created content for compliance with standards and requirements, as well as manage the moderation process.
   This role helps to ensure security for all users of the platform.
   > The moderator group must be specified through the Django administration panel

### USER ROLE ASSIGNMENT

1. **Authorization in the admin panel**: Log in to the admin panel of your Django project by going to the URL,
   usually http://127.0.0.1:8000/admin/, and enter your admin credentials.
2. **Navigating to users**: In the administrative panel, find the section related to user management.
3. **Selecting a user**: Find the user to whom you want to assign a specific group and select them by clicking on their
   details.
4. **Edit User**: In the opened user edit page, you should find the "Groups" section which allows you to manage the
   user's
   groups.
5. **Selecting a group**: In this section you will see a list of available groups. Select the group you want to assign
   to the
   user.
6. **Saving changes**: After selecting the group, make sure to save the changes by clicking on the corresponding "Save"
   button.

## TECHNOLOGIES

**Python 3.x**: The project is based on the Python programming language, which ensures clean and readable code as well
as
ample opportunities for extensibility.

**Django**: Django is used as the framework for developing the web application, providing a structured and scalable
approach
to web development.

**Stripe API**: Integration with Stripe API provides secure and convenient subscription payment, making the platform an
ideal choice for online information sales

**Celery**: Celery Worker is activated to handle asynchronous tasks and improve project performance. This allows you to
handle background tasks such as sending a confirmation code to your phone and handling lengthy transactions.

**Docker**: Docker is used to simplify the deployment and management of an application in a containerized environment.
Docker provides isolation and portability of the application, which makes the deployment process more convenient and
reliable.

## CONTACT

If you have any questions, suggestions or need support, feel free to contact me. I am available to help you with your
project and answer all your questions. You can reach me at the following contacts:

**E-mail**: dima.captan@yandex.ru

**Telegram**: @Kaverz1n.

## SPECIAL THANKS

I would like to express my sincere gratitude to you for using the project and for the trust you have shown me. Your
participation and support are invaluable to me and to the development of my application
>README WAS TRANSLATED IN ENGLISH BY DEEPL. THERE ARE MAY BE GRAMMATICAL MISTAKES