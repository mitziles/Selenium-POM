Feature: Aplicare filtre

    Scenario Outline: Utilizatorul aplica filtre pentru o anumita incaltaminte
        Given Userul intra pe site
        Then Userul da click pe search bar
        Then Userul introduce numele unei perechi de incaltaminte "<nume>"
        Then Userul alege o "<culoare>"
        Then Userul alege o anumite "<marime>"

        Examples:
            | nume      | culoare   | marime    |
            | Nike      | Gri   | 35        |

