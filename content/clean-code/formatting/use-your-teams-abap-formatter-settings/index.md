---
title: "Use your team's ABAP Formatter settings"
weight: 40
params:
  source: "https://github.com/SAP/styleguides/blob/main/clean-abap/CleanABAP.md#use-your-teams-abap-formatter-settings"
---

Always use your team's ABAP Formatter settings.
Specify them under
* Eclipse: Right-click on the project in the Project Explorer > _Properties_ > _ABAP Development_ > _Editors_ > _Source Code Editors_ > _ABAP Formatter_
* Eclipse (alternative navigation): _Menu_ > _Window_ > _Preferences_ > _ABAP Development_ > _Editors_ > _Source Code Editors_ > Click on the _ABAP Formatter_ link on the right-hand side > Select project in pop-up
* SAP GUI: _Menu_ > _Utilities_ > _Settings ..._ > _ABAP Editor_ > _Pretty Printer_.

Set _Indent_ and _Convert Uppercase/Lowercase_ > _Uppercase Keyword_
as agreed in your team.

> [Upper vs. Lower Case](/clean-code/deep-dives/upper-vs-lower-case/) explains
> why we do not give clear guidance for the type case of keywords.
>
> Read more in _Chapter 5: Formatting: Team Rules_ of [Robert C. Martin's _Clean Code_](https://www.oreilly.com/library/view/clean-code/9780136083238/).
