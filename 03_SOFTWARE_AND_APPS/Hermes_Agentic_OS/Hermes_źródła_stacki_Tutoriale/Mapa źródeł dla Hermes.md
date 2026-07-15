<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Tak, poproszę. Przygotuj praktyczną mapę źródeł.

Przy budowie własnego „Hermes Agentic OS” warto potraktować dokumentację jak ścieżkę szkoleniową w kilku etapach: najpierw fundamenty, potem skille, pamięć, integracje i dopiero na końcu produkcyjny OS oparty o wiele profili i agentów.[^1][^2]

## Etap 1 – Fundamenty agenta

Cel: zrozumieć pętlę agenta, strukturę projektu i podstawowe komendy.

Kolejność czytania i użycia:

- Strona główna dokumentacji: „Hermes Agent Documentation” – opis koncepcji, co odróżnia Hermes od zwykłego chatbota (pętla, pamięć, skille, profile).[^3]
- „Quickstart Tutorial / Your first conversation” – jak zainstalować, uruchomić pierwszą sesję i zobaczyć podstawowe możliwości.[^3]
- „Learning Path” – oficjalna ścieżka: po Quickstarcie przejście do CLI usage, konfiguracji, a dopiero później Tools, Skills i Memory.[^1][^3]
- Repozytorium GitHub `NousResearch/hermes-agent` – przejrzenie struktury katalogów (`skills/`, `optional-skills/`, `tools/`, `gateway/`, `website/docs`) żeby zobaczyć, gdzie „fizycznie” mieszkają funkcje OS-u.[^4]

Praktyka dla Ciebie:

- Zainstaluj Hermesa i uruchom `hermes init` / `hermes setup` według oficjalnego Quickstartu, żeby mieć działającą bazę pod OS.[^5][^3]
- Zrób kilka rozmów z agentem z poziomu CLI, zanim dodasz cokolwiek własnego.[^1]


## Etap 2 – Skille jako „warstwa OS”

Cel: traktować skille jak moduły OS-u (pakiety funkcjonalne), które da się komponować.

Kluczowe oficjalne źródła:

- „Skills System / Working with Skills” – przegląd, czym są skille, jak agent je ładuje, jakie są strategie wywołania.[^6][^3]
- „Creating Skills” (Developer Guide) – definicja formatu pliku skill, sekcje, progressive disclosure, patterny do instrukcji.[^7]
- „Bundled Skills Catalog” – pełny katalog wbudowanych skilli z opisami, wymaganiami i przykładami użycia.[^8][^1]
- „Optional Skills Catalog” – dodatkowe skille, które można doinstalować i zobaczyć, jak rozwiązują bardziej złożone przypadki (DevOps, research, productivity itd.).[^8]

Jak zbudować z tego mapę OS:

- Potraktuj katalog Bundled Skills jako „system apps” – przejdź kategorie (research, content, knowledge management, DevOps, productivity) i wybierz te, które pokrywają Twój workflow.[^8]
- Dla każdego wybranego skillu przeczytaj jego indywidualną stronę w docs – zauważ, jak opisuje „kiedy użyć” i „jakie ma ograniczenia”.[^1]
- Następnie napisz 1–2 własne skille inspirowane tym patternem – np. skill do obsługi Twojej bazy wiedzy, pipeline’u contentowego czy CRM.[^7]


## Etap 3 – Pamięć, profile, multi-agent

Cel: przejść od pojedynczego agenta „asystenta” do OS-u z wieloma profilami i długoterminową pamięcią.

Źródła:

- Sekcje „Memory” w dokumentacji Hermes – opis jak działa pamięć, jakie są providerzy i jak wygląda konfiguracja.[^3]
- Integracje pamięci z zewnętrznymi systemami, np. Hindsight (Persistent long-term memory with Hermes) – jak włączyć, jak działa automatyczne przywoływanie kontekstu.[^9]
- „Profiles” i „Cron / Gateways” w przewodnikach użytkownika i blogach (np. tutorial UserOrbit: Profiles, cron, product workflows) – pokazują, jak z jednego Hermesa zrobić system wielu agentów z różnymi uprawnieniami.[^2]

Jak to przełożyć na Agentic OS:

- Najpierw skonfiguruj jednego providera pamięci (lokalny lub Hindsight) i sprawdź `hermes memory status`, żeby mieć stabilną bazę long-term.[^9]
- Zdefiniuj kilka profili (np. „dev”, „product”, „research”, „ops”) i na każdy nałóż inny zestaw skilli + inne uprawnienia (np. tylko read, read+write).[^10][^2]
- Wykorzystaj cron/gateways, żeby część profili działała jak „usługi systemowe” (np. agent raportowy, agent monitorujący, agent do researchu).[^2]


