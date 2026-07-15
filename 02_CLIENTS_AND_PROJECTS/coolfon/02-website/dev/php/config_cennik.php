<?php
/**
 * COOLFON GSM - Centralna konfiguracja systemu wycen cennika gsm i integracji Magboss.pl B2B API
 * 
 * Tutaj można swobodnie modyfikować klucze dostępu, domyślne marże serwisu na części oraz
 * koszty robocizny przypisane do odpowiednich poziomów skomplikowania usterki.
 */

return [
    // Dane integracji Magboss.pl (ProQoS SE API)
    // Zostaw pusty ciąg znaków '', aby skrypt działał w bezpiecznym trybie offline/scrapera (pobierającym z części parts_pricing.json)
    'MAGBOSS_API_KEY' => '', 
    
    // Waluta i stawka podatku VAT (dla klienta indywidualnego na stronie wyświetlamy ceny brutto)
    'VAT_RATE' => 1.23, // 23% VAT
    
    // Polityka marżowa (narzuty na ceny hurtowe netto części)
    'MARKUP_DEFAULT' => 1.20, // +20% marży na droższe części (ekrany, itp.)
    'MARKUP_CHEAP' => 1.35,   // +35% marży na tańsze części (baterie, porty), aby zabezpieczyć minimalną rentowność

    // Matryca kosztów robocizny serwisu (robocizna brutto w PLN)
    'LABOR_COSTS' => [
        // Wymiana ekranu (szybki/wyświetlacza)
        'screen' => [
            'budget' => 130, // Prostsze modele, ekrany płaskie LCD (np. iPhone 11, Samsung A35)
            'mid'    => 170, // Ekrany OLED płaskie (np. Samsung A54, iPhone 12, iPhone 13, Redmi Note 13)
            'high'   => 230, // Precyzyjnie klejone ekrany OLED flagowców (np. iPhone 14 Pro, Samsung S22, S23)
            'ultra'  => 280, // Ekrany zagięte/najnowsze flagowce (np. iPhone 15 Pro Max, Samsung S24 Ultra)
        ],
        
        // Wymiana baterii
        'battery' => [
            'standard' => 90,  // Standardowe baterie klejone w większości marek
            'premium'  => 140, // Modele Apple iPhone (zabezpieczenie przed komunikatem iOS o nieznanej części / programowanie taśmy)
        ],
        
        // Wymiana gniazda USB / portu ładowania
        'usb' => [
            'standard' => 110, // Wymiana kompletnej dolnej płytki z portem USB-C/Lightning
        ]
    ],

    // Klasyfikacja modeli pod kątem trudności naprawy (dla poprawnego przypisania robocizny)
    'DIFFICULTY_MAPPING' => [
        // Apple iPhone
        'iphone-15-pro-max' => ['screen' => 'ultra', 'battery' => 'premium', 'usb' => 'standard'],
        'iphone-15-pro'     => ['screen' => 'high',  'battery' => 'premium', 'usb' => 'standard'],
        'iphone-15'         => ['screen' => 'high',  'battery' => 'premium', 'usb' => 'standard'],
        'iphone-14-pro-max' => ['screen' => 'high',  'battery' => 'premium', 'usb' => 'standard'],
        'iphone-14-pro'     => ['screen' => 'high',  'battery' => 'premium', 'usb' => 'standard'],
        'iphone-14'         => ['screen' => 'mid',   'battery' => 'premium', 'usb' => 'standard'],
        'iphone-13-pro-max' => ['screen' => 'high',  'battery' => 'premium', 'usb' => 'standard'],
        'iphone-13'         => ['screen' => 'mid',   'battery' => 'premium', 'usb' => 'standard'],
        'iphone-12'         => ['screen' => 'mid',   'battery' => 'premium', 'usb' => 'standard'],
        'iphone-11'         => ['screen' => 'budget', 'battery' => 'premium', 'usb' => 'standard'],
        
        // Samsung Galaxy
        'galaxy-s24-ultra' => ['screen' => 'ultra',  'battery' => 'standard', 'usb' => 'standard'],
        'galaxy-s24'       => ['screen' => 'high',   'battery' => 'standard', 'usb' => 'standard'],
        'galaxy-s23-ultra' => ['screen' => 'ultra',  'battery' => 'standard', 'usb' => 'standard'],
        'galaxy-s23'       => ['screen' => 'high',   'battery' => 'standard', 'usb' => 'standard'],
        'galaxy-s22-ultra' => ['screen' => 'ultra',  'battery' => 'standard', 'usb' => 'standard'],
        'galaxy-s22'       => ['screen' => 'high',   'battery' => 'standard', 'usb' => 'standard'],
        'galaxy-s21'       => ['screen' => 'high',   'battery' => 'standard', 'usb' => 'standard'],
        'galaxy-a54'       => ['screen' => 'mid',    'battery' => 'standard', 'usb' => 'standard'],
        'galaxy-a35'       => ['screen' => 'budget', 'battery' => 'standard', 'usb' => 'standard'],
        
        // Xiaomi / Redmi / POCO
        'xiaomi-13'     => ['screen' => 'mid',    'battery' => 'standard', 'usb' => 'standard'],
        'redmi-note-13' => ['screen' => 'mid',    'battery' => 'standard', 'usb' => 'standard'],
        'redmi-note-12' => ['screen' => 'mid',    'battery' => 'standard', 'usb' => 'standard'],
        'poco-x6'       => ['screen' => 'mid',    'battery' => 'standard', 'usb' => 'standard'],
        'poco-x5'       => ['screen' => 'mid',    'battery' => 'standard', 'usb' => 'standard']
    ]
];
