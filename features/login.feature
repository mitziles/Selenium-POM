Feature: Incercare login

    Scenario Outline: Loginul unui utilizator cu date valabile
        Given Utilizatorul acceseaza siteul
        Then Utilizatorul da click pe butonul de login
        Then Introduce credentialele: email "<email>" si parola "<password>"
        When Apasa pe butonul de conectare
        Then Loginul a reusit

        Examples:
            | email   | password   |
            | x | y |

