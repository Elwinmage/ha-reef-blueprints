#!/usr/bin/env python3
"""Generate the reef heater test blueprint in the eight supported languages.

Not meant to be run on its own: gen_blueprints.py calls generate(), so CI, the
release workflow and regen.sh keep working from a single entry point, and the
repository keeps a single version number.

Edit STRINGS and BODY below, never the generated YAML.
"""

from __future__ import annotations

from pathlib import Path

from blueprint_lib import METER_LOOKUP

REPO = "https://github.com/Elwinmage/ha-reef-blueprints"
SLUG = "reef_heater_test"

# ---------------------------------------------------------------------------
# Logic, shared by every language.
#
# One run keeps a single heater powered and cuts the others, so a temperature
# drop points at that heater. Three constraints shape the sequence:
#
#   * A heater must never stay off because the run died. A delay does not
#     survive a restart or a reload, so `startup` and `reload` turn back on
#     whatever is off. Saving any automation fires automation_reloaded, so
#     `reload` only acts within the window a test may have been running in:
#     outside it, a heater that is off was cut on purpose, for instance by a
#     thermal safety. The top-level conditions keep last_triggered meaningful
#     by not counting the daily non-test firings. Mode `single` drops the
#     event while a live test is holding the heaters off.
#
#   * A blueprint cannot create helpers, so nothing is stored. The rotation is
#     derived from the calendar day: same answer after a restart, no state to
#     lose. The trade-off is that changing the heater list shifts the rotation.
#
#   * The sequence stays flat on purpose. `wait` and variables set inside an
#     `if` do not reliably reach the outer scope across Home Assistant
#     versions, so every path runs through the same top-level steps and a test
#     that must not run simply waits for zero seconds.
#
# Keeping the temperature proves little on its own: a warm room hides a dead
# heater. So a meter, when there is one, turns the verdict into a proof. It
# needs two waits in a row because a run cannot note that the heater drew
# while it is waiting: the first one ends on that event, the second one holds
# the test for the time left. Both are at top level for the reason above.
#
# The median is used for the temperature: with three probes, one failing or
# drifting probe cannot decide the verdict on its own.
# ---------------------------------------------------------------------------

BODY = """
mode: single
max_exceeded: silent

trigger:
  - platform: time
    at: !input test_time
    id: schedule
  - platform: event
    event_type: reef_heater_test
    id: manual
  - platform: homeassistant
    event: start
    id: startup
  - platform: event
    event_type: automation_reloaded
    id: reload
  - platform: state
    entity_id: !input pause_entities
    to: "off"
    id: pause_end

variables:
  heaters: !input heaters
  temperature_sensors: !input temperature_sensors
  test_time: !input test_time
  cycle_days: !input cycle_days
  test_duration: !input test_duration
  max_drop: !input max_drop
  abort_temperature: !input abort_temperature
  pause_entities: !input pause_entities
  room_sensor: !input room_sensor
  heater_setpoint: !input heater_setpoint
  power_sensors: !input power_sensors
  power_threshold: !input power_threshold
  result_entity: !input result_entity
  notify_devices: !input notify_devices
  notify_channel: !input notify_channel
  # automation.trigger (the Run button) has no trigger id.
  trigger_id: "{{ trigger.id | default('manual') }}"
  day_number: "{{ now().toordinal() }}"
  # Guarded by the id: `trigger.event` is the string "start" on the
  # homeassistant trigger, and an error here would stop the recovery run.
  requested: >-
    {{ trigger.event.data.heater | default('')
       if trigger.id | default('') == 'manual' else '' }}

condition:
  - alias: "Today is a test day"
    condition: template
    value_template: >-
      {{ trigger_id != 'schedule' or day_number % (cycle_days | int) == 0 }}
  - alias: "A manual request is aimed at this instance"
    condition: template
    value_template: "{{ requested == '' or requested in heaters }}"
  - alias: "A reload can only have killed a test that had started"
    condition: template
    value_template: >-
      {{ trigger_id != 'reload'
         or now().timestamp() - as_timestamp(this.attributes.last_triggered, 0)
            < (test_duration | int + 5) * 60 }}

action:
  # Integrations are still loading when Home Assistant reports it has started.
  - delay: "{{ 120 if trigger_id == 'startup' else 0 }}"

  - alias: "Find the meter and the mode of each heater"
    variables:
      # The list given by hand wins, for a relay in series with a meter that
      # sits on another device. A socket's mode comes with its role.
      links: >-
        {%- set ns = namespace(items=[]) -%}
        {%- set manual = power_sensors
              if power_sensors | count == heaters | count else [] -%}
        {%- for h in heaters -%}
METER_LOOKUP
          {%- set modes = (ents | select('is_state_attr', 'reef_role',
                prefix ~ '_mode') | list) if prefix else [] -%}
          {%- set ns.items = ns.items + [{
            'heater': h,
            'power': manual[loop.index0] if manual else meter,
            'mode': modes[0] if modes else '',
          }] -%}
        {%- endfor -%}
        {{ ns.items }}
      # A socket following a probe or a schedule is regulated by the strip:
      # `standby` reads as off although nothing is wrong, and forcing it would
      # take the regulation away.
      driven_heaters: >-
        {%- set ns = namespace(items=[]) -%}
        {%- for l in links if l.mode and states(l.mode) not in ['on', 'off'] -%}
          {%- set ns.items = ns.items + [l.heater] -%}
        {%- endfor -%}
        {{ ns.items }}

  - alias: "Check whether a test can start"
    variables:
      is_test: "{{ trigger_id in ['schedule', 'manual'] }}"
      started_at: "{{ now().timestamp() }}"
      start_temp: >-
        {{ temperature_sensors | map('states') | select('is_number')
           | map('float') | list | median(none) }}
      paused_at_start: >-
        {{ pause_entities | select('is_state', 'on') | list | count > 0 }}
      room_temp: >-
        {{ states(room_sensor) | float(none) if room_sensor != '' else none }}
      # In summer a heater has nothing to do: its thermostat stays open, the
      # tank does not move, and a test would pass, or give no verdict, without
      # having proved anything. The room is compared to the lower of the tank
      # and the setpoint, because the tank usually sits above the room. A tank
      # already past the setpoint keeps the thermostat open just as well,
      # hence the second test, beyond the drop allowed for a normal swing.
      no_demand: >-
        {%- set ref = ([start_temp, heater_setpoint | float]
              if heater_setpoint | float > 0 else [start_temp]) | min
              if start_temp is number else none -%}
        {{ ref is number and (
             (room_temp is number and room_temp >= ref)
             or (heater_setpoint | float > 0
                 and start_temp > heater_setpoint | float + max_drop)) }}
      skip_reason: >-
        {%- if not is_test -%}
        {%- elif heaters | count < 2 -%} too_few
        {%- elif power_sensors | count not in [0, heaters | count] -%} power_list
        {%- elif paused_at_start -%} paused
        {%- elif start_temp is not number -%} no_temperature
        {%- elif start_temp < abort_temperature -%} too_cold
        {%- elif no_demand -%} no_demand
        {%- elif driven_heaters | count > 0 -%} driven
        {%- elif heaters | reject('is_state', 'on') | list | count > 0 -%} heater_off
        {%- endif -%}
      run_test: "{{ is_test and skip_reason == '' }}"
      target: >-
        {%- if not run_test -%}
        {%- elif requested != '' -%} {{ requested }}
        {%- else -%}
          {%- set offset = 0 if trigger_id == 'schedule' else 1 -%}
          {{ heaters[(day_number // (cycle_days | int) + offset) % (heaters | count)] }}
        {%- endif -%}
      to_cut: "{{ heaters | reject('eq', target) | list if run_test else [] }}"
      target_name: "{{ state_attr(target, 'friendly_name') or target }}"
      target_power: >-
        {{ (links | selectattr('heater', 'eq', target)
            | map(attribute='power') | list + [''])[0] }}
      # Read before the cut: a heater idling on its own thermostat draws
      # nothing either way, so only one that was drawing proves its relay.
      drawing_before: >-
        {%- set ns = namespace(items=[]) -%}
        {%- for l in links
              if l.power and states(l.power) | float(0) > power_threshold -%}
          {%- set ns.items = ns.items + [l.heater] -%}
        {%- endfor -%}
        {{ ns.items }}
      # Long enough for a polled meter: the RS Power refreshes once a minute.
      settle: >-
        {{ 180 if links | selectattr('heater', 'in', to_cut)
           | selectattr('power') | list | count > 0 else 0 }}

  - if:
      - "{{ run_test }}"
    then:
      - service: switch.turn_off
        target:
          entity_id: "{{ to_cut }}"

  - alias: "Let the meters catch up with the cut"
    delay: "{{ settle }}"

  - alias: "Check that the relays really opened"
    variables:
      cut_report: >-
        {%- set ns = namespace(stuck=[], proven=[], unproven=[]) -%}
        {%- for l in links if l.power and l.heater in to_cut -%}
          {%- set name = state_attr(l.heater, 'friendly_name') or l.heater -%}
          {%- if states(l.power) | float(0) > power_threshold -%}
            {%- set ns.stuck = ns.stuck + [name] -%}
          {%- elif l.heater in drawing_before -%}
            {%- set ns.proven = ns.proven + [name] -%}
          {%- else -%}
            {%- set ns.unproven = ns.unproven + [name] -%}
          {%- endif -%}
        {%- endfor -%}
        {{ {'stuck': ns.stuck, 'proven': ns.proven, 'unproven': ns.unproven} }}
      relay_stuck: "{{ cut_report.stuck | count > 0 }}"
      heat_at_start: >-
        {{ target_power != '' and states(target_power) | float(0) > power_threshold }}

  # A template trigger fires on an edge, so a heater already drawing is
  # settled by heat_at_start above and this wait only runs until the timeout.
  - alias: "Hold the test until the heater proves itself, or something goes wrong"
    wait_for_trigger:
      - platform: template
        id: heat_seen
        value_template: >-
          {{ target_power != ''
             and states(target_power) | float(0) > power_threshold }}
WAIT_TRIGGERS
    timeout:
      seconds: >-
        {{ test_duration | int * 60 - settle
           if run_test and not relay_stuck else 0 }}
    continue_on_timeout: true

  - alias: "Note what the first wait saw"
    variables:
      first_stop: "{{ wait.trigger.id if wait.trigger is not none else '' }}"
      heat_seen: "{{ heat_at_start or first_stop == 'heat_seen' }}"

  - alias: "Finish the test once the heater has proved itself"
    wait_for_trigger:
WAIT_TRIGGERS
    timeout:
      seconds: >-
        {{ max(test_duration | int * 60 - (now().timestamp() - started_at), 0)
           if first_stop == 'heat_seen' else 0 }}
    continue_on_timeout: true

  - alias: "Read the result before the heaters come back"
    variables:
      end_temp: >-
        {{ temperature_sensors | map('states') | select('is_number')
           | map('float') | list | median(none) }}
      # A template trigger only fires on a false-to-true edge, so a relay that
      # never opened is invisible to the waits above: without this check, a
      # test where nothing was cut would pass.
      stopped_by: >-
        {%- if relay_stuck -%} relay_stuck
        {%- elif wait.trigger is not none -%} {{ wait.trigger.id }}
        {%- elif first_stop not in ['', 'heat_seen'] -%} {{ first_stop }}
        {%- elif to_cut | reject('is_state', 'off') | list | count > 0 -%} heater_changed
        {%- endif -%}
      elapsed: "{{ ((now().timestamp() - started_at) / 60) | round(0) | int }}"
      paused_now: >-
        {{ pause_entities | select('is_state', 'on') | list | count > 0 }}
      to_restore: >-
        {%- if paused_now -%} []
        {%- elif run_test -%} {{ to_cut }}
        {%- elif is_test -%} []
        {%- else -%}
          {{ heaters | select('is_state', 'off')
             | reject('in', driven_heaters) | list }}
        {%- endif -%}

  - if:
      - "{{ to_restore | count > 0 }}"
    then:
      - service: switch.turn_on
        target:
          entity_id: "{{ to_restore }}"
        continue_on_error: true

  - alias: "Give the relays time to answer"
    delay: "{{ 30 if to_restore | count > 0 else 0 }}"

  - alias: "Write the report"
    variables:
      still_off: "{{ to_restore | reject('is_state', 'on') | list }}"
      start_text: >-
        {{ start_temp | round(2) if start_temp is number else '?' }}
      end_text: "{{ end_temp | round(2) if end_temp is number else '?' }}"
      room_text: "{{ room_temp | round(1) if room_temp is number else '?' }}"
      setpoint_text: >-
        {{ heater_setpoint if heater_setpoint | float > 0 else '?' }}
      fell: >-
        {{ stopped_by in ['too_cold', 'dropped']
           or (stopped_by == '' and start_temp is number and end_temp is number
               and start_temp - end_temp > max_drop) }}
      metered: "{{ target_power != '' }}"
      message: >-
        {%- if not is_test -%}
          {%- if to_restore | count > 0 -%}MSG_RECOVERED{%- endif -%}
        {%- elif skip_reason == 'too_few' -%}MSG_SKIP_TOO_FEW
        {%- elif skip_reason == 'power_list' -%}MSG_SKIP_POWER_LIST
        {%- elif skip_reason == 'paused' -%}MSG_SKIP_PAUSED
        {%- elif skip_reason == 'no_temperature' -%}MSG_SKIP_NO_TEMPERATURE
        {%- elif skip_reason == 'too_cold' -%}MSG_SKIP_TOO_COLD
        {%- elif skip_reason == 'no_demand' -%}MSG_SKIP_NO_DEMAND
        {%- elif skip_reason == 'driven' -%}MSG_SKIP_DRIVEN
        {%- elif skip_reason == 'heater_off' -%}MSG_SKIP_HEATER_OFF
        {%- elif relay_stuck -%}MSG_STUCK
        {%- elif fell and metered and not heat_seen -%}MSG_DEAD
        {%- elif fell and metered -%}MSG_WEAK
        {%- elif stopped_by == 'too_cold' -%}MSG_FAIL_COLD
        {%- elif fell -%}MSG_FAIL_DROP
        {%- elif stopped_by != '' -%}MSG_INTERRUPTED
        {%- elif metered and not heat_seen -%}MSG_NO_DEMAND
        {%- elif metered -%}MSG_OK MSG_HEAT_OK
        {%- else -%}MSG_OK
        {%- endif -%}
        {%- if run_test and not relay_stuck and stopped_by in ['', 'dropped', 'too_cold'] -%}
          {%- if cut_report.proven | count > 0 %} MSG_CUT_OK{%- endif -%}
          {%- if cut_report.unproven | count > 0 %} MSG_CUT_UNPROVEN{%- endif -%}
        {%- endif -%}
        {%- if paused_now and run_test %} MSG_PAUSED_NOTE{%- endif -%}
        {%- if still_off | count > 0 %} MSG_STILL_OFF{%- endif -%}

  - condition: template
    value_template: "{{ message | length > 0 }}"

  # A text helper keeps the last outcome, and its history keeps the others.
  - if:
      - "{{ result_entity != '' }}"
    then:
      - service: input_text.set_value
        target:
          entity_id: "{{ result_entity }}"
        data:
          value: >-
            {{ (now().strftime('%Y-%m-%d') ~ ' ' ~ message)
               [:state_attr(result_entity, 'max') | int(100)] }}
        continue_on_error: true

  - alias: "Dispatch to each selected mobile device"
    repeat:
      for_each: "{{ notify_devices }}"
      sequence:
        - variables:
            # `name`, not `name_by_user`: the notify service slug is frozen
            # at install time and ignores later renames in the UI.
            mobile_slug: >-
              {{ (device_attr(repeat.item, 'name')
                  or repeat.item) | slugify }}
        - service: "notify.mobile_app_{{ mobile_slug }}"
          continue_on_error: true
          data:
            title: "TITLE_TEXT"
            message: "{{ message }}"
            data: >-
              {{
                {
                  'tag': 'reef_heater_test',
                  'channel': notify_channel
                } if notify_channel else {'tag': 'reef_heater_test'}
              }}
"""

