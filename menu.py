# -*- coding: utf-8 -*-
"""Speisekarte China Wok Dao.

Nummerierung rekonstruiert aus der Notion-Seite. Die Anker 41a/41b/45b und
46a/46b/50b bestaetigen eine durchlaufende Nummerierung.

Preise: Feld "p" leer lassen, bis die Preisliste vorliegt. Sobald alle p-Werte
gefuellt sind, blendet der Generator automatisch eine Preisspalte ein.

Format je Gericht: (nummer, bezeichnung, [zusatzstoffe], preis)
"""

RESTAURANT = {
    "name": "China Wok Dao",
    "street": "Hauptstr. 158",
    "zip": "66976",
    "city": "Rodalben",
    "country": "DE",
    "phone_display": "06331 / 140888",
    "phone_tel": "+496331140888",
    "owner": "Viet Thanh Dao",          # Impressum: Inhaber, inhaltlich verantwortlich
    "email": "lindadao92@gmail.com",
    "maps": "https://www.google.com/maps/search/?api=1&query=Hauptstr.+158+66976+Rodalben",
    "domain": "chinawokdao.com",
}

HOURS = [
    # (Label, [(von, bis), ...] als Minuten-Paare fuer die Live-Anzeige)
    ("Montag",         [("17:00", "22:00")]),
    ("Dienstag",       [("11:00", "14:00"), ("17:00", "22:00")]),
    ("Mittwoch",       [("11:00", "14:00"), ("17:00", "22:00")]),
    ("Donnerstag",     [("11:00", "14:00"), ("17:00", "22:00")]),
    ("Freitag",        [("11:00", "14:00"), ("17:00", "22:00")]),
    ("Samstag",        [("11:00", "14:00"), ("17:00", "22:00")]),
    ("Sonntag",        [("11:00", "14:00"), ("17:00", "22:00")]),
]

ADDITIVES = [
    ("1",  "mit Konservierungsstoffen"),
    ("2",  "mit Antioxidationsmitteln"),
    ("3",  "mit Geschmacksverstaerker"),
    ("4",  "mit Phosphat"),
    ("5",  "mit Suessungsmitteln"),
    ("6",  "koffeinhaltig"),
    ("7",  "mit Farbstoff"),
    ("11", "mit Suessstoff Aspartam (enthaelt eine Phenylalaninquelle)"),
]

G3 = ["3"]
G1234 = ["1", "2", "3", "4"]

