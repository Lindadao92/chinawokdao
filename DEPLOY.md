# chinawokdao.com

Statische Seite, eine Datei. Gebaut aus `menu.py` mit `python3 build.py`.

## Aenderungen an der Karte

1. `menu.py` bearbeiten (Gerichte, Preise, Oeffnungszeiten, Adresse)
2. `python3 build.py`
3. `npx wrangler pages deploy site --project-name china-wok-dao`

Preise: das vierte Feld je Gericht. Sobald mindestens eines gefuellt ist,
blendet der Generator die Preisspalte automatisch ein.

## Variante A: GoDaddy (nur mit Webhosting-Paket)

Setzt ein cPanel-Webhosting bei GoDaddy voraus. Pruefen unter
Mein Konto, Meine Produkte, Eintrag "Webhosting" oder "cPanel".
Der reine Domain-Eintrag reicht nicht, und der Website Builder auch nicht,
weil der keine eigenen HTML-Dateien annimmt.

1. Domainweiterleitung auf Notion entfernen
2. cPanel oeffnen, Dateimanager, Ordner `public_html`
3. Inhalt von `site/` hochladen: index.html, robots.txt, sitemap.xml
4. Fertig. Keine DNS-Aenderung noetig, die Domain zeigt schon dorthin.

`_headers` ist eine Cloudflare-Datei und wird hier nicht gebraucht.

## Variante B: Cloudflare Pages (kostenlos)

```
npx wrangler login
npx wrangler pages project create china-wok-dao --production-branch main
npx wrangler pages deploy site --project-name china-wok-dao
```

Danach laeuft die Seite unter china-wok-dao.pages.dev.

Domain umstellen, Reihenfolge ist wichtig:

1. Bei GoDaddy die Domainweiterleitung auf Notion ausschalten
2. Bei Cloudflare die Domain hinzufuegen (Add a site)
3. Die zwei Nameserver von Cloudflare bei GoDaddy eintragen
4. Warten bis Cloudflare die Domain als aktiv meldet, meist unter einer Stunde
5. Im Pages-Projekt unter Custom domains chinawokdao.com und
   www.chinawokdao.com hinzufuegen

Die Domain bleibt bei GoDaddy registriert, nur die DNS-Verwaltung wandert.
Noetig, weil die Domain ohne www auf Pages zeigen soll und GoDaddy dafuer
keinen passenden Eintragstyp anbietet.

## Offen

- [x] Impressum: Viet Thanh Dao, lindadao92@gmail.com
- [ ] E-Mail-Adresse bestaetigen (im Chat stand lindadao92gmail.com ohne @)
- [ ] Adresse bestaetigen: Hauptstr. 158, 66976 Rodalben
- [ ] Nummerierung gegen die gedruckte Karte pruefen
- [ ] Preise eintragen
- [ ] Eigene Fotos der Gerichte