# Everything that ends a test early. Both waits watch the same list.
WAIT_TRIGGERS = """\
      - platform: template
        id: too_cold
        value_template: >-
          {% set t = temperature_sensors | map('states') | select('is_number')
             | map('float') | list | median(none) %}
          {{ t is number and t < abort_temperature }}
        for: "00:02:00"
      - platform: template
        id: dropped
        value_template: >-
          {% set t = temperature_sensors | map('states') | select('is_number')
             | map('float') | list | median(none) %}
          {{ t is number and start_temp - t > max_drop }}
        for: "00:02:00"
      # Anything that touches the heaters during a test wins: a thermal
      # safety elsewhere has more information than this automation.
      - platform: template
        id: heater_changed
        value_template: >-
          {{ to_cut | reject('is_state', 'off') | list | count > 0
             or not is_state(target, 'on') }}
        for: "00:01:00"
      - platform: template
        id: paused
        value_template: >-
          {{ pause_entities | select('is_state', 'on') | list | count > 0 }}
      - platform: template
        id: no_temperature
        value_template: >-
          {{ temperature_sensors | map('states') | select('is_number')
             | list | count == 0 }}
        for: "00:10:00"\
"""

# Placeholders usable in the messages, mapped to their Jinja expression.
PLACEHOLDERS = {
    "{heater}": "{{ target_name }}",
    "{minutes}": "{{ elapsed }}",
    "{start}": "{{ start_text }}",
    "{end}": "{{ end_text }}",
    "{limit}": "{{ abort_temperature }}",
    "{drop}": "{{ max_drop }}",
    "{still_off}": "{{ still_off | join(', ') }}",
    "{room}": "{{ room_text }}",
    "{setpoint}": "{{ setpoint_text }}",
    "{stuck}": "{{ cut_report.stuck | join(', ') }}",
    "{proven}": "{{ cut_report.proven | join(', ') }}",
    "{unproven}": "{{ cut_report.unproven | join(', ') }}",
}

MESSAGES = {
    "MSG_RECOVERED": "msg_recovered",
    "MSG_SKIP_TOO_FEW": "msg_skip_too_few",
    "MSG_SKIP_PAUSED": "msg_skip_paused",
    "MSG_SKIP_NO_TEMPERATURE": "msg_skip_no_temperature",
    "MSG_SKIP_POWER_LIST": "msg_skip_power_list",
    "MSG_SKIP_DRIVEN": "msg_skip_driven",
    "MSG_SKIP_NO_DEMAND": "msg_skip_no_demand",
    "MSG_STUCK": "msg_stuck",
    "MSG_DEAD": "msg_dead",
    "MSG_WEAK": "msg_weak",
    "MSG_NO_DEMAND": "msg_no_demand",
    "MSG_HEAT_OK": "msg_heat_ok",
    "MSG_CUT_OK": "msg_cut_ok",
    "MSG_CUT_UNPROVEN": "msg_cut_unproven",
    "MSG_SKIP_TOO_COLD": "msg_skip_too_cold",
    "MSG_SKIP_HEATER_OFF": "msg_skip_heater_off",
    "MSG_FAIL_COLD": "msg_fail_cold",
    "MSG_FAIL_DROP": "msg_fail_drop",
    "MSG_INTERRUPTED": "msg_interrupted",
    "MSG_OK": "msg_ok",
    "MSG_PAUSED_NOTE": "msg_paused_note",
    "MSG_STILL_OFF": "msg_still_off",
}

# Longest first, so that no marker is cut by a shorter one.
MARKERS = [*sorted(MESSAGES, key=len, reverse=True), "TITLE_TEXT"]

# ---------------------------------------------------------------------------
# Translations
# ---------------------------------------------------------------------------

STRINGS: dict[str, dict[str, str]] = {
    "en": {
        "sec_measure": "Measurement and history",
        "power_sensors": "Power sensors (optional)",
        "power_sensors_desc": "Filled in automatically for a Red Sea socket or a smart plug: leave empty. Only needed when the meter is on another device, and then give one sensor per heater, in the same order as the list of heaters.",
        "power_threshold": "Consumption threshold",
        "power_threshold_desc": "Above this value a heater counts as drawing power, at or below it as not drawing. Keep it above the standby reading of the meter.",
        "result_entity": "Last result (optional)",
        "result_entity_desc": "A text helper that receives the date and the result of each run. Its history keeps the earlier ones. Give it a maximum length of 255.",
        "msg_skip_power_list": "Test not run: give as many power sensors as heaters.",
        "msg_skip_driven": "Test not run: a socket follows a probe or a schedule, set it to manual.",
        "msg_stuck": "{stuck} still draws power after the cut: stuck relay? Test stopped, check it now.",
        "msg_dead": "{heater} drew nothing while the tank cooled: {start}° → {end}° in {minutes} min. This heater looks dead.",
        "msg_weak": "{heater} heated but could not hold the tank alone: {start}° → {end}° in {minutes} min. Undersized or failing.",
        "room_sensor": "Room temperature (optional)",
        "room_sensor_desc": "Skips the test when the room is at or above the tank or the setpoint: the heater would have nothing to do, and the test would prove nothing. Strongly advised, above all without a power meter.",
        "heater_setpoint": "Heater setpoint (optional)",
        "heater_setpoint_desc": "The temperature set on the heater's thermostat, 0 if unknown. Also skips the test when the tank is already above it.",
        "msg_skip_no_demand": "Test not run: the heater would have nothing to do (tank {start}°, room {room}°, setpoint {setpoint}°).",
        "msg_no_demand": "No verdict for {heater}: {start}° → {end}° in {minutes} min, but it never drew power, so it was not proven. Its thermostat may be set too low, or the room warm enough for it to stay idle.",
        "msg_heat_ok": "Consumption confirmed.",
        "msg_cut_ok": "Cut confirmed for {proven}.",
        "msg_cut_unproven": "Cut not provable for {unproven}, not drawing beforehand.",
        "name": "Reef heater test",
        "description": (
            "Periodically proves that each heater can hold the tank on its "
            "own: one heater stays powered, the others are cut for the "
            "duration of the test, and the result is sent to your phone. The "
            "test stops early and restores every heater if the temperature "
            "falls, and heaters left off by a restart are turned back on. "
            "Needs at least two heaters."
        ),
        "sec_equipment": "Equipment",
        "heaters": "Heaters",
        "heaters_desc": (
            "The switches powering the heaters. They are all expected to be "
            "on outside a test, and any heater found off after a restart is "
            "turned back on: to take one out of service, remove it from this "
            "list."
        ),
        "sensors": "Temperature sensors",
        "sensors_desc": (
            "Probes in the water. The median is used, so with three probes "
            "a single faulty one cannot change the verdict."
        ),
        "sec_schedule": "Schedule",
        "test_time": "Start time",
        "test_time_desc": (
            "Avoid a test that overlaps a change of lighting or fan speed: "
            "either one moves the temperature by itself."
        ),
        "cycle_days": "Days between tests",
        "cycle_days_desc": (
            "One heater is tested each time, in turn. With two heaters and "
            "14 days, each heater is tested every four weeks."
        ),
        "test_duration": "Test duration",
        "test_duration_desc": (
            "A large volume reacts slowly: under about two hours, a heater "
            "that does nothing can go unnoticed."
        ),
        "sec_safety": "Safety",
        "max_drop": "Allowed temperature drop",
        "max_drop_desc": (
            "Beyond this drop from the starting temperature the test fails "
            "and stops at once. Keep it above the resolution of your probes."
        ),
        "abort_temperature": "Abort temperature",
        "abort_temperature_desc": (
            "Below this value no test starts, and a running test stops and "
            "restores the heaters."
        ),
        "pause_entities": "Maintenance entities (optional)",
        "pause_entities_desc": (
            "While any of these is on, no test starts and heaters are not "
            "turned back on, since they may be out of the water. They are "
            "restored when it goes off."
        ),
        "sec_notify": "Notifications",
        "notify_devices": "Mobile devices to notify",
        "notify_devices_desc": (
            "Receive the result of each test. Only phones and tablets "
            "registered through the Home Assistant app are listed."
        ),
        "notify_channel": "Android channel (optional)",
        "notify_channel_desc": (
            "Channel name passed in `data.channel`. Leave empty for the "
            "default channel. iOS ignores this field."
        ),
        "title": "Reef — heater test",
        "msg_ok": (
            "{heater} held the tank alone for {minutes} min: "
            "{start}° → {end}°. Test passed."
        ),
        "msg_fail_drop": (
            "{heater} did not hold the tank alone: {start}° → {end}° after "
            "{minutes} min (allowed drop: {drop}°). Check this heater."
        ),
        "msg_fail_cold": (
            "Test of {heater} stopped after {minutes} min: {end}° is below "
            "{limit}°. Heaters restored, check this heater."
        ),
        "msg_interrupted": (
            "Test of {heater} interrupted after {minutes} min, no verdict "
            "({start}° → {end}°)."
        ),
        "msg_skip_too_few": "Test not run: at least two heaters are needed.",
        "msg_skip_paused": "Test not run: maintenance in progress.",
        "msg_skip_no_temperature": "Test not run: no temperature available.",
        "msg_skip_too_cold": "Test not run: {start}° is below {limit}°.",
        "msg_skip_heater_off": ("Test not run: all heaters must be on before a test."),
        "msg_recovered": (
            "A test was interrupted by a restart: heaters turned back on."
        ),
        "msg_paused_note": ("Maintenance in progress: heaters stay off until it ends."),
        "msg_still_off": "Warning, still off: {still_off}.",
    },
    "fr": {
        "sec_measure": "Mesure et historique",
        "power_sensors": "Capteurs de puissance (optionnel)",
        "power_sensors_desc": "Trouvés automatiquement pour une prise Red Sea ou une prise connectée : laissez vide. Utile seulement si le compteur est sur un autre appareil, avec alors un capteur par chauffage, dans le même ordre que la liste des chauffages.",
        "power_threshold": "Seuil de consommation",
        "power_threshold_desc": "Au-dessus de cette valeur, un chauffage est considéré comme consommant ; en dessous ou à égalité, comme ne consommant pas. Gardez-la au-dessus de la veille du compteur.",
        "result_entity": "Dernier résultat (optionnel)",
        "result_entity_desc": "Un helper texte qui reçoit la date et le résultat de chaque exécution. Son historique garde les précédents. Donnez-lui une longueur maximale de 255.",
        "msg_skip_power_list": "Test non lancé : donnez autant de capteurs de puissance que de chauffages.",
        "msg_skip_driven": "Test non lancé : une prise suit une sonde ou un programme, passez-la en manuel.",
        "msg_stuck": "{stuck} consomme encore après la coupure : relais collé ? Test arrêté, vérifiez tout de suite.",
        "msg_dead": "{heater} n'a rien consommé alors que le bac refroidissait : {start}° → {end}° en {minutes} min. Ce chauffage semble HS.",
        "msg_weak": "{heater} a chauffé mais n'a pas tenu le bac seul : {start}° → {end}° en {minutes} min. Sous-dimensionné ou en fin de vie.",
        "room_sensor": "Température de la pièce (optionnel)",
        "room_sensor_desc": "Évite le test quand la pièce est à la température du bac ou de la consigne, ou au-dessus : le chauffage n'aurait rien à faire et le test ne prouverait rien. Fortement conseillé, surtout sans compteur.",
        "heater_setpoint": "Consigne du chauffage (optionnel)",
        "heater_setpoint_desc": "La température réglée sur le thermostat du chauffage, 0 si inconnue. Évite aussi le test quand le bac est déjà au-dessus.",
        "msg_skip_no_demand": "Test non lancé : le chauffage n'aurait rien à faire (bac {start}°, pièce {room}°, consigne {setpoint}°).",
        "msg_no_demand": "Pas de verdict pour {heater} : {start}° → {end}° en {minutes} min, mais il n'a jamais consommé, donc rien n'est prouvé. Son thermostat est peut-être réglé trop bas, ou la pièce assez chaude pour qu'il reste au repos.",
        "msg_heat_ok": "Consommation confirmée.",
        "msg_cut_ok": "Coupure confirmée pour {proven}.",
        "msg_cut_unproven": "Coupure non vérifiable pour {unproven}, qui ne consommait pas avant.",
        "name": "Test des chauffages du récif",
        "description": (
            "Vérifie périodiquement que chaque chauffage tient le bac à lui "
            "seul : un chauffage reste alimenté, les autres sont coupés le "
            "temps du test, et le résultat est envoyé sur votre téléphone. Le "
            "test s'arrête plus tôt et rétablit tous les chauffages si la "
            "température chute, et les chauffages restés coupés après un "
            "redémarrage sont rallumés. Il faut au moins deux chauffages."
        ),
        "sec_equipment": "Équipement",
        "heaters": "Chauffages",
        "heaters_desc": (
            "Les interrupteurs qui alimentent les chauffages. Ils sont censés "
            "être tous allumés hors test, et tout chauffage trouvé coupé "
            "après un redémarrage est rallumé : pour en retirer un du "
            "service, enlevez-le de cette liste."
        ),
        "sensors": "Capteurs de température",
        "sensors_desc": (
            "Les sondes dans l'eau. La médiane est utilisée : avec trois "
            "sondes, une seule sonde défaillante ne peut pas changer le "
            "verdict."
        ),
        "sec_schedule": "Programmation",
        "test_time": "Heure de début",
        "test_time_desc": (
            "Évitez qu'un test recouvre un changement d'éclairage ou de "
            "vitesse des ventilateurs : chacun fait bouger la température à "
            "lui seul."
        ),
        "cycle_days": "Jours entre deux tests",
        "cycle_days_desc": (
            "Un seul chauffage est testé à chaque fois, à tour de rôle. Avec "
            "deux chauffages et 14 jours, chacun est testé toutes les quatre "
            "semaines."
        ),
        "test_duration": "Durée du test",
        "test_duration_desc": (
            "Un grand volume réagit lentement : en dessous de deux heures "
            "environ, un chauffage inactif peut passer inaperçu."
        ),
        "sec_safety": "Sécurité",
        "max_drop": "Baisse de température tolérée",
        "max_drop_desc": (
            "Au-delà de cette baisse par rapport à la température de départ, "
            "le test échoue et s'arrête aussitôt. Gardez une valeur "
            "supérieure à la résolution de vos sondes."
        ),
        "abort_temperature": "Température d'abandon",
        "abort_temperature_desc": (
            "En dessous de cette valeur, aucun test ne démarre, et un test en "
            "cours s'arrête et rétablit les chauffages."
        ),
        "pause_entities": "Entités de maintenance (optionnel)",
        "pause_entities_desc": (
            "Tant que l'une d'elles est active, aucun test ne démarre et les "
            "chauffages ne sont pas rallumés, car ils peuvent être hors de "
            "l'eau. Ils sont rétablis quand elle se désactive."
        ),
        "sec_notify": "Notifications",
        "notify_devices": "Mobiles à notifier",
        "notify_devices_desc": (
            "Ils reçoivent le résultat de chaque test. Seuls les téléphones "
            "et tablettes enregistrés via l'application Home Assistant "
            "apparaissent."
        ),
        "notify_channel": "Canal Android (optionnel)",
        "notify_channel_desc": (
            "Nom de canal passé dans `data.channel`. Laissez vide pour le "
            "canal par défaut. iOS ignore ce champ."
        ),
        "title": "Récif — test des chauffages",
        "msg_ok": (
            "{heater} a tenu le bac seul pendant {minutes} min : "
            "{start}° → {end}°. Test réussi."
        ),
        "msg_fail_drop": (
            "{heater} n'a pas tenu le bac seul : {start}° → {end}° en "
            "{minutes} min (baisse tolérée : {drop}°). Vérifiez ce chauffage."
        ),
        "msg_fail_cold": (
            "Test de {heater} arrêté après {minutes} min : {end}° est sous "
            "{limit}°. Chauffages rétablis, vérifiez ce chauffage."
        ),
        "msg_interrupted": (
            "Test de {heater} interrompu après {minutes} min, pas de verdict "
            "({start}° → {end}°)."
        ),
        "msg_skip_too_few": "Test non lancé : il faut au moins deux chauffages.",
        "msg_skip_paused": "Test non lancé : maintenance en cours.",
        "msg_skip_no_temperature": "Test non lancé : aucune température disponible.",
        "msg_skip_too_cold": "Test non lancé : {start}° est sous {limit}°.",
        "msg_skip_heater_off": (
            "Test non lancé : tous les chauffages doivent être allumés avant un test."
        ),
        "msg_recovered": (
            "Un test a été interrompu par un redémarrage : chauffages rallumés."
        ),
        "msg_paused_note": (
            "Maintenance en cours : les chauffages restent coupés jusqu'à sa fin."
        ),
        "msg_still_off": "Attention, toujours coupé : {still_off}.",
    },
    "de": {
        "sec_measure": "Messung und Verlauf",
        "power_sensors": "Leistungssensoren (optional)",
        "power_sensors_desc": "Werden für eine Red-Sea-Steckdose oder eine smarte Steckdose automatisch gefunden: leer lassen. Nur nötig, wenn der Zähler an einem anderen Gerät hängt, dann ein Sensor pro Heizung in derselben Reihenfolge wie die Heizungsliste.",
        "power_threshold": "Verbrauchsschwelle",
        "power_threshold_desc": "Oberhalb dieses Werts gilt eine Heizung als verbrauchend, darunter oder gleich als nicht verbrauchend. Über dem Standby-Wert des Zählers halten.",
        "result_entity": "Letztes Ergebnis (optional)",
        "result_entity_desc": "Ein Text-Helfer, der Datum und Ergebnis jedes Laufs erhält. Sein Verlauf behält die früheren. Maximale Länge auf 255 setzen.",
        "msg_skip_power_list": "Test nicht gestartet: Geben Sie so viele Leistungssensoren wie Heizungen an.",
        "msg_skip_driven": "Test nicht gestartet: Eine Steckdose folgt einem Fühler oder Zeitplan, bitte auf manuell stellen.",
        "msg_stuck": "{stuck} verbraucht nach dem Abschalten weiter: Relais verklebt? Test gestoppt, bitte sofort prüfen.",
        "msg_dead": "{heater} hat nichts verbraucht, während das Becken abkühlte: {start}° → {end}° in {minutes} Min. Diese Heizung scheint defekt.",
        "msg_weak": "{heater} hat geheizt, das Becken aber nicht allein gehalten: {start}° → {end}° in {minutes} Min. Zu schwach oder verschlissen.",
        "room_sensor": "Raumtemperatur (optional)",
        "room_sensor_desc": "Überspringt den Test, wenn der Raum so warm wie Becken oder Sollwert oder wärmer ist: Die Heizung hätte nichts zu tun, und der Test würde nichts beweisen. Sehr empfohlen, vor allem ohne Zähler.",
        "heater_setpoint": "Heizungs-Sollwert (optional)",
        "heater_setpoint_desc": "Die am Thermostat der Heizung eingestellte Temperatur, 0 wenn unbekannt. Überspringt den Test auch, wenn das Becken schon darüber liegt.",
        "msg_skip_no_demand": "Test nicht gestartet: Die Heizung hätte nichts zu tun (Becken {start}°, Raum {room}°, Sollwert {setpoint}°).",
        "msg_no_demand": "Kein Ergebnis für {heater}: {start}° → {end}° in {minutes} Min., aber kein Verbrauch, also nichts bewiesen. Der Thermostat ist vielleicht zu niedrig eingestellt, oder der Raum ist so warm, dass sie aus bleibt.",
        "msg_heat_ok": "Verbrauch bestätigt.",
        "msg_cut_ok": "Abschaltung bestätigt für {proven}.",
        "msg_cut_unproven": "Abschaltung nicht prüfbar für {unproven}, vorher kein Verbrauch.",
        "name": "Riff-Heizungstest",
        "description": (
            "Prüft regelmäßig, ob jede Heizung das Becken allein halten kann: "
            "Eine Heizung bleibt eingeschaltet, die anderen werden für die "
            "Testdauer abgeschaltet, und das Ergebnis wird an Ihr Telefon "
            "gesendet. Fällt die Temperatur, endet der Test vorzeitig und "
            "alle Heizungen werden wieder eingeschaltet; auch nach einem "
            "Neustart ausgeschaltet gebliebene Heizungen gehen wieder an. "
            "Mindestens zwei Heizungen sind erforderlich."
        ),
        "sec_equipment": "Ausstattung",
        "heaters": "Heizungen",
        "heaters_desc": (
            "Die Schalter, die die Heizungen versorgen. Außerhalb eines Tests "
            "sollen alle eingeschaltet sein, und jede nach einem Neustart "
            "ausgeschaltete Heizung wird wieder eingeschaltet: Um eine außer "
            "Betrieb zu nehmen, entfernen Sie sie aus dieser Liste."
        ),
        "sensors": "Temperatursensoren",
        "sensors_desc": (
            "Die Fühler im Wasser. Es wird der Median verwendet: Bei drei "
            "Fühlern kann ein einzelner defekter das Ergebnis nicht ändern."
        ),
        "sec_schedule": "Zeitplan",
        "test_time": "Startzeit",
        "test_time_desc": (
            "Vermeiden Sie Überschneidungen mit Licht- oder "
            "Lüfterwechseln: Beides verändert die Temperatur von selbst."
        ),
        "cycle_days": "Tage zwischen den Tests",
        "cycle_days_desc": (
            "Es wird jeweils eine Heizung getestet, reihum. Bei zwei Heizungen "
            "und 14 Tagen wird jede alle vier Wochen getestet."
        ),
        "test_duration": "Testdauer",
        "test_duration_desc": (
            "Ein großes Volumen reagiert langsam: Unter etwa zwei Stunden "
            "kann eine untätige Heizung unbemerkt bleiben."
        ),
        "sec_safety": "Sicherheit",
        "max_drop": "Zulässiger Temperaturabfall",
        "max_drop_desc": (
            "Wird dieser Abfall gegenüber der Starttemperatur überschritten, "
            "schlägt der Test fehl und endet sofort. Wählen Sie einen Wert "
            "über der Auflösung Ihrer Fühler."
        ),
        "abort_temperature": "Abbruchtemperatur",
        "abort_temperature_desc": (
            "Unterhalb dieses Werts startet kein Test, und ein laufender Test "
            "endet und schaltet die Heizungen wieder ein."
        ),
        "pause_entities": "Wartungsentitäten (optional)",
        "pause_entities_desc": (
            "Solange eine davon eingeschaltet ist, startet kein Test und die "
            "Heizungen werden nicht eingeschaltet, da sie außerhalb des "
            "Wassers sein könnten. Sie gehen wieder an, sobald sie ausgeht."
        ),
        "sec_notify": "Benachrichtigungen",
        "notify_devices": "Zu benachrichtigende Mobilgeräte",
        "notify_devices_desc": (
            "Sie erhalten das Ergebnis jedes Tests. Es werden nur über die "
            "Home-Assistant-App registrierte Telefone und Tablets angezeigt."
        ),
        "notify_channel": "Android-Kanal (optional)",
        "notify_channel_desc": (
            "Kanalname für `data.channel`. Für den Standardkanal leer lassen. "
            "iOS ignoriert dieses Feld."
        ),
        "title": "Riff — Heizungstest",
        "msg_ok": (
            "{heater} hat das Becken {minutes} Min. allein gehalten: "
            "{start}° → {end}°. Test bestanden."
        ),
        "msg_fail_drop": (
            "{heater} hat das Becken nicht allein gehalten: {start}° → {end}° "
            "in {minutes} Min. (zulässig: {drop}°). Bitte prüfen."
        ),
        "msg_fail_cold": (
            "Test von {heater} nach {minutes} Min. gestoppt: {end}° liegt "
            "unter {limit}°. Heizungen wieder an, bitte prüfen."
        ),
        "msg_interrupted": (
            "Test von {heater} nach {minutes} Min. unterbrochen, kein Ergebnis "
            "({start}° → {end}°)."
        ),
        "msg_skip_too_few": (
            "Test nicht gestartet: Mindestens zwei Heizungen sind nötig."
        ),
        "msg_skip_paused": "Test nicht gestartet: Wartung läuft.",
        "msg_skip_no_temperature": "Test nicht gestartet: keine Temperatur verfügbar.",
        "msg_skip_too_cold": "Test nicht gestartet: {start}° liegt unter {limit}°.",
        "msg_skip_heater_off": (
            "Test nicht gestartet: Alle Heizungen müssen eingeschaltet sein."
        ),
        "msg_recovered": (
            "Ein Test wurde durch einen Neustart unterbrochen: Heizungen "
            "wieder eingeschaltet."
        ),
        "msg_paused_note": "Wartung läuft: Die Heizungen bleiben bis zum Ende aus.",
        "msg_still_off": "Achtung, weiterhin aus: {still_off}.",
    },
    "es": {
        "sec_measure": "Medición e historial",
        "power_sensors": "Sensores de potencia (opcional)",
        "power_sensors_desc": "Se encuentran automáticamente para un enchufe Red Sea o un enchufe inteligente: déjelo vacío. Solo es útil si el medidor está en otro dispositivo, con un sensor por calentador, en el mismo orden que la lista de calentadores.",
        "power_threshold": "Umbral de consumo",
        "power_threshold_desc": "Por encima de este valor un calentador se considera en consumo; igual o por debajo, sin consumo. Manténgalo por encima del reposo del medidor.",
        "result_entity": "Último resultado (opcional)",
        "result_entity_desc": "Un ayudante de texto que recibe la fecha y el resultado de cada ejecución. Su historial conserva los anteriores. Dele una longitud máxima de 255.",
        "msg_skip_power_list": "Prueba no iniciada: indique tantos sensores de potencia como calentadores.",
        "msg_skip_driven": "Prueba no iniciada: un enchufe sigue una sonda o un programa, póngalo en manual.",
        "msg_stuck": "{stuck} sigue consumiendo tras el corte: ¿relé pegado? Prueba detenida, revíselo ahora.",
        "msg_dead": "{heater} no consumió nada mientras el acuario se enfriaba: {start}° → {end}° en {minutes} min. Este calentador parece averiado.",
        "msg_weak": "{heater} calentó pero no mantuvo el acuario solo: {start}° → {end}° en {minutes} min. Insuficiente o desgastado.",
        "room_sensor": "Temperatura de la habitación (opcional)",
        "room_sensor_desc": "Evita la prueba cuando la habitación está a la temperatura del acuario o de la consigna, o por encima: el calentador no tendría nada que hacer y la prueba no demostraría nada. Muy recomendable, sobre todo sin medidor.",
        "heater_setpoint": "Consigna del calentador (opcional)",
        "heater_setpoint_desc": "La temperatura ajustada en el termostato del calentador, 0 si se desconoce. También evita la prueba cuando el acuario ya está por encima.",
        "msg_skip_no_demand": "Prueba no iniciada: el calentador no tendría nada que hacer (acuario {start}°, habitación {room}°, consigna {setpoint}°).",
        "msg_no_demand": "Sin resultado para {heater}: {start}° → {end}° en {minutes} min, pero nunca consumió, así que nada está probado. Quizá su termostato esté demasiado bajo, o la habitación lo bastante cálida para que siga en reposo.",
        "msg_heat_ok": "Consumo confirmado.",
        "msg_cut_ok": "Corte confirmado para {proven}.",
        "msg_cut_unproven": "Corte no verificable para {unproven}, que no consumía antes.",
        "name": "Prueba de calentadores del arrecife",
        "description": (
            "Comprueba periódicamente que cada calentador mantiene el acuario "
            "por sí solo: un calentador sigue encendido, los demás se apagan "
            "durante la prueba y el resultado se envía a su teléfono. La "
            "prueba se detiene antes y restablece todos los calentadores si "
            "la temperatura baja, y los calentadores que quedan apagados tras "
            "un reinicio vuelven a encenderse. Se necesitan al menos dos "
            "calentadores."
        ),
        "sec_equipment": "Equipo",
        "heaters": "Calentadores",
        "heaters_desc": (
            "Los interruptores que alimentan los calentadores. Fuera de una "
            "prueba deben estar todos encendidos, y cualquier calentador "
            "apagado tras un reinicio se vuelve a encender: para retirar uno "
            "del servicio, quítelo de esta lista."
        ),
        "sensors": "Sensores de temperatura",
        "sensors_desc": (
            "Las sondas en el agua. Se usa la mediana: con tres sondas, una "
            "sola defectuosa no puede cambiar el resultado."
        ),
        "sec_schedule": "Programación",
        "test_time": "Hora de inicio",
        "test_time_desc": (
            "Evite que una prueba coincida con un cambio de iluminación o de "
            "velocidad de los ventiladores: ambos mueven la temperatura por "
            "sí solos."
        ),
        "cycle_days": "Días entre pruebas",
        "cycle_days_desc": (
            "Se prueba un solo calentador cada vez, por turnos. Con dos "
            "calentadores y 14 días, cada uno se prueba cada cuatro semanas."
        ),
        "test_duration": "Duración de la prueba",
        "test_duration_desc": (
            "Un gran volumen reacciona despacio: por debajo de unas dos "
            "horas, un calentador inactivo puede pasar desapercibido."
        ),
        "sec_safety": "Seguridad",
        "max_drop": "Bajada de temperatura tolerada",
        "max_drop_desc": (
            "Más allá de esta bajada respecto a la temperatura inicial, la "
            "prueba falla y se detiene de inmediato. Mantenga un valor "
            "superior a la resolución de sus sondas."
        ),
        "abort_temperature": "Temperatura de cancelación",
        "abort_temperature_desc": (
            "Por debajo de este valor no se inicia ninguna prueba, y una "
            "prueba en curso se detiene y restablece los calentadores."
        ),
        "pause_entities": "Entidades de mantenimiento (opcional)",
        "pause_entities_desc": (
            "Mientras alguna esté activa, no se inicia ninguna prueba y los "
            "calentadores no se encienden, porque pueden estar fuera del "
            "agua. Se restablecen cuando se desactiva."
        ),
        "sec_notify": "Notificaciones",
        "notify_devices": "Móviles a notificar",
        "notify_devices_desc": (
            "Reciben el resultado de cada prueba. Solo aparecen los teléfonos "
            "y tabletas registrados con la aplicación Home Assistant."
        ),
        "notify_channel": "Canal Android (opcional)",
        "notify_channel_desc": (
            "Nombre de canal enviado en `data.channel`. Déjelo vacío para el "
            "canal predeterminado. iOS ignora este campo."
        ),
        "title": "Arrecife — prueba de calentadores",
        "msg_ok": (
            "{heater} mantuvo el acuario solo durante {minutes} min: "
            "{start}° → {end}°. Prueba superada."
        ),
        "msg_fail_drop": (
            "{heater} no mantuvo el acuario solo: {start}° → {end}° en "
            "{minutes} min (bajada tolerada: {drop}°). Revise este calentador."
        ),
        "msg_fail_cold": (
            "Prueba de {heater} detenida tras {minutes} min: {end}° está por "
            "debajo de {limit}°. Calentadores restablecidos, revise este "
            "calentador."
        ),
        "msg_interrupted": (
            "Prueba de {heater} interrumpida tras {minutes} min, sin resultado "
            "({start}° → {end}°)."
        ),
        "msg_skip_too_few": (
            "Prueba no iniciada: se necesitan al menos dos calentadores."
        ),
        "msg_skip_paused": "Prueba no iniciada: mantenimiento en curso.",
        "msg_skip_no_temperature": "Prueba no iniciada: ninguna temperatura disponible.",
        "msg_skip_too_cold": "Prueba no iniciada: {start}° está por debajo de {limit}°.",
        "msg_skip_heater_off": (
            "Prueba no iniciada: todos los calentadores deben estar encendidos."
        ),
        "msg_recovered": (
            "Un reinicio interrumpió una prueba: calentadores encendidos de nuevo."
        ),
        "msg_paused_note": (
            "Mantenimiento en curso: los calentadores siguen apagados hasta "
            "que termine."
        ),
        "msg_still_off": "Atención, sigue apagado: {still_off}.",
    },
    "it": {
        "sec_measure": "Misura e cronologia",
        "power_sensors": "Sensori di potenza (opzionale)",
        "power_sensors_desc": "Trovati automaticamente per una presa Red Sea o una presa smart: lasciate vuoto. Serve solo se il misuratore è su un altro dispositivo, con un sensore per riscaldatore, nello stesso ordine dell'elenco dei riscaldatori.",
        "power_threshold": "Soglia di consumo",
        "power_threshold_desc": "Sopra questo valore un riscaldatore è considerato in consumo; pari o sotto, non in consumo. Mantenetela sopra lo standby del misuratore.",
        "result_entity": "Ultimo risultato (opzionale)",
        "result_entity_desc": "Un helper di testo che riceve la data e il risultato di ogni esecuzione. La sua cronologia conserva i precedenti. Impostate una lunghezza massima di 255.",
        "msg_skip_power_list": "Test non avviato: indicate tanti sensori di potenza quanti riscaldatori.",
        "msg_skip_driven": "Test non avviato: una presa segue una sonda o un programma, mettetela in manuale.",
        "msg_stuck": "{stuck} consuma ancora dopo lo spegnimento: relè incollato? Test fermato, controllate subito.",
        "msg_dead": "{heater} non ha consumato nulla mentre la vasca si raffreddava: {start}° → {end}° in {minutes} min. Questo riscaldatore sembra guasto.",
        "msg_weak": "{heater} ha scaldato ma non ha retto la vasca da solo: {start}° → {end}° in {minutes} min. Sottodimensionato o usurato.",
        "room_sensor": "Temperatura della stanza (opzionale)",
        "room_sensor_desc": "Evita il test quando la stanza è alla temperatura della vasca o del setpoint, o più calda: il riscaldatore non avrebbe nulla da fare e il test non dimostrerebbe nulla. Vivamente consigliato, soprattutto senza misuratore.",
        "heater_setpoint": "Setpoint del riscaldatore (opzionale)",
        "heater_setpoint_desc": "La temperatura impostata sul termostato del riscaldatore, 0 se sconosciuta. Evita il test anche quando la vasca è già sopra.",
        "msg_skip_no_demand": "Test non avviato: il riscaldatore non avrebbe nulla da fare (vasca {start}°, stanza {room}°, setpoint {setpoint}°).",
        "msg_no_demand": "Nessun risultato per {heater}: {start}° → {end}° in {minutes} min, ma non ha mai consumato, quindi nulla è provato. Il termostato potrebbe essere troppo basso, o la stanza abbastanza calda da lasciarlo a riposo.",
        "msg_heat_ok": "Consumo confermato.",
        "msg_cut_ok": "Spegnimento confermato per {proven}.",
        "msg_cut_unproven": "Spegnimento non verificabile per {unproven}, che prima non consumava.",
        "name": "Test dei riscaldatori del reef",
        "description": (
            "Verifica periodicamente che ogni riscaldatore regga la vasca da "
            "solo: un riscaldatore resta acceso, gli altri vengono spenti per "
            "la durata del test e il risultato arriva sul telefono. Il test "
            "si ferma prima e ripristina tutti i riscaldatori se la "
            "temperatura scende, e i riscaldatori rimasti spenti dopo un "
            "riavvio vengono riaccesi. Servono almeno due riscaldatori."
        ),
        "sec_equipment": "Attrezzatura",
        "heaters": "Riscaldatori",
        "heaters_desc": (
            "Gli interruttori che alimentano i riscaldatori. Fuori da un test "
            "devono essere tutti accesi, e ogni riscaldatore trovato spento "
            "dopo un riavvio viene riacceso: per metterne uno fuori servizio, "
            "toglietelo da questo elenco."
        ),
        "sensors": "Sensori di temperatura",
        "sensors_desc": (
            "Le sonde in acqua. Viene usata la mediana: con tre sonde, una "
            "sola difettosa non può cambiare il risultato."
        ),
        "sec_schedule": "Programmazione",
        "test_time": "Ora di inizio",
        "test_time_desc": (
            "Evitate che un test si sovrapponga a un cambio di illuminazione "
            "o di velocità delle ventole: entrambi spostano la temperatura da "
            "soli."
        ),
        "cycle_days": "Giorni tra due test",
        "cycle_days_desc": (
            "Viene testato un solo riscaldatore alla volta, a rotazione. Con "
            "due riscaldatori e 14 giorni, ciascuno è testato ogni quattro "
            "settimane."
        ),
        "test_duration": "Durata del test",
        "test_duration_desc": (
            "Un grande volume reagisce lentamente: sotto le due ore circa, un "
            "riscaldatore inattivo può passare inosservato."
        ),
        "sec_safety": "Sicurezza",
        "max_drop": "Calo di temperatura tollerato",
        "max_drop_desc": (
            "Oltre questo calo rispetto alla temperatura iniziale il test "
            "fallisce e si ferma subito. Mantenete un valore superiore alla "
            "risoluzione delle sonde."
        ),
        "abort_temperature": "Temperatura di interruzione",
        "abort_temperature_desc": (
            "Sotto questo valore nessun test parte, e un test in corso si "
            "ferma e ripristina i riscaldatori."
        ),
        "pause_entities": "Entità di manutenzione (opzionale)",
        "pause_entities_desc": (
            "Finché una di esse è attiva, nessun test parte e i riscaldatori "
            "non vengono riaccesi, perché potrebbero essere fuori dall'acqua. "
            "Vengono ripristinati quando si disattiva."
        ),
        "sec_notify": "Notifiche",
        "notify_devices": "Dispositivi mobili da avvisare",
        "notify_devices_desc": (
            "Ricevono il risultato di ogni test. Compaiono solo telefoni e "
            "tablet registrati tramite l'app Home Assistant."
        ),
        "notify_channel": "Canale Android (opzionale)",
        "notify_channel_desc": (
            "Nome del canale passato in `data.channel`. Lasciate vuoto per il "
            "canale predefinito. iOS ignora questo campo."
        ),
        "title": "Reef — test dei riscaldatori",
        "msg_ok": (
            "{heater} ha retto la vasca da solo per {minutes} min: "
            "{start}° → {end}°. Test superato."
        ),
        "msg_fail_drop": (
            "{heater} non ha retto la vasca da solo: {start}° → {end}° in "
            "{minutes} min (calo tollerato: {drop}°). Controllate questo "
            "riscaldatore."
        ),
        "msg_fail_cold": (
            "Test di {heater} fermato dopo {minutes} min: {end}° è sotto "
            "{limit}°. Riscaldatori ripristinati, controllate questo "
            "riscaldatore."
        ),
        "msg_interrupted": (
            "Test di {heater} interrotto dopo {minutes} min, nessun risultato "
            "({start}° → {end}°)."
        ),
        "msg_skip_too_few": "Test non avviato: servono almeno due riscaldatori.",
        "msg_skip_paused": "Test non avviato: manutenzione in corso.",
        "msg_skip_no_temperature": "Test non avviato: nessuna temperatura disponibile.",
        "msg_skip_too_cold": "Test non avviato: {start}° è sotto {limit}°.",
        "msg_skip_heater_off": (
            "Test non avviato: tutti i riscaldatori devono essere accesi."
        ),
        "msg_recovered": ("Un riavvio ha interrotto un test: riscaldatori riaccesi."),
        "msg_paused_note": (
            "Manutenzione in corso: i riscaldatori restano spenti fino alla fine."
        ),
        "msg_still_off": "Attenzione, ancora spento: {still_off}.",
    },
    "nl": {
        "sec_measure": "Meting en geschiedenis",
        "power_sensors": "Vermogenssensoren (optioneel)",
        "power_sensors_desc": "Worden automatisch gevonden voor een Red Sea-contactdoos of slimme stekker: laat leeg. Alleen nodig als de meter op een ander apparaat zit, dan één sensor per verwarming, in dezelfde volgorde als de lijst met verwarmingen.",
        "power_threshold": "Verbruiksdrempel",
        "power_threshold_desc": "Boven deze waarde telt een verwarming als verbruikend, gelijk of eronder als niet verbruikend. Houd hem boven de stand-bywaarde van de meter.",
        "result_entity": "Laatste resultaat (optioneel)",
        "result_entity_desc": "Een teksthelper die de datum en het resultaat van elke run krijgt. Zijn geschiedenis bewaart de eerdere. Geef hem een maximale lengte van 255.",
        "msg_skip_power_list": "Test niet gestart: geef evenveel vermogenssensoren als verwarmingen.",
        "msg_skip_driven": "Test niet gestart: een contactdoos volgt een sonde of programma, zet hem op handmatig.",
        "msg_stuck": "{stuck} verbruikt nog na het uitschakelen: relais vastgeplakt? Test gestopt, controleer het nu.",
        "msg_dead": "{heater} verbruikte niets terwijl de bak afkoelde: {start}° → {end}° in {minutes} min. Deze verwarming lijkt defect.",
        "msg_weak": "{heater} heeft verwarmd maar hield de bak niet alleen op temperatuur: {start}° → {end}° in {minutes} min. Te zwak of versleten.",
        "room_sensor": "Kamertemperatuur (optioneel)",
        "room_sensor_desc": "Slaat de test over als de kamer even warm is als de bak of het instelpunt, of warmer: de verwarming zou niets te doen hebben en de test zou niets bewijzen. Sterk aangeraden, vooral zonder meter.",
        "heater_setpoint": "Instelpunt van de verwarming (optioneel)",
        "heater_setpoint_desc": "De temperatuur die op de thermostaat van de verwarming staat, 0 indien onbekend. Slaat de test ook over als de bak er al boven zit.",
        "msg_skip_no_demand": "Test niet gestart: de verwarming zou niets te doen hebben (bak {start}°, kamer {room}°, instelpunt {setpoint}°).",
        "msg_no_demand": "Geen uitslag voor {heater}: {start}° → {end}° in {minutes} min, maar hij verbruikte nooit iets, dus niets is bewezen. Zijn thermostaat staat misschien te laag, of de kamer is warm genoeg om hem uit te laten.",
        "msg_heat_ok": "Verbruik bevestigd.",
        "msg_cut_ok": "Uitschakeling bevestigd voor {proven}.",
        "msg_cut_unproven": "Uitschakeling niet aantoonbaar voor {unproven}, die vooraf niets verbruikte.",
        "name": "Rifverwarmingstest",
        "description": (
            "Controleert regelmatig of elke verwarming de bak alleen op "
            "temperatuur kan houden: één verwarming blijft aan, de andere "
            "gaan uit tijdens de test en het resultaat gaat naar uw telefoon. "
            "De test stopt eerder en herstelt alle verwarmingen als de "
            "temperatuur daalt, en verwarmingen die na een herstart uit zijn "
            "gebleven gaan weer aan. Er zijn minstens twee verwarmingen nodig."
        ),
        "sec_equipment": "Apparatuur",
        "heaters": "Verwarmingen",
        "heaters_desc": (
            "De schakelaars die de verwarmingen voeden. Buiten een test horen "
            "ze allemaal aan te staan, en elke verwarming die na een herstart "
            "uit staat gaat weer aan: haal er een uit deze lijst om hem buiten "
            "gebruik te stellen."
        ),
        "sensors": "Temperatuursensoren",
        "sensors_desc": (
            "De sondes in het water. De mediaan wordt gebruikt: bij drie "
            "sondes kan één defecte de uitslag niet veranderen."
        ),
        "sec_schedule": "Planning",
        "test_time": "Starttijd",
        "test_time_desc": (
            "Vermijd een test die samenvalt met een wisseling van verlichting "
            "of ventilatorsnelheid: beide veranderen zelf de temperatuur."
        ),
        "cycle_days": "Dagen tussen tests",
        "cycle_days_desc": (
            "Elke keer wordt één verwarming getest, om de beurt. Met twee "
            "verwarmingen en 14 dagen wordt elk om de vier weken getest."
        ),
        "test_duration": "Testduur",
        "test_duration_desc": (
            "Een groot volume reageert traag: onder ongeveer twee uur kan een "
            "inactieve verwarming onopgemerkt blijven."
        ),
        "sec_safety": "Veiligheid",
        "max_drop": "Toegestane temperatuurdaling",
        "max_drop_desc": (
            "Boven deze daling ten opzichte van de starttemperatuur mislukt "
            "de test en stopt hij meteen. Houd de waarde boven de resolutie "
            "van uw sondes."
        ),
        "abort_temperature": "Afbreektemperatuur",
        "abort_temperature_desc": (
            "Onder deze waarde start geen test, en een lopende test stopt en "
            "herstelt de verwarmingen."
        ),
        "pause_entities": "Onderhoudsentiteiten (optioneel)",
        "pause_entities_desc": (
            "Zolang een daarvan aan staat, start er geen test en gaan "
            "verwarmingen niet aan, omdat ze uit het water kunnen zijn. Ze "
            "worden hersteld zodra die uit gaat."
        ),
        "sec_notify": "Meldingen",
        "notify_devices": "Mobiele apparaten voor meldingen",
        "notify_devices_desc": (
            "Zij krijgen het resultaat van elke test. Alleen telefoons en "
            "tablets die via de Home Assistant-app zijn geregistreerd, staan "
            "in de lijst."
        ),
        "notify_channel": "Android-kanaal (optioneel)",
        "notify_channel_desc": (
            "Kanaalnaam voor `data.channel`. Laat leeg voor het "
            "standaardkanaal. iOS negeert dit veld."
        ),
        "title": "Rif — verwarmingstest",
        "msg_ok": (
            "{heater} hield de bak {minutes} min alleen op temperatuur: "
            "{start}° → {end}°. Test geslaagd."
        ),
        "msg_fail_drop": (
            "{heater} hield de bak niet alleen op temperatuur: "
            "{start}° → {end}° in {minutes} min (toegestane daling: {drop}°). "
            "Controleer deze verwarming."
        ),
        "msg_fail_cold": (
            "Test van {heater} gestopt na {minutes} min: {end}° ligt onder "
            "{limit}°. Verwarmingen hersteld, controleer deze verwarming."
        ),
        "msg_interrupted": (
            "Test van {heater} onderbroken na {minutes} min, geen uitslag "
            "({start}° → {end}°)."
        ),
        "msg_skip_too_few": "Test niet gestart: minstens twee verwarmingen nodig.",
        "msg_skip_paused": "Test niet gestart: onderhoud bezig.",
        "msg_skip_no_temperature": "Test niet gestart: geen temperatuur beschikbaar.",
        "msg_skip_too_cold": "Test niet gestart: {start}° ligt onder {limit}°.",
        "msg_skip_heater_off": (
            "Test niet gestart: alle verwarmingen moeten aan staan."
        ),
        "msg_recovered": (
            "Een herstart onderbrak een test: verwarmingen weer aangezet."
        ),
        "msg_paused_note": (
            "Onderhoud bezig: de verwarmingen blijven uit tot het klaar is."
        ),
        "msg_still_off": "Let op, nog steeds uit: {still_off}.",
    },
    "pl": {
        "sec_measure": "Pomiar i historia",
        "power_sensors": "Czujniki mocy (opcjonalnie)",
        "power_sensors_desc": "Wykrywane automatycznie dla gniazda Red Sea lub inteligentnej wtyczki: pozostaw puste. Potrzebne tylko, gdy licznik jest na innym urządzeniu, wtedy po jednym czujniku na grzałkę, w tej samej kolejności co lista grzałek.",
        "power_threshold": "Próg poboru",
        "power_threshold_desc": "Powyżej tej wartości grzałka jest uznawana za pobierającą moc, poniżej lub przy równej za niepobierającą. Ustaw powyżej odczytu czuwania licznika.",
        "result_entity": "Ostatni wynik (opcjonalnie)",
        "result_entity_desc": "Pomocnik tekstowy otrzymujący datę i wynik każdego uruchomienia. Jego historia zachowuje poprzednie. Ustaw maksymalną długość 255.",
        "msg_skip_power_list": "Test nieuruchomiony: podaj tyle czujników mocy, ile grzałek.",
        "msg_skip_driven": "Test nieuruchomiony: gniazdo podąża za sondą lub harmonogramem, przełącz je na tryb ręczny.",
        "msg_stuck": "{stuck} nadal pobiera moc po wyłączeniu: sklejony przekaźnik? Test zatrzymany, sprawdź natychmiast.",
        "msg_dead": "{heater} nic nie pobrała, gdy akwarium stygło: {start}° → {end}° w {minutes} min. Ta grzałka wygląda na uszkodzoną.",
        "msg_weak": "{heater} grzała, ale nie utrzymała akwarium sama: {start}° → {end}° w {minutes} min. Za słaba lub zużyta.",
        "room_sensor": "Temperatura pomieszczenia (opcjonalnie)",
        "room_sensor_desc": "Pomija test, gdy w pomieszczeniu jest tyle stopni co w akwarium lub na nastawie albo więcej: grzałka nie miałaby nic do roboty, a test niczego by nie dowiódł. Zdecydowanie zalecane, zwłaszcza bez licznika.",
        "heater_setpoint": "Nastawa grzałki (opcjonalnie)",
        "heater_setpoint_desc": "Temperatura ustawiona na termostacie grzałki, 0 jeśli nieznana. Pomija test także wtedy, gdy akwarium jest już powyżej niej.",
        "msg_skip_no_demand": "Test nieuruchomiony: grzałka nie miałaby nic do roboty (akwarium {start}°, pomieszczenie {room}°, nastawa {setpoint}°).",
        "msg_no_demand": "Brak wyniku dla {heater}: {start}° → {end}° w {minutes} min, ale nie pobrała mocy, więc nic nie zostało udowodnione. Jej termostat może być ustawiony za nisko albo w pomieszczeniu jest na tyle ciepło, że pozostała w spoczynku.",
        "msg_heat_ok": "Pobór potwierdzony.",
        "msg_cut_ok": "Wyłączenie potwierdzone dla {proven}.",
        "msg_cut_unproven": "Wyłączenia nie da się potwierdzić dla {unproven}, wcześniej bez poboru.",
        "name": "Test grzałek rafy",
        "description": (
            "Okresowo sprawdza, czy każda grzałka sama utrzyma temperaturę w "
            "akwarium: jedna grzałka pozostaje włączona, pozostałe są "
            "wyłączane na czas testu, a wynik trafia na telefon. Test kończy "
            "się wcześniej i przywraca wszystkie grzałki, gdy temperatura "
            "spada, a grzałki wyłączone po restarcie są włączane ponownie. "
            "Potrzebne są co najmniej dwie grzałki."
        ),
        "sec_equipment": "Sprzęt",
        "heaters": "Grzałki",
        "heaters_desc": (
            "Przełączniki zasilające grzałki. Poza testem wszystkie powinny "
            "być włączone, a każda grzałka wyłączona po restarcie jest "
            "włączana ponownie: aby wycofać jedną z użytku, usuń ją z tej "
            "listy."
        ),
        "sensors": "Czujniki temperatury",
        "sensors_desc": (
            "Sondy w wodzie. Używana jest mediana: przy trzech sondach jedna "
            "uszkodzona nie zmieni wyniku."
        ),
        "sec_schedule": "Harmonogram",
        "test_time": "Godzina rozpoczęcia",
        "test_time_desc": (
            "Unikaj testu nakładającego się na zmianę oświetlenia lub "
            "prędkości wentylatorów: każda z nich sama zmienia temperaturę."
        ),
        "cycle_days": "Dni między testami",
        "cycle_days_desc": (
            "Za każdym razem testowana jest jedna grzałka, po kolei. Przy "
            "dwóch grzałkach i 14 dniach każda jest testowana co cztery "
            "tygodnie."
        ),
        "test_duration": "Czas testu",
        "test_duration_desc": (
            "Duża objętość reaguje powoli: poniżej około dwóch godzin "
            "niedziałająca grzałka może pozostać niezauważona."
        ),
        "sec_safety": "Bezpieczeństwo",
        "max_drop": "Dopuszczalny spadek temperatury",
        "max_drop_desc": (
            "Po przekroczeniu tego spadku względem temperatury początkowej "
            "test kończy się niepowodzeniem i natychmiast zatrzymuje. Ustaw "
            "wartość większą niż rozdzielczość sond."
        ),
        "abort_temperature": "Temperatura przerwania",
        "abort_temperature_desc": (
            "Poniżej tej wartości test się nie rozpocznie, a trwający test "
            "zatrzyma się i przywróci grzałki."
        ),
        "pause_entities": "Encje konserwacji (opcjonalnie)",
        "pause_entities_desc": (
            "Gdy którakolwiek jest włączona, test się nie rozpocznie, a "
            "grzałki nie zostaną włączone, ponieważ mogą być poza wodą. Są "
            "przywracane po jej wyłączeniu."
        ),
        "sec_notify": "Powiadomienia",
        "notify_devices": "Urządzenia mobilne do powiadamiania",
        "notify_devices_desc": (
            "Otrzymują wynik każdego testu. Na liście są tylko telefony i "
            "tablety zarejestrowane przez aplikację Home Assistant."
        ),
        "notify_channel": "Kanał Android (opcjonalnie)",
        "notify_channel_desc": (
            "Nazwa kanału przekazywana w `data.channel`. Pozostaw puste dla "
            "kanału domyślnego. iOS ignoruje to pole."
        ),
        "title": "Rafa — test grzałek",
        "msg_ok": (
            "{heater} sama utrzymała akwarium przez {minutes} min: "
            "{start}° → {end}°. Test zaliczony."
        ),
        "msg_fail_drop": (
            "{heater} nie utrzymała akwarium sama: {start}° → {end}° w "
            "{minutes} min (dopuszczalny spadek: {drop}°). Sprawdź tę grzałkę."
        ),
        "msg_fail_cold": (
            "Test {heater} zatrzymany po {minutes} min: {end}° to mniej niż "
            "{limit}°. Grzałki przywrócone, sprawdź tę grzałkę."
        ),
        "msg_interrupted": (
            "Test {heater} przerwany po {minutes} min, brak wyniku ({start}° → {end}°)."
        ),
        "msg_skip_too_few": (
            "Test nieuruchomiony: potrzebne są co najmniej dwie grzałki."
        ),
        "msg_skip_paused": "Test nieuruchomiony: trwa konserwacja.",
        "msg_skip_no_temperature": "Test nieuruchomiony: brak temperatury.",
        "msg_skip_too_cold": "Test nieuruchomiony: {start}° to mniej niż {limit}°.",
        "msg_skip_heater_off": (
            "Test nieuruchomiony: wszystkie grzałki muszą być włączone."
        ),
        "msg_recovered": "Restart przerwał test: grzałki włączone ponownie.",
        "msg_paused_note": (
            "Trwa konserwacja: grzałki pozostają wyłączone do jej zakończenia."
        ),
        "msg_still_off": "Uwaga, nadal wyłączone: {still_off}.",
    },
    "pt": {
        "sec_measure": "Medição e histórico",
        "power_sensors": "Sensores de potência (opcional)",
        "power_sensors_desc": "Encontrados automaticamente para uma tomada Red Sea ou uma tomada inteligente: deixe vazio. Só é útil se o medidor estiver noutro dispositivo, com um sensor por aquecedor, pela mesma ordem da lista de aquecedores.",
        "power_threshold": "Limiar de consumo",
        "power_threshold_desc": "Acima deste valor um aquecedor conta como a consumir; igual ou abaixo, como sem consumo. Mantenha-o acima do repouso do medidor.",
        "result_entity": "Último resultado (opcional)",
        "result_entity_desc": "Um auxiliar de texto que recebe a data e o resultado de cada execução. O seu histórico guarda os anteriores. Dê-lhe um comprimento máximo de 255.",
        "msg_skip_power_list": "Teste não iniciado: indique tantos sensores de potência como aquecedores.",
        "msg_skip_driven": "Teste não iniciado: uma tomada segue uma sonda ou um programa, passe-a para manual.",
        "msg_stuck": "{stuck} continua a consumir após o corte: relé colado? Teste parado, verifique já.",
        "msg_dead": "{heater} não consumiu nada enquanto o aquário arrefecia: {start}° → {end}° em {minutes} min. Este aquecedor parece avariado.",
        "msg_weak": "{heater} aqueceu mas não manteve o aquário sozinho: {start}° → {end}° em {minutes} min. Insuficiente ou desgastado.",
        "room_sensor": "Temperatura da divisão (opcional)",
        "room_sensor_desc": "Evita o teste quando a divisão está à temperatura do aquário ou da consigna, ou acima: o aquecedor não teria nada a fazer e o teste não provaria nada. Muito aconselhado, sobretudo sem medidor.",
        "heater_setpoint": "Consigna do aquecedor (opcional)",
        "heater_setpoint_desc": "A temperatura regulada no termóstato do aquecedor, 0 se desconhecida. Evita também o teste quando o aquário já está acima.",
        "msg_skip_no_demand": "Teste não iniciado: o aquecedor não teria nada a fazer (aquário {start}°, divisão {room}°, consigna {setpoint}°).",
        "msg_no_demand": "Sem resultado para {heater}: {start}° → {end}° em {minutes} min, mas nunca consumiu, logo nada ficou provado. O termóstato pode estar demasiado baixo, ou a divisão quente o suficiente para ficar em repouso.",
        "msg_heat_ok": "Consumo confirmado.",
        "msg_cut_ok": "Corte confirmado para {proven}.",
        "msg_cut_unproven": "Corte não verificável para {unproven}, que não consumia antes.",
        "name": "Teste dos aquecedores do recife",
        "description": (
            "Verifica periodicamente que cada aquecedor mantém o aquário "
            "sozinho: um aquecedor fica ligado, os outros são desligados "
            "durante o teste e o resultado é enviado para o seu telemóvel. O "
            "teste termina mais cedo e repõe todos os aquecedores se a "
            "temperatura descer, e os aquecedores que ficam desligados após "
            "um reinício voltam a ligar-se. São necessários pelo menos dois "
            "aquecedores."
        ),
        "sec_equipment": "Equipamento",
        "heaters": "Aquecedores",
        "heaters_desc": (
            "Os interruptores que alimentam os aquecedores. Fora de um teste "
            "devem estar todos ligados, e qualquer aquecedor desligado após "
            "um reinício volta a ligar-se: para retirar um de serviço, "
            "remova-o desta lista."
        ),
        "sensors": "Sensores de temperatura",
        "sensors_desc": (
            "As sondas na água. É usada a mediana: com três sondas, uma só "
            "avariada não pode alterar o resultado."
        ),
        "sec_schedule": "Agendamento",
        "test_time": "Hora de início",
        "test_time_desc": (
            "Evite que um teste coincida com uma mudança de iluminação ou de "
            "velocidade das ventoinhas: ambas alteram a temperatura por si."
        ),
        "cycle_days": "Dias entre testes",
        "cycle_days_desc": (
            "É testado um aquecedor de cada vez, à vez. Com dois aquecedores "
            "e 14 dias, cada um é testado de quatro em quatro semanas."
        ),
        "test_duration": "Duração do teste",
        "test_duration_desc": (
            "Um grande volume reage devagar: abaixo de cerca de duas horas, "
            "um aquecedor inativo pode passar despercebido."
        ),
        "sec_safety": "Segurança",
        "max_drop": "Descida de temperatura tolerada",
        "max_drop_desc": (
            "Acima desta descida em relação à temperatura inicial, o teste "
            "falha e para de imediato. Mantenha um valor superior à resolução "
            "das sondas."
        ),
        "abort_temperature": "Temperatura de interrupção",
        "abort_temperature_desc": (
            "Abaixo deste valor nenhum teste começa, e um teste em curso para "
            "e repõe os aquecedores."
        ),
        "pause_entities": "Entidades de manutenção (opcional)",
        "pause_entities_desc": (
            "Enquanto alguma estiver ativa, nenhum teste começa e os "
            "aquecedores não são ligados, pois podem estar fora de água. São "
            "repostos quando ela se desativa."
        ),
        "sec_notify": "Notificações",
        "notify_devices": "Dispositivos móveis a notificar",
        "notify_devices_desc": (
            "Recebem o resultado de cada teste. Só aparecem os telemóveis e "
            "tablets registados através da aplicação Home Assistant."
        ),
        "notify_channel": "Canal Android (opcional)",
        "notify_channel_desc": (
            "Nome do canal enviado em `data.channel`. Deixe vazio para o "
            "canal predefinido. O iOS ignora este campo."
        ),
        "title": "Recife — teste dos aquecedores",
        "msg_ok": (
            "{heater} manteve o aquário sozinho durante {minutes} min: "
            "{start}° → {end}°. Teste aprovado."
        ),
        "msg_fail_drop": (
            "{heater} não manteve o aquário sozinho: {start}° → {end}° em "
            "{minutes} min (descida tolerada: {drop}°). Verifique este "
            "aquecedor."
        ),
        "msg_fail_cold": (
            "Teste de {heater} parado após {minutes} min: {end}° está abaixo "
            "de {limit}°. Aquecedores repostos, verifique este aquecedor."
        ),
        "msg_interrupted": (
            "Teste de {heater} interrompido após {minutes} min, sem resultado "
            "({start}° → {end}°)."
        ),
        "msg_skip_too_few": (
            "Teste não iniciado: são necessários pelo menos dois aquecedores."
        ),
        "msg_skip_paused": "Teste não iniciado: manutenção em curso.",
        "msg_skip_no_temperature": "Teste não iniciado: nenhuma temperatura disponível.",
        "msg_skip_too_cold": "Teste não iniciado: {start}° está abaixo de {limit}°.",
        "msg_skip_heater_off": (
            "Teste não iniciado: todos os aquecedores têm de estar ligados."
        ),
        "msg_recovered": (
            "Um reinício interrompeu um teste: aquecedores ligados de novo."
        ),
        "msg_paused_note": (
            "Manutenção em curso: os aquecedores ficam desligados até ao fim."
        ),
        "msg_still_off": "Atenção, ainda desligado: {still_off}.",
    },
}


