<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Wskaż mi wszystkie źródła strony dotyczące Hermes Agentic OS, czyli oficjalne źródła strony ze skillami i inne z których mogę korzystać budując swój system.

Poniżej masz najważniejsze, oficjalne źródła do Hermes Agent / Hermes Agentic OS, które warto traktować jako bazę przy budowie własnego systemu. Najważniejsze są: oficjalna dokumentacja, katalog skilli, repozytorium GitHub oraz oficjalne kanały społeczności i integracji.[^1][^2][^3]

## Oficjalne źródła

| Źródło | Do czego służy |
| :-- | :-- |
| [Dokumentacja Hermes Agent](https://hermes-agent.nousresearch.com/docs/) | Główne centrum wiedzy: instalacja, konfiguracja, workflow, bezpieczeństwo, architektura, pamięć, MCP, skills [^1]. |
| [GitHub: NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) | Kod źródłowy, issue tracker, releases, wkład do projektu, pliki repo i foldery systemowe [^3]. |
| [Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog) | Pełna lista wbudowanych skilli, ich opisy i ścieżki do definicji [^2]. |
| [Optional Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog) | Dodatkowe, instalowalne skill-packi poza standardowym zestawem [^1]. |
| [Skills System](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) | Jak Hermes ładuje skill, jak działają skille i jak je tworzyć [^1]. |
| [Creating Skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills) | Oficjalny przewodnik tworzenia własnych skilli [^4]. |
| [Developer Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/architecture) | Architektura, projektowanie systemu, rozszerzanie Hermes [^1]. |
| [Contributing Guide](https://hermes-agent.nousresearch.com/docs/developer-guide/contributing) | Zasady wkładu do projektu i praca z kodem [^3]. |

## Źródła do skilli

Najbardziej praktyczne źródła, jeśli budujesz własny system skill-based, to katalog skilli i przewodnik tworzenia skilli. Oficjalny katalog pokazuje, jak Hermes organizuje wbudowane skille w grupy, np. `software-development`, `github`, `productivity`, `research`, `mcp`, `creative` i inne. Oficjalna dokumentacja opisuje też, że skille są przenośne, współdzielone i instalowalne, a Hermes wspiera też społecznościowy Skills Hub.[^2][^1]

Przy budowie własnego systemu szczególnie przydadzą się:

- [Bundled Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog).[^2]
- [Optional Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog).[^1]
- [Working with Skills](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills).[^5]
- [Creating Skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills).[^4]


## Zasoby techniczne

Jeśli chcesz budować coś kompatybilnego lub inspirowanego Hermes, zwróć uwagę na machine-readable wejścia do dokumentacji. Oficjalna strona publikuje [llms.txt](https://hermes-agent.nousresearch.com/docs/assets/files/llms-bcf65f79b33e57e6c0cce5b9627945d4.txt) oraz [llms-full.txt](https://hermes-agent.nousresearch.com/docs/assets/files/llms-full-1a9fc8671bab03c652f97c9c9d1f07d7.txt), które służą do ładowania całej dokumentacji do kontekstu modelu. Repozytorium GitHub zawiera też praktyczne elementy implementacyjne: `skills/`, `optional-skills/`, `plugins/`, `tools/`, `gateway/`, `providers/`, `docs/` i `website/`.[^3][^1]

To oznacza, że do budowy własnego systemu możesz korzystać z:

- struktury repo i sposobu organizacji plików,[^3]
- dokumentacji skilli i ich katalogu,[^2]
- oficjalnych entrypointów docs dla LLM.[^1]


## Oficjalne kanały

W dokumentacji i repozytorium jako oficjalne kanały pojawiają się też:

- [Discord Hermes / Nous Research](https://discord.gg/NousResearch).[^3][^1]
- [GitHub Discussions](https://github.com/NousResearch/hermes-agent/discussions).[^1]
- [Skills Hub](https://agentskills.io/) jako społecznościowy standard / hub skilli.[^1]


## Co bym traktował jako „must use”

Jeśli chcesz budować własny system w oparciu o Hermes, zacznij od tych czterech pozycji:

1. [Documentation home](https://hermes-agent.nousresearch.com/docs/).[^1]
2. [Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog).[^2]
3. [Creating Skills](https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills).[^4]
4. [GitHub repo](https://github.com/NousResearch/hermes-agent).[^3]

Jeśli chcesz, mogę w następnym kroku ułożyć Ci z tego **praktyczną mapę źródeł pod budowę własnego Agentic OS**: co czytać w jakiej kolejności, z podziałem na architekturę, skille, memory, MCP i integracje.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^24][^25][^26][^27][^28][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://github.com/nousresearch/hermes-agent

[^2]: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills

[^3]: https://www.youtube.com/watch?v=VLKA2OFOOtQ\&vl=pl

[^4]: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills

[^5]: https://hermes-agent.nousresearch.com/docs/ko/guides/work-with-skills

[^6]: https://www.reddit.com/r/hermesagent/comments/1rt5syt/complete_hermes_agent_setup_guide/

[^7]: https://dev.to/truongpx396/hermes-agent-deep-dive-build-your-own-guide-1pcc

[^8]: https://modimihir07.github.io/agentic-os/

[^9]: https://www.youtube.com/watch?v=dLk2Imx-0uk

[^10]: https://www.youtube.com/watch?v=1ve4Atbqmoo

[^11]: https://github.com/fathah/hermes-desktop

[^12]: https://hermes-agent.org

[^13]: https://skillsllm.com/skill/hermes-agent

[^14]: https://www.youtube.com/watch?v=jp9jRyDC9OE

[^15]: https://docs.openwebui.com/getting-started/quick-start/connect-an-agent/hermes-agent/

[^16]: https://hermesagent.org.cn/en/docs/developer-guide/creating-skills

[^17]: https://ht-x.com/posts/2026/03/github-nousresearch-hermes-agent-the-agent-that-gr/

[^18]: https://hermes-agent.nousresearch.com/docs/reference/skills-catalog

[^19]: https://hermes-agent.nousresearch.com/docs/

[^20]: https://hermes-agent.nousresearch.com/docs/ko/user-guide/skills/bundled/research/research-arxiv

[^21]: https://hermes-agent.nousresearch.com/docs/zh-Hans/user-guide/skills/bundled/software-development/software-development-writing-plans

[^22]: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/research/research-qmd

[^23]: https://github.com/NousResearch/hermes-agent-self-evolution

[^24]: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/software-development/software-development-code-wiki

[^25]: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-shop-app

[^26]: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/learning-path.md

[^27]: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/productivity/productivity-here-now

[^28]: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/skills-catalog.md

