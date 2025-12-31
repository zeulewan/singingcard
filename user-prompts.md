# User Prompts Log

This file tracks all user prompts and major decisions throughout the project.

---

## Session 1: December 30, 2025

### Initial Research Request

> using perplexity find the best way to use kicad as claude code agent such as yourself and use plugings and everything too. i need you to do auto routing, use the jlc plug in library and select chips. also then look at if you can use the jlcpcb api plugin to order it yourself. be thorough about your research. extremely thorough. search far and wide find the best tools. maybe it's an MCP servert or maybe it's just the kicad api directly. An importatn note is that you need to use third party pluging such as autorouter and stuff. you also need ot be ablet oclean up any mistakes, and furethermore also inspect the schematic and layout visually using screenshots of kicad. you dont necessariliy need kicad to visuallze you could use some third party app. I just have no idea what's out there. find the best workflow for an agent using kicad.

**Result:** Created comprehensive research document `kicad-agent-workflow-research.md`

---

### Workflow Setup Request

> install all the tools that you think are best. keep them in another document describing everthing. remember to keep it concise. to put it into perspective i want to ask you to design and order an entire PCB from start to end i dont want to actually do anything myself except give you the project requirements and maybe set up api keys and whatnot. settle on the best tools write that in a plan. you will need to select components, make sure they're available on jlc, with the jlc tools plug in or the api, recurse on that in case it's not available, you'll need to research all the chips and their pins and connections, then you'll need to connect everything together in the schematic with labels and stuff. you'll need ot make sure it visually looks correct and things dont overlap and stuff, then you'll have to do the routing, i'll specifyt the rough board size and shape, you'll arrange things using a tools or something then you'll need to run the design rules checker and verify everything. btw you'll need to make sure the curtrent requremetns of ttraces are good. then you'll export it and use teh jlc api if you can to order it. you also need to make sure by the way taht everything is assembleable by jlc. you'll ask the user for relevant questions regarding teh fabrication if not specified such as color and time for fabrications and whatnot. make sure you keep notes of things in relevant markdown files. keep it well organized, keep in mind that you only have so long of a context length. you'll need a couple files such as a claude skill for kicad usage, just make that a local project skill, you'll need a md file for now to just make sure you install and document all the thigns you installed. you'll need a file for the actual specificatiosn of the project where you note what the user wants. and you may need other md files for anything else like maybe misc notes or idk what.
> so by the way I will maybe check things here and there but i hope to not have to. i'll give you project requirements later, just get your notes and skill set up. settle on what tools you want to use and how you're going to format your notes. this is goingto be a really long project to we need to stay on top of it

**Decision:** Use kicad-mcp-python, FreeRouting, SKiDL, easyeda2kicad, KiBot

---

### Directory Corrections

> all kicad files shall go in a folder within the current folder called kicad. you also need to set up the repo now. add a readme saying this is an attempt to get claude code to make a pcb front start to finish

**Action:** Updated directory structure, initialized git repo, created README

---

### Virtual Environment & Prompts Tracking

> the kicad root folder shoudl jsut be right in a fodler in teh current folder called kicad. make sure anything you install is in a venv. keep track btw of all prompts i give you in a file called user promts.md

**Action:** All Python packages to be installed in venv/, created this file

---

## Project Requirements

*To be added when user provides project specifications*
