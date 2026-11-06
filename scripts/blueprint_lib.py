"""What the blueprints of this repository share.

Blueprints cannot include one another, so a piece of logic needed by several
of them lives here and is spliced in by the generators.
"""

from __future__ import annotations

# Finds the power sensor of the switch `h`, into the Jinja variable `meter`.
#
# A redsea socket or port publishes its consumption under a role derived from
# its switch, which holds in every language and survives renames. Without a
# role, a smart plug is recognised by having a single power sensor on its
# device. A role with no matching sensor means no meter, never a guess among
# the other sockets of the strip.
METER_LOOKUP = """\
          {%- set role = state_attr(h, 'reef_role') or '' -%}
          {%- set prefix = role[:-7] if role.endswith('_on_off') else '' -%}
          {%- set d = device_id(h) -%}
          {%- set ents = device_entities(d) if d else [] -%}
          {%- set own = (ents | select('is_state_attr', 'reef_role',
                prefix ~ '_consumption') | list) if prefix else [] -%}
          {%- set meters = ents | select('match', 'sensor[.]')
                | select('is_state_attr', 'device_class', 'power') | list -%}
          {%- set meter = own[0] if own
                else meters[0] if meters | count == 1 and not prefix
                else '' -%}"""
