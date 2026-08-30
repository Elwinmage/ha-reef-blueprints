#!/usr/bin/env python3
"""Generate the reef maintenance blueprint in the eight supported languages.

Usage, from the repository root::

    python3 scripts/gen_blueprints.py
    python3 scripts/check_blueprints.py

Home Assistant blueprints have no i18n mechanism: one file per language, each
imported separately. Writing them by hand means eight copies of the same 200
lines of Jinja drifting apart, so only the translatable strings live here and
the logic exists once.

Edit STRINGS and BODY below, never the generated YAML.
"""

from __future__ import annotations

import sys
from pathlib import Path

VERSION = "0.1.0"
REPO = "https://github.com/Elwinmage/ha-reef-blueprints"
OUT = Path("blueprints/automation")

LANGS = ["en", "fr", "de", "es", "it", "nl", "pl", "pt"]

# ---------------------------------------------------------------------------
# Logic, shared by every language.
#
# Two checks, deliberately built on different foundations:
#
#   * Maintenance uses the `reef_role` attribute, so any integration that
#     publishes the contract is covered without touching this file.
#
#   * Reachability cannot: Home Assistant drops extra_state_attributes from an
#     unavailable entity, so `reef_role` vanishes exactly when the device goes
#     offline. It therefore works from a device list the user picks, which is
#     also why there is no "exclude" selector -- you choose what to watch.
# ---------------------------------------------------------------------------

BODY = """
trigger:
  - platform: time_pattern
    minutes: "/5"

variables:
  notify_devices: !input notify_devices
  notify_channel: !input notify_channel
  notify_maintenance: !input notify_maintenance
  maintenance_respect_switch: !input maintenance_respect_switch
  notify_unavailable: !input notify_unavailable
  watched_devices: !input watched_devices
  # The shared contract. Every integration of the ecosystem tags its
  # maintenance buttons with a reef_role starting with this prefix.
  role_maintenance_prefix: "maint_"

action:
  - alias: "Build the alerts list"
    variables:
      alerts: >
        {%- set ns = namespace(items=[]) -%}

        {#- 1) Maintenance overdue.
            Scans the button domain only: a maintenance task is always a
            button, and iterating one domain instead of the whole state
            machine keeps this cheap at every run. -#}
        {%- if notify_maintenance -%}
          {%- for e in states.button -%}
            {%- set role = e.attributes.get('reef_role') or '' -%}
            {%- if role.startswith(role_maintenance_prefix) -%}
              {#- Per-task opt-out: the button mirrors its companion notify
                  switch in the `notify` attribute. A missing attribute is
                  treated as enabled, so an older integration still works. -#}
              {%- set notify_flag = e.attributes.get('notify') -%}
              {%- set muted = maintenance_respect_switch and notify_flag is false -%}
              {%- set dl = e.attributes.get('days_left') -%}
              {%- if dl is number and dl < 0 and not muted -%}
                {%- set d = device_id(e.entity_id) -%}
                {%- set dname = (d and (device_attr(d, 'name_by_user')
                                        or device_attr(d, 'name')))
                                or e.entity_id -%}
                {%- set ns.items = ns.items + [{
                  'type': 'maintenance',
                  'device': dname,
                  'message': MSG_OVERDUE,
                }] -%}
              {%- endif -%}
            {%- endif -%}
          {%- endfor -%}
        {%- endif -%}

        {#- 2) Unreachable devices: every entity of a watched device is
            unavailable. Driven by the picked list rather than by reef_role,
            which an unavailable entity no longer exposes. -#}
        {%- if notify_unavailable -%}
          {%- for d in watched_devices -%}
            {%- set dents = device_entities(d) -%}
            {%- set total = dents | count -%}
            {%- set unav = dents | select('is_state', 'unavailable') | list | count -%}
            {%- if total > 0 and unav == total -%}
              {%- set ns.items = ns.items + [{
                'type': 'unreachable',
                'device': device_attr(d, 'name_by_user')
                          or device_attr(d, 'name') or d,
                'message': MSG_UNREACHABLE,
              }] -%}
            {%- endif -%}
          {%- endfor -%}
        {%- endif -%}

        {{ ns.items }}

  - alias: "Notify for each alert"
    if:
      - "{{ alerts | length > 0 }}"
    then:
      - repeat:
          for_each: "{{ alerts }}"
          sequence:
            - variables:
                title: "TITLE_PREFIX{{ repeat.item.device }}"
                message: "{{ repeat.item.message }}"
                # Unique tag per (device, alert type) so a new notification
                # replaces the previous one instead of stacking.
                notif_tag: "reef_{{ repeat.item.device }}_{{ repeat.item.type }}"
            - alias: "Dispatch to each selected mobile device"
              repeat:
                for_each: "{{ notify_devices }}"
                sequence:
                  - variables:
                      # `name`, not `name_by_user`: the notify service slug is
                      # frozen at install time and ignores later renames in the
                      # Home Assistant UI.
                      mobile_slug: >-
                        {{ (device_attr(repeat.item, 'name')
                            or repeat.item) | slugify }}
                  - service: "notify.mobile_app_{{ mobile_slug }}"
                    data:
                      title: "{{ title }}"
                      message: "{{ message }}"
                      data: >-
                        {{
                          {
                            'tag': notif_tag,
                            'channel': notify_channel
                          } if notify_channel else {'tag': notif_tag}
                        }}
"""

