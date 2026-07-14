# 🚀 07-deploy — Wdrożenia, Domeny i DNS

Centrum instrukcji wdrożeniowych dla infrastruktury projektu LifeWave / X2O, konfiguracji subdomen oraz rekordów DNS.

---

## 🌐 Mapowanie Domeny i Subdomeny (Systeme.io)
Aby zachować pełen profesjonalizm i dbać o markę osobistą, podepniemy lejek pod profesjonalną subdomenę:
-   **Propozycja subdomeny:** `lifewave.holisticjson.pl` lub `woda.jaison.pl` (zależnie od wybranej domeny głównej).
-   **Wdrożenie:** 
    1.  Dodanie subdomeny w panelu Systeme.io.
    2.  Konfiguracja rekordów **CNAME** u rejestratora domeny (np. Hostido / Cloudflare) zgodnie z wytycznymi Systeme.io w celu weryfikacji i generowania darmowego certyfikatu SSL.

---

## 📧 Bezpieczeństwo Poczty (SPF, DKIM, DMARC)
Aby zapobiec lądowaniu naszych newsletterów w folderze "Spam", n8n lub Systeme.io będą korzystać z odpowiednio uwierzytelnionych skrzynek pocztowych:
-   Każda domena wysyłkowa musi posiadać prawidłowo skonfigurowane rekordy **TXT** dla **SPF**, **DKIM** oraz **DMARC**.
-   Systeme.io udostępnia dedykowane rekordy CNAME do weryfikacji DKIM, które należy bezwzględnie wdrożyć przed startem jakiejkolwiek wysyłki.
