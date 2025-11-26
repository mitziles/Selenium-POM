Feature: Applying Filters

    Scenario Outline: User applies filters for a specific footwear item
        Given The user is on the site
        Then The user clicks the search bar
        Then The user enters the name of a footwear item "<name>"
        Then The user selects a "<color>"
        Then The user selects a specific "<size>"

        Examples:
            | name  | color | size |
            | Nike  | Gri  | 35   |