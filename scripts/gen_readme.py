#!/usr/bin/env python3
"""Generate README.md and its seven translations from one source.

Usage, from the repository root::

    python3 scripts/gen_readme.py
    python3 ../reeftank/scripts/gen_ecosystem.py   # run from the parent dir

Order matters: this script writes the whole file, so it must run *before*
gen_ecosystem.py, which inserts the shared "Related projects" block.

Edit T below, never the generated files.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = "https://github.com/Elwinmage/ha-reef-blueprints"
RAW = "https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main"
SITE = "https://elwinmage.github.io/reeftank/"
BEAT = "https://github.com/Elwinmage/ha-reefbeat-component"

# Flag, language code, path. English is the root README.
LANGS = [
    ("gb", "en", "README.md"),
    ("fr", "fr", "doc/fr/README.fr.md"),
    ("de", "de", "doc/de/README.de.md"),
    ("es", "es", "doc/es/README.es.md"),
    ("it", "it", "doc/it/README.it.md"),
    ("nl", "nl", "doc/nl/README.nl.md"),
    ("pl", "pl", "doc/pl/README.pl.md"),
    ("pt", "pt", "doc/pt/README.pt.md"),
]

# Clone counter, kept in a gist by the github-clone-count-badge action: the
# GitHub API only serves the last 14 days, so the count has to live outside the
# repository.
CLONE_GIST = (
    "https://gist.githubusercontent.com/Elwinmage/"
    "b4d01d48acce8199974b015b9ea23b3b/raw/clone.json"
)

BADGES = f"""[![GH-release](https://img.shields.io/github/v/release/Elwinmage/ha-reef-blueprints.svg?style=flat-square)]({REPO}/releases)
[![Ruff Status]({REPO}/actions/workflows/main.yml/badge.svg)]({REPO}/actions/workflows/main.yml)
[![Validate blueprints]({REPO}/actions/workflows/validate.yml/badge.svg)]({REPO}/actions/workflows/validate.yml)
[![GH-last-commit](https://img.shields.io/github/last-commit/Elwinmage/ha-reef-blueprints.svg?style=flat-square)]({REPO}/commits/main)
[![GitHub Clones](https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count&url={CLONE_GIST}&logo=github)](https://github.com/MShawon/github-clone-count-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![BuyMeCoffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat-square)](https://paypal.me/Elwinmage)"""

T: dict[str, dict[str, str]] = {
    "en": {
        "title": "Reef blueprints 🐬",
        "ecosystem_line": f"Part of the [**ReefTech Project Ecosystem**]({SITE})",
        "languages": "Supported Languages",
        "intro": (
            "Home Assistant automation blueprints for the ReefTech ecosystem. "
            "They notify you on your phone about **overdue maintenance** and "
            "**unreachable devices**, whichever integration your equipment "
            "comes from, **test your heaters** one at a time and **watch your "
            "relays** for an appliance that keeps drawing power once off."
        ),
        "why_title": "Why a separate repository",
        "why": (
            "Maintenance tasks are published by three integrations, so a "
            "blueprint watching them belongs to none of them in particular. "
            "It finds the tasks through the shared `reef_role` attribute, "
            "which means a future integration honouring the same contract is "
            "covered without republishing anything here.\n\n"
            f"Alerts specific to Red Sea hardware — abnormal modes, "
            f"calibrations, ReefDose heads, ReefRun sensors — stay in "
            f"[**ReefBeat watch**]({BEAT}/tree/main/blueprints/automation), "
            "shipped with the integration that produces those entities and "
            "versioned with it."
        ),
        "install_title": "Installation",
        "install": (
            "Pick your language and press the button. Home Assistant opens "
            "the import dialog; the blueprint then appears under "
            "**Settings → Automations & scenes → Blueprints**."
        ),
        "install_note": (
            "The languages are separate blueprints: importing two of them "
            "gives you two entries. Home Assistant has no translation "
            "mechanism for blueprints, which is also why this page is "
            "generated rather than written eight times."
        ),
        "heater_title": "Heater test",
        "heater_what": "`reef_heater_test` proves that each heater can hold the tank on its own. One heater stays powered, the others are cut for the duration of the test, one heater per run in rotation. The result reaches your phone. The test stops early and restores the heaters on an excessive drop or below the abort temperature, and leaves the decision to anything else that touches the heaters in the meantime.",
        "heater_safety": "Heaters left off by a Home Assistant restart are turned back on two minutes after startup. Disabling the automation during a test is the one case it cannot recover from: finish the test first. To start a test yourself, use the automation's **Run** button for the next heater in the rotation, or fire the `reef_heater_test` event with `heater: switch.your_heater` to pick one.",
        "heater_power": "A meter makes the verdict a proof, since a warm room can hide a dead heater. It is found automatically for a Red Sea socket or a smart plug: the test then tells a dead heater from an undersized one, gives no verdict when the heater never drew power, and checks that the cut heaters really stopped drawing. A heater on a socket that follows a probe or a schedule is refused: set the socket to manual first. An optional text helper keeps the last result, and its history the earlier ones.",
        "heater_summer": "In summer a heater has nothing to do once the room reaches the tank or the setpoint, and a test would prove nothing, so give the room temperature and the setpoint: the test is then skipped and says why.",
        "relay_title": "Relay watch",
        "relay_what": "`reef_relay_watch` warns you when a relay reads off but its appliance still draws power: a welded contact, or a socket that no longer obeys. It checks every socket of the chosen ReefControl-Power and every port of the chosen ReefControl every five minutes, along with any smart plug you add, and also catches a contact that welds long after the switch went off. No test, nothing is switched.",
        "what_title": "What it watches",
        "what_maintenance": (
            "**Overdue maintenance.** Every button carrying a `reef_role` "
            "that starts with `maint_`, alerting when its `days_left` turns "
            "negative. No configuration: the tasks are discovered. Each task "
            "has its own notification switch, which the blueprint honours by "
            "default so you can mute one job without muting the rest."
        ),
        "what_unreachable": (
            "**Unreachable devices.** A device is reported when all of its "
            "entities are unavailable. This one takes an explicit device "
            "list, and the reason is worth knowing: Home Assistant strips the "
            "attributes of an unavailable entity, so `reef_role` disappears "
            "exactly when the device goes offline. Discovery is impossible "
            "here, so you choose what matters."
        ),
        "notes_title": "Good to know",
        "note_freq": (
            "The automation runs every 5 minutes. It scans the `button` "
            "domain only, so the cost does not grow with the size of your "
            "installation."
        ),
        "note_tag": (
            "One notification per mobile device, tagged per device and alert "
            "type: a new alert replaces the previous one instead of stacking."
        ),
        "note_throttle": (
            "Maintenance alerts are re-sent at a configurable interval "
            "(1–24 h, default 4 h). Unreachable-device alerts are sent once "
            "and do not repeat (`alert_once`)."
        ),
        "note_ios": (
            "The Android channel field is ignored by iOS. Leave it as is if "
            "you only use iPhones."
        ),
        "dev_title": "Development",
        "dev": (
            "`scripts/gen_blueprints.py` produces the YAML files from "
            "one template and one string table; `scripts/gen_readme.py` does "
            "the same for this page. Never edit the generated files: CI "
            "regenerates them and fails if the result differs.\n\n"
            "`scripts/check_blueprints.py` is what stands in for a test "
            "suite. It parses every file, compares the inputs against the "
            "English reference, checks that each input is wired into a "
            "variable, and compiles the Jinja — an unbalanced tag otherwise "
            "only shows up as an automation that silently stops firing."
        ),
    },
    "fr": {
        "title": "Reef blueprints 🐬",
        "ecosystem_line": f"Fait partie de l'[**écosystème ReefTech**]({SITE})",
        "languages": "Langues disponibles",
        "intro": (
            "Blueprints d'automatisation Home Assistant pour l'écosystème "
            "ReefTech. Ils vous préviennent sur votre téléphone des "
            "**entretiens en retard** et des **appareils injoignables**, quelle "
            "que soit l'intégration dont vient votre matériel, **testent vos "
            "chauffages** un par un et **surveillent vos relais** pour repérer "
            "un appareil qui consomme encore une fois coupé."
        ),
        "why_title": "Pourquoi un dépôt séparé",
        "why": (
            "Les tâches de maintenance sont publiées par trois intégrations : "
            "un blueprint qui les surveille n'appartient à aucune en "
            "particulier. Il trouve les tâches par l'attribut commun "
            "`reef_role`, ce qui signifie qu'une future intégration honorant "
            "le même contrat sera couverte sans rien republier ici.\n\n"
            f"Les alertes propres au matériel Red Sea — modes anormaux, "
            f"calibrations, têtes ReefDose, capteurs ReefRun — restent dans "
            f"[**ReefBeat watch**]({BEAT}/tree/main/blueprints/automation), "
            "livré avec l'intégration qui produit ces entités et versionné "
            "avec elle."
        ),
        "install_title": "Installation",
        "install": (
            "Choisissez votre langue et pressez le bouton. Home Assistant "
            "ouvre la boîte d'import ; le blueprint apparaît ensuite dans "
            "**Paramètres → Automatisations et scènes → Blueprints**."
        ),
        "install_note": (
            "Les langues sont des blueprints distincts : en importer deux vous "
            "en donne deux. Home Assistant n'a aucun mécanisme de traduction "
            "pour les blueprints, ce qui explique aussi pourquoi cette page "
            "est générée plutôt qu'écrite huit fois."
        ),
        "heater_title": "Test des chauffages",
        "heater_what": "`reef_heater_test` vérifie que chaque chauffage tient le bac à lui seul. Un chauffage reste alimenté, les autres sont coupés le temps du test, un chauffage par exécution à tour de rôle. Le résultat arrive sur votre téléphone. Le test s'arrête plus tôt et rétablit les chauffages en cas de baisse excessive ou sous la température d'abandon, et cède la main à tout ce qui agit sur les chauffages entre-temps.",
        "heater_safety": "Les chauffages restés coupés après un redémarrage de Home Assistant sont rallumés deux minutes après le démarrage. Désactiver l'automatisation pendant un test est le seul cas dont elle ne peut pas se remettre : laissez d'abord le test finir. Pour lancer un test vous-même, utilisez le bouton **Exécuter** de l'automatisation pour le prochain chauffage de la rotation, ou émettez l'événement `reef_heater_test` avec `heater: switch.votre_chauffage` pour en choisir un.",
        "heater_power": "Un compteur transforme le verdict en preuve, car une pièce chaude peut masquer un chauffage mort. Il est trouvé automatiquement pour une prise Red Sea ou une prise connectée : le test distingue alors un chauffage mort d'un chauffage sous-dimensionné, ne rend pas de verdict si le chauffage n'a jamais consommé, et vérifie que les chauffages coupés ne consomment plus. Un chauffage sur une prise qui suit une sonde ou un programme est refusé : passez d'abord la prise en manuel. Un helper texte optionnel garde le dernier résultat, et son historique les précédents.",
        "heater_summer": "En été, un chauffage n'a plus rien à faire dès que la pièce atteint la température du bac ou la consigne, et un test ne prouverait rien : renseignez la température de la pièce et la consigne, le test est alors évité et le signale.",
        "relay_title": "Surveillance des relais",
        "relay_what": "`reef_relay_watch` vous prévient quand un relais est coupé alors que son appareil consomme encore : contact collé, ou prise qui n'obéit plus. Toutes les cinq minutes, il contrôle chaque prise des ReefControl-Power choisis et chaque port des ReefControl choisis, ainsi que les prises connectées ajoutées, et repère aussi un contact qui colle longtemps après la coupure. Aucun test, rien n'est commuté.",
        "what_title": "Ce qui est surveillé",
        "what_maintenance": (
            "**Entretiens en retard.** Chaque bouton portant un `reef_role` "
            "commençant par `maint_`, avec alerte quand son `days_left` "
            "devient négatif. Aucune configuration : les tâches sont "
            "découvertes. Chaque tâche a son propre interrupteur de "
            "notification, respecté par défaut, pour couper une intervention "
            "sans couper les autres."
        ),
        "what_unreachable": (
            "**Appareils injoignables.** Un appareil est signalé quand toutes "
            "ses entités sont indisponibles. Celui-ci demande une liste "
            "explicite, et la raison mérite d'être connue : Home Assistant "
            "supprime les attributs d'une entité indisponible, donc "
            "`reef_role` disparaît précisément quand l'appareil tombe. La "
            "découverte est impossible ici, c'est donc vous qui choisissez ce "
            "qui compte."
        ),
        "notes_title": "Bon à savoir",
        "note_freq": (
            "L'automatisation tourne toutes les 5 minutes. Elle ne balaie que "
            "le domaine `button`, son coût ne croît donc pas avec la taille de "
            "votre installation."
        ),
        "note_tag": (
            "Une notification par mobile, étiquetée par appareil et par type "
            "d'alerte : une nouvelle alerte remplace la précédente au lieu de "
            "s'empiler."
        ),
        "note_throttle": (
            "Les alertes de maintenance sont renvoyées à un intervalle "
            "configurable (1–24 h, défaut 4 h). Les alertes d'appareils "
            "injoignables ne sont envoyées qu'une seule fois "
            "(`alert_once`)."
        ),
        "note_ios": (
            "Le champ canal Android est ignoré par iOS. Laissez-le tel quel si "
            "vous n'utilisez que des iPhone."
        ),
        "dev_title": "Développement",
        "dev": (
            "`scripts/gen_blueprints.py` produit les fichiers YAML depuis "
            "un seul gabarit et une table de chaînes ; `scripts/gen_readme.py` "
            "fait de même pour cette page. N'éditez jamais les fichiers "
            "générés : la CI les régénère et échoue si le résultat diffère.\n\n"
            "`scripts/check_blueprints.py` tient lieu de suite de tests. Il "
            "parse chaque fichier, compare les entrées à la référence "
            "anglaise, vérifie que chacune est bien câblée dans une variable, "
            "et compile le Jinja — une balise mal fermée ne se verrait sinon "
            "que sous la forme d'une automatisation qui cesse de se "
            "déclencher."
        ),
    },
    "de": {
        "title": "Reef blueprints 🐬",
        "ecosystem_line": f"Teil des [**ReefTech Project Ecosystem**]({SITE})",
        "languages": "Verfügbare Sprachen",
        "intro": (
            "Home-Assistant-Automatisierungs-Blueprints für das "
            "ReefTech-Ökosystem. Sie benachrichtigen Sie auf dem Telefon über "
            "**überfällige Wartungen** und **nicht erreichbare Geräte**, "
            "unabhängig davon, aus welcher Integration Ihre Technik stammt, "
            "**testen Ihre Heizer** einzeln und **überwachen Ihre Relais** auf "
            "ein Gerät, das nach dem Ausschalten weiter Strom zieht."
        ),
        "why_title": "Warum ein eigenes Repository",
        "why": (
            "Wartungsaufgaben werden von drei Integrationen veröffentlicht; "
            "ein Blueprint, der sie überwacht, gehört zu keiner davon im "
            "Besonderen. Er findet die Aufgaben über das gemeinsame "
            "`reef_role`-Attribut, sodass eine künftige Integration mit "
            "demselben Vertrag abgedeckt ist, ohne dass hier etwas neu "
            "veröffentlicht werden müsste.\n\n"
            f"Meldungen speziell zu Red-Sea-Technik — abweichende Modi, "
            f"Kalibrierungen, ReefDose-Köpfe, ReefRun-Sensoren — bleiben in "
            f"[**ReefBeat watch**]({BEAT}/tree/main/blueprints/automation), "
            "ausgeliefert mit der Integration, die diese Entitäten erzeugt, "
            "und mit ihr versioniert."
        ),
        "install_title": "Installation",
        "install": (
            "Sprache wählen und auf die Schaltfläche drücken. Home Assistant "
            "öffnet den Importdialog; der Blueprint erscheint danach unter "
            "**Einstellungen → Automatisierungen & Szenen → Blueprints**."
        ),
        "install_note": (
            "Die Sprachen sind getrennte Blueprints: wer zwei importiert, hat "
            "zwei Einträge. Home Assistant hat keinen Übersetzungsmechanismus "
            "für Blueprints — auch deshalb wird diese Seite generiert statt "
            "achtmal geschrieben."
        ),
        "heater_title": "Heizungstest",
        "heater_what": "`reef_heater_test` prüft, ob jede Heizung das Becken allein halten kann. Eine Heizung bleibt eingeschaltet, die anderen werden für die Testdauer abgeschaltet, pro Lauf eine Heizung im Wechsel. Das Ergebnis kommt auf Ihr Telefon. Bei zu starkem Abfall oder unter der Abbruchtemperatur endet der Test vorzeitig und stellt die Heizungen wieder her; greift währenddessen etwas anderes in die Heizungen ein, überlässt er diesem die Entscheidung.",
        "heater_safety": "Nach einem Neustart von Home Assistant ausgeschaltet gebliebene Heizungen werden zwei Minuten nach dem Start wieder eingeschaltet. Das Deaktivieren der Automatisierung während eines Tests ist der einzige Fall, von dem sie sich nicht erholen kann: Lassen Sie den Test zuerst enden. Um selbst einen Test zu starten, nutzen Sie die Schaltfläche **Ausführen** der Automatisierung für die nächste Heizung im Wechsel, oder senden Sie das Ereignis `reef_heater_test` mit `heater: switch.ihre_heizung`, um eine auszuwählen.",
        "heater_power": "Ein Zähler macht das Ergebnis zum Beweis, denn ein warmer Raum kann eine defekte Heizung verbergen. Er wird für eine Red-Sea-Steckdose oder eine smarte Steckdose automatisch gefunden: Der Test unterscheidet dann eine defekte von einer zu schwachen Heizung, gibt kein Ergebnis, wenn die Heizung nie verbraucht hat, und prüft, ob die abgeschalteten Heizungen wirklich nichts mehr verbrauchen. Eine Heizung an einer Steckdose, die einem Fühler oder Zeitplan folgt, wird abgelehnt: Stellen Sie die Steckdose zuerst auf manuell. Ein optionaler Text-Helfer behält das letzte Ergebnis, sein Verlauf die früheren.",
        "heater_summer": "Im Sommer hat eine Heizung nichts zu tun, sobald der Raum die Beckentemperatur oder den Sollwert erreicht, und ein Test würde nichts beweisen: Geben Sie Raumtemperatur und Sollwert an, dann wird der Test übersprungen und meldet das.",
        "relay_title": "Relaisüberwachung",
        "relay_what": "`reef_relay_watch` warnt Sie, wenn ein Relais ausgeschaltet ist, sein Gerät aber weiter verbraucht: verklebter Kontakt oder eine Steckdose, die nicht mehr gehorcht. Alle fünf Minuten prüft es jede Steckdose der gewählten ReefControl-Power und jeden Port der gewählten ReefControl sowie hinzugefügte smarte Steckdosen und erkennt auch einen Kontakt, der lange nach dem Abschalten verklebt. Kein Test, es wird nichts geschaltet.",
        "what_title": "Was überwacht wird",
        "what_maintenance": (
            "**Überfällige Wartung.** Jede Schaltfläche mit einer "
            "`reef_role`, die mit `maint_` beginnt; gemeldet wird, sobald ihr "
            "`days_left` negativ wird. Keine Konfiguration: die Aufgaben "
            "werden gefunden. Jede Aufgabe hat ihren eigenen "
            "Benachrichtigungsschalter, den der Blueprint standardmäßig "
            "beachtet, damit Sie eine einzelne Arbeit stummschalten können."
        ),
        "what_unreachable": (
            "**Nicht erreichbare Geräte.** Ein Gerät wird gemeldet, wenn alle "
            "seine Entitäten nicht verfügbar sind. Dies braucht eine "
            "ausdrückliche Geräteliste, und der Grund ist wissenswert: Home "
            "Assistant entfernt die Attribute einer nicht verfügbaren "
            "Entität, `reef_role` verschwindet also genau dann, wenn das "
            "Gerät ausfällt. Automatische Erkennung ist hier unmöglich, also "
            "wählen Sie selbst."
        ),
        "notes_title": "Gut zu wissen",
        "note_freq": (
            "Die Automatisierung läuft alle 5 Minuten. Sie durchsucht nur die "
            "`button`-Domäne, der Aufwand wächst also nicht mit der Größe "
            "Ihrer Installation."
        ),
        "note_tag": (
            "Eine Benachrichtigung je Mobilgerät, markiert nach Gerät und "
            "Meldungstyp: eine neue Meldung ersetzt die vorige, statt sich zu "
            "stapeln."
        ),
        "note_throttle": (
            "Wartungsmeldungen werden in einem einstellbaren Intervall "
            "(1–24 h, Standard 4 h) erneut gesendet. Meldungen nicht "
            "erreichbarer Geräte werden nur einmal gesendet "
            "(`alert_once`)."
        ),
        "note_ios": (
            "Das Android-Kanal-Feld wird von iOS ignoriert. Lassen Sie es "
            "unverändert, wenn Sie nur iPhones nutzen."
        ),
        "dev_title": "Entwicklung",
        "dev": (
            "`scripts/gen_blueprints.py` erzeugt die YAML-Dateien aus "
            "einer Vorlage und einer Zeichenketten-Tabelle; "
            "`scripts/gen_readme.py` tut dasselbe für diese Seite. Bearbeiten "
            "Sie die erzeugten Dateien nie: die CI erzeugt sie neu und "
            "schlägt fehl, wenn das Ergebnis abweicht.\n\n"
            "`scripts/check_blueprints.py` ersetzt die Testsuite. Es parst "
            "jede Datei, vergleicht die Eingaben mit der englischen Referenz, "
            "prüft ob jede in eine Variable verdrahtet ist, und kompiliert "
            "das Jinja — ein unausgeglichenes Tag zeigt sich sonst nur als "
            "Automatisierung, die stillschweigend nicht mehr auslöst."
        ),
    },
    "es": {
        "title": "Reef blueprints 🐬",
        "ecosystem_line": f"Parte del [**ecosistema ReefTech**]({SITE})",
        "languages": "Idiomas disponibles",
        "intro": (
            "Blueprints de automatización de Home Assistant para el ecosistema "
            "ReefTech. Le avisan en el móvil de los **mantenimientos "
            "vencidos** y de los **dispositivos no disponibles**, venga su "
            "equipo de la integración que venga, **prueban sus calentadores** "
            "uno a uno y **vigilan sus relés** para detectar un aparato que "
            "sigue consumiendo una vez apagado."
        ),
        "why_title": "Por qué un repositorio aparte",
        "why": (
            "Las tareas de mantenimiento las publican tres integraciones, así "
            "que un blueprint que las vigile no pertenece a ninguna en "
            "concreto. Encuentra las tareas por el atributo común "
            "`reef_role`, lo que significa que una integración futura que "
            "respete el mismo contrato quedará cubierta sin republicar nada "
            "aquí.\n\n"
            f"Los avisos propios del hardware Red Sea — modos anómalos, "
            f"calibraciones, cabezales ReefDose, sensores ReefRun — se quedan "
            f"en [**ReefBeat watch**]({BEAT}/tree/main/blueprints/automation), "
            "distribuido con la integración que produce esas entidades y "
            "versionado con ella."
        ),
        "install_title": "Instalación",
        "install": (
            "Elija su idioma y pulse el botón. Home Assistant abre el diálogo "
            "de importación; el blueprint aparece luego en **Ajustes → "
            "Automatizaciones y escenas → Blueprints**."
        ),
        "install_note": (
            "Los idiomas son blueprints distintos: importar dos le da dos "
            "entradas. Home Assistant no tiene mecanismo de traducción para "
            "blueprints, que es también por lo que esta página se genera en "
            "vez de escribirse ocho veces."
        ),
        "heater_title": "Prueba de calentadores",
        "heater_what": "`reef_heater_test` comprueba que cada calentador mantiene el acuario por sí solo. Un calentador sigue encendido, los demás se apagan durante la prueba, un calentador por ejecución y por turnos. El resultado llega a su teléfono. La prueba se detiene antes y restablece los calentadores ante una bajada excesiva o por debajo de la temperatura de cancelación, y cede ante cualquier otra cosa que actúe sobre los calentadores mientras tanto.",
        "heater_safety": "Los calentadores que quedan apagados tras un reinicio de Home Assistant se encienden dos minutos después del arranque. Desactivar la automatización durante una prueba es el único caso del que no puede recuperarse: deje antes que la prueba termine. Para iniciar una prueba usted mismo, use el botón **Ejecutar** de la automatización para el siguiente calentador de la rotación, o emita el evento `reef_heater_test` con `heater: switch.su_calentador` para elegir uno.",
        "heater_power": "Un medidor convierte el resultado en una prueba, porque una habitación cálida puede ocultar un calentador averiado. Se encuentra automáticamente para un enchufe Red Sea o un enchufe inteligente: la prueba distingue entonces un calentador averiado de uno insuficiente, no da resultado si el calentador nunca consumió y comprueba que los calentadores apagados dejan de consumir. Un calentador en un enchufe que sigue una sonda o un programa se rechaza: ponga antes el enchufe en manual. Un ayudante de texto opcional guarda el último resultado, y su historial los anteriores.",
        "heater_summer": "En verano, un calentador no tiene nada que hacer cuando la habitación alcanza la temperatura del acuario o la consigna, y una prueba no demostraría nada: indique la temperatura de la habitación y la consigna, y la prueba se evitará y lo avisará.",
        "relay_title": "Vigilancia de relés",
        "relay_what": "`reef_relay_watch` le avisa cuando un relé está apagado pero su aparato sigue consumiendo: contacto pegado o un enchufe que ya no obedece. Cada cinco minutos comprueba cada enchufe de los ReefControl-Power elegidos y cada puerto de los ReefControl elegidos, además de los enchufes inteligentes añadidos, y detecta también un contacto que se pega mucho después del apagado. Sin prueba, no se conmuta nada.",
        "what_title": "Qué se vigila",
        "what_maintenance": (
            "**Mantenimientos vencidos.** Todo botón con un `reef_role` que "
            "empieza por `maint_`, avisando cuando su `days_left` se vuelve "
            "negativo. Sin configuración: las tareas se descubren solas. Cada "
            "tarea tiene su propio interruptor de notificación, respetado por "
            "defecto, para silenciar un trabajo sin silenciar los demás."
        ),
        "what_unreachable": (
            "**Dispositivos no disponibles.** Se avisa de un dispositivo "
            "cuando todas sus entidades están no disponibles. Este necesita "
            "una lista explícita, y la razón vale la pena: Home Assistant "
            "elimina los atributos de una entidad no disponible, así que "
            "`reef_role` desaparece justo cuando el dispositivo cae. El "
            "descubrimiento es imposible aquí, así que elige usted."
        ),
        "notes_title": "Conviene saber",
        "note_freq": (
            "La automatización se ejecuta cada 5 minutos. Solo recorre el "
            "dominio `button`, así que el coste no crece con el tamaño de su "
            "instalación."
        ),
        "note_tag": (
            "Una notificación por móvil, etiquetada por dispositivo y tipo de "
            "aviso: un aviso nuevo sustituye al anterior en lugar de "
            "apilarse."
        ),
        "note_throttle": (
            "Las alertas de mantenimiento se reenvían a un intervalo "
            "configurable (1–24 h, por defecto 4 h). Las alertas de "
            "dispositivos no disponibles se envían una sola vez "
            "(`alert_once`)."
        ),
        "note_ios": (
            "El campo de canal Android lo ignora iOS. Déjelo tal cual si solo "
            "usa iPhone."
        ),
        "dev_title": "Desarrollo",
        "dev": (
            "`scripts/gen_blueprints.py` produce los ficheros YAML desde "
            "una plantilla y una tabla de cadenas; `scripts/gen_readme.py` "
            "hace lo mismo con esta página. No edite nunca los ficheros "
            "generados: la CI los regenera y falla si el resultado difiere.\n\n"
            "`scripts/check_blueprints.py` hace las veces de suite de "
            "pruebas. Analiza cada fichero, compara las entradas con la "
            "referencia inglesa, comprueba que cada una está cableada a una "
            "variable, y compila el Jinja — una etiqueta desequilibrada solo "
            "se vería, si no, como una automatización que deja de dispararse."
        ),
    },
    "it": {
        "title": "Reef blueprints 🐬",
        "ecosystem_line": f"Parte dell'[**ecosistema ReefTech**]({SITE})",
        "languages": "Lingue disponibili",
        "intro": (
            "Blueprint di automazione Home Assistant per l'ecosistema "
            "ReefTech. Vi avvisano sul telefono delle **manutenzioni scadute** "
            "e dei **dispositivi irraggiungibili**, da qualunque integrazione "
            "provenga la vostra attrezzatura, **provano i riscaldatori** uno "
            "alla volta e **sorvegliano i relè** per scoprire un apparecchio "
            "che consuma ancora una volta spento."
        ),
        "why_title": "Perché un repository separato",
        "why": (
            "Le attività di manutenzione sono pubblicate da tre integrazioni: "
            "un blueprint che le sorveglia non appartiene a nessuna in "
            "particolare. Trova le attività tramite l'attributo comune "
            "`reef_role`, il che significa che una futura integrazione che "
            "rispetti lo stesso contratto sarà coperta senza ripubblicare "
            "nulla qui.\n\n"
            f"Gli avvisi propri dell'hardware Red Sea — modalità anomale, "
            f"calibrazioni, teste ReefDose, sensori ReefRun — restano in "
            f"[**ReefBeat watch**]({BEAT}/tree/main/blueprints/automation), "
            "distribuito con l'integrazione che produce quelle entità e "
            "versionato con essa."
        ),
        "install_title": "Installazione",
        "install": (
            "Scegliete la lingua e premete il pulsante. Home Assistant apre la "
            "finestra di importazione; il blueprint compare poi in "
            "**Impostazioni → Automazioni e scene → Blueprint**."
        ),
        "install_note": (
            "Le lingue sono blueprint distinti: importarne due ne dà due. Home "
            "Assistant non ha alcun meccanismo di traduzione per i blueprint, "
            "ed è anche il motivo per cui questa pagina è generata invece di "
            "essere scritta otto volte."
        ),
        "heater_title": "Test dei riscaldatori",
        "heater_what": "`reef_heater_test` verifica che ogni riscaldatore regga la vasca da solo. Un riscaldatore resta acceso, gli altri vengono spenti per la durata del test, un riscaldatore per esecuzione a rotazione. Il risultato arriva sul telefono. Il test si ferma prima e ripristina i riscaldatori in caso di calo eccessivo o sotto la temperatura di interruzione, e cede a qualsiasi altra cosa agisca sui riscaldatori nel frattempo.",
        "heater_safety": "I riscaldatori rimasti spenti dopo un riavvio di Home Assistant vengono riaccesi due minuti dopo l'avvio. Disattivare l'automazione durante un test è l'unico caso da cui non può riprendersi: lasciate prima finire il test. Per avviare un test da soli, usate il pulsante **Esegui** dell'automazione per il prossimo riscaldatore della rotazione, oppure emettete l'evento `reef_heater_test` con `heater: switch.vostro_riscaldatore` per sceglierne uno.",
        "heater_power": "Un misuratore trasforma il risultato in una prova, perché una stanza calda può nascondere un riscaldatore guasto. Viene trovato automaticamente per una presa Red Sea o una presa smart: il test distingue allora un riscaldatore guasto da uno sottodimensionato, non dà risultato se il riscaldatore non ha mai consumato e verifica che i riscaldatori spenti non consumino più. Un riscaldatore su una presa che segue una sonda o un programma viene rifiutato: mettete prima la presa in manuale. Un helper di testo opzionale conserva l'ultimo risultato, e la sua cronologia i precedenti.",
        "heater_summer": "In estate un riscaldatore non ha nulla da fare quando la stanza raggiunge la temperatura della vasca o il setpoint, e un test non dimostrerebbe nulla: indicate la temperatura della stanza e il setpoint, il test viene evitato e lo segnala.",
        "relay_title": "Sorveglianza dei relè",
        "relay_what": "`reef_relay_watch` vi avvisa quando un relè è spento ma il suo apparecchio consuma ancora: contatto incollato o presa che non obbedisce più. Ogni cinque minuti controlla ogni presa dei ReefControl-Power scelti e ogni porta dei ReefControl scelti, oltre alle prese smart aggiunte, e rileva anche un contatto che si incolla molto dopo lo spegnimento. Nessun test, non viene commutato nulla.",
        "what_title": "Cosa viene sorvegliato",
        "what_maintenance": (
            "**Manutenzioni scadute.** Ogni pulsante con un `reef_role` che "
            "inizia per `maint_`, con avviso quando il suo `days_left` diventa "
            "negativo. Nessuna configurazione: le attività vengono trovate da "
            "sole. Ogni attività ha il proprio interruttore di notifica, "
            "rispettato per impostazione predefinita, così potete silenziarne "
            "una senza silenziare le altre."
        ),
        "what_unreachable": (
            "**Dispositivi irraggiungibili.** Un dispositivo viene segnalato "
            "quando tutte le sue entità sono non disponibili. Questo richiede "
            "un elenco esplicito, e il motivo merita di essere noto: Home "
            "Assistant rimuove gli attributi di un'entità non disponibile, "
            "quindi `reef_role` sparisce proprio quando il dispositivo cade. "
            "Qui la scoperta automatica è impossibile, quindi scegliete voi."
        ),
        "notes_title": "Da sapere",
        "note_freq": (
            "L'automazione gira ogni 5 minuti. Percorre solo il dominio "
            "`button`, quindi il costo non cresce con la dimensione della "
            "vostra installazione."
        ),
        "note_tag": (
            "Una notifica per dispositivo mobile, etichettata per dispositivo "
            "e tipo di avviso: un nuovo avviso sostituisce il precedente "
            "invece di accumularsi."
        ),
        "note_throttle": (
            "Le notifiche di manutenzione vengono reinviate a un "
            "intervallo configurabile (1–24 h, predefinito 4 h). Le "
            "notifiche di dispositivi irraggiungibili vengono inviate "
            "una sola volta (`alert_once`)."
        ),
        "note_ios": (
            "Il campo canale Android è ignorato da iOS. Lasciatelo com'è se "
            "usate solo iPhone."
        ),
        "dev_title": "Sviluppo",
        "dev": (
            "`scripts/gen_blueprints.py` produce i file YAML da un "
            "modello e una tabella di stringhe; `scripts/gen_readme.py` fa lo "
            "stesso per questa pagina. Non modificate mai i file generati: la "
            "CI li rigenera e fallisce se il risultato differisce.\n\n"
            "`scripts/check_blueprints.py` fa le veci della suite di test. "
            "Analizza ogni file, confronta gli input con il riferimento "
            "inglese, verifica che ciascuno sia collegato a una variabile, e "
            "compila il Jinja — un tag sbilanciato altrimenti si manifesta "
            "solo come un'automazione che smette di scattare."
        ),
    },
    "nl": {
        "title": "Reef blueprints 🐬",
        "ecosystem_line": f"Onderdeel van het [**ReefTech Project Ecosystem**]({SITE})",
        "languages": "Beschikbare talen",
        "intro": (
            "Home Assistant automatiserings-blueprints voor het "
            "ReefTech-ecosysteem. Ze waarschuwen u op uw telefoon over "
            "**achterstallig onderhoud** en **onbereikbare apparaten**, uit "
            "welke integratie uw apparatuur ook komt, **testen uw verwarmers** "
            "één voor één en **bewaken uw relais** op een apparaat dat na "
            "uitschakelen stroom blijft trekken."
        ),
        "why_title": "Waarom een aparte repository",
        "why": (
            "Onderhoudstaken worden door drie integraties gepubliceerd; een "
            "blueprint die ze bewaakt hoort bij geen van drieën in het "
            "bijzonder. Hij vindt de taken via het gedeelde "
            "`reef_role`-attribuut, waardoor een toekomstige integratie met "
            "hetzelfde contract gedekt is zonder dat hier iets opnieuw "
            "gepubliceerd hoeft te worden.\n\n"
            f"Meldingen die specifiek zijn voor Red Sea-apparatuur — "
            f"afwijkende modi, kalibraties, ReefDose-koppen, ReefRun-sensoren "
            f"— blijven in "
            f"[**ReefBeat watch**]({BEAT}/tree/main/blueprints/automation), "
            "meegeleverd met de integratie die die entiteiten maakt en "
            "daarmee mee versioneerd."
        ),
        "install_title": "Installatie",
        "install": (
            "Kies uw taal en druk op de knop. Home Assistant opent het "
            "importvenster; de blueprint verschijnt daarna onder "
            "**Instellingen → Automatiseringen en scènes → Blueprints**."
        ),
        "install_note": (
            "De talen zijn losse blueprints: wie er twee importeert krijgt er "
            "twee. Home Assistant heeft geen vertaalmechanisme voor "
            "blueprints, en ook daarom wordt deze pagina gegenereerd in plaats "
            "van acht keer geschreven."
        ),
        "heater_title": "Verwarmingstest",
        "heater_what": "`reef_heater_test` controleert of elke verwarming de bak alleen op temperatuur kan houden. Eén verwarming blijft aan, de andere gaan uit tijdens de test, per run één verwarming om de beurt. Het resultaat komt op uw telefoon. Bij een te grote daling of onder de afbreektemperatuur stopt de test eerder en herstelt hij de verwarmingen, en hij laat de beslissing over aan al het andere dat intussen op de verwarmingen ingrijpt.",
        "heater_safety": "Verwarmingen die na een herstart van Home Assistant uit zijn gebleven, gaan twee minuten na het opstarten weer aan. De automatisering uitschakelen tijdens een test is het enige geval waarvan ze niet kan herstellen: laat de test eerst afronden. Om zelf een test te starten, gebruikt u de knop **Uitvoeren** van de automatisering voor de volgende verwarming in de rotatie, of stuurt u het event `reef_heater_test` met `heater: switch.uw_verwarming` om er een te kiezen.",
        "heater_power": "Een meter maakt van de uitslag een bewijs, want een warme kamer kan een defecte verwarming verbergen. Hij wordt automatisch gevonden voor een Red Sea-contactdoos of slimme stekker: de test onderscheidt dan een defecte van een te zwakke verwarming, geeft geen uitslag als de verwarming nooit verbruikte en controleert of de uitgeschakelde verwarmingen echt niets meer verbruiken. Een verwarming op een contactdoos die een sonde of programma volgt, wordt geweigerd: zet de contactdoos eerst op handmatig. Een optionele teksthelper bewaart het laatste resultaat, zijn geschiedenis de eerdere.",
        "heater_summer": "In de zomer heeft een verwarming niets te doen zodra de kamer de baktemperatuur of het instelpunt bereikt, en een test zou niets bewijzen: geef de kamertemperatuur en het instelpunt op, dan wordt de test overgeslagen en gemeld.",
        "relay_title": "Relaisbewaking",
        "relay_what": "`reef_relay_watch` waarschuwt u als een relais uit staat maar het apparaat nog verbruikt: een vastgeplakt contact of een contactdoos die niet meer gehoorzaamt. Elke vijf minuten controleert het elke contactdoos van de gekozen ReefControl-Power en elke poort van de gekozen ReefControl, plus toegevoegde slimme stekkers, en het ziet ook een contact dat lang na het uitschakelen vastplakt. Geen test, er wordt niets geschakeld.",
        "what_title": "Wat er bewaakt wordt",
        "what_maintenance": (
            "**Achterstallig onderhoud.** Elke knop met een `reef_role` die "
            "met `maint_` begint, met een melding zodra de `days_left` negatief "
            "wordt. Geen configuratie: de taken worden gevonden. Elke taak "
            "heeft een eigen meldingsschakelaar, standaard gerespecteerd, "
            "zodat u één klus kunt dempen zonder de rest."
        ),
        "what_unreachable": (
            "**Onbereikbare apparaten.** Een apparaat wordt gemeld wanneer al "
            "zijn entiteiten niet beschikbaar zijn. Hiervoor is een expliciete "
            "apparatenlijst nodig, en de reden is het weten waard: Home "
            "Assistant verwijdert de attributen van een niet-beschikbare "
            "entiteit, dus `reef_role` verdwijnt precies wanneer het apparaat "
            "uitvalt. Ontdekken kan hier niet, dus kiest u zelf."
        ),
        "notes_title": "Goed om te weten",
        "note_freq": (
            "De automatisering draait elke 5 minuten. Ze doorzoekt alleen het "
            "`button`-domein, dus de kosten groeien niet mee met de omvang van "
            "uw installatie."
        ),
        "note_tag": (
            "Eén melding per mobiel apparaat, getagd per apparaat en type "
            "melding: een nieuwe melding vervangt de vorige in plaats van zich "
            "op te stapelen."
        ),
        "note_throttle": (
            "Onderhoudsmeldingen worden opnieuw verstuurd met een "
            "instelbaar interval (1–24 u, standaard 4 u). Meldingen "
            "van onbereikbare apparaten worden slechts één keer "
            "verzonden (`alert_once`)."
        ),
        "note_ios": (
            "Het Android-kanaalveld wordt door iOS genegeerd. Laat het staan "
            "als u alleen iPhones gebruikt."
        ),
        "dev_title": "Ontwikkeling",
        "dev": (
            "`scripts/gen_blueprints.py` maakt de YAML-bestanden uit één "
            "sjabloon en één tekstentabel; `scripts/gen_readme.py` doet "
            "hetzelfde voor deze pagina. Bewerk de gegenereerde bestanden "
            "nooit: de CI genereert ze opnieuw en faalt als het resultaat "
            "afwijkt.\n\n"
            "`scripts/check_blueprints.py` vervangt de testsuite. Het leest "
            "elk bestand, vergelijkt de invoervelden met de Engelse referentie, "
            "controleert of elk veld aan een variabele is gekoppeld, en "
            "compileert de Jinja — een niet-gesloten tag laat zich anders "
            "alleen zien als een automatisering die stilletjes niet meer "
            "afgaat."
        ),
    },
    "pl": {
        "title": "Reef blueprints 🐬",
        "ecosystem_line": f"Część [**ekosystemu ReefTech**]({SITE})",
        "languages": "Dostępne języki",
        "intro": (
            "Blueprinty automatyzacji Home Assistant dla ekosystemu ReefTech. "
            "Powiadamiają na telefonie o **zaległych konserwacjach** i o "
            "**niedostępnych urządzeniach**, niezależnie od tego, z której "
            "integracji pochodzi sprzęt, **testują grzałki** pojedynczo i "
            "**nadzorują przekaźniki**, wykrywając urządzenie, które pobiera "
            "prąd po wyłączeniu."
        ),
        "why_title": "Dlaczego osobne repozytorium",
        "why": (
            "Zadania konserwacji publikują trzy integracje, więc blueprint "
            "który je obserwuje nie należy do żadnej w szczególności. Znajduje "
            "zadania przez wspólny atrybut `reef_role`, co oznacza, że "
            "przyszła integracja respektująca ten sam kontrakt będzie objęta "
            "bez publikowania tu czegokolwiek.\n\n"
            f"Alerty właściwe sprzętowi Red Sea — nietypowe tryby, kalibracje, "
            f"głowice ReefDose, czujniki ReefRun — zostają w "
            f"[**ReefBeat watch**]({BEAT}/tree/main/blueprints/automation), "
            "dostarczanym z integracją tworzącą te encje i wersjonowanym razem "
            "z nią."
        ),
        "install_title": "Instalacja",
        "install": (
            "Wybierz język i naciśnij przycisk. Home Assistant otworzy okno "
            "importu; blueprint pojawi się następnie w **Ustawienia → "
            "Automatyzacje i sceny → Blueprinty**."
        ),
        "install_note": (
            "Języki to osobne blueprinty: zaimportowanie dwóch daje dwa wpisy. "
            "Home Assistant nie ma mechanizmu tłumaczeń dla blueprintów — "
            "dlatego też ta strona jest generowana, a nie pisana osiem razy."
        ),
        "heater_title": "Test grzałek",
        "heater_what": "`reef_heater_test` sprawdza, czy każda grzałka sama utrzyma temperaturę w akwarium. Jedna grzałka pozostaje włączona, pozostałe są wyłączane na czas testu, po jednej grzałce na uruchomienie, po kolei. Wynik trafia na telefon. Przy zbyt dużym spadku lub poniżej temperatury przerwania test kończy się wcześniej i przywraca grzałki, a pierwszeństwo oddaje wszystkiemu innemu, co w tym czasie działa na grzałki.",
        "heater_safety": "Grzałki wyłączone po restarcie Home Assistant są włączane dwie minuty po uruchomieniu. Wyłączenie automatyzacji w trakcie testu to jedyny przypadek, z którego nie potrafi się ona podnieść: najpierw pozwól testowi się zakończyć. Aby uruchomić test samodzielnie, użyj przycisku **Uruchom** automatyzacji dla następnej grzałki w kolejce albo wyślij zdarzenie `reef_heater_test` z `heater: switch.twoja_grzalka`, aby wybrać konkretną.",
        "heater_power": "Licznik zamienia wynik w dowód, bo ciepłe pomieszczenie może ukryć uszkodzoną grzałkę. Jest wykrywany automatycznie dla gniazda Red Sea lub inteligentnej wtyczki: test odróżnia wtedy grzałkę uszkodzoną od zbyt słabej, nie daje wyniku, jeśli grzałka nigdy nie pobrała mocy, i sprawdza, czy wyłączone grzałki przestały pobierać moc. Grzałka na gnieździe podążającym za sondą lub harmonogramem jest odrzucana: najpierw przełącz gniazdo na tryb ręczny. Opcjonalny pomocnik tekstowy przechowuje ostatni wynik, a jego historia poprzednie.",
        "heater_summer": "Latem grzałka nie ma nic do roboty, gdy pomieszczenie osiągnie temperaturę akwarium lub nastawę, a test niczego by nie dowiódł: podaj temperaturę pomieszczenia i nastawę, a test zostanie pominięty i to zgłosi.",
        "relay_title": "Nadzór przekaźników",
        "relay_what": "`reef_relay_watch` ostrzega, gdy przekaźnik jest wyłączony, a urządzenie nadal pobiera moc: sklejony styk lub gniazdo, które przestało słuchać. Co pięć minut sprawdza każde gniazdo wybranych ReefControl-Power i każdy port wybranych ReefControl oraz dodane inteligentne wtyczki, a także wykrywa styk, który skleja się długo po wyłączeniu. Żadnego testu, nic nie jest przełączane.",
        "what_title": "Co jest obserwowane",
        "what_maintenance": (
            "**Zaległe konserwacje.** Każdy przycisk z `reef_role` "
            "zaczynającym się od `maint_`, z alertem gdy jego `days_left` "
            "stanie się ujemny. Bez konfiguracji: zadania są wykrywane. Każde "
            "zadanie ma własny przełącznik powiadomień, domyślnie "
            "respektowany, aby wyciszyć jedną pracę bez wyciszania reszty."
        ),
        "what_unreachable": (
            "**Niedostępne urządzenia.** Urządzenie jest zgłaszane, gdy "
            "wszystkie jego encje są niedostępne. To wymaga jawnej listy, a "
            "powód warto znać: Home Assistant usuwa atrybuty niedostępnej "
            "encji, więc `reef_role` znika dokładnie wtedy, gdy urządzenie "
            "przestaje odpowiadać. Wykrywanie jest tu niemożliwe, więc "
            "wybierasz sam."
        ),
        "notes_title": "Warto wiedzieć",
        "note_freq": (
            "Automatyzacja uruchamia się co 5 minut. Przeszukuje wyłącznie "
            "domenę `button`, więc koszt nie rośnie wraz z rozmiarem "
            "instalacji."
        ),
        "note_tag": (
            "Jedno powiadomienie na urządzenie mobilne, tagowane według "
            "urządzenia i typu alertu: nowy alert zastępuje poprzedni zamiast "
            "się nawarstwiać."
        ),
        "note_throttle": (
            "Alerty konserwacji są powtarzane w konfigurowalnym "
            "interwale (1–24 godz., domyślnie 4 godz.). Alerty "
            "niedostępnych urządzeń są wysyłane tylko raz "
            "(`alert_once`)."
        ),
        "note_ios": (
            "Pole kanału Androida jest ignorowane przez iOS. Zostaw je bez "
            "zmian, jeśli używasz tylko iPhone'ów."
        ),
        "dev_title": "Rozwój",
        "dev": (
            "`scripts/gen_blueprints.py` tworzy pliki YAML z jednego "
            "szablonu i jednej tabeli ciągów; `scripts/gen_readme.py` robi to "
            "samo dla tej strony. Nigdy nie edytuj plików generowanych: CI "
            "generuje je ponownie i kończy się błędem, jeśli wynik się "
            "różni.\n\n"
            "`scripts/check_blueprints.py` zastępuje zestaw testów. Parsuje "
            "każdy plik, porównuje wejścia z referencją angielską, sprawdza "
            "czy każde jest podpięte do zmiennej i kompiluje Jinja — "
            "niezamknięty tag inaczej objawiłby się tylko jako automatyzacja, "
            "która po cichu przestaje działać."
        ),
    },
    "pt": {
        "title": "Reef blueprints 🐬",
        "ecosystem_line": f"Parte do [**ecossistema ReefTech**]({SITE})",
        "languages": "Idiomas disponíveis",
        "intro": (
            "Blueprints de automação do Home Assistant para o ecossistema "
            "ReefTech. Avisam-no no telemóvel das **manutenções em atraso** e "
            "dos **aparelhos inacessíveis**, venha o seu equipamento da "
            "integração que vier, **testam os seus aquecedores** um a um e "
            "**vigiam os seus relés** para detetar um aparelho que continua a "
            "consumir depois de desligado."
        ),
        "why_title": "Porquê um repositório separado",
        "why": (
            "As tarefas de manutenção são publicadas por três integrações, "
            "por isso um blueprint que as vigie não pertence a nenhuma em "
            "particular. Encontra as tarefas pelo atributo comum `reef_role`, "
            "o que significa que uma integração futura que respeite o mesmo "
            "contrato ficará coberta sem republicar nada aqui.\n\n"
            f"Os avisos próprios do hardware Red Sea — modos anómalos, "
            f"calibrações, cabeças ReefDose, sensores ReefRun — ficam em "
            f"[**ReefBeat watch**]({BEAT}/tree/main/blueprints/automation), "
            "distribuído com a integração que produz essas entidades e "
            "versionado com ela."
        ),
        "install_title": "Instalação",
        "install": (
            "Escolha o seu idioma e prima o botão. O Home Assistant abre a "
            "caixa de importação; o blueprint aparece depois em "
            "**Definições → Automações e cenas → Blueprints**."
        ),
        "install_note": (
            "Os idiomas são blueprints distintos: importar dois dá-lhe duas "
            "entradas. O Home Assistant não tem mecanismo de tradução para "
            "blueprints, o que também explica por que esta página é gerada em "
            "vez de escrita oito vezes."
        ),
        "heater_title": "Teste dos aquecedores",
        "heater_what": "`reef_heater_test` verifica que cada aquecedor mantém o aquário sozinho. Um aquecedor fica ligado, os outros são desligados durante o teste, um aquecedor por execução, à vez. O resultado chega ao seu telemóvel. O teste para mais cedo e repõe os aquecedores perante uma descida excessiva ou abaixo da temperatura de interrupção, e cede a tudo o que entretanto atue sobre os aquecedores.",
        "heater_safety": "Os aquecedores que ficam desligados após um reinício do Home Assistant voltam a ligar-se dois minutos após o arranque. Desativar a automatização durante um teste é o único caso de que não consegue recuperar: deixe primeiro o teste terminar. Para iniciar um teste, use o botão **Executar** da automatização para o aquecedor seguinte da rotação, ou emita o evento `reef_heater_test` com `heater: switch.o_seu_aquecedor` para escolher um.",
        "heater_power": "Um medidor transforma o resultado numa prova, porque uma divisão quente pode esconder um aquecedor avariado. É encontrado automaticamente para uma tomada Red Sea ou uma tomada inteligente: o teste distingue então um aquecedor avariado de um insuficiente, não dá resultado se o aquecedor nunca consumiu e verifica que os aquecedores desligados deixam de consumir. Um aquecedor numa tomada que segue uma sonda ou um programa é recusado: passe primeiro a tomada para manual. Um auxiliar de texto opcional guarda o último resultado, e o seu histórico os anteriores.",
        "heater_summer": "No verão, um aquecedor não tem nada a fazer quando a divisão atinge a temperatura do aquário ou a consigna, e um teste não provaria nada: indique a temperatura da divisão e a consigna, e o teste é evitado e avisa disso.",
        "relay_title": "Vigilância de relés",
        "relay_what": "`reef_relay_watch` avisa quando um relé está desligado mas o aparelho continua a consumir: contacto colado ou uma tomada que já não obedece. A cada cinco minutos verifica cada tomada dos ReefControl-Power escolhidos e cada porta dos ReefControl escolhidos, além das tomadas inteligentes adicionadas, e deteta também um contacto que cola muito depois de desligar. Sem teste, nada é comutado.",
        "what_title": "O que é vigiado",
        "what_maintenance": (
            "**Manutenções em atraso.** Todos os botões com um `reef_role` "
            "começado por `maint_`, avisando quando o seu `days_left` fica "
            "negativo. Sem configuração: as tarefas são descobertas. Cada "
            "tarefa tem o seu próprio interruptor de notificação, respeitado "
            "por omissão, para silenciar um trabalho sem silenciar os "
            "restantes."
        ),
        "what_unreachable": (
            "**Aparelhos inacessíveis.** Um aparelho é assinalado quando todas "
            "as suas entidades estão indisponíveis. Este exige uma lista "
            "explícita, e a razão vale a pena: o Home Assistant remove os "
            "atributos de uma entidade indisponível, por isso o `reef_role` "
            "desaparece precisamente quando o aparelho cai. A descoberta é "
            "impossível aqui, por isso escolhe você."
        ),
        "notes_title": "Bom saber",
        "note_freq": (
            "A automação corre a cada 5 minutos. Percorre apenas o domínio "
            "`button`, portanto o custo não cresce com o tamanho da sua "
            "instalação."
        ),
        "note_tag": (
            "Uma notificação por telemóvel, etiquetada por aparelho e tipo de "
            "aviso: um aviso novo substitui o anterior em vez de se empilhar."
        ),
        "note_throttle": (
            "Os alertas de manutenção são reenviados num intervalo "
            "configurável (1–24 h, predefinido 4 h). Os alertas de "
            "aparelhos inacessíveis são enviados apenas uma vez "
            "(`alert_once`)."
        ),
        "note_ios": (
            "O campo de canal Android é ignorado pelo iOS. Deixe-o como está "
            "se só usar iPhones."
        ),
        "dev_title": "Desenvolvimento",
        "dev": (
            "`scripts/gen_blueprints.py` produz os ficheiros YAML a "
            "partir de um modelo e de uma tabela de cadeias; "
            "`scripts/gen_readme.py` faz o mesmo para esta página. Nunca edite "
            "os ficheiros gerados: a CI regenera-os e falha se o resultado "
            "diferir.\n\n"
            "`scripts/check_blueprints.py` faz as vezes da suite de testes. "
            "Analisa cada ficheiro, compara as entradas com a referência "
            "inglesa, verifica que cada uma está ligada a uma variável, e "
            "compila o Jinja — uma etiqueta desequilibrada só se veria, caso "
            "contrário, como uma automação que deixa de disparar."
        ),
    },
}

# Language names shown next to each import button, always in that language so
# a reader recognises their own without knowing the page's language.
NATIVE = {
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "es": "Español",
    "it": "Italiano",
    "nl": "Nederlands",
    "pl": "Polski",
    "pt": "Português",
}


def language_bar(current: str) -> str:
    """The flag row, with the current language shown but not linked."""
    parts = []
    for flag, code, path in LANGS:
        img = (
            f'<img src="https://flagicons.lipis.dev/flags/4x3/{flag}.svg" width="5%"/>'
        )
        parts.append(img if code == current else f"[{img}]({REPO}/blob/main/{path})")
    return " ".join(parts)


def import_buttons(slug: str) -> str:
    """One import badge per language, since blueprints are not translatable."""
    rows = ["| | |", "|---|---|"]
    for _, code, _ in LANGS:
        url = f"{RAW}/blueprints/automation/{slug}.{code}.yaml"
        badge = (
            "[![Open your Home Assistant instance and show the blueprint "
            "import dialog with a specific blueprint pre-filled.]"
            "(https://my.home-assistant.io/badges/blueprint_import.svg)]"
            f"(https://my.home-assistant.io/redirect/blueprint_import/"
            f"?blueprint_url={url})"
        )
        rows.append(f"| **{NATIVE[code]}** | {badge} |")
    return "\n".join(rows)


ECOSYSTEM_START = "<!-- ecosystem:start -->"
ECOSYSTEM_END = "<!-- ecosystem:end -->"


def preserve_ecosystem(existing: str, generated: str) -> str:
    """Carry an existing "Related projects" block into the new content.

    That block is written by reeftank/scripts/gen_ecosystem.py, which lives in
    another repository and is not available in CI. Without this, regenerating
    would silently drop it, and the workflow that checks the generated files
    are up to date would fail on every run.

    The block goes back where gen_ecosystem puts it: just before the first
    second-level heading.
    """
    start = existing.find(ECOSYSTEM_START)
    if start == -1:
        return generated
    end = existing.find(ECOSYSTEM_END)
    if end == -1:
        return generated
    block = existing[start : end + len(ECOSYSTEM_END)]

    at = generated.find("\n## ")
    if at == -1:
        return generated
    return generated[: at + 1] + block + "\n\n" + generated[at + 1 :]


def render(code: str) -> str:
    t = T[code]
    icon = f"{RAW}/icon.png"
    return f"""# {t["title"]}
> {t["ecosystem_line"]}
<p align="center">
  <img src="{icon}"  width="50%"/>
</p>

{BADGES}

# {t["languages"]}: {language_bar(code)}

{t["intro"]}

## {t["why_title"]}

{t["why"]}

## {t["install_title"]}

{t["install"]}

{import_buttons("reef_maintenance_notify")}

{t["install_note"]}

## {t["what_title"]}

- {t["what_maintenance"]}
- {t["what_unreachable"]}

## {t["heater_title"]}

{t["heater_what"]}

{t["heater_power"]}

{t["heater_summer"]}

{t["heater_safety"]}

{import_buttons("reef_heater_test")}

## {t["relay_title"]}

{t["relay_what"]}

{import_buttons("reef_relay_watch")}

## {t["notes_title"]}

- {t["note_freq"]}
- {t["note_tag"]}
- {t["note_throttle"]}
- {t["note_ios"]}

## {t["dev_title"]}

{t["dev"]}
"""


def main() -> None:
    missing = [
        (code, key)
        for _, code, _ in LANGS
        for key in T["en"]
        if key not in T.get(code, {})
    ]
    if missing:
        raise SystemExit(f"untranslated keys: {missing}")

    for _, code, path in LANGS:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        existing = target.read_text(encoding="utf-8") if target.exists() else ""
        target.write_text(preserve_ecosystem(existing, render(code)), encoding="utf-8")
        print("written", path)


if __name__ == "__main__":
    sys.exit(main())
