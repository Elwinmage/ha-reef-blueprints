# Reef blueprints 🔔
> Parte del [**ecosistema ReefTech**](https://elwinmage.github.io/reeftank/)
<p align="center">
  <img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/icon.png"  width="50%"/>
</p>

[![GH-release](https://img.shields.io/github/v/release/Elwinmage/ha-reef-blueprints.svg?style=flat-square)](https://github.com/Elwinmage/ha-reef-blueprints/releases)
[![Ruff Status](https://github.com/Elwinmage/ha-reef-blueprints/actions/workflows/main.yml/badge.svg)](https://github.com/Elwinmage/ha-reef-blueprints/actions/workflows/main.yml)
[![Validate blueprints](https://github.com/Elwinmage/ha-reef-blueprints/actions/workflows/validate.yml/badge.svg)](https://github.com/Elwinmage/ha-reef-blueprints/actions/workflows/validate.yml)
[![GH-last-commit](https://img.shields.io/github/last-commit/Elwinmage/ha-reef-blueprints.svg?style=flat-square)](https://github.com/Elwinmage/ha-reef-blueprints/commits/main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![BuyMeCoffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=flat-square)](https://paypal.me/Elwinmage)

# Idiomas disponibles: [<img src="https://flagicons.lipis.dev/flags/4x3/gb.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/README.md) [<img src="https://flagicons.lipis.dev/flags/4x3/fr.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/fr/README.fr.md) [<img src="https://flagicons.lipis.dev/flags/4x3/de.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/de/README.de.md) <img src="https://flagicons.lipis.dev/flags/4x3/es.svg" width="5%"/> [<img src="https://flagicons.lipis.dev/flags/4x3/it.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/it/README.it.md) [<img src="https://flagicons.lipis.dev/flags/4x3/nl.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/nl/README.nl.md) [<img src="https://flagicons.lipis.dev/flags/4x3/pl.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/pl/README.pl.md) [<img src="https://flagicons.lipis.dev/flags/4x3/pt.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/pt/README.pt.md)

Blueprints de automatización de Home Assistant para el ecosistema ReefTech. Le avisan en el móvil de los **mantenimientos vencidos** y de los **dispositivos no disponibles**, venga su equipo de la integración que venga.

<!-- ecosystem:start -->

## Proyectos relacionados

Los proyectos ReefTech encajan entre sí: las integraciones traen tu equipo a Home Assistant, la tarjeta lo muestra y lo controla, y el respaldo lo mantiene en marcha durante un corte. Cada uno funciona también por su cuenta.

<table>
  <tr>
    <th width="100px"></th>
    <th>Proyecto</th>
    <th>Función</th>
    <th>Funciona con</th>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/main/icon.png" width="64" alt="ha-reefbeat-component" /></td>
    <td><a href="https://github.com/Elwinmage/ha-reefbeat-component"><b>ha-reefbeat-component</b></a></td>
    <td>Dispositivos Red Sea ReefBeat, controlados localmente sin cloud: ReefATO+, ReefControl, ReefControl-Power, ReefDose, ReefLed, ReefMat, ReefRun y ReefWave.<br />blueprint de alertas para modos anómalos, calibraciones y batería baja. <a href="https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/refs/heads/main/blueprints/automation/redsea_alerts.en.yaml"><img src="https://my.home-assistant.io/badges/blueprint_import.svg" alt="Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled." /></a></td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-aquamedic-component/main/icon.png" width="64" alt="ha-aquamedic-component" /></td>
    <td><a href="https://github.com/Elwinmage/ha-aquamedic-component"><b>ha-aquamedic-component</b></a></td>
    <td>Bombas Aqua Medic a través de la API cloud Gizwits: bombas de movimiento EcoDrift y SmartDrift, bombas DC Runner de retorno y de skimmer.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-maintenance-component/main/icon.png" width="64" alt="ha-reef-maintenance-component" /></td>
    <td><a href="https://github.com/Elwinmage/ha-reef-maintenance-component"><b>ha-reef-maintenance-component</b></a></td>
    <td>Seguimiento de limpieza y desgaste del equipo que Home Assistant no puede consultar: bombas de movimiento, bombas de retorno, skimmers, reactores, todo lo que mantienes a mano.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-card/main/icon.png" width="64" alt="ha-reef-card" /></td>
    <td><a href="https://github.com/Elwinmage/ha-reef-card"><b>ha-reef-card</b></a></td>
    <td>Vista gráfica interactiva de cada dispositivo en tu panel, y la única forma de editar programaciones avanzadas. Lee las tres integraciones mediante el contrato <code>reef_role</code> común, sin configuración del lado de la tarjeta.</td>
    <td>las tres integraciones</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/icon.png" width="64" alt="ha-reef-blueprints" /></td>
    <td><b>ha-reef-blueprints</b><br /><i>(este repositorio)</i></td>
    <td>Blueprints de notificación comunes a todo el ecosistema: mantenimientos vencidos encontrados por el contrato <code>reef_role</code>, y dispositivos que dejaron de responder. Ocho idiomas.</td>
    <td>las tres integraciones</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/reefbeatEnergyBackup/main/icon.png" width="64" alt="reefbeatEnergyBackup" /></td>
    <td><a href="https://github.com/Elwinmage/reefbeatEnergyBackup"><b>reefbeatEnergyBackup</b></a></td>
    <td>Respaldo por batería ante cortes de luz. Un pack 24V LiFePO₄ gobernado por una Raspberry Pi, con degradación progresiva de la velocidad de las bombas según el estado de carga.</td>
    <td>por su cuenta, o junto a ha-reefbeat-component</td>
  </tr>
</table>

Todos están documentados juntos en la [página del proyecto ReefTech](https://elwinmage.github.io/reeftank/).

<!-- ecosystem:end -->

## Por qué un repositorio aparte

Las tareas de mantenimiento las publican tres integraciones, así que un blueprint que las vigile no pertenece a ninguna en concreto. Encuentra las tareas por el atributo común `reef_role`, lo que significa que una integración futura que respete el mismo contrato quedará cubierta sin republicar nada aquí.

Los avisos propios del hardware Red Sea — modos anómalos, calibraciones, cabezales ReefDose, sensores ReefRun — se quedan en [**ReefBeat watch**](https://github.com/Elwinmage/ha-reefbeat-component/tree/main/blueprints/automation), distribuido con la integración que produce esas entidades y versionado con ella.

## Instalación

Elija su idioma y pulse el botón. Home Assistant abre el diálogo de importación; el blueprint aparece luego en **Ajustes → Automatizaciones y escenas → Blueprints**.

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

Los idiomas son blueprints distintos: importar dos le da dos entradas. Home Assistant no tiene mecanismo de traducción para blueprints, que es también por lo que esta página se genera en vez de escribirse ocho veces.

## Qué se vigila

- **Mantenimientos vencidos.** Todo botón con un `reef_role` que empieza por `maint_`, avisando cuando su `days_left` se vuelve negativo. Sin configuración: las tareas se descubren solas. Cada tarea tiene su propio interruptor de notificación, respetado por defecto, para silenciar un trabajo sin silenciar los demás.
- **Dispositivos no disponibles.** Se avisa de un dispositivo cuando todas sus entidades están no disponibles. Este necesita una lista explícita, y la razón vale la pena: Home Assistant elimina los atributos de una entidad no disponible, así que `reef_role` desaparece justo cuando el dispositivo cae. El descubrimiento es imposible aquí, así que elige usted.

## Conviene saber

- La automatización se ejecuta cada 5 minutos. Solo recorre el dominio `button`, así que el coste no crece con el tamaño de su instalación.
- Una notificación por móvil, etiquetada por dispositivo y tipo de aviso: un aviso nuevo sustituye al anterior en lugar de apilarse.
- El campo de canal Android lo ignora iOS. Déjelo tal cual si solo usa iPhone.

## Desarrollo

`scripts/gen_blueprints.py` produce los ocho ficheros YAML desde una plantilla y una tabla de cadenas; `scripts/gen_readme.py` hace lo mismo con esta página. No edite nunca los ficheros generados: la CI los regenera y falla si el resultado difiere.

`scripts/check_blueprints.py` hace las veces de suite de pruebas. Analiza cada fichero, compara las entradas con la referencia inglesa, comprueba que cada una está cableada a una variable, y compila el Jinja — una etiqueta desequilibrada solo se vería, si no, como una automatización que deja de dispararse.
