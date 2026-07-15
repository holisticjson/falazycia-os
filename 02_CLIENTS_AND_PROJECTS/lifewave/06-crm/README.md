# 👥 06-crm — Zarządzanie Leadami i Tagowanie (Systeme.io)

Katalog dedykowany listom kontaktów, segmentacji leadów, notatkom handlowym oraz architekturze tagów w Systeme.io dla projektu LifeWave / X2O.

---

## 🏷️ Architektura Tagów w Systeme.io
W MLM kluczem do sukcesu jest precyzyjna segmentacja i brak spamu. Każdy kontakt wpadający do bazy musi otrzymać odpowiedni zestaw tagów, aby otrzymywać wyłącznie treści, które go interesują:

| Tag w Systeme.io | Opis Segmentu | Dalsza Akcja Automatyczna |
|------------------|---------------|---------------------------|
| `lw-lead` | Ogólny zapis na darmowy poradnik PDF | Start sekwencji edukacyjnej o zdrowiu komórkowym |
| `lw-klient-detal` | Osoba zainteresowana wyłącznie plastrami/X2O | Oferty produktowe, promocje, instrukcje obsługi |
| `lw-partner-biznes` | Osoba nastawiona na budowę downline/MLM | Sekwencja o pasywnym dochodzie, zaproszenia na Zoom |
| `lw-hot-lead` | Osoba, która wypełniła ankietę kwalifikacyjną | Powiadomienie na Telegram Tomasza przez bota Hermes o konieczności kontaktu |

---

## 📞 Kwalifikacja ADHD-friendly
Zamiast "zimnych telefonów", ankieta na stronie filtruje leady na autopilocie. Dane z ankiet są zbierane i analizowane, a Tomasz otrzymuje przejrzysty, skondensowany brief o gorącym leadzie bezpośrednio na Telegramie, co zapobiega przebodźcowaniu i oszczędza energię dopaminową.
