---
description: 'Manage Atlas: init, update [release tag], models [filter], config'
agent: Auto
subagent: false
---

Load the skill `atlas` from the Atlas installation in use and carry out exactly the requested action.
The first word is the action (`init`, `update`, `models` or `config`); the remaining text is its arguments.
Without an action or with an unknown action, only show the available invocations. Do not start an implicit setup or update.
Invocation: /atlas $ARGUMENTS