SECTIONS = [
    ("suppen", "Suppen", "", [
        ("1",  "Peking Suppe, sauer-scharf", G3, ""),
        ("2",  "Frische Mixgemüsesuppe", G3, ""),
        ("3",  "Hühnersuppe mit Bambussprossen und Champignons", G3, ""),
        ("4",  "Wan-Tan-Suppe", G3, ""),
        ("5a", "Kung-Fu-Suppe, scharf", G3, ""),
        ("5b", "Nudelsuppe mit Krabben", G3, ""),
    ]),
    ("vorspeisen", "Vorspeisen", "", [
        ("6",  "Krabbenchips", [], ""),
        ("7a", "Gebackene Wan-Tan, 8 Stück", [], ""),
        ("7b", "Mini-Rolle, süß-sauer", [], ""),
        ("8",  "Frühlingsrolle, groß", G3, ""),
        ("9",  "Krabben-Salat", [], ""),
        ("10", "Gemischter Salat", [], ""),
        ("11", "Hühnerfleisch-Salat", [], ""),
        ("12", "Hähnchenspieße mit Erdnuss-Sauce", G3, ""),
    ]),
    ("schwein", "Schweinefleisch", "mit Reis", [
        ("13", "Schweinefleisch, Chop-Suey", G3, ""),
        ("14", "Schweinefleisch mit Bambussprossen, Paprika-Sauce (Gung-Po), scharf", G3, ""),
        ("15", "Schweinefleisch mit Bambussprossen und Champignons", G3, ""),
        ("16", "Schweinefleisch knusprig gebacken in süß-saurer Sauce", G3, ""),
        ("17", "Schweinefleisch nach Szechuan-Art mit Gemüse, Knoblauch, pikanter Sauce, scharf", G3, ""),
        ("18", "Schweinefleisch mit Gemüse und Curry-Sauce", G3, ""),
    ]),
    ("rind", "Rindfleisch", "mit Reis", [
        ("19", "Rinderfilet, Chop-Suey", G3, ""),
        ("20", "Rindfleisch mit Bambussprossen, Paprika-Sauce (Gung-Po), scharf", G3, ""),
        ("21", "Rindfleisch mit Bambus und Champignons", G3, ""),
        ("22", "Rindfleisch nach Szechuan-Art mit Gemüse und pikanter Knoblauch-Sauce, scharf", G3, ""),
        ("23", "Rindfleisch mit Zwiebeln", G3, ""),
        ("24", "Rindfleisch mit Gemüse und Curry-Sauce", G3, ""),
    ]),
    ("huhn", "Hühnerfleisch", "mit Reis", [
        ("25", "Hähnchenbrustfilet, Chop-Suey", G3, ""),
        ("26", "Hähnchenbrustfilet mit Bambussprossen, Paprika-Sauce (Gung-Po), scharf", G3, ""),
        ("27", "Hähnchenbrustfilet mit Bambussprossen und Champignons", G3, ""),
        ("28", "Hähnchenbrustfilet mit Ananas in süß-saurer Sauce", G3, ""),
        ("29", "Hähnchenbrustfilet nach Szechuan-Art mit Gemüse, Knoblauch, pikanter Sauce, scharf", G3, ""),
        ("30", "Hähnchenbrustfilet mit Gemüse und Curry-Sauce, scharf", G3, ""),
        ("31", "Knusprig paniertes Hähnchenbrustfilet nach Can-Ton-Art mit chinesischem Gemüse", G3, ""),
        ("32", "Hähnchenbrustfilet paniert, gebacken mit süß-saurer Sauce", G3, ""),
    ]),
    ("ente", "Gegrillte Ente", "mit Reis", [
        ("33", "Ente, Chop-Suey, mit Gemüse", G3, ""),
        ("34", "Ente mit Bambussprossen, Paprika-Sauce (Gung-Po), scharf", G3, ""),
        ("35", "Ente mit Ananas in süß-saurer Sauce", G3, ""),
        ("36", "Knusprige Ente nach Can-Ton-Art mit chinesischem Gemüse", G3, ""),
        ("37", "China-Wok spezial, knusprige Ente mit Gemüse, scharf mit Knoblauch", G3, ""),
    ]),
    ("fisch", "Fisch", "mit Reis", [
        ("38", "Gebackenes Fischfilet in süß-saurer Sauce", G3, ""),
        ("39", "Gebackenes Fischfilet nach Szechuan-Art", G3, ""),
        ("40", "Gebackenes Fischfilet mit Curry und Gemüse", G3, ""),
    ]),
    ("reis", "Reisgerichte", "", [
        ("41a", "Gebratener Reis mit Hähnchenfleisch", G3, ""),
        ("41b", "Gebratener Reis mit paniertem Hähnchenbrustfilet", G3, ""),
        ("42", "Gebratener Reis mit Schweinefleisch", G3, ""),
        ("43", "Gebratener Reis mit Rindfleisch", G3, ""),
        ("44", "Gebratener Reis mit Krabben", G3, ""),
        ("45a", "Nasi-Goreng", G1234, ""),
        ("45b", "Gebratener Reis mit gegrillter Ente", G3, ""),
    ]),
    ("nudeln", "Nudelgerichte", "", [
        ("46a", "Gebratene Nudeln mit Hähnchenfleisch", G3, ""),
        ("46b", "Gebratene Nudeln mit paniertem Hähnchenbrustfilet", G3, ""),
        ("47", "Gebratene Nudeln mit Schweinefleisch", G3, ""),
        ("48", "Gebratene Nudeln mit Rindfleisch", G3, ""),
        ("49", "Gebratene Nudeln mit Krabben", G3, ""),
        ("50a", "Bami-Goreng", G1234, ""),
        ("50b", "Gebratene Nudeln mit gegrillter Ente", G3, ""),
    ]),
    ("spezial", "Spezialitäten", "mit Reis", [
        ("51", "„Chow Sam Sing“ Krabben, Hühnerfleisch, Schweinefleisch, chinesisches Gemüse", G3, ""),
        ("52", "„Chow-Kan á la China“ Krabben, Ente, Hühnerfleisch, Schweinefleisch und chinesisches pikantes Gemüse", G3, ""),
        ("53", "Knuspriges Hähnchen mit pikanter Erdnuss-Sauce", G3, ""),
        ("54", "„Shangai-Hähnchen“ in scharfer süß-saurer Sauce", G3, ""),
        ("55", "„Drachen-Feuer“ Rinderfilet, Ente, Hühnerfleisch, Krabben und Paprika, sehr scharf mit Knoblauch", G3, ""),
        ("56", "Dreierlei Fleisch mit chinesischem Gemüse: Hühnerbrustfilet, Rinderfilet, Schweinefilet", G3, ""),
    ]),
    ("vegetarisch", "Vegetarische Gerichte", "", [
        ("57", "Frisches chinesisches Mixgemüse, pikant, scharf", G3, ""),
        ("58", "Gebratener Reis mit chinesischem Mixgemüse", G3, ""),
        ("59", "Gebratene Nudeln mit Gemüse", G3, ""),
    ]),
    ("hummerkrabben", "Hummerkrabben", "mit Reis", [
        ("68", "Hummer-Krabben, Chop-Suey", G3, ""),
        ("69", "Hummer-Krabben mit Bambussprossen, Paprika-Sauce (Gung-Po), scharf", G3, ""),
        ("70", "Hummer-Krabben knusprig gebacken in süß-saurer Sauce", G3, ""),
        ("71", "Hummer-Krabben nach Szechuan-Art mit Gemüse, Knoblauch, pikanter Sauce, scharf", [], ""),
        ("72", "Hummer-Krabben mit Gemüse und Curry-Sauce", G3, ""),
    ]),
    ("spez-ente", "Spezialitäten Ente", "mit Reis", [
        ("73", "Knusprige Ente mit pikanter Erdnuss-Sauce", G3, ""),
        ("74", "Gäng Ped Muh: Ente mit Bambus, Paprika, Bohnen, Thai-Curry und Kokosmilch, sehr scharf", G3, ""),
        ("75", "Panäng Muh: Ente mit Kokosmilch, Bambus, Paprika, Bohnen und spezieller Thai-Currymischung, scharf", G3, ""),
    ]),
    ("spez-huhn", "Spezialitäten Hähnchen", "mit Reis", [
        ("76", "Knusprige Hähnchenschenkel nach Can-Ton-Art", G3, ""),
        ("77", "Knusprige Hähnchenschenkel mit Curry und Gemüse, scharf", G3, ""),
        ("78", "Knusprige Hähnchenschenkel mit Bambussprossen, Paprika-Sauce (Gung-Po), scharf", G3, ""),
    ]),
    ("thai-reisnudeln", "Thai-Spezialitäten Reisnudeln", "", [
        ("79", "Gebratene Reisnudeln mit Hühnerfleisch und Gemüse", [], ""),
        ("80", "Gebratene Reisnudeln mit Krabben und Gemüse", [], ""),
        ("81", "Gebratene Reisnudeln mit Schinken, Huhn, Krabben und Gemüse", G1234, ""),
    ]),
    ("thai-schwein", "Thai-Spezialitäten Schweinefleisch", "mit Reis", [
        ("82", "Schweinefleisch mit Ananas, Paprika und süß-saurer Sauce", [], ""),
        ("83", "„Koon-Po-Chi“ Schweinefilet mit chinesischem Gemüse, scharf", G3, ""),
        ("84", "Muh Tord Gratain Prig Thai: Schweinefilet mit Bohnen, Knoblauch, Peperoni", G3, ""),
        ("85", "Gäng Ped Muh: Schweinefleisch mit Bambus, Paprika, Bohnen, Thai-Curry und Kokosmilch, sehr scharf", G3, ""),
        ("86", "Panäng Muh: Schweinefleisch mit Kokosmilch, Bambus, Paprika, Bohnen und spezieller Thai-Currymischung, scharf", G3, ""),
    ]),
    ("thai-rind", "Thai-Spezialitäten Rindfleisch", "mit Reis", [
        ("87", "Rinderfilet mit Ananas, Paprika und süß-saurer Sauce", G3, ""),
        ("88", "„Koon-Po-Au“ Rinderfilet mit chinesischem Gemüse, scharf", G3, ""),
        ("89", "Nüa Tord Gratian Prig Thai: Rindfleisch mit Bohnen, Knoblauch, Peperoni und Thai-Basilikum, scharf", G3, ""),
        ("90", "Gäng Pet Nüa: Rindfleisch mit Bambus, Paprika, Bohnen, Thai-Curry und Kokosmilch, sehr scharf", G3, ""),
        ("91", "Panäng Nüa: Rindfleisch mit Kokosmilch, Bambus, Paprika, Bohnen und spezieller Thai-Currymischung", G3, ""),
    ]),
    ("thai-huhn", "Thai-Spezialitäten Hühnerfleisch", "mit Reis", [
        ("92", "Hähnchenbrustfilet mit Ananas und süß-saurer Sauce", G3, ""),
        ("93", "„Kon-Po-Kai“ Hähnchenbrustfilet mit chinesischem Gemüse, scharf", G3, ""),
        ("94", "Gai Tord Gratain Prig: Hühnerfleisch, Bohnen, Knoblauch, Peperoni und Thai-Basilikum, scharf", G3, ""),
        ("95", "Gäng Pet Gai: Hühnerfleisch mit Bambus, Paprika, Bohnen, Thai-Curry und Kokosmilch, sehr scharf", G3, ""),
        ("96", "Panäng Gai: Hühnerfleisch mit Bambus, Kokosmilch, Paprika, Bohnen und spezieller Thai-Currymischung, scharf", G3, ""),
    ]),
    ("beilagen", "Beilagen", "", [
        ("60", "Gekochter Reis", [], ""),
        ("61", "Gebratener Reis", G3, ""),
        ("62", "Gebratene Nudeln", G3, ""),
        ("63", "Pommes frites", [], ""),
    ]),
    ("nachtisch", "Nachtisch", "", [
        ("64", "Gebackene Banane in Honig", [], ""),
        ("65", "Gebackene Banane in Honig mit Vanilleeis", [], ""),
        ("66", "Gebackene Ananas in Honig", [], ""),
        ("67", "Gebackene Ananas in Honig mit Vanilleeis", [], ""),
    ]),
    ("getraenke", "Getränke", "", [
        ("", "Fanta, Cola, Cola light, Sprite, Mezzo-Mix, Pepsi", [], ""),
        ("", "Mineralwasser, Flasche", [], ""),
        ("", "Apfelsaft, Apfelsaftschorle", [], ""),
        ("", "Lycheesaft, Guavensaft, Mangosaft", [], ""),
        ("", "Bitburger", [], ""),
        ("", "Weizen, Hefe", [], ""),
        ("", "Chinesisches Tsing-Tao Bier", [], ""),
        ("", "Pflaumenwein, auch als Flasche", [], ""),
        ("", "Sake, auch als Flasche", [], ""),
        ("", "Reisschnaps (Kao Lang)", [], ""),
        ("", "Fernet Branca", [], ""),
        ("", "Jasmintee, Grüner Tee", [], ""),
    ]),
]
