Feature: Login Attempt

    Scenario Outline: User login with valid credentials
        Given The user accesses the site
        Then The user clicks the login button
        Then Enters credentials: email "<email>" and password "<password>"
        When Clicks the connect button
        Then Login was successful

        Examples:
            | email | password |
            | x     | y        |