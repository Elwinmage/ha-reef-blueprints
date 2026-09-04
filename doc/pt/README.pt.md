# Reef blueprints 🐬
> Parte do [**ecossistema ReefTech**](https://elwinmage.github.io/reeftank/)
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

# Idiomas disponíveis: [<img src="https://flagicons.lipis.dev/flags/4x3/gb.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/README.md) [<img src="https://flagicons.lipis.dev/flags/4x3/fr.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/fr/README.fr.md) [<img src="https://flagicons.lipis.dev/flags/4x3/de.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/de/README.de.md) [<img src="https://flagicons.lipis.dev/flags/4x3/es.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/es/README.es.md) [<img src="https://flagicons.lipis.dev/flags/4x3/it.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/it/README.it.md) [<img src="https://flagicons.lipis.dev/flags/4x3/nl.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/nl/README.nl.md) [<img src="https://flagicons.lipis.dev/flags/4x3/pl.svg" width="5%"/>](https://github.com/Elwinmage/ha-reef-blueprints/blob/main/doc/pl/README.pl.md) <img src="https://flagicons.lipis.dev/flags/4x3/pt.svg" width="5%"/>

Blueprints de automação do Home Assistant para o ecossistema ReefTech. Avisam-no no telemóvel das **manutenções em atraso** e dos **aparelhos inacessíveis**, venha o seu equipamento da integração que vier.

<!-- ecosystem:start -->

## Projetos relacionados

Os projetos ReefTech encaixam-se entre si: as integrações trazem o seu equipamento para o Home Assistant, o cartão mostra-o e comanda-o, e o backup mantém-no a funcionar durante um corte. Cada um funciona também sozinho.

<table>
  <tr>
    <th width="100px"></th>
    <th>Projeto</th>
    <th>Função</th>
    <th>Funciona com</th>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/main/icon.png" width="64" alt="ha-reefbeat-component" /></td>
    <td>🐠<br /><a href="https://github.com/Elwinmage/ha-reefbeat-component"><b>ha-reefbeat-component</b></a></td>
    <td>Aparelhos Red Sea ReefBeat, comandados localmente sem cloud: ReefATO+, ReefControl, ReefControl-Power, ReefDose, ReefLed, ReefMat, ReefRun e ReefWave.<br />blueprint de alertas para modos anómalos, calibrações e bateria fraca. <a href="https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https://raw.githubusercontent.com/Elwinmage/ha-reefbeat-component/refs/heads/main/blueprints/automation/redsea_alerts.en.yaml"><img src="https://my.home-assistant.io/badges/blueprint_import.svg" alt="Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled." /></a></td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-aquamedic-component/main/icon.png" width="64" alt="ha-aquamedic-component" /></td>
    <td>🌊<br /><a href="https://github.com/Elwinmage/ha-aquamedic-component"><b>ha-aquamedic-component</b></a></td>
    <td>Bombas Aqua Medic através da API cloud Gizwits: bombas de circulação EcoDrift e SmartDrift, bombas DC Runner de retorno e do escumador.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-maintenance-component/main/icon.png" width="64" alt="ha-reef-maintenance-component" /></td>
    <td>🐙<br /><a href="https://github.com/Elwinmage/ha-reef-maintenance-component"><b>ha-reef-maintenance-component</b></a></td>
    <td>Acompanhamento da limpeza e do desgaste do equipamento que o Home Assistant não consegue interrogar: bombas de circulação, bombas de retorno, escumadores, reatores, tudo o que trata à mão.</td>
    <td>ha-reef-card</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-card/main/icon.png" width="64" alt="ha-reef-card" /></td>
    <td>🪸<br /><a href="https://github.com/Elwinmage/ha-reef-card"><b>ha-reef-card</b></a></td>
    <td>Vista gráfica interativa de cada aparelho no seu painel, e a única forma de editar os programas avançados. Lê as três integrações através do contrato <code>reef_role</code> comum, sem configuração do lado do cartão.</td>
    <td>as três integrações</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/ha-reef-blueprints/main/icon.png" width="64" alt="ha-reef-blueprints" /></td>
    <td>🐬<br /><b>ha-reef-blueprints</b><br /><i>(este repositório)</i></td>
    <td>Blueprints de notificação comuns a todo o ecossistema: manutenções em atraso encontradas pelo contrato <code>reef_role</code>, e aparelhos que ficaram inacessíveis. Oito idiomas.</td>
    <td>as três integrações</td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/Elwinmage/reefbeatEnergyBackup/main/icon.png" width="64" alt="reefbeatEnergyBackup" /></td>
    <td>⚡<br /><a href="https://github.com/Elwinmage/reefbeatEnergyBackup"><b>reefbeatEnergyBackup</b></a></td>
    <td>Backup por bateria em caso de corte. Um pack 24V LiFePO₄ comandado por um Raspberry Pi, com degradação progressiva da velocidade das bombas conforme o estado de carga.</td>
    <td>sozinho, ou a par do ha-reefbeat-component</td>
  </tr>
</table>

Estão todos documentados em conjunto na [página do projeto ReefTech](https://elwinmage.github.io/reeftank/).

<!-- ecosystem:end -->

## Porquê um repositório separado

As tarefas de manutenção são publicadas por três integrações, por isso um blueprint que as vigie não pertence a nenhuma em particular. Encontra as tarefas pelo atributo comum `reef_role`, o que significa que uma integração futura que respeite o mesmo contrato ficará coberta sem republicar nada aqui.

Os avisos próprios do hardware Red Sea — modos anómalos, calibrações, cabeças ReefDose, sensores ReefRun — ficam em [**ReefBeat watch**](https://github.com/Elwinmage/ha-reefbeat-component/tree/main/blueprints/automation), distribuído com a integração que produz essas entidades e versionado com ela.

## Instalação

Escolha o seu idioma e prima o botão. O Home Assistant abre a caixa de importação; o blueprint aparece depois em **Definições → Automações e cenas → Blueprints**.

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

Os idiomas são blueprints distintos: importar dois dá-lhe duas entradas. O Home Assistant não tem mecanismo de tradução para blueprints, o que também explica por que esta página é gerada em vez de escrita oito vezes.

## O que é vigiado

- **Manutenções em atraso.** Todos os botões com um `reef_role` começado por `maint_`, avisando quando o seu `days_left` fica negativo. Sem configuração: as tarefas são descobertas. Cada tarefa tem o seu próprio interruptor de notificação, respeitado por omissão, para silenciar um trabalho sem silenciar os restantes.
- **Aparelhos inacessíveis.** Um aparelho é assinalado quando todas as suas entidades estão indisponíveis. Este exige uma lista explícita, e a razão vale a pena: o Home Assistant remove os atributos de uma entidade indisponível, por isso o `reef_role` desaparece precisamente quando o aparelho cai. A descoberta é impossível aqui, por isso escolhe você.

## Bom saber

- A automação corre a cada 5 minutos. Percorre apenas o domínio `button`, portanto o custo não cresce com o tamanho da sua instalação.
- Uma notificação por telemóvel, etiquetada por aparelho e tipo de aviso: um aviso novo substitui o anterior em vez de se empilhar.
- Os alertas de manutenção são reenviados num intervalo configurável (1–24 h, predefinido 4 h). Os alertas de aparelhos inacessíveis são enviados apenas uma vez (`alert_once`).
- O campo de canal Android é ignorado pelo iOS. Deixe-o como está se só usar iPhones.

## Desenvolvimento

`scripts/gen_blueprints.py` produz os oito ficheiros YAML a partir de um modelo e de uma tabela de cadeias; `scripts/gen_readme.py` faz o mesmo para esta página. Nunca edite os ficheiros gerados: a CI regenera-os e falha se o resultado diferir.

`scripts/check_blueprints.py` faz as vezes da suite de testes. Analisa cada ficheiro, compara as entradas com a referência inglesa, verifica que cada uma está ligada a uma variável, e compila o Jinja — uma etiqueta desequilibrada só se veria, caso contrário, como uma automação que deixa de disparar.