## Etap 4 – Integracje, modele i narzędzia

Cel: warstwa „systemowa” – modele, narzędzia, integracje z zewnętrznymi usługami.

Najważniejsze źródła:

- „Configuration” / „Models \& Providers” w oficjalnej dokumentacji – jak podpiąć OpenAI, OpenRouter, lokalne modele (Ollama, vLLM, Unsloth).[^11][^5][^3]
- Przewodniki integracyjne, np. Unsloth (local models) czy Unslo­th/Nowledge/Hindsight – jak ustawić custom OpenAI endpoint, API keys, env.[^12][^5][^9]
- Zewnętrzne deep-dive’y: „Hermes Agent deep dive – build-your-own guide” – tłumaczy trójwarstwową architekturę (surfaces, agent core, execution backends) i jak z tego zrobić produkcyjny pipeline.[^13]

Jak tego użyć w projekcie:

- Na etapie OS-u zdefiniuj „klasę” modeli: np. modele do reasoning vs. do kodu vs. do generowania contentu – i skonfiguruj je w Hermes w zależności od profilu.[^11]
- W narzędziach (tools) i integracjach ustaw minimalny, bezpieczny zestaw: np. filesystem, terminal, HTTP, wybrane API – tak, by każdy profil miał tylko to, czego potrzebuje.[^10][^2]


## Etap 5 – Całościowy Agentic OS z Hermes jako rdzeniem

Cel: złożyć to w pełen OS: wiele profili, rozdzielone uprawnienia, skille jako moduły, pamięć długoterminowa, integracje.

Propozycja kolejności z wykorzystaniem źródeł:

1. Przerób `Learning Path` + Quickstart, aż będziesz czuł się swobodnie z CLI i configiem.[^3][^1]
2. Przejdź katalog Bundled Skills i wybierz zestaw „core OS”: research, knowledge, coding, productivity, integracje web.[^8]
3. Skonfiguruj pamięć (local/Hindsight) i 3–5 profili odpowiadających rolom w Twoim systemie (np. Research, Ops, Content, Growth, Support).[^9][^2]
4. Do każdego profilu przypisz dedykowane skille i poziom uprawnień – inspirując się produkcyjnymi przewodnikami (Hermes w setupach produkcyjnych, blogi dla inżynierów/PM-ów).[^2][^10]
5. Doinstaluj integracje (modele lokalne, zewnętrzne API) wg przewodników integracyjnych, traktując je jako „sterowniki sprzętu” OS-u.[^5][^9]

Jeśli chcesz, mogę na tej bazie zaproponować Ci konkretny **„stack Hermes Agentic OS” pod Twoje use-case’y (ADHD, produktywność, content, automatyzacje)** z listą skilli, profili i integracji do wdrożenia w pierwszej iteracji.
<span style="display:none">[^14][^15][^16][^17]</span>

<div align="center">⁂</div>

[^1]: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/learning-path.md

[^2]: https://userorbit.com/blog/getting-started-with-hermes-agent

[^3]: https://hermes-agent.lzw.me/docs/en/

[^4]: https://github.com/nousresearch/hermes-agent

[^5]: https://unsloth.ai/docs/integrations/hermes-agent

[^6]: https://hermes-agent.nousresearch.com/docs/ko/guides/work-with-skills

[^7]: https://hermes-agent.nousresearch.com/docs/developer-guide/creating-skills

[^8]: https://felo.ai/blog/best-hermes-agent-skills-2026/

[^9]: https://hindsight.vectorize.io/sdks/integrations/hermes

[^10]: https://www.glukhov.org/ai-systems/hermes/production-setup/

[^11]: https://lushbinary.com/blog/hermes-agent-developer-guide-setup-skills-self-improving-ai/

[^12]: https://mem.nowledge.co/docs/integrations/hermes

[^13]: https://dev.to/truongpx396/hermes-agent-deep-dive-build-your-own-guide-1pcc

[^14]: https://www.linkedin.com/pulse/getting-started-hermes-agent-your-self-improving-ai-assistant-maio-tys6e

[^15]: https://www.datacamp.com/es/tutorial/hermes-agent

[^16]: https://skillsllm.com/skill/hermes-agent

[^17]: https://www.reddit.com/r/hermesagent/comments/1rt5syt/complete_hermes_agent_setup_guide/