def header(lang: str, version: str) -> str:
    """Blueprint metadata and input selectors for one language."""
    s = STRINGS[lang]
    return f"""# Generated by scripts/gen_heater_test.py -- do not edit by hand.
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
    equipment_section:
      name: {s["sec_equipment"]}
      icon: mdi:heating-coil
      input:
        heaters:
          name: {s["heaters"]}
          description: >
            {s["heaters_desc"]}
          selector:
            entity:
              domain: switch
              multiple: true
        temperature_sensors:
          name: {s["sensors"]}
          description: >
            {s["sensors_desc"]}
          selector:
            entity:
              domain: sensor
              multiple: true

    schedule_section:
      name: {s["sec_schedule"]}
      icon: mdi:calendar-clock
      input:
        test_time:
          name: {s["test_time"]}
          description: >
            {s["test_time_desc"]}
          default: "09:00:00"
          selector:
            time: {{}}
        cycle_days:
          name: {s["cycle_days"]}
          description: >
            {s["cycle_days_desc"]}
          default: 14
          selector:
            number:
              min: 1
              max: 60
              mode: box
        test_duration:
          name: {s["test_duration"]}
          description: >
            {s["test_duration_desc"]}
          default: 240
          selector:
            number:
              min: 30
              max: 720
              step: 30
              unit_of_measurement: min
              mode: slider

    safety_section:
      name: {s["sec_safety"]}
      icon: mdi:shield-alert-outline
      input:
        max_drop:
          name: {s["max_drop"]}
          description: >
            {s["max_drop_desc"]}
          default: 0.3
          selector:
            number:
              min: 0.1
              max: 2
              step: 0.1
              unit_of_measurement: "°"
              mode: slider
        abort_temperature:
          name: {s["abort_temperature"]}
          description: >
            {s["abort_temperature_desc"]}
          default: 24.5
          selector:
            number:
              min: 15
              max: 30
              step: 0.1
              unit_of_measurement: "°"
              mode: box
        pause_entities:
          name: {s["pause_entities"]}
          description: >
            {s["pause_entities_desc"]}
          default: []
          selector:
            entity:
              multiple: true

    measure_section:
      name: {s["sec_measure"]}
      icon: mdi:flash
      collapsed: true
      input:
        room_sensor:
          name: {s["room_sensor"]}
          description: >
            {s["room_sensor_desc"]}
          default: ""
          selector:
            entity:
              domain: sensor
        heater_setpoint:
          name: {s["heater_setpoint"]}
          description: >
            {s["heater_setpoint_desc"]}
          default: 0
          selector:
            number:
              min: 0
              max: 35
              step: 0.1
              unit_of_measurement: "°"
              mode: box
        power_sensors:
          name: {s["power_sensors"]}
          description: >
            {s["power_sensors_desc"]}
          default: []
          selector:
            entity:
              domain: sensor
              device_class: power
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
        result_entity:
          name: {s["result_entity"]}
          description: >
            {s["result_entity_desc"]}
          default: ""
          selector:
            entity:
              domain: input_text

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
    """Header plus the shared body, with the messages substituted."""
    s = STRINGS[lang]
    body = BODY.replace("WAIT_TRIGGERS", WAIT_TRIGGERS).replace(
        "METER_LOOKUP", METER_LOOKUP
    )
    for marker in MARKERS:
        text = s["title"] if marker == "TITLE_TEXT" else s[MESSAGES[marker]]
        for placeholder, expression in PLACEHOLDERS.items():
            text = text.replace(placeholder, expression)
        body = body.replace(marker, text)
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
