# Reef blueprints 🐬
> Część [**ekosystemu ReefTech**](https://elwinmage.github.io/reeftank/)
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

# Dostępne języki: [<img src="https://flagicons.lipis.dev/flags/4x3/gb.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/README.md) [<img src="https://flagicons.lipis.dev/flags/4x3/fr.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/fr/README.fr.md) [<img src="https://flagicons.lipis.dev/flags/4x3/de.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/de/README.de.md) [<img src="https://flagicons.lipis.dev/flags/4x3/es.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/es/README.es.md) [<img src="https://flagicons.lipis.dev/flags/4x3/it.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/it/README.it.md) [<img src="https://flagicons.lipis.dev/flags/4x3/nl.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/nl/README.nl.md) <img src="https://flagicons.lipis.dev/flags/4x3/pl.svg" width="5%"/> [<img src="https://flagicons.lipis.dev/flags/4x3/pt.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/pt/README.pt.md)

Blueprinty automatyzacji Home Assistant dla ekosystemu ReefTech. Powiadamiają na telefonie o **zaległych konserwacjach** i o **niedostępnych urządzeniach**, niezależnie od tego, z której integracji pochodzi sprzęt.

<!-- ecosystem:start -->

## Powiązane projekty

Projekty ReefTech uzupełniają się: integracje wprowadzają sprzęt do Home Assistant, karta go wyświetla i steruje nim, a zasilanie awaryjne utrzymuje go w ruchu podczas przerwy w zasilaniu. Każdy działa również samodzielnie.

<table>
  <tr>
    <th width="100px"></th>
    <th>Projekt</th>
    <th>Rola</th>
    <th>Współpracuje z</th>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/main/icon.png" width="64" alt="ha-reefbeat-component" /></td>
    <td>🐠<br /><a href="https://github.com/Elwinmage/ha-reefbeat-component"><b>ha-reefbeat-component</b></a></td>
    <td>Urządzenia Red Sea ReefBeat, sterowane lokalnie bez chmury: ReefATO+, ReefControl, ReefControl-Power, ReefDose, ReefLed, ReefMat, ReefRun i ReefWave.<br />blueprint alertów dla nietypowych trybów, kalibracji i niskiego poziomu baterii. <a href="https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/refs/heads/main/blueprints/automation/redsea_alerts.en.yaml"><img src="https://my.home-assistant.io/badges/blueprint_import.svg" alt="Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled." /></a></td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-aquamedic-component/main/icon.png" width="64" alt="ha-aquamedic-component" /></td>
    <td>🌊<br /><a href="https://github.com/Elwinmage/ha-aquamedic-component"><b>ha-aquamedic-component</b></a></td>
    <td>Pompy Aqua Medic przez chmurowe API Gizwits: pompy cyrkulacyjne EcoDrift i SmartDrift, pompy DC Runner obiegowe i do odpieniacza.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-maintenance-component/main/icon.png" width="64" alt="ha-reef-maintenance-component" /></td>
    <td>🐙<br /><a href="https://github.com/Elwinmage/ha-reef-maintenance-component"><b>ha-reef-maintenance-component</b></a></td>
    <td>Śledzenie czyszczenia i zużycia sprzętu, do którego Home Assistant nie ma dostępu: pompy cyrkulacyjne, pompy obiegowe, odpieniacze, reaktory, wszystko co obsługujesz ręcznie.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-card/main/icon.png" width="64" alt="ha-reef-card" /></td>
    <td>🪸<br /><a href="https://github.com/Elwinmage/ha-reef-card"><b>ha-reef-card</b></a></td>
    <td>Interaktywny widok graficzny każdego urządzenia na pulpicie i jedyny sposób edycji zaawansowanych harmonogramów. Odczytuje trzy integracje przez wspólny kontrakt <code>reef_role</code>, bez konfiguracji po stronie karty.</td>
    <td>wszystkie trzy integracje</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/icon.png" width="64" alt="ha-reef-blueprints" /></td>
    <td>🐬<br /><b>ha-reef-blueprints</b><br /><i>(to repozytorium)</i></td>
    <td>Blueprinty powiadomień wspólne dla całego ekosystemu: zaległe konserwacje znajdowane przez kontrakt <code>reef_role</code> oraz urządzenia, które przestały odpowiadać. Osiem języków.</td>
    <td>wszystkie trzy integracje</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/reefbeatEnergyBackup/main/icon.png" width="64" alt="reefbeatEnergyBackup" /></td>
    <td>⚡<br /><a href="https://github.com/Elwinmage/reefbeatEnergyBackup"><b>reefbeatEnergyBackup</b></a></td>
    <td>Zasilanie awaryjne na wypadek przerw w zasilaniu. Pakiet 24V LiFePO₄ sterowany przez Raspberry Pi, ze stopniowym obniżaniem prędkości pomp zależnie od stanu naładowania.</td>
    <td>samodzielnie lub razem z ha-reefbeat-component</td>
  </tr>
</table>

Wszystkie są udokumentowane razem na [stronie projektu ReefTech](https://elwinmage.github.io/reeftank/).

<!-- ecosystem:end -->

## Dlaczego osobne repozytorium

Zadania konserwacji publikują trzy integracje, więc blueprint który je obserwuje nie należy do żadnej w szczególności. Znajduje zadania przez wspólny atrybut `reef_role`, co oznacza, że przyszła integracja respektująca ten sam kontrakt będzie objęta bez publikowania tu czegokolwiek.

Alerty właściwe sprzętowi Red Sea — nietypowe tryby, kalibracje, głowice ReefDose, czujniki ReefRun — zostają w [**ReefBeat watch**](https://github.com/Elwinmage/ha-reefbeat-component/tree/main/blueprints/automation), dostarczanym z integracją tworzącą te encje i wersjonowanym razem z nią.

## Instalacja

Wybierz język i naciśnij przycisk. Home Assistant otworzy okno importu; blueprint pojawi się następnie w **Ustawienia → Automatyzacje i sceny → Blueprinty**.

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

Języki to osobne blueprinty: zaimportowanie dwóch daje dwa wpisy. Home Assistant nie ma mechanizmu tłumaczeń dla blueprintów — dlatego też ta strona jest generowana, a nie pisana osiem razy.

## Co jest obserwowane

- **Zaległe konserwacje.** Każdy przycisk z `reef_role` zaczynającym się od `maint_`, z alertem gdy jego `days_left` stanie się ujemny. Bez konfiguracji: zadania są wykrywane. Każde zadanie ma własny przełącznik powiadomień, domyślnie respektowany, aby wyciszyć jedną pracę bez wyciszania reszty.
- **Niedostępne urządzenia.** Urządzenie jest zgłaszane, gdy wszystkie jego encje są niedostępne. To wymaga jawnej listy, a powód warto znać: Home Assistant usuwa atrybuty niedostępnej encji, więc `reef_role` znika dokładnie wtedy, gdy urządzenie przestaje odpowiadać. Wykrywanie jest tu niemożliwe, więc wybierasz sam.

## Warto wiedzieć

- Automatyzacja uruchamia się co 5 minut. Przeszukuje wyłącznie domenę `button`, więc koszt nie rośnie wraz z rozmiarem instalacji.
- Jedno powiadomienie na urządzenie mobilne, tagowane według urządzenia i typu alertu: nowy alert zastępuje poprzedni zamiast się nawarstwiać.
- Pole kanału Androida jest ignorowane przez iOS. Zostaw je bez zmian, jeśli używasz tylko iPhone'ów.

## Rozwój

`scripts/gen_blueprints.py` tworzy osiem plików YAML z jednego szablonu i jednej tabeli ciągów; `scripts/gen_readme.py` robi to samo dla tej strony. Nigdy nie edytuj plików generowanych: CI generuje je ponownie i kończy się błędem, jeśli wynik się różni.

`scripts/check_blueprints.py` zastępuje zestaw testów. Parsuje każdy plik, porównuje wejścia z referencją angielską, sprawdza czy każde jest podpięte do zmiennej i kompiluje Jinja — niezamknięty tag inaczej objawiłby się tylko jako automatyzacja, która po cichu przestaje działać.
