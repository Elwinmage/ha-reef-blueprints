#!/usr/bin/env python3
"""Generate the relay watch blueprint in the eight supported languages.

Not meant to be run on its own: gen_blueprints.py calls generate().

Edit STRINGS and BODY below, never the generated YAML.
"""

from __future__ import annotations

from pathlib import Path

from blueprint_lib import METER_LOOKUP

REPO = "https://github.com/Elwinmage/ha-reef-blueprints"
SLUG = "reef_relay_watch"

# ---------------------------------------------------------------------------
# Logic, shared by every language.
#
# A relay that reads off while its appliance still draws power is a welded
# contact or a socket that no longer obeys. It is a check on the current state
# rather than a reaction to the switch going off, for three reasons: a device
# picked in the selector expands to entities a state trigger cannot list, a
# run parked on a delay would not survive a restart, and a relay that welds
# hours after the last switch is caught as well.
#
# Only switches carrying the `_on_off` role are taken from a picked device: its
# other switches are settings, and pairing one with the device's power sensor
# would raise a false alarm. A plain smart plug goes in the explicit list.
# ---------------------------------------------------------------------------

BODY = """
trigger:
  - platform: time_pattern
    minutes: "/5"

variables:
  watched_devices: !input watched_devices
  relays: !input relays
  power_threshold: !input power_threshold
  grace_minutes: !input grace_minutes
  notify_devices: !input notify_devices
  notify_channel: !input notify_channel

action:
  - alias: "Find the relays that are off but still draw power"
    variables:
      alerts: >-
        {%- set found = namespace(items=relays | list) -%}
        {%- for device in watched_devices -%}
          {%- for e in device_entities(device) | select('match', 'switch[.]') -%}
            {%- if (state_attr(e, 'reef_role') or '').endswith('_on_off') -%}
              {%- set found.items = found.items + [e] -%}
            {%- endif -%}
          {%- endfor -%}
        {%- endfor -%}
        {%- set ns = namespace(items=[]) -%}
        {%- for h in found.items | unique -%}
METER_LOOKUP
          {%- if meter and is_state(h, 'off')
                and (now() - states[h].last_changed).total_seconds()
                    > grace_minutes * 60
                and states(meter) | float(0) > power_threshold -%}
            {%- set ns.items = ns.items + [{
              'relay': h,
              'name': state_attr(h, 'friendly_name') or h,
              'power': states(meter),
            }] -%}
          {%- endif -%}
        {%- endfor -%}
        {{ ns.items }}

  - alias: "Notify for each relay"
    repeat:
      for_each: "{{ alerts }}"
      sequence:
        - variables:
            relay: "{{ repeat.item.relay }}"
            message: "MSG_STILL_DRAWING"
        - alias: "Dispatch to each selected mobile device"
          repeat:
            for_each: "{{ notify_devices }}"
            sequence:
              - variables:
                  # `name`, not `name_by_user`: the notify service slug is
                  # frozen at install time and ignores later renames in the UI.
                  mobile_slug: >-
                    {{ (device_attr(repeat.item, 'name')
                        or repeat.item) | slugify }}
              - service: "notify.mobile_app_{{ mobile_slug }}"
                continue_on_error: true
                data:
                  title: "TITLE_TEXT"
                  message: "{{ message }}"
                  # alert_once: the check repeats every five minutes for as
                  # long as the fault lasts, the phone should buzz only once.
                  data: >-
                    {{
                      {
                        'tag': 'reef_relay_' ~ relay,
                        'channel': notify_channel,
                        'alert_once': true
                      } if notify_channel else {
                        'tag': 'reef_relay_' ~ relay,
                        'alert_once': true
                      }
                    }}
"""

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "name": "Reef relay watch",
        "description": "Warns you when a relay reads off but its appliance still draws power: a welded contact, or a socket that no longer obeys. It runs all the time, for every socket of the chosen devices.",
        "sec_watch": "What to watch",
        "watched_devices": "Red Sea devices",
        "watched_devices_desc": "Every socket of a ReefControl-Power and every port of a ReefControl is watched, with its own consumption sensor found automatically.",
        "relays": "Other relays",
        "relays_desc": "Switches from other integrations. Only those whose device carries a single power sensor can be watched, as a smart plug does.",
        "power_threshold": "Consumption threshold",
        "power_threshold_desc": "Above this value, a relay that is off counts as still drawing power. Keep it above the standby reading of the meter.",
        "grace_minutes": "Delay after switching off",
        "grace_minutes_desc": "Time left to the meter to catch up after the relay opens. The RS Power refreshes once a minute, so keep at least 3 minutes.",
        "sec_notify": "Notifications",
        "notify_devices": "Mobile devices to notify",
        "notify_devices_desc": "Only phones and tablets registered through the Home Assistant app are listed.",
        "notify_channel": "Android channel (optional)",
        "notify_channel_desc": "Channel name passed in `data.channel`. Leave empty for the default channel. iOS ignores this field.",
        "title": "Reef — relay",
        "msg_still_drawing": "{relay} is off but still draws {power} W: stuck relay?",
    },
    "fr": {
        "name": "Surveillance des relais du récif",
        "description": "Vous prévient quand un relais est coupé alors que son appareil consomme encore : contact collé, ou prise qui n'obéit plus. La surveillance tourne en permanence, sur toutes les prises des appareils choisis.",
        "sec_watch": "Quoi surveiller",
        "watched_devices": "Appareils Red Sea",
        "watched_devices_desc": "Chaque prise d'un ReefControl-Power et chaque port d'un ReefControl est surveillé, avec son capteur de consommation trouvé automatiquement.",
        "relays": "Autres relais",
        "relays_desc": "Interrupteurs d'autres intégrations. Seuls ceux dont l'appareil porte un unique capteur de puissance peuvent être surveillés, comme une prise connectée.",
        "power_threshold": "Seuil de consommation",
        "power_threshold_desc": "Au-dessus de cette valeur, un relais coupé est considéré comme consommant encore. Gardez-la au-dessus de la veille du compteur.",
        "grace_minutes": "Délai après la coupure",
        "grace_minutes_desc": "Temps laissé au compteur pour se mettre à jour après l'ouverture du relais. Le RS Power se rafraîchit une fois par minute : gardez au moins 3 minutes.",
        "sec_notify": "Notifications",
        "notify_devices": "Mobiles à notifier",
        "notify_devices_desc": "Seuls les téléphones et tablettes enregistrés via l'application Home Assistant apparaissent.",
        "notify_channel": "Canal Android (optionnel)",
        "notify_channel_desc": "Nom de canal passé dans `data.channel`. Laissez vide pour le canal par défaut. iOS ignore ce champ.",
        "title": "Récif — relais",
        "msg_still_drawing": "{relay} est coupé mais consomme encore {power} W : relais collé ?",
    },
    "de": {
        "name": "Riff-Relaisüberwachung",
        "description": "Warnt Sie, wenn ein Relais ausgeschaltet ist, sein Gerät aber weiter Strom verbraucht: verklebter Kontakt oder eine Steckdose, die nicht mehr gehorcht. Die Überwachung läuft ständig, für alle Steckdosen der gewählten Geräte.",
        "sec_watch": "Was überwacht wird",
        "watched_devices": "Red-Sea-Geräte",
        "watched_devices_desc": "Jede Steckdose eines ReefControl-Power und jeder Port eines ReefControl wird überwacht, der zugehörige Verbrauchssensor wird automatisch gefunden.",
        "relays": "Weitere Relais",
        "relays_desc": "Schalter anderer Integrationen. Überwacht werden können nur solche, deren Gerät genau einen Leistungssensor hat, wie eine smarte Steckdose.",
        "power_threshold": "Verbrauchsschwelle",
        "power_threshold_desc": "Oberhalb dieses Werts gilt ein ausgeschaltetes Relais als weiter verbrauchend. Über dem Standby-Wert des Zählers halten.",
        "grace_minutes": "Verzögerung nach dem Abschalten",
        "grace_minutes_desc": "Zeit, die der Zähler nach dem Öffnen des Relais zum Aktualisieren bekommt. Das RS Power aktualisiert einmal pro Minute: mindestens 3 Minuten beibehalten.",
        "sec_notify": "Benachrichtigungen",
        "notify_devices": "Zu benachrichtigende Mobilgeräte",
        "notify_devices_desc": "Es werden nur über die Home-Assistant-App registrierte Telefone und Tablets angezeigt.",
        "notify_channel": "Android-Kanal (optional)",
        "notify_channel_desc": "Kanalname für `data.channel`. Für den Standardkanal leer lassen. iOS ignoriert dieses Feld.",
        "title": "Riff — Relais",
        "msg_still_drawing": "{relay} ist aus, verbraucht aber noch {power} W: Relais verklebt?",
    },
    "es": {
        "name": "Vigilancia de relés del arrecife",
        "description": "Le avisa cuando un relé está apagado pero su aparato sigue consumiendo: contacto pegado o un enchufe que ya no obedece. La vigilancia funciona de forma continua, en todos los enchufes de los dispositivos elegidos.",
        "sec_watch": "Qué vigilar",
        "watched_devices": "Dispositivos Red Sea",
        "watched_devices_desc": "Se vigila cada enchufe de un ReefControl-Power y cada puerto de un ReefControl, con su sensor de consumo encontrado automáticamente.",
        "relays": "Otros relés",
        "relays_desc": "Interruptores de otras integraciones. Solo se pueden vigilar aquellos cuyo dispositivo tiene un único sensor de potencia, como un enchufe inteligente.",
        "power_threshold": "Umbral de consumo",
        "power_threshold_desc": "Por encima de este valor, un relé apagado se considera aún en consumo. Manténgalo por encima del reposo del medidor.",
        "grace_minutes": "Retardo tras el apagado",
        "grace_minutes_desc": "Tiempo que se deja al medidor para actualizarse tras abrirse el relé. El RS Power se actualiza una vez por minuto: mantenga al menos 3 minutos.",
        "sec_notify": "Notificaciones",
        "notify_devices": "Móviles a notificar",
        "notify_devices_desc": "Solo aparecen los teléfonos y tabletas registrados con la aplicación Home Assistant.",
        "notify_channel": "Canal Android (opcional)",
        "notify_channel_desc": "Nombre de canal enviado en `data.channel`. Déjelo vacío para el canal predeterminado. iOS ignora este campo.",
        "title": "Arrecife — relé",
        "msg_still_drawing": "{relay} está apagado pero sigue consumiendo {power} W: ¿relé pegado?",
    },
    "it": {
        "name": "Sorveglianza relè del reef",
        "description": "Vi avvisa quando un relè è spento ma il suo apparecchio consuma ancora: contatto incollato o presa che non obbedisce più. La sorveglianza è continua, su tutte le prese dei dispositivi scelti.",
        "sec_watch": "Cosa sorvegliare",
        "watched_devices": "Dispositivi Red Sea",
        "watched_devices_desc": "Viene sorvegliata ogni presa di un ReefControl-Power e ogni porta di un ReefControl, con il sensore di consumo trovato automaticamente.",
        "relays": "Altri relè",
        "relays_desc": "Interruttori di altre integrazioni. Si possono sorvegliare solo quelli il cui dispositivo ha un unico sensore di potenza, come una presa smart.",
        "power_threshold": "Soglia di consumo",
        "power_threshold_desc": "Sopra questo valore, un relè spento è considerato ancora in consumo. Mantenetela sopra lo standby del misuratore.",
        "grace_minutes": "Ritardo dopo lo spegnimento",
        "grace_minutes_desc": "Tempo lasciato al misuratore per aggiornarsi dopo l'apertura del relè. L'RS Power si aggiorna una volta al minuto: mantenete almeno 3 minuti.",
        "sec_notify": "Notifiche",
        "notify_devices": "Dispositivi mobili da avvisare",
        "notify_devices_desc": "Compaiono solo telefoni e tablet registrati tramite l'app Home Assistant.",
        "notify_channel": "Canale Android (opzionale)",
        "notify_channel_desc": "Nome del canale passato in `data.channel`. Lasciate vuoto per il canale predefinito. iOS ignora questo campo.",
        "title": "Reef — relè",
        "msg_still_drawing": "{relay} è spento ma consuma ancora {power} W: relè incollato?",
    },
    "nl": {
        "name": "Rifrelaisbewaking",
        "description": "Waarschuwt u als een relais uit staat maar het apparaat nog stroom verbruikt: een vastgeplakt contact of een contactdoos die niet meer gehoorzaamt. De bewaking loopt continu, voor alle contactdozen van de gekozen apparaten.",
        "sec_watch": "Wat bewaken",
        "watched_devices": "Red Sea-apparaten",
        "watched_devices_desc": "Elke contactdoos van een ReefControl-Power en elke poort van een ReefControl wordt bewaakt, met de bijbehorende verbruikssensor automatisch gevonden.",
        "relays": "Andere relais",
        "relays_desc": "Schakelaars van andere integraties. Alleen die met precies één vermogenssensor op hun apparaat kunnen worden bewaakt, zoals een slimme stekker.",
        "power_threshold": "Verbruiksdrempel",
        "power_threshold_desc": "Boven deze waarde telt een uitgeschakeld relais als nog verbruikend. Houd hem boven de stand-bywaarde van de meter.",
        "grace_minutes": "Vertraging na uitschakelen",
        "grace_minutes_desc": "Tijd voor de meter om bij te werken nadat het relais opent. De RS Power ververst eens per minuut: houd minstens 3 minuten aan.",
        "sec_notify": "Meldingen",
        "notify_devices": "Mobiele apparaten voor meldingen",
        "notify_devices_desc": "Alleen telefoons en tablets die via de Home Assistant-app zijn geregistreerd, staan in de lijst.",
        "notify_channel": "Android-kanaal (optioneel)",
        "notify_channel_desc": "Kanaalnaam voor `data.channel`. Laat leeg voor het standaardkanaal. iOS negeert dit veld.",
        "title": "Rif — relais",
        "msg_still_drawing": "{relay} staat uit maar verbruikt nog {power} W: relais vastgeplakt?",
    },
    "pl": {
        "name": "Nadzór przekaźników rafy",
        "description": "Ostrzega, gdy przekaźnik jest wyłączony, a urządzenie nadal pobiera moc: sklejony styk lub gniazdo, które przestało słuchać. Nadzór działa stale, na wszystkich gniazdach wybranych urządzeń.",
        "sec_watch": "Co nadzorować",
        "watched_devices": "Urządzenia Red Sea",
        "watched_devices_desc": "Nadzorowane jest każde gniazdo ReefControl-Power i każdy port ReefControl, a czujnik poboru jest znajdowany automatycznie.",
        "relays": "Inne przekaźniki",
        "relays_desc": "Przełączniki z innych integracji. Nadzorować można tylko te, których urządzenie ma jeden czujnik mocy, jak inteligentna wtyczka.",
        "power_threshold": "Próg poboru",
        "power_threshold_desc": "Powyżej tej wartości wyłączony przekaźnik jest uznawany za nadal pobierający moc. Ustaw powyżej odczytu czuwania licznika.",
        "grace_minutes": "Opóźnienie po wyłączeniu",
        "grace_minutes_desc": "Czas na aktualizację licznika po otwarciu przekaźnika. RS Power odświeża się raz na minutę: zachowaj co najmniej 3 minuty.",
        "sec_notify": "Powiadomienia",
        "notify_devices": "Urządzenia mobilne do powiadamiania",
        "notify_devices_desc": "Na liście są tylko telefony i tablety zarejestrowane przez aplikację Home Assistant.",
        "notify_channel": "Kanał Android (opcjonalnie)",
        "notify_channel_desc": "Nazwa kanału przekazywana w `data.channel`. Pozostaw puste dla kanału domyślnego. iOS ignoruje to pole.",
        "title": "Rafa — przekaźnik",
        "msg_still_drawing": "{relay} jest wyłączony, ale nadal pobiera {power} W: sklejony przekaźnik?",
    },
    "pt": {
        "name": "Vigilância de relés do recife",
        "description": "Avisa quando um relé está desligado mas o aparelho continua a consumir: contacto colado ou uma tomada que já não obedece. A vigilância funciona em permanência, em todas as tomadas dos dispositivos escolhidos.",
        "sec_watch": "O que vigiar",
        "watched_devices": "Dispositivos Red Sea",
        "watched_devices_desc": "Cada tomada de um ReefControl-Power e cada porta de um ReefControl é vigiada, com o sensor de consumo encontrado automaticamente.",
        "relays": "Outros relés",
        "relays_desc": "Interruptores de outras integrações. Só podem ser vigiados aqueles cujo dispositivo tem um único sensor de potência, como uma tomada inteligente.",
        "power_threshold": "Limiar de consumo",
        "power_threshold_desc": "Acima deste valor, um relé desligado conta como ainda a consumir. Mantenha-o acima do repouso do medidor.",
        "grace_minutes": "Atraso após desligar",
        "grace_minutes_desc": "Tempo dado ao medidor para se atualizar após a abertura do relé. O RS Power atualiza uma vez por minuto: mantenha pelo menos 3 minutos.",
        "sec_notify": "Notificações",
        "notify_devices": "Dispositivos móveis a notificar",
        "notify_devices_desc": "Só aparecem os telemóveis e tablets registados através da aplicação Home Assistant.",
        "notify_channel": "Canal Android (opcional)",
        "notify_channel_desc": "Nome do canal enviado em `data.channel`. Deixe vazio para o canal predefinido. O iOS ignora este campo.",
        "title": "Recife — relé",
        "msg_still_drawing": "{relay} está desligado mas ainda consome {power} W: relé colado?",
    },
}


