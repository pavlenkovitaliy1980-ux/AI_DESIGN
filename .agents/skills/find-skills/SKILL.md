---
name: find-skills
description: Use when the user asks to find, recommend, compare, install, create, or manage Codex/agent skills for a specific workflow. Especially useful for AI_DESIGN, engineering automation, PDF, DWG, DOCX, Excel, VOR, PNR, cable journals, CAD/BIM, Revit, project documentation, and low-voltage/electrical design tasks.
---

# Find Skills

Use this skill when the user wants to find, choose, create, install, compare, or manage skills.

## Main workflow

1. Identify the user's practical task:
   - PDF analysis;
   - DWG/CAD drawing analysis;
   - DOCX generation;
   - Excel/specification processing;
   - VOR/BOQ generation;
   - PNR generation;
   - cable journal checking;
   - Revit/BIM automation;
   - engineering documentation;
   - AI_DESIGN project automation.

2. Decide what is needed:
   - existing skill;
   - new custom skill;
   - repository-specific skill;
   - global user skill;
   - plugin;
   - script-assisted skill.

3. Recommend the installation location:

Repository-specific skill:

```text
<project>/.agents/skills/<skill-name>/SKILL.md