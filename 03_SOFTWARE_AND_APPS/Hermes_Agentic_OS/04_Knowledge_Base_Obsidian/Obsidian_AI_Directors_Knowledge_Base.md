# Baza Wiedzy (Obsidian) i Procedury SOP dla AI

System Zarządu (Virtual Board: CEO, CMO, CTO itp.) potrzebuje zasilenia wiedzą o firmie klienta, aby był w pełni zautomatyzowany. Proces on-boardingu wiedzy zorganizowany jest wokół Obsidiana.

## 1. Złoty Standard: Wytyczne Mirek Burnejko AI Biznes Lab
Zarządzanie operacyjne systemem zaczyna się w katalogu:
`C:\Aplikacje MVP\02_knowledge_base\raw\Mirek_Burnejko_AI_Biznes_Lab`

Dokumenty i ankiety tam zawarte to nasz **Blueprint** – fundament SOP dla dyrektorów (AI Personas). Zanim jakikolwiek dyrektor zostanie wygenerowany, proces przepuszcza dane wejściowe przez te rygorystyczne checklisty. Baza musi zostać uporządkowana tak, by stanowiła "serce" procedur startowych dla każdego nowego wdrożenia (projektu klienta).

## 2. Pliki Osobowości (Persona Files)
Zalążki wiedzy i osobowości są ładowane z fundamentalnych plików Markodown (zawartych jako template'y w naszym folderze `04_Knowledge_Base_Obsidian`):
*   `user.md`: Główny profil użytkownika/klienta, jego wizja, wartości biznesowe, ograniczenia.
*   `soul.md`: Emocjonalny wektor bota – Tone-of-Voice, styl pisania, charakterystyczne "żarty" lub zasady psychologiczne (np. filtry dopaminowe dla ADHD).
*   `memory.md`: Długoterminowa pamięć podręczna projektów w toku, do której dyrektorzy mają ciągły dostęp.
*   `o_mnie.md`: Informacje tła (Background kontekstowy) o założycielu, budujące głębię relacji na linii Bot-Właściciel.

## 3. Workflow Inicjacyjny nowego klienta
1. Utworzenie nowego folderu (Vaultu) Obsidian dla klienta.
2. Odpytanie klienta za pomocą checklisty z `AI_Biznes_Lab`.
3. Wygenerowanie na podstawie tych ankiet plików Persona (`user.md`, `soul.md`).
4. Wpięcie tych plików jako podstawy (System Prompts i RAG) do konkretnych "Agentów Dyrektorów" w Hermesie.