def header(lang: str, version: str) -> str:
    """Blueprint metadata and input selectors for one language."""
    s = STRINGS[lang]
    return f"""# Generated by scripts/gen_relay_watch.py -- do not edit by hand.
# Edit the strings in that script and run gen_blueprints.py again.
blueprint:
  name: {s["name"]} ({lang}) — v{version}
  description: >
    {s["description"]}
  domain: automation
  source_url: {REPO}
  homeassistant:
    min_version: "2024.8.0"
  input:
    watch_section:
      name: {s["sec_watch"]}
      icon: mdi:electric-switch
      input:
        watched_devices:
          name: {s["watched_devices"]}
          description: >
            {s["watched_devices_desc"]}
          default: []
          selector:
            device:
              integration: redsea
              multiple: true
        relays:
          name: {s["relays"]}
          description: >
            {s["relays_desc"]}
          default: []
          selector:
            entity:
              domain: switch
              multiple: true
        power_threshold:
          name: {s["power_threshold"]}
          description: >
            {s["power_threshold_desc"]}
          default: 10
          selector:
            number:
              min: 1
              max: 100
              unit_of_measurement: W
              mode: box
        grace_minutes:
          name: {s["grace_minutes"]}
          description: >
            {s["grace_minutes_desc"]}
          default: 5
          selector:
            number:
              min: 2
              max: 60
              unit_of_measurement: min
              mode: box

    notify_section:
      name: {s["sec_notify"]}
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
"""


def render(lang: str, version: str) -> str:
    """Header plus the shared body, with the strings substituted."""
    s = STRINGS[lang]
    message = (
        s["msg_still_drawing"]
        .replace("{relay}", "{{ repeat.item.name }}")
        .replace("{power}", "{{ repeat.item.power }}")
    )
    body = (
        BODY.replace("METER_LOOKUP", METER_LOOKUP)
        .replace("MSG_STILL_DRAWING", message)
        .replace("TITLE_TEXT", s["title"])
    )
    return header(lang, version) + body


def generate(langs: list[str], out: Path, version: str) -> None:
    """Write one blueprint per language."""
    missing = [
        (lang, key)
        for lang in langs
        for key in STRINGS["en"]
        if key not in STRINGS.get(lang, {})
    ]
    if missing:
        raise SystemExit(f"untranslated keys: {missing}")

    for lang in langs:
        path = out / f"{SLUG}.{lang}.yaml"
        path.write_text(render(lang, version), encoding="utf-8")
        print("written", path)