# ---------------------------------------------------------------------------
# Translations
# ---------------------------------------------------------------------------

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "name": "Reef maintenance watch",
        "description": (
            "Notifies you about **overdue maintenance** on any integration of "
            "the ReefTech ecosystem, and about **devices that went "
            "unreachable**.\\n\\n"
            "Maintenance detection needs no configuration: it finds the tasks "
            "through the `reef_role` attribute, so ha-reefbeat-component, "
            "ha-aquamedic-component and ha-reef-maintenance-component are all "
            "covered, and so is any future integration publishing the same "
            "contract.\\n\\n"
            "Reachability works from the device list you pick below. Home "
            "Assistant hides the attributes of an unavailable entity, so this "
            "check cannot discover devices on its own."
        ),
        "notify_section": "Notification targets",
        "notify_devices": "Mobile devices to notify",
        "notify_devices_desc": (
            "The device(s) that receive the notifications. Only phones and "
            "tablets registered through the Home Assistant Companion app are "
            "listed. One notification is sent per device."
        ),
        "notify_channel": "Android channel (optional)",
        "notify_channel_desc": (
            "Channel name passed in `data.channel`, to group these "
            "notifications and give them their own sound or priority. Leave "
            "empty for the default channel. iOS ignores this field."
        ),
        "maintenance_section": "Maintenance overdue",
        "notify_maintenance": "Enable",
        "notify_maintenance_desc": (
            "Watches every button carrying a `reef_role` that starts with "
            "`maint_`, and alerts when its `days_left` goes negative."
        ),
        "respect_switch": "Respect the per-task notification switches",
        "respect_switch_desc": (
            "When enabled, a task whose «(notifications)» switch is off is "
            "skipped even when overdue. Leave it on unless you want the alert "
            "regardless of the switches."
        ),
        "unreachable_section": "Unreachable devices",
        "notify_unavailable": "Enable",
        "watched_devices": "Devices to watch",
        "watched_devices_desc": (
            "A device is reported unreachable when all of its entities are "
            "unavailable. The list is explicit because an unavailable entity "
            "no longer exposes the `reef_role` attribute this blueprint would "
            "otherwise use to find it. Leave empty to disable the check."
        ),
        "msg_overdue": "Maintenance overdue by {days} days: {task}",
        "msg_unreachable": "Device unreachable",
        "title_prefix": "Reef — ",
    },
    "fr": {
        "name": "Surveillance maintenance récif",
        "description": (
            "Vous prévient des **entretiens en retard** sur toutes les "
            "intégrations de l'écosystème ReefTech, et des **appareils devenus "
            "injoignables**.\\n\\n"
            "La détection des entretiens ne demande aucune configuration : "
            "elle trouve les tâches par l'attribut `reef_role`, donc "
            "ha-reefbeat-component, ha-aquamedic-component et "
            "ha-reef-maintenance-component sont couverts, ainsi que toute "
            "future intégration publiant le même contrat.\\n\\n"
            "L'injoignabilité s'appuie sur la liste d'appareils que vous "
            "choisissez ci-dessous. Home Assistant masque les attributs d'une "
            "entité indisponible : ce contrôle ne peut donc pas découvrir les "
            "appareils tout seul."
        ),
        "notify_section": "Destinataires des notifications",
        "notify_devices": "Mobiles à notifier",
        "notify_devices_desc": (
            "Le ou les appareils qui recevront les notifications. Seuls les "
            "téléphones et tablettes enregistrés via l'application Home "
            "Assistant apparaissent. Une notification est envoyée par appareil."
        ),
        "notify_channel": "Canal Android (optionnel)",
        "notify_channel_desc": (
            "Nom de canal passé dans `data.channel`, pour regrouper ces "
            "notifications et leur donner un son ou une priorité propres. "
            "Laissez vide pour le canal par défaut. iOS ignore ce champ."
        ),
        "maintenance_section": "Entretien en retard",
        "notify_maintenance": "Activer",
        "notify_maintenance_desc": (
            "Surveille chaque bouton portant un `reef_role` commençant par "
            "`maint_`, et alerte quand son `days_left` devient négatif."
        ),
        "respect_switch": "Respecter les interrupteurs de notification par tâche",
        "respect_switch_desc": (
            "Si activé, une tâche dont l'interrupteur « (notifications) » est "
            "coupé est ignorée même en retard. Laissez activé, sauf si vous "
            "voulez l'alerte quels que soient les interrupteurs."
        ),
        "unreachable_section": "Appareils injoignables",
        "notify_unavailable": "Activer",
        "watched_devices": "Appareils à surveiller",
        "watched_devices_desc": (
            "Un appareil est signalé injoignable quand toutes ses entités sont "
            "indisponibles. La liste est explicite car une entité indisponible "
            "n'expose plus l'attribut `reef_role` qui aurait permis de la "
            "trouver. Laissez vide pour désactiver ce contrôle."
        ),
        "msg_overdue": "Entretien en retard de {days} jours : {task}",
        "msg_unreachable": "Appareil injoignable",
        "title_prefix": "Récif — ",
    },
    "de": {
        "name": "Riff-Wartungsüberwachung",
        "description": (
            "Benachrichtigt Sie über **überfällige Wartungen** in allen "
            "Integrationen des ReefTech-Ökosystems und über **nicht mehr "
            "erreichbare Geräte**.\\n\\n"
            "Die Wartungserkennung braucht keine Konfiguration: sie findet die "
            "Aufgaben über das `reef_role`-Attribut, also sind "
            "ha-reefbeat-component, ha-aquamedic-component und "
            "ha-reef-maintenance-component abgedeckt, ebenso jede künftige "
            "Integration mit demselben Vertrag.\\n\\n"
            "Die Erreichbarkeit stützt sich auf die unten gewählte Geräteliste. "
            "Home Assistant blendet die Attribute einer nicht verfügbaren "
            "Entität aus, diese Prüfung kann Geräte daher nicht selbst finden."
        ),
        "notify_section": "Benachrichtigungsziele",
        "notify_devices": "Zu benachrichtigende Mobilgeräte",
        "notify_devices_desc": (
            "Die Geräte, die die Benachrichtigungen erhalten. Es werden nur "
            "Telefone und Tablets angezeigt, die über die Home Assistant "
            "Companion App registriert sind. Pro Gerät wird eine "
            "Benachrichtigung gesendet."
        ),
        "notify_channel": "Android-Kanal (optional)",
        "notify_channel_desc": (
            "In `data.channel` übergebener Kanalname, um diese "
            "Benachrichtigungen zu gruppieren und ihnen eigenen Ton oder "
            "eigene Priorität zu geben. Leer lassen für den Standardkanal. iOS "
            "ignoriert dieses Feld."
        ),
        "maintenance_section": "Überfällige Wartung",
        "notify_maintenance": "Aktivieren",
        "notify_maintenance_desc": (
            "Überwacht jede Schaltfläche mit einer `reef_role`, die mit "
            "`maint_` beginnt, und meldet, wenn ihr `days_left` negativ wird."
        ),
        "respect_switch": "Die Benachrichtigungsschalter je Aufgabe beachten",
        "respect_switch_desc": (
            "Wenn aktiviert, wird eine Aufgabe, deren Schalter "
            "«(Benachrichtigungen)» aus ist, auch bei Überfälligkeit "
            "übersprungen. Aktiviert lassen, außer Sie wollen die Meldung "
            "unabhängig von den Schaltern."
        ),
        "unreachable_section": "Nicht erreichbare Geräte",
        "notify_unavailable": "Aktivieren",
        "watched_devices": "Zu überwachende Geräte",
        "watched_devices_desc": (
            "Ein Gerät gilt als nicht erreichbar, wenn alle seine Entitäten "
            "nicht verfügbar sind. Die Liste ist ausdrücklich, weil eine nicht "
            "verfügbare Entität das `reef_role`-Attribut nicht mehr zeigt, über "
            "das sie sonst gefunden würde. Leer lassen, um die Prüfung zu "
            "deaktivieren."
        ),
        "msg_overdue": "Wartung {days} Tage überfällig: {task}",
        "msg_unreachable": "Gerät nicht erreichbar",
        "title_prefix": "Riff — ",
    },
    "es": {
        "name": "Vigilancia de mantenimiento del arrecife",
        "description": (
            "Le avisa de los **mantenimientos vencidos** en cualquier "
            "integración del ecosistema ReefTech, y de los **dispositivos que "
            "han dejado de responder**.\\n\\n"
            "La detección de mantenimientos no necesita configuración: "
            "encuentra las tareas por el atributo `reef_role`, así que "
            "ha-reefbeat-component, ha-aquamedic-component y "
            "ha-reef-maintenance-component quedan cubiertos, y también "
            "cualquier integración futura que publique el mismo contrato.\\n\\n"
            "La disponibilidad se apoya en la lista de dispositivos que elija "
            "más abajo. Home Assistant oculta los atributos de una entidad no "
            "disponible, así que esta comprobación no puede descubrirlos sola."
        ),
        "notify_section": "Destinatarios de las notificaciones",
        "notify_devices": "Móviles a notificar",
        "notify_devices_desc": (
            "Los dispositivos que recibirán las notificaciones. Solo aparecen "
            "los teléfonos y tabletas registrados con la app Home Assistant. Se "
            "envía una notificación por dispositivo."
        ),
        "notify_channel": "Canal de Android (opcional)",
        "notify_channel_desc": (
            "Nombre de canal pasado en `data.channel`, para agrupar estas "
            "notificaciones y darles su propio sonido o prioridad. Déjelo vacío "
            "para el canal por defecto. iOS ignora este campo."
        ),
        "maintenance_section": "Mantenimiento vencido",
        "notify_maintenance": "Activar",
        "notify_maintenance_desc": (
            "Vigila cada botón con un `reef_role` que empiece por `maint_`, y "
            "avisa cuando su `days_left` se vuelve negativo."
        ),
        "respect_switch": "Respetar los interruptores de notificación por tarea",
        "respect_switch_desc": (
            "Si está activado, una tarea cuyo interruptor «(notificaciones)» "
            "esté apagado se omite aunque esté vencida. Déjelo activado salvo "
            "que quiera el aviso pase lo que pase."
        ),
        "unreachable_section": "Dispositivos no disponibles",
        "notify_unavailable": "Activar",
        "watched_devices": "Dispositivos a vigilar",
        "watched_devices_desc": (
            "Un dispositivo se señala como no disponible cuando todas sus "
            "entidades lo están. La lista es explícita porque una entidad no "
            "disponible ya no expone el atributo `reef_role` que habría "
            "permitido encontrarla. Déjela vacía para desactivar la "
            "comprobación."
        ),
        "msg_overdue": "Mantenimiento vencido hace {days} días: {task}",
        "msg_unreachable": "Dispositivo no disponible",
        "title_prefix": "Arrecife — ",
    },
    "it": {
        "name": "Sorveglianza manutenzione barriera",
        "description": (
            "Vi avvisa delle **manutenzioni scadute** su qualunque integrazione "
            "dell'ecosistema ReefTech e dei **dispositivi diventati "
            "irraggiungibili**.\\n\\n"
            "Il rilevamento delle manutenzioni non richiede configurazione: "
            "trova le attività tramite l'attributo `reef_role`, quindi "
            "ha-reefbeat-component, ha-aquamedic-component e "
            "ha-reef-maintenance-component sono coperti, così come ogni futura "
            "integrazione che pubblichi lo stesso contratto.\\n\\n"
            "La raggiungibilità si basa sull'elenco di dispositivi che "
            "scegliete qui sotto. Home Assistant nasconde gli attributi di "
            "un'entità non disponibile, quindi questo controllo non può "
            "scoprirli da solo."
        ),
        "notify_section": "Destinatari delle notifiche",
        "notify_devices": "Dispositivi mobili da notificare",
        "notify_devices_desc": (
            "I dispositivi che riceveranno le notifiche. Compaiono solo "
            "telefoni e tablet registrati tramite l'app Home Assistant. Viene "
            "inviata una notifica per dispositivo."
        ),
        "notify_channel": "Canale Android (facoltativo)",
        "notify_channel_desc": (
            "Nome del canale passato in `data.channel`, per raggruppare queste "
            "notifiche e dare loro suono o priorità propri. Lasciate vuoto per "
            "il canale predefinito. iOS ignora questo campo."
        ),
        "maintenance_section": "Manutenzione scaduta",
        "notify_maintenance": "Attiva",
        "notify_maintenance_desc": (
            "Sorveglia ogni pulsante con un `reef_role` che inizia per "
            "`maint_`, e avvisa quando il suo `days_left` diventa negativo."
        ),
        "respect_switch": "Rispetta gli interruttori di notifica per attività",
        "respect_switch_desc": (
            "Se attivo, un'attività il cui interruttore «(notifiche)» è spento "
            "viene saltata anche se scaduta. Lasciate attivo, a meno che non "
            "vogliate l'avviso a prescindere dagli interruttori."
        ),
        "unreachable_section": "Dispositivi irraggiungibili",
        "notify_unavailable": "Attiva",
        "watched_devices": "Dispositivi da sorvegliare",
        "watched_devices_desc": (
            "Un dispositivo è segnalato irraggiungibile quando tutte le sue "
            "entità sono non disponibili. L'elenco è esplicito perché "
            "un'entità non disponibile non espone più l'attributo `reef_role` "
            "che avrebbe permesso di trovarla. Lasciate vuoto per disattivare "
            "il controllo."
        ),
        "msg_overdue": "Manutenzione scaduta da {days} giorni: {task}",
        "msg_unreachable": "Dispositivo irraggiungibile",
        "title_prefix": "Barriera — ",
    },
    "nl": {
        "name": "Rif-onderhoudsbewaking",
        "description": (
            "Waarschuwt u voor **achterstallig onderhoud** in elke integratie "
            "van het ReefTech-ecosysteem, en voor **apparaten die onbereikbaar "
            "zijn geworden**.\\n\\n"
            "De onderhoudsdetectie vergt geen configuratie: ze vindt de taken "
            "via het `reef_role`-attribuut, dus ha-reefbeat-component, "
            "ha-aquamedic-component en ha-reef-maintenance-component zijn "
            "gedekt, net als elke toekomstige integratie met hetzelfde "
            "contract.\\n\\n"
            "De bereikbaarheid werkt met de apparatenlijst die u hieronder "
            "kiest. Home Assistant verbergt de attributen van een niet-"
            "beschikbare entiteit, dus deze controle kan apparaten niet zelf "
            "ontdekken."
        ),
        "notify_section": "Ontvangers van meldingen",
        "notify_devices": "Te waarschuwen mobiele apparaten",
        "notify_devices_desc": (
            "De apparaten die de meldingen ontvangen. Alleen telefoons en "
            "tablets die via de Home Assistant Companion-app zijn "
            "geregistreerd verschijnen hier. Er wordt één melding per apparaat "
            "verstuurd."
        ),
        "notify_channel": "Android-kanaal (optioneel)",
        "notify_channel_desc": (
            "Kanaalnaam die in `data.channel` wordt meegegeven, om deze "
            "meldingen te groeperen en een eigen geluid of prioriteit te geven. "
            "Laat leeg voor het standaardkanaal. iOS negeert dit veld."
        ),
        "maintenance_section": "Achterstallig onderhoud",
        "notify_maintenance": "Inschakelen",
        "notify_maintenance_desc": (
            "Bewaakt elke knop met een `reef_role` die met `maint_` begint, en "
            "waarschuwt zodra de `days_left` negatief wordt."
        ),
        "respect_switch": "Respecteer de meldingsschakelaars per taak",
        "respect_switch_desc": (
            "Indien ingeschakeld wordt een taak waarvan de schakelaar "
            "«(meldingen)» uit staat overgeslagen, ook bij achterstand. Laat "
            "aan staan, tenzij u de melding hoe dan ook wilt."
        ),
        "unreachable_section": "Onbereikbare apparaten",
        "notify_unavailable": "Inschakelen",
        "watched_devices": "Te bewaken apparaten",
        "watched_devices_desc": (
            "Een apparaat geldt als onbereikbaar wanneer al zijn entiteiten "
            "niet beschikbaar zijn. De lijst is expliciet omdat een niet-"
            "beschikbare entiteit het `reef_role`-attribuut niet meer toont "
            "waarmee ze anders gevonden zou worden. Laat leeg om de controle "
            "uit te zetten."
        ),
        "msg_overdue": "Onderhoud {days} dagen achterstallig: {task}",
        "msg_unreachable": "Apparaat onbereikbaar",
        "title_prefix": "Rif — ",
    },
    "pl": {
        "name": "Monitor konserwacji rafy",
        "description": (
            "Powiadamia o **zaległych konserwacjach** w każdej integracji "
            "ekosystemu ReefTech oraz o **urządzeniach, które przestały "
            "odpowiadać**.\\n\\n"
            "Wykrywanie konserwacji nie wymaga konfiguracji: znajduje zadania "
            "przez atrybut `reef_role`, więc ha-reefbeat-component, "
            "ha-aquamedic-component i ha-reef-maintenance-component są objęte, "
            "podobnie jak każda przyszła integracja publikująca ten sam "
            "kontrakt.\\n\\n"
            "Dostępność opiera się na liście urządzeń wybranej poniżej. Home "
            "Assistant ukrywa atrybuty niedostępnej encji, więc ta kontrola nie "
            "potrafi sama ich odnaleźć."
        ),
        "notify_section": "Odbiorcy powiadomień",
        "notify_devices": "Urządzenia mobilne do powiadomienia",
        "notify_devices_desc": (
            "Urządzenia, które otrzymają powiadomienia. Wyświetlane są tylko "
            "telefony i tablety zarejestrowane w aplikacji Home Assistant. Na "
            "każde urządzenie wysyłane jest jedno powiadomienie."
        ),
        "notify_channel": "Kanał Androida (opcjonalnie)",
        "notify_channel_desc": (
            "Nazwa kanału przekazywana w `data.channel`, aby zgrupować te "
            "powiadomienia i nadać im własny dźwięk lub priorytet. Zostaw puste "
            "dla kanału domyślnego. iOS ignoruje to pole."
        ),
        "maintenance_section": "Zaległa konserwacja",
        "notify_maintenance": "Włącz",
        "notify_maintenance_desc": (
            "Obserwuje każdy przycisk z `reef_role` zaczynającym się od "
            "`maint_` i alarmuje, gdy jego `days_left` staje się ujemny."
        ),
        "respect_switch": "Uwzględniaj przełączniki powiadomień poszczególnych zadań",
        "respect_switch_desc": (
            "Gdy włączone, zadanie z wyłączonym przełącznikiem «(powiadomienia)» "
            "jest pomijane nawet gdy zalega. Zostaw włączone, chyba że chcesz "
            "alert niezależnie od przełączników."
        ),
        "unreachable_section": "Niedostępne urządzenia",
        "notify_unavailable": "Włącz",
        "watched_devices": "Urządzenia do obserwacji",
        "watched_devices_desc": (
            "Urządzenie jest zgłaszane jako niedostępne, gdy wszystkie jego "
            "encje są niedostępne. Lista jest jawna, ponieważ niedostępna encja "
            "nie udostępnia już atrybutu `reef_role`, po którym można by ją "
            "odnaleźć. Zostaw pustą, aby wyłączyć tę kontrolę."
        ),
        "msg_overdue": "Konserwacja zaległa o {days} dni: {task}",
        "msg_unreachable": "Urządzenie niedostępne",
        "title_prefix": "Rafa — ",
    },
    "pt": {
        "name": "Vigilância de manutenção do recife",
        "description": (
            "Avisa-o das **manutenções em atraso** em qualquer integração do "
            "ecossistema ReefTech, e dos **aparelhos que ficaram "
            "inacessíveis**.\\n\\n"
            "A deteção de manutenções não precisa de configuração: encontra as "
            "tarefas pelo atributo `reef_role`, por isso "
            "ha-reefbeat-component, ha-aquamedic-component e "
            "ha-reef-maintenance-component ficam cobertos, tal como qualquer "
            "integração futura que publique o mesmo contrato.\\n\\n"
            "A acessibilidade assenta na lista de aparelhos que escolher "
            "abaixo. O Home Assistant esconde os atributos de uma entidade "
            "indisponível, pelo que esta verificação não os consegue descobrir "
            "sozinha."
        ),
        "notify_section": "Destinatários das notificações",
        "notify_devices": "Telemóveis a notificar",
        "notify_devices_desc": (
            "Os aparelhos que receberão as notificações. Só aparecem telemóveis "
            "e tablets registados através da aplicação Home Assistant. É "
            "enviada uma notificação por aparelho."
        ),
        "notify_channel": "Canal Android (opcional)",
        "notify_channel_desc": (
            "Nome do canal passado em `data.channel`, para agrupar estas "
            "notificações e dar-lhes som ou prioridade próprios. Deixe vazio "
            "para o canal predefinido. O iOS ignora este campo."
        ),
        "maintenance_section": "Manutenção em atraso",
        "notify_maintenance": "Ativar",
        "notify_maintenance_desc": (
            "Vigia cada botão com um `reef_role` começado por `maint_`, e avisa "
            "quando o seu `days_left` fica negativo."
        ),
        "respect_switch": "Respeitar os interruptores de notificação por tarefa",
        "respect_switch_desc": (
            "Se ativado, uma tarefa cujo interruptor «(notificações)» esteja "
            "desligado é ignorada mesmo em atraso. Deixe ativado, salvo se "
            "quiser o aviso independentemente dos interruptores."
        ),
        "unreachable_section": "Aparelhos inacessíveis",
        "notify_unavailable": "Ativar",
        "watched_devices": "Aparelhos a vigiar",
        "watched_devices_desc": (
            "Um aparelho é dado como inacessível quando todas as suas entidades "
            "estão indisponíveis. A lista é explícita porque uma entidade "
            "indisponível já não expõe o atributo `reef_role` que permitiria "
            "encontrá-la. Deixe vazia para desativar a verificação."
        ),
        "msg_overdue": "Manutenção em atraso de {days} dias: {task}",
        "msg_unreachable": "Aparelho inacessível",
        "title_prefix": "Recife — ",
    },
}


