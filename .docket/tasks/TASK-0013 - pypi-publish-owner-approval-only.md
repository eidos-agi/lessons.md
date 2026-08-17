---
id: TASK-0013
title: PyPI publish — owner approval only
status: To Do
created: '2026-08-17'
priority: low
milestone: MS-0001
tags:
  - pypi
  - blocked
acceptance-criteria:
  - Owner explicitly approves PyPI
  - shipr attempt records that approval
  - twine/uv publish only after that
definition-of-done:
  - Package on PyPI at a version matching pyproject, or task archived because owner declined
blocked_reason: 'shipr approval_gates: PyPI publish. CHARTER invariant no_pypi_without_owner.'
subtasks:
  - TASK-0014
  - TASK-0015
  - TASK-0016
---
Not a completion criterion for the LEARN leg. Do not treat GitHub main as unfinished solely because PyPI is empty.
