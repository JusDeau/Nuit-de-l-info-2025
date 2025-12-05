																		----- La Faille -----
Le site ne contient pas de système de connexion (avec mot de passe et identifiant) cependant une faille commune de log a été reproduite.
Elle consiste simplement à oublier de réinitialiser les entrées-sorties au retour sur la page d'accueil, ce qui permet de forcer l'accès grâce à une attaque appellée "path traversal".
L'idée est simple et les stratégies multiples : accéder à l'aborescence derriere le site afin d'avoir accès à ses données (mots de passe, identifiants, données potentiellement moneyables comme des emails).
Comme les logs sont mal faits, rien n'empeche une tierce personne de reculer dans l'arborescence, surtout si elle est mal organisée.
Si les répertoirs ne sont pas définit, les noms et emplacements par defaut sont connus (exemple : ../etc/passwd) et l'accès y est d'autant plus simple.

Même si cette attaque peut être plus évoluée, se protéger au moins un minimum est très simple : 
- changer les noms des répertoirs
- créer sa propre arborescence commencant à la racine du site et nécessitant une connexion préalable sûre pour accéder aux données sensibles
- hasher au minimum les couples identifiant-mot de passe (des bibliothèques permettent généralement de le faire simplement)
- chiffrer, même de façon modérée, les informations moneyables
De cette façon, si le système de log échoue, l'accès aux informations sera au moins plus difficile, et la racine étant vraiment le début, un potentiel hacker ne peut explorer l'aborescence avec un simple ..
De même, avec un code bien organisé, normalement l'accès à l'arborescence par la commande -ls n'est pas possible.

--> pour l'essayer sur le site, .. à partir de n'importe quelle page suffit (par exemple : /main_page_jour/..)