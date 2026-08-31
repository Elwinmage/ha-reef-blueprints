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
        "title": "Reef blueprints 🔔",
        "ecosystem_line": f"Part of the [**ReefTech Project Ecosystem**]({SITE})",
        "languages": "Supported Languages",
        "intro": (
            "Home Assistant automation blueprints for the ReefTech ecosystem. "
            "They notify you on your phone about **overdue maintenance** and "
            "**unreachable devices**, whichever integration your equipment "
            "comes from."
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
        "note_ios": (
            "The Android channel field is ignored by iOS. Leave it as is if "
            "you only use iPhones."
        ),
        "dev_title": "Development",
        "dev": (
            "`scripts/gen_blueprints.py` produces the eight YAML files from "
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
        "title": "Reef blueprints 🔔",
        "ecosystem_line": f"Fait partie de l'[**écosystème ReefTech**]({SITE})",
        "languages": "Langues disponibles",
        "intro": (
            "Blueprints d'automatisation Home Assistant pour l'écosystème "
            "ReefTech. Ils vous préviennent sur votre téléphone des "
            "**entretiens en retard** et des **appareils injoignables**, quelle "
            "que soit l'intégration dont vient votre matériel."
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
        "note_ios": (
            "Le champ canal Android est ignoré par iOS. Laissez-le tel quel si "
            "vous n'utilisez que des iPhone."
        ),
        "dev_title": "Développement",
        "dev": (
            "`scripts/gen_blueprints.py` produit les huit fichiers YAML depuis "
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
        "title": "Reef blueprints 🔔",
        "ecosystem_line": f"Teil des [**ReefTech Project Ecosystem**]({SITE})",
        "languages": "Verfügbare Sprachen",
        "intro": (
            "Home-Assistant-Automatisierungs-Blueprints für das "
            "ReefTech-Ökosystem. Sie benachrichtigen Sie auf dem Telefon über "
            "**überfällige Wartungen** und **nicht erreichbare Geräte**, "
            "unabhängig davon, aus welcher Integration Ihre Technik stammt."
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
        "note_ios": (
            "Das Android-Kanal-Feld wird von iOS ignoriert. Lassen Sie es "
            "unverändert, wenn Sie nur iPhones nutzen."
        ),
        "dev_title": "Entwicklung",
        "dev": (
            "`scripts/gen_blueprints.py` erzeugt die acht YAML-Dateien aus "
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
        "title": "Reef blueprints 🔔",
        "ecosystem_line": f"Parte del [**ecosistema ReefTech**]({SITE})",
        "languages": "Idiomas disponibles",
        "intro": (
            "Blueprints de automatización de Home Assistant para el ecosistema "
            "ReefTech. Le avisan en el móvil de los **mantenimientos "
            "vencidos** y de los **dispositivos no disponibles**, venga su "
            "equipo de la integración que venga."
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
        "note_ios": (
            "El campo de canal Android lo ignora iOS. Déjelo tal cual si solo "
            "usa iPhone."
        ),
        "dev_title": "Desarrollo",
        "dev": (
            "`scripts/gen_blueprints.py` produce los ocho ficheros YAML desde "
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
        "title": "Reef blueprints 🔔",
        "ecosystem_line": f"Parte dell'[**ecosistema ReefTech**]({SITE})",
        "languages": "Lingue disponibili",
        "intro": (
            "Blueprint di automazione Home Assistant per l'ecosistema "
            "ReefTech. Vi avvisano sul telefono delle **manutenzioni scadute** "
            "e dei **dispositivi irraggiungibili**, da qualunque integrazione "
            "provenga la vostra attrezzatura."
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
        "note_ios": (
            "Il campo canale Android è ignorato da iOS. Lasciatelo com'è se "
            "usate solo iPhone."
        ),
        "dev_title": "Sviluppo",
        "dev": (
            "`scripts/gen_blueprints.py` produce gli otto file YAML da un "
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
        "title": "Reef blueprints 🔔",
        "ecosystem_line": f"Onderdeel van het [**ReefTech Project Ecosystem**]({SITE})",
        "languages": "Beschikbare talen",
        "intro": (
            "Home Assistant automatiserings-blueprints voor het "
            "ReefTech-ecosysteem. Ze waarschuwen u op uw telefoon over "
            "**achterstallig onderhoud** en **onbereikbare apparaten**, uit "
            "welke integratie uw apparatuur ook komt."
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
        "note_ios": (
            "Het Android-kanaalveld wordt door iOS genegeerd. Laat het staan "
            "als u alleen iPhones gebruikt."
        ),
        "dev_title": "Ontwikkeling",
        "dev": (
            "`scripts/gen_blueprints.py` maakt de acht YAML-bestanden uit één "
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
        "title": "Reef blueprints 🔔",
        "ecosystem_line": f"Część [**ekosystemu ReefTech**]({SITE})",
        "languages": "Dostępne języki",
        "intro": (
            "Blueprinty automatyzacji Home Assistant dla ekosystemu ReefTech. "
            "Powiadamiają na telefonie o **zaległych konserwacjach** i o "
            "**niedostępnych urządzeniach**, niezależnie od tego, z której "
            "integracji pochodzi sprzęt."
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
        "note_ios": (
            "Pole kanału Androida jest ignorowane przez iOS. Zostaw je bez "
            "zmian, jeśli używasz tylko iPhone'ów."
        ),
        "dev_title": "Rozwój",
        "dev": (
            "`scripts/gen_blueprints.py` tworzy osiem plików YAML z jednego "
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
        "title": "Reef blueprints 🔔",
        "ecosystem_line": f"Parte do [**ecossistema ReefTech**]({SITE})",
        "languages": "Idiomas disponíveis",
        "intro": (
            "Blueprints de automação do Home Assistant para o ecossistema "
            "ReefTech. Avisam-no no telemóvel das **manutenções em atraso** e "
            "dos **aparelhos inacessíveis**, venha o seu equipamento da "
            "integração que vier."
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
        "note_ios": (
            "O campo de canal Android é ignorado pelo iOS. Deixe-o como está "
            "se só usar iPhones."
        ),
        "dev_title": "Desenvolvimento",
        "dev": (
            "`scripts/gen_blueprints.py` produz os oito ficheiros YAML a "
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


def import_buttons() -> str:
    """One import badge per language, since blueprints are not translatable."""
    rows = ["| | |", "|---|---|"]
    for _, code, _ in LANGS:
        url = f"{RAW}/blueprints/automation/reef_maintenance_notify.{code}.yaml"
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

{import_buttons()}

{t["install_note"]}

## {t["what_title"]}

- {t["what_maintenance"]}
- {t["what_unreachable"]}

## {t["notes_title"]}

- {t["note_freq"]}
- {t["note_tag"]}
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