def header(lang: str) -> str:
    """The blueprint metadata and inputs, in one language."""
    s = STRINGS[lang]
    return f"""# Generated by scripts/gen_blueprints.py -- do not edit by hand.
# Edit the strings in that script and run it again.
blueprint:
  name: {s["name"]} ({lang}) — v{VERSION}
  description: >
    {s["description"]}
  domain: automation
  source_url: {REPO}
  input:
    notify_section:
      name: {s["notify_section"]}
      icon: mdi:bell-outline
      input:
        notify_devices:
          name: {s["notify_devices"]}
          description: >
            {s["notify_devices_desc"]}
          selector:
            device:
              integration: mobile_app
              multiple: true
        notify_channel:
          name: {s["notify_channel"]}
          description: >
            {s["notify_channel_desc"]}
          default: "Reef"
          selector:
            text:

    maintenance_section:
      name: {s["maintenance_section"]}
      icon: mdi:wrench-clock
      input:
        notify_maintenance:
          name: {s["notify_maintenance"]}
          description: >
            {s["notify_maintenance_desc"]}
          default: true
          selector: {{boolean: {{}}}}
        maintenance_respect_switch:
          name: {s["respect_switch"]}
          description: >
            {s["respect_switch_desc"]}
          default: true
          selector: {{boolean: {{}}}}

    unreachable_section:
      name: {s["unreachable_section"]}
      icon: mdi:lan-disconnect
      input:
        notify_unavailable:
          name: {s["notify_unavailable"]}
          default: true
          selector: {{boolean: {{}}}}
        watched_devices:
          name: {s["watched_devices"]}
          description: >
            {s["watched_devices_desc"]}
          default: []
          selector:
            device:
              multiple: true
"""


