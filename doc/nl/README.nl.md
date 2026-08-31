# Reef blueprints 🔔
> Onderdeel van het [**ReefTech Project Ecosystem**](https://elwinmage.github.io/reeftank/)
<p align="center">
  <img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/icon.png"  width="50%"/>
</p>

[![GH-release](https://img.shields.io/github/v/release/Elwinmage/ha-reef-blueprints.svg?style=flat-square)](https://github.com/Elwinmage/ha-reef-blueprints/releases)
[![Ruff Status](https://github.com/Elwinmage/ha-reef-blueprints/actions/workflows/main.yml/badge.svg)](https://github.com/Elwinmage/ha-reef-blueprints/actions/workflows/main.yml)
[![Validate blueprints](https://github.com/Elwinmage/ha-reef-blueprints/actions/workflows/validate.yml/badge.svg)](https://github.com/Elwinmage/ha-reef-blueprints/actions/workflows/validate.yml)
[![GH-last-commit](https://img.shields.io/github/last-commit/Elwinmage/ha-reef-blueprints.svg?style=flat-square)](https://github.com/Elwinmage/ha-reef-blueprints/commits/main)
[![GitHub Clones](https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count&url=https://gist.githubusercontent.com/Elwinmage/b4d01d48acce8199974b015b9ea23b3b/raw/clone.json&logo=github)](https://github.com/MShawon/github-clone-count-badge)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![BuyMeCoffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat-square)](https://paypal.me/Elwinmage)

# Beschikbare talen: [<img src="https://flagicons.lipis.dev/flags/4x3/gb.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/README.md) [<img src="https://flagicons.lipis.dev/flags/4x3/fr.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/fr/README.fr.md) [<img src="https://flagicons.lipis.dev/flags/4x3/de.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/de/README.de.md) [<img src="https://flagicons.lipis.dev/flags/4x3/es.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/es/README.es.md) [<img src="https://flagicons.lipis.dev/flags/4x3/it.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/it/README.it.md) <img src="https://flagicons.lipis.dev/flags/4x3/nl.svg" width="5%"/> [<img src="https://flagicons.lipis.dev/flags/4x3/pl.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/pl/README.pl.md) [<img src="https://flagicons.lipis.dev/flags/4x3/pt.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/pt/README.pt.md)

Home Assistant automatiserings-blueprints voor het ReefTech-ecosysteem. Ze waarschuwen u op uw telefoon over **achterstallig onderhoud** en **onbereikbare apparaten**, uit welke integratie uw apparatuur ook komt.

<!-- ecosystem:start -->

## Verwante projecten

De ReefTech-projecten grijpen in elkaar: de integraties brengen uw apparatuur in Home Assistant, de kaart toont en bedient ze, en de back-up houdt alles draaiend tijdens een stroomuitval. Elk werkt ook op zichzelf.

<table>
  <tr>
    <th width="100px"></th>
    <th>Project</th>
    <th>Rol</th>
    <th>Werkt samen met</th>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/main/icon.png" width="64" alt="ha-reefbeat-component" /></td>
    <td><a href="https://github.com/Elwinmage/ha-reefbeat-component"><b>ha-reefbeat-component</b></a></td>
    <td>Red Sea ReefBeat-apparaten, lokaal aangestuurd zonder cloud: ReefATO+, ReefControl, ReefControl-Power, ReefDose, ReefLed, ReefMat, ReefRun en ReefWave.<br />blueprint met meldingen voor afwijkende modi, kalibraties en lage accu. <a href="https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/refs/heads/main/blueprints/automation/redsea_alerts.en.yaml"><img src="https://my.home-assistant.io/badges/blueprint_import.svg" alt="Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled." /></a></td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-aquamedic-component/main/icon.png" width="64" alt="ha-aquamedic-component" /></td>
    <td><a href="https://github.com/Elwinmage/ha-aquamedic-component"><b>ha-aquamedic-component</b></a></td>
    <td>Aqua Medic-pompen via de Gizwits-cloud-API: EcoDrift- en SmartDrift-stromingspompen, DC Runner opvoer- en afschuimerpompen.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-maintenance-component/main/icon.png" width="64" alt="ha-reef-maintenance-component" /></td>
    <td><a href="https://github.com/Elwinmage/ha-reef-maintenance-component"><b>ha-reef-maintenance-component</b></a></td>
    <td>Schoonmaak- en slijtageopvolging voor apparatuur die Home Assistant niet kan uitlezen: stromingspompen, opvoerpompen, eiwitafschuimers, reactoren, alles wat u met de hand onderhoudt.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-card/main/icon.png" width="64" alt="ha-reef-card" /></td>
    <td><a href="https://github.com/Elwinmage/ha-reef-card"><b>ha-reef-card</b></a></td>
    <td>Interactieve grafische weergave van elk apparaat op uw dashboard, en de enige manier om geavanceerde schema's te bewerken. Leest de drie integraties via het gedeelde <code>reef_role</code>-contract, zonder configuratie aan de kaartzijde.</td>
    <td>alle drie de integraties</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/icon.png" width="64" alt="ha-reef-blueprints" /></td>
    <td><b>ha-reef-blueprints</b><br /><i>(deze repository)</i></td>
    <td>Meldings-blueprints voor het hele ecosysteem: achterstallig onderhoud gevonden via het <code>reef_role</code>-contract, en apparaten die onbereikbaar zijn geworden. Acht talen.</td>
    <td>alle drie de integraties</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/reefbeatEnergyBackup/main/icon.png" width="64" alt="reefbeatEnergyBackup" /></td>
    <td><a href="https://github.com/Elwinmage/reefbeatEnergyBackup"><b>reefbeatEnergyBackup</b></a></td>
    <td>Accuback-up bij stroomuitval. Een 24V LiFePO₄-pakket aangestuurd door een Raspberry Pi, met de pompsnelheid die geleidelijk zakt met de laadtoestand.</td>
    <td>zelfstandig, of samen met ha-reefbeat-component</td>
  </tr>
</table>

Alles staat samen gedocumenteerd op de [ReefTech-projectpagina](https://elwinmage.github.io/reeftank/).

<!-- ecosystem:end -->

## Waarom een aparte repository

Onderhoudstaken worden door drie integraties gepubliceerd; een blueprint die ze bewaakt hoort bij geen van drieën in het bijzonder. Hij vindt de taken via het gedeelde `reef_role`-attribuut, waardoor een toekomstige integratie met hetzelfde contract gedekt is zonder dat hier iets opnieuw gepubliceerd hoeft te worden.

Meldingen die specifiek zijn voor Red Sea-apparatuur — afwijkende modi, kalibraties, ReefDose-koppen, ReefRun-sensoren — blijven in [**ReefBeat watch**](https://github.com/Elwinmage/ha-reefbeat-component/tree/main/blueprints/automation), meegeleverd met de integratie die die entiteiten maakt en daarmee mee versioneerd.

## Installatie

Kies uw taal en druk op de knop. Home Assistant opent het importvenster; de blueprint verschijnt daarna onder **Instellingen → Automatiseringen en scènes → Blueprints**.

| | |
|---|---|
| **English** | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/blueprints/automation/reef_maintenance_notify.en.yaml) |
| **Français** | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/blueprints/automation/reef_maintenance_notify.fr.yaml) |
| **Deutsch** | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/blueprints/automation/reef_maintenance_notify.de.yaml) |
| **Español** | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/blueprints/automation/reef_maintenance_notify.es.yaml) |
| **Italiano** | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/blueprints/automation/reef_maintenance_notify.it.yaml) |
| **Nederlands** | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/blueprints/automation/reef_maintenance_notify.nl.yaml) |
| **Polski** | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/blueprints/automation/reef_maintenance_notify.pl.yaml) |
| **Português** | [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/blueprints/automation/reef_maintenance_notify.pt.yaml) |

De talen zijn losse blueprints: wie er twee importeert krijgt er twee. Home Assistant heeft geen vertaalmechanisme voor blueprints, en ook daarom wordt deze pagina gegenereerd in plaats van acht keer geschreven.

## Wat er bewaakt wordt

- **Achterstallig onderhoud.** Elke knop met een `reef_role` die met `maint_` begint, met een melding zodra de `days_left` negatief wordt. Geen configuratie: de taken worden gevonden. Elke taak heeft een eigen meldingsschakelaar, standaard gerespecteerd, zodat u één klus kunt dempen zonder de rest.
- **Onbereikbare apparaten.** Een apparaat wordt gemeld wanneer al zijn entiteiten niet beschikbaar zijn. Hiervoor is een expliciete apparatenlijst nodig, en de reden is het weten waard: Home Assistant verwijdert de attributen van een niet-beschikbare entiteit, dus `reef_role` verdwijnt precies wanneer het apparaat uitvalt. Ontdekken kan hier niet, dus kiest u zelf.

## Goed om te weten

- De automatisering draait elke 5 minuten. Ze doorzoekt alleen het `button`-domein, dus de kosten groeien niet mee met de omvang van uw installatie.
- Eén melding per mobiel apparaat, getagd per apparaat en type melding: een nieuwe melding vervangt de vorige in plaats van zich op te stapelen.
- Het Android-kanaalveld wordt door iOS genegeerd. Laat het staan als u alleen iPhones gebruikt.

## Ontwikkeling

`scripts/gen_blueprints.py` maakt de acht YAML-bestanden uit één sjabloon en één tekstentabel; `scripts/gen_readme.py` doet hetzelfde voor deze pagina. Bewerk de gegenereerde bestanden nooit: de CI genereert ze opnieuw en faalt als het resultaat afwijkt.

`scripts/check_blueprints.py` vervangt de testsuite. Het leest elk bestand, vergelijkt de invoervelden met de Engelse referentie, controleert of elk veld aan een variabele is gekoppeld, en compileert de Jinja — een niet-gesloten tag laat zich anders alleen zien als een automatisering die stilletjes niet meer afgaat.
