# Reef blueprints 🔔
> Parte dell'[**ecosistema ReefTech**](https://elwinmage.github.io/reeftank/)
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

# Lingue disponibili: [<img src="https://flagicons.lipis.dev/flags/4x3/gb.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/README.md) [<img src="https://flagicons.lipis.dev/flags/4x3/fr.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/fr/README.fr.md) [<img src="https://flagicons.lipis.dev/flags/4x3/de.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/de/README.de.md) [<img src="https://flagicons.lipis.dev/flags/4x3/es.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/es/README.es.md) <img src="https://flagicons.lipis.dev/flags/4x3/it.svg" width="5%"/> [<img src="https://flagicons.lipis.dev/flags/4x3/nl.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/nl/README.nl.md) [<img src="https://flagicons.lipis.dev/flags/4x3/pl.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/pl/README.pl.md) [<img src="https://flagicons.lipis.dev/flags/4x3/pt.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/pt/README.pt.md)

Blueprint di automazione Home Assistant per l'ecosistema ReefTech. Vi avvisano sul telefono delle **manutenzioni scadute** e dei **dispositivi irraggiungibili**, da qualunque integrazione provenga la vostra attrezzatura.

<!-- ecosystem:start -->

## Progetti correlati

I progetti ReefTech si incastrano tra loro: le integrazioni portano la tua attrezzatura in Home Assistant, la scheda la mostra e la pilota, e il backup la mantiene in funzione durante un blackout. Ognuno funziona anche da solo.

<table>
  <tr>
    <th width="100px"></th>
    <th>Progetto</th>
    <th>Ruolo</th>
    <th>Funziona con</th>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/main/icon.png" width="64" alt="ha-reefbeat-component" /></td>
    <td><a href="https://github.com/Elwinmage/ha-reefbeat-component"><b>ha-reefbeat-component</b></a></td>
    <td>Dispositivi Red Sea ReefBeat, pilotati in locale senza cloud: ReefATO+, ReefControl, ReefControl-Power, ReefDose, ReefLed, ReefMat, ReefRun e ReefWave.<br />blueprint di allerta per modalità anomale, calibrazioni e batteria scarica. <a href="https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/refs/heads/main/blueprints/automation/redsea_alerts.en.yaml"><img src="https://my.home-assistant.io/badges/blueprint_import.svg" alt="Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled." /></a></td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-aquamedic-component/main/icon.png" width="64" alt="ha-aquamedic-component" /></td>
    <td><a href="https://github.com/Elwinmage/ha-aquamedic-component"><b>ha-aquamedic-component</b></a></td>
    <td>Pompe Aqua Medic tramite l'API cloud Gizwits: pompe di movimento EcoDrift e SmartDrift, pompe DC Runner di risalita e dello schiumatoio.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-maintenance-component/main/icon.png" width="64" alt="ha-reef-maintenance-component" /></td>
    <td><a href="https://github.com/Elwinmage/ha-reef-maintenance-component"><b>ha-reef-maintenance-component</b></a></td>
    <td>Tracciamento di pulizia e usura per l'attrezzatura che Home Assistant non può interrogare: pompe di movimento, pompe di risalita, schiumatoi, reattori, tutto ciò che curi a mano.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-card/main/icon.png" width="64" alt="ha-reef-card" /></td>
    <td><a href="https://github.com/Elwinmage/ha-reef-card"><b>ha-reef-card</b></a></td>
    <td>Vista grafica interattiva di ogni dispositivo sulla tua dashboard, e unico modo per modificare le programmazioni avanzate. Legge le tre integrazioni tramite il contratto <code>reef_role</code> comune, senza configurazione lato scheda.</td>
    <td>tutte e tre le integrazioni</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/icon.png" width="64" alt="ha-reef-blueprints" /></td>
    <td><b>ha-reef-blueprints</b><br /><i>(questo repository)</i></td>
    <td>Blueprint di notifica comuni a tutto l'ecosistema: manutenzioni scadute trovate tramite il contratto <code>reef_role</code>, e dispositivi diventati irraggiungibili. Otto lingue.</td>
    <td>tutte e tre le integrazioni</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/reefbeatEnergyBackup/main/icon.png" width="64" alt="reefbeatEnergyBackup" /></td>
    <td><a href="https://github.com/Elwinmage/reefbeatEnergyBackup"><b>reefbeatEnergyBackup</b></a></td>
    <td>Backup a batteria in caso di blackout. Un pacco 24V LiFePO₄ gestito da un Raspberry Pi, con degrado progressivo della velocità delle pompe in base allo stato di carica.</td>
    <td>da solo, o insieme a ha-reefbeat-component</td>
  </tr>
</table>

Sono tutti documentati insieme sulla [pagina del progetto ReefTech](https://elwinmage.github.io/reeftank/).

<!-- ecosystem:end -->

## Perché un repository separato

Le attività di manutenzione sono pubblicate da tre integrazioni: un blueprint che le sorveglia non appartiene a nessuna in particolare. Trova le attività tramite l'attributo comune `reef_role`, il che significa che una futura integrazione che rispetti lo stesso contratto sarà coperta senza ripubblicare nulla qui.

Gli avvisi propri dell'hardware Red Sea — modalità anomale, calibrazioni, teste ReefDose, sensori ReefRun — restano in [**ReefBeat watch**](https://github.com/Elwinmage/ha-reefbeat-component/tree/main/blueprints/automation), distribuito con l'integrazione che produce quelle entità e versionato con essa.

## Installazione

Scegliete la lingua e premete il pulsante. Home Assistant apre la finestra di importazione; il blueprint compare poi in **Impostazioni → Automazioni e scene → Blueprint**.

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

Le lingue sono blueprint distinti: importarne due ne dà due. Home Assistant non ha alcun meccanismo di traduzione per i blueprint, ed è anche il motivo per cui questa pagina è generata invece di essere scritta otto volte.

## Cosa viene sorvegliato

- **Manutenzioni scadute.** Ogni pulsante con un `reef_role` che inizia per `maint_`, con avviso quando il suo `days_left` diventa negativo. Nessuna configurazione: le attività vengono trovate da sole. Ogni attività ha il proprio interruttore di notifica, rispettato per impostazione predefinita, così potete silenziarne una senza silenziare le altre.
- **Dispositivi irraggiungibili.** Un dispositivo viene segnalato quando tutte le sue entità sono non disponibili. Questo richiede un elenco esplicito, e il motivo merita di essere noto: Home Assistant rimuove gli attributi di un'entità non disponibile, quindi `reef_role` sparisce proprio quando il dispositivo cade. Qui la scoperta automatica è impossibile, quindi scegliete voi.

## Da sapere

- L'automazione gira ogni 5 minuti. Percorre solo il dominio `button`, quindi il costo non cresce con la dimensione della vostra installazione.
- Una notifica per dispositivo mobile, etichettata per dispositivo e tipo di avviso: un nuovo avviso sostituisce il precedente invece di accumularsi.
- Il campo canale Android è ignorato da iOS. Lasciatelo com'è se usate solo iPhone.

## Sviluppo

`scripts/gen_blueprints.py` produce gli otto file YAML da un modello e una tabella di stringhe; `scripts/gen_readme.py` fa lo stesso per questa pagina. Non modificate mai i file generati: la CI li rigenera e fallisce se il risultato differisce.

`scripts/check_blueprints.py` fa le veci della suite di test. Analizza ogni file, confronta gli input con il riferimento inglese, verifica che ciascuno sia collegato a una variabile, e compila il Jinja — un tag sbilanciato altrimenti si manifesta solo come un'automazione che smette di scattare.