def render(lang: str) -> str:
    """Header plus the shared body, with the message strings substituted."""
    s = STRINGS[lang]

    # The message is a Jinja expression, not a literal: the placeholders are
    # spliced into a concatenation. A trailing `~ ""` is stripped so a message
    # ending on a placeholder does not leave a dangling concat.
    overdue = (
        s["msg_overdue"]
        .replace("{days}", '" ~ (-dl) ~ "')
        .replace(
            "{task}", "\" ~ (e.attributes.get('friendly_name') or e.entity_id) ~ \""
        )
    )
    overdue = f'"{overdue}"'.replace(' ~ ""', "").replace('"" ~ ', "")
    body = (
        BODY.replace("MSG_OVERDUE", overdue)
        .replace("MSG_UNREACHABLE", f"'{s['msg_unreachable']}'")
        .replace("TITLE_PREFIX", s["title_prefix"])
    )
    return header(lang) + body


def main() -> None:
    missing = [
        (lang, key)
        for lang in LANGS
        for key in STRINGS["en"]
        if key not in STRINGS.get(lang, {})
    ]
    if missing:
        raise SystemExit(f"untranslated keys: {missing}")

    OUT.mkdir(parents=True, exist_ok=True)
    for lang in LANGS:
        path = OUT / f"reef_maintenance_notify.{lang}.yaml"
        path.write_text(render(lang), encoding="utf-8")
        print("written", path)


if __name__ == "__main__":
    sys.exit(main())
