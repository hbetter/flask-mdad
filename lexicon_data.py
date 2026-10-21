# Inhalte der Lexikonseite (/lexicon, templates/lexicon.html).
#
# Bewusst als statische Daten im Code statt in der Datenbank: Die Seite
# soll ohne Bedienfeld gepflegt werden, Texte werden direkt hier geaendert.
# Grundlage sind die SEO-Texte aus dem Ordner "SEO Texte mit Seitenwerk"
# (BGM, BGF, Resilienz, Transformation, Teamentwicklung usw.), fuer das
# Lexikon gekuerzt und neutral formuliert.
#
# Aufbau eines Eintrags:
#   slug      - Anker auf der Seite (/lexicon#resilienz), nur a-z, 0-9, "-"
#   term      - angezeigter Begriff (bestimmt auch die Buchstabengruppe)
#   aliases   - weitere Bezeichnungen, werden angezeigt und von der Suche gefunden
#   category  - Schluessel aus LEXICON_CATEGORIES
#   short     - Kurzdefinition (ein Satz, hervorgehoben)
#   body      - Absaetze nach der Kurzdefinition
#   points    - optionale Aufzaehlung als (Stichwort, Text)-Paare
#   body_after- optionale Absaetze nach der Aufzaehlung
#   related   - Slugs verwandter Eintraege ("Siehe auch")

import unicodedata


LEXICON_CATEGORIES = [
    ("health", "Gesundheit & BGM"),
    ("psychology", "Psychologie in der Arbeitswelt"),
    ("change", "Transformation & Wandel"),
    ("leadership", "Führung, Team & Organisation"),
    ("play", "Spielbasierte Methoden"),
]
LEXICON_CATEGORY_LABELS = dict(LEXICON_CATEGORIES)


LEXICON_TERMS = [
    # ------------------------------------------------------------------
    # Gesundheit & BGM
    # ------------------------------------------------------------------
    {
        "slug": "gesundheit",
        "term": "Gesundheit",
        "category": "health",
        "short": "Mehr als die Abwesenheit von Krankheit: ein Zusammenspiel aus körperlichem, psychischem und sozialem Wohlbefinden.",
        "body": [
            "Physische und psychische Gesundheit sind eng miteinander verknüpft. Chronischer Stress kann sich etwa in Rückenschmerzen oder Herz-Kreislauf-Beschwerden zeigen, während körperliche Erkrankungen häufig das seelische Wohl beeinträchtigen. Gesundheit wird deshalb als Balance verschiedener Bereiche verstanden.",
            "Im Arbeitskontext ist Gesundheit ein oft unterschätzter Erfolgsfaktor: Ein gesunder Arbeitsplatz fördert das Wohlbefinden der Mitarbeitenden ebenso wie Produktivität, Motivation und Innovationskraft eines Unternehmens.",
        ],
        "related": ["physische-gesundheit", "mentale-gesundheit", "gesundheitsfoerderung", "bgm"],
    },
    {
        "slug": "physische-gesundheit",
        "term": "Physische Gesundheit",
        "aliases": ["Körperliche Gesundheit"],
        "category": "health",
        "short": "Die Funktionsfähigkeit des Körpers, ein stabiles Immunsystem und allgemeine körperliche Fitness – die Grundlage für ein aktives Leben.",
        "body": [
            "Ausgewogene Ernährung, regelmäßige Bewegung und ausreichend Schlaf sind die wichtigsten Stellschrauben; Vorsorgeuntersuchungen und Impfungen ergänzen sie präventiv.",
            "Am Arbeitsplatz wird die physische Gesundheit vor allem durch ergonomische Arbeitsplätze, Bewegung und Pausen unterstützt. Langes Sitzen, monotone Bewegungsabläufe und fehlende Pausen führen dagegen häufig zu Rückenschmerzen, Müdigkeit und langfristigen Erkrankungen. Körperliche und psychische Gesundheit beeinflussen sich dabei gegenseitig.",
        ],
        "related": ["gesundheit", "ergonomie", "mentale-gesundheit"],
    },
    {
        "slug": "bgm",
        "term": "Betriebliches Gesundheitsmanagement (BGM)",
        "aliases": ["BGM", "Gesundheitsmanagement"],
        "category": "health",
        "short": "Strategische Planung, Steuerung und Verankerung aller Maßnahmen, die Gesundheit und Leistungsfähigkeit der Menschen im Betrieb erhalten und fördern.",
        "body": [
            "Anders als einzelne Gesundheitstage oder sporadische Workshops setzt BGM auf eine dauerhafte Integration in die Betriebsstruktur: klare Ziele, Prävention, eine gesundheitsgerechte Gestaltung von Arbeitsprozessen und die aktive Beteiligung der Beschäftigten.",
            "Typische Handlungsfelder sind Arbeitsplatzgestaltung, gesundheitsfördernde Angebote, psychische Gesundheit, Work-Life-Balance sowie Kommunikation und Führung. Führungskräfte spielen eine Schlüsselrolle, weil sie das Arbeitsklima prägen und als Vorbild wirken.",
            "Gut umgesetzt kann BGM Fehlzeiten senken, die Zufriedenheit der Mitarbeitenden erhöhen und die Attraktivität als Arbeitgeber stärken.",
        ],
        "related": ["bgf", "gefaehrdungsbeurteilung", "bem", "praevention"],
    },
    {
        "slug": "bgf",
        "term": "Betriebliche Gesundheitsförderung (BGF)",
        "aliases": ["BGF"],
        "category": "health",
        "short": "Alle konkreten Maßnahmen im Betrieb, die die physische und psychische Gesundheit der Beschäftigten erhalten, fördern und verbessern.",
        "body": [
            "Zur BGF gehören etwa ergonomische Arbeitsplätze, Bewegungsprogramme und bewegte Pausen, Angebote zu Stressbewältigung und Achtsamkeit, Coachings, ein gesundes Verpflegungsangebot sowie Vorsorge- und Check-up-Aktionen.",
            "BGF ist ein Baustein des betrieblichen Gesundheitsmanagements: Während das BGM den strategischen Rahmen setzt, beschreibt die BGF die Maßnahmen, die im Arbeitsalltag ankommen. Ein wertschätzendes Betriebsklima gilt dabei selbst als wirksamer Gesundheitsfaktor.",
        ],
        "related": ["bgm", "gesundheitsfoerderung", "ergonomie"],
    },
    {
        "slug": "gesundheitsfoerderung",
        "term": "Gesundheitsförderung",
        "category": "health",
        "short": "Ganzheitlicher Ansatz, der Bedingungen für ein gesundes Leben schafft, statt nur Krankheiten zu vermeiden.",
        "body": [
            "Die zwei zentralen Säulen sind die physische Gesundheit – Bewegung, ausgewogene Ernährung, ausreichend Schlaf – und die psychische Gesundheit, etwa durch Stressbewältigung, Entspannungstechniken, ein stabiles soziales Netzwerk und einen offenen Umgang mit mentalen Herausforderungen. Ergänzt wird beides durch Prävention.",
            "In Zeiten zunehmender Belastungen durch Stress, Bewegungsmangel oder ungesunde Lebensgewohnheiten gewinnt Gesundheitsförderung im privaten wie im beruflichen Umfeld an Bedeutung.",
        ],
        "related": ["bgf", "praevention", "gesundheit"],
    },
    {
        "slug": "praevention",
        "term": "Prävention",
        "category": "health",
        "short": "Vorbeugende Maßnahmen, die gesundheitliche Risiken frühzeitig erkennen und Erkrankungen verhindern sollen.",
        "body": [
            "Dazu zählen Vorsorgeuntersuchungen, Impfaktionen und Gesundheits-Check-ups ebenso wie die vorbeugende Gestaltung der Arbeitsbedingungen – etwa durch Ergonomie, klare Aufgaben und eine realistische Arbeitslast. Präventive Maßnahmen wirken langfristig und können krankheitsbedingte Fehlzeiten reduzieren.",
        ],
        "related": ["bgf", "gefaehrdungsbeurteilung", "fehlzeiten"],
    },
    {
        "slug": "gefaehrdungsbeurteilung",
        "term": "Gefährdungsbeurteilung",
        "category": "health",
        "short": "Systematische Analyse, welche Belastungen und Gefährdungen an einem Arbeitsplatz bestehen und welche Schutzmaßnahmen nötig sind.",
        "body": [
            "In Deutschland ist sie für Arbeitgeber nach dem Arbeitsschutzgesetz verpflichtend und umfasst ausdrücklich auch psychische Belastungen – etwa durch Zeitdruck, unklare Aufgaben oder Konflikte. Ihre Ergebnisse sind häufig der Ausgangspunkt für Maßnahmen des betrieblichen Gesundheitsmanagements.",
        ],
        "related": ["bgm", "praevention", "stressoren"],
    },
    {
        "slug": "bem",
        "term": "Betriebliches Eingliederungsmanagement (BEM)",
        "aliases": ["BEM"],
        "category": "health",
        "short": "Verfahren, mit dem Arbeitgeber Beschäftigte nach längerer Arbeitsunfähigkeit bei der Rückkehr unterstützen und erneuten Ausfällen vorbeugen.",
        "body": [
            "Arbeitgeber müssen ein BEM anbieten, wenn Beschäftigte innerhalb von zwölf Monaten länger als sechs Wochen ununterbrochen oder wiederholt arbeitsunfähig waren (§ 167 Abs. 2 SGB IX). Die Teilnahme ist für die Beschäftigten freiwillig.",
            "Steigende BEM-Fallzahlen können ein Hinweis darauf sein, dass Belastungen im Unternehmen zunehmen – und dass präventive Ansätze des Gesundheitsmanagements gestärkt werden sollten.",
        ],
        "related": ["bgm", "fehlzeiten"],
    },
    {
        "slug": "fehlzeiten",
        "term": "Fehlzeiten und Krankenstand",
        "aliases": ["Krankenstand"],
        "category": "health",
        "short": "Krankheitsbedingte Abwesenheiten von Beschäftigten; der Krankenstand gibt ihren Anteil an der Sollarbeitszeit an.",
        "body": [
            "Häufige Ursachen sind Atemwegs- und Muskel-Skelett-Erkrankungen sowie psychische Erkrankungen. Hohe Fehlzeiten belasten nicht nur die Betroffenen, sondern auch die Teams, die ihre Aufgaben übernehmen müssen.",
            "Präventive Gesundheitsförderung, ein gutes Arbeitsklima und Resilienzförderung können krankheitsbedingte Ausfälle senken.",
        ],
        "related": ["praevention", "praesentismus", "bgm", "bem"],
    },
    {
        "slug": "praesentismus",
        "term": "Präsentismus",
        "category": "health",
        "short": "Arbeiten trotz Krankheit – Beschäftigte sind anwesend, aber gesundheitlich eingeschränkt und weniger leistungsfähig.",
        "body": [
            "Präsentismus entsteht häufig aus Pflichtgefühl, Angst um den Arbeitsplatz, hoher Arbeitslast oder der Sorge, Kolleginnen und Kollegen im Stich zu lassen. Er kann Erkrankungen verschleppen, Fehler begünstigen und Ansteckungen im Team fördern.",
            "Weil Präsentismus in keiner Fehlzeitenstatistik auftaucht, wird er leicht übersehen – dabei kann er die Produktivität eines Unternehmens stärker beeinträchtigen als krankheitsbedingte Abwesenheit. Eine Kultur, in der Erholung erlaubt ist, und ein wirksames Gesundheitsmanagement wirken dem entgegen.",
        ],
        "related": ["fehlzeiten", "bgf", "unternehmenskultur"],
    },
    {
        "slug": "ergonomie",
        "term": "Ergonomische Arbeitsplatzgestaltung",
        "aliases": ["Ergonomie", "Arbeitsplatzgestaltung"],
        "category": "health",
        "short": "Gestaltung von Arbeitsplätzen und Arbeitsabläufen, die körperliche Belastungen verringert und Langzeitschäden vorbeugt.",
        "body": [
            "Beispiele sind höhenverstellbare Schreibtische, gut angepasste Stühle, ein optimal eingerichteter Bildschirmarbeitsplatz, natürliche Beleuchtung und Lärmschutz. Langes Sitzen, monotone Bewegungsabläufe und fehlende Pausen gelten als typische Risikofaktoren.",
        ],
        "related": ["bgf", "praevention"],
    },
    {
        "slug": "work-life-balance",
        "term": "Work-Life-Balance",
        "category": "health",
        "short": "Ausgewogenes Verhältnis zwischen beruflichen Anforderungen und privatem Leben.",
        "body": [
            "Flexible Arbeitszeiten, Homeoffice-Optionen, Angebote zur Kinderbetreuung und die Möglichkeit, wirklich abzuschalten, erleichtern die Vereinbarkeit von Beruf und Privatleben. Eine gesunde Balance beugt Erschöpfung vor, stärkt die mentale Gesundheit und ist für viele Beschäftigte ein wichtiges Kriterium bei der Wahl ihres Arbeitgebers.",
        ],
        "related": ["mentale-gesundheit", "hybride-arbeit", "mitarbeiterbindung"],
    },
    {
        "slug": "mentale-gesundheit",
        "term": "Mentale Gesundheit",
        "aliases": ["Mental Health", "Psychische Gesundheit"],
        "category": "health",
        "short": "Emotionales, psychisches und soziales Gleichgewicht – und die Fähigkeit, mit den Höhen und Tiefen des Lebens umzugehen.",
        "body": [
            "Mentale Gesundheit ist mehr als die Abwesenheit psychischer Erkrankungen. Dazu gehört, sich selbst zu verstehen, Emotionen zu regulieren und gesunde Entscheidungen zu treffen. Sie ist ein dynamischer Zustand, der von persönlichen Erfahrungen, sozialen Beziehungen und äußeren Faktoren wie Stress oder Veränderungen beeinflusst wird.",
            "Im Arbeitsalltag wirken vor allem Arbeitsbelastung, Arbeitsklima und Beziehungen, die Sinnhaftigkeit der Tätigkeit und die Work-Life-Balance auf die mentale Gesundheit. Unternehmen, die offen mit dem Thema umgehen und Unterstützung anbieten, schaffen Vertrauen – und profitieren von engagierten, leistungsfähigen Teams.",
        ],
        "related": ["resilienz", "psychologische-sicherheit", "stress", "burnout"],
    },
    {
        "slug": "burnout",
        "term": "Burnout",
        "aliases": ["Burn-out"],
        "category": "health",
        "short": "Zustand tiefer emotionaler, körperlicher und geistiger Erschöpfung, der mit anhaltender Überlastung im Beruf in Verbindung gebracht wird.",
        "body": [
            "Die Weltgesundheitsorganisation beschreibt Burn-out in der ICD-11 als berufsbezogenes Phänomen, das aus chronischem Stress am Arbeitsplatz entsteht, der nicht erfolgreich bewältigt wurde. Als Risikofaktoren gelten unter anderem hoher Leistungsdruck, unrealistische Deadlines, ständige Erreichbarkeit, fehlende Anerkennung und ein angespanntes Betriebsklima.",
            "Wer Anzeichen bei sich bemerkt, sollte ärztliche oder psychotherapeutische Unterstützung suchen. Unternehmen können vor allem vorbeugend wirken – durch gesunde Arbeitsbedingungen, eine realistische Arbeitsplanung und eine Kultur, in der Belastungen offen angesprochen werden dürfen.",
        ],
        "related": ["stress", "mentale-gesundheit", "stressmanagement"],
    },
    {
        "slug": "stress",
        "term": "Stress",
        "category": "health",
        "short": "Körperliche und psychische Reaktion auf Anforderungen, die als belastend wahrgenommen werden.",
        "body": [
            "In Situationen, die als bedrohlich empfunden werden, aktiviert der Körper das sympathische Nervensystem und schüttet Stresshormone wie Adrenalin und Cortisol aus – die sogenannte Kampf-oder-Flucht-Reaktion. Herzschlag und Atmung beschleunigen sich, die Muskeln spannen sich an.",
            "Kurzfristig ist diese Reaktion hilfreich. Hält die Belastung jedoch an, kann chronischer Stress zu Erschöpfung, Schlaf- und Konzentrationsproblemen sowie zu Herz-Kreislauf-Erkrankungen oder psychischen Störungen beitragen.",
        ],
        "related": ["stressoren", "stressmanagement", "resilienz"],
    },
    {
        "slug": "stressoren",
        "term": "Stressoren",
        "aliases": ["Stressfaktoren"],
        "category": "health",
        "short": "Auslöser von Stress – von außen kommend oder in der Person selbst liegend.",
        "body": [
            "Äußere Stressoren im Arbeitsalltag sind etwa Zeitdruck, Überforderung durch Aufgabenfülle oder Komplexität, mangelnde Anerkennung, Konflikte und fehlende oder unklare Kommunikation. Innere Stressoren sind zum Beispiel Perfektionismus oder die Angst vor Fehlern. Wirksame Stressbewältigung setzt an beiden Bereichen an.",
        ],
        "related": ["stress", "stressmanagement"],
    },
    {
        "slug": "stressmanagement",
        "term": "Stressmanagement",
        "aliases": ["Stressbewältigung"],
        "category": "health",
        "short": "Strategien und Techniken, um Stressauslöser zu verringern und besser mit Belastungen umzugehen.",
        "body": [
            "Ziel ist nicht, Stress vollständig zu vermeiden, sondern die Balance zwischen den Anforderungen des Alltags und den individuellen Ressourcen herzustellen. Zentrale Ansätze sind das Erkennen von Stressfaktoren, Entspannungstechniken wie Progressive Muskelentspannung, Meditation oder Atemübungen sowie ein gesunder Lebensstil mit Bewegung, Ernährung und ausreichend Schlaf.",
            "Stress entsteht häufig in den Strukturen, nicht nur beim Einzelnen. Arbeitgeber können deshalb viel beitragen:",
        ],
        "points": [
            ("Klare Strukturen", "eindeutige Verantwortlichkeiten und transparente Kommunikation nehmen Unsicherheit."),
            ("Flexibilität", "Homeoffice und flexible Arbeitszeiten erleichtern eine gute Work-Life-Balance."),
            ("Gesundheitsförderung", "Workshops zu Stressmanagement, Bewegungsangebote und ergonomische Arbeitsplätze wirken präventiv."),
            ("Wertschätzung", "regelmäßiges Feedback, Lob und die Förderung individueller Stärken stärken das Selbstvertrauen."),
        ],
        "body_after": [
            "Stress ist auch ein gesellschaftliches Thema: Stressbedingte Ausfälle verursachen erhebliche Kosten, während ein bewusster Umgang mit Stress die Lebensqualität deutlich verbessern kann.",
        ],
        "related": ["stress", "entspannungstechniken", "achtsamkeit", "resilienzfoerderung"],
    },
    {
        "slug": "entspannungstechniken",
        "term": "Entspannungstechniken",
        "aliases": ["Progressive Muskelentspannung", "Autogenes Training"],
        "category": "health",
        "short": "Übungen, die Körper und Geist gezielt beruhigen und so helfen, Stress abzubauen.",
        "body": [
            "Bekannte Verfahren sind die Progressive Muskelentspannung nach Edmund Jacobson, bei der Muskelgruppen nacheinander an- und wieder entspannt werden, und das Autogene Training nach Johannes Heinrich Schultz, eine Form der konzentrativen Selbstentspannung. Hinzu kommen Meditation, Atemübungen und Yoga.",
            "Regelmäßig geübt, wirken Entspannungstechniken nachweislich positiv auf die Stressbewältigung. Im Betrieb lassen sie sich als Kurse, kurze Übungseinheiten oder bewusste Pausen in den Alltag integrieren.",
        ],
        "related": ["stressmanagement", "achtsamkeit", "bgf"],
    },

    # ------------------------------------------------------------------
    # Psychologie in der Arbeitswelt
    # ------------------------------------------------------------------
    {
        "slug": "resilienz",
        "term": "Resilienz",
        "aliases": ["psychische Widerstandskraft"],
        "category": "psychology",
        "short": "Psychische Widerstandskraft: die Fähigkeit, Stress, Rückschläge und Krisen zu bewältigen und gestärkt daraus hervorzugehen.",
        "body": [
            "Der Begriff geht auf das lateinische „resilire“ zurück – „zurückspringen“ oder „abprallen“. Resiliente Menschen lassen sich nicht so leicht aus der Bahn werfen, bleiben auch in schwierigen Zeiten handlungsfähig und wachsen an Herausforderungen.",
            "Die Resilienzforschung – unter anderem mit den Arbeiten von Emmy Werner und Ann Masten – zeigt: Resilienz ist keine angeborene Eigenschaft, sondern lässt sich wie ein Muskel trainieren. Sie ist nicht nur für Einzelne bedeutsam, sondern auch für Teams und ganze Organisationen, die sich in einer schnell wandelnden Arbeitswelt immer wieder anpassen müssen.",
            "Im Alltag zeigt sich Resilienz in einem resilienten Lebensstil: einer gesunden Lebensführung mit Bewegung, Ernährung und Schlaf, einem wirksamen Umgang mit Stress, tragfähigen sozialen Beziehungen und einer optimistischen Grundhaltung, die Herausforderungen auch als Chance zum Wachsen sieht.",
            "Für Dr. Irene Preußner, die Entwicklerin von MENSCH DENK AN DICH®, soll Resilienz nicht erklärt, sondern erlebt werden – erst die eigene Erfahrung macht sie im Arbeitsalltag verfügbar.",
        ],
        "related": ["resilienz-spiele", "resilienzfaktoren", "resilienzfoerderung", "resilienztraining"],
    },
    {
        "slug": "resilienzfaktoren",
        "term": "Resilienzfaktoren",
        "category": "psychology",
        "short": "Eigenschaften, Fähigkeiten und Bedingungen, die Menschen widerstandsfähiger machen.",
        "body": [
            "Häufig genannt werden Achtsamkeit und Selbstreflexion, Akzeptanz und Anpassungsfähigkeit, lösungsorientiertes Denken, positives Denken und realistischer Optimismus, der Fokus auf das, was sich beeinflussen lässt, Selbstwirksamkeit, emotionale Stabilität und Emotionsregulation, Empathie, soziale Unterstützung durch ein stabiles Netzwerk, ein klares Bild der eigenen Ziele, die Bereitschaft, Verantwortung zu übernehmen, sowie gesunde Routinen.",
            "Viele dieser Faktoren entfalten sich im Miteinander: Das Umfeld und die Unterstützung durch andere spielen für die Resilienz eine zentrale Rolle.",
        ],
        "related": ["resilienz", "achtsamkeit", "loesungsorientierung"],
    },
    {
        "slug": "resilienzfoerderung",
        "term": "Resilienzförderung",
        "category": "psychology",
        "short": "Gezielte Stärkung der Widerstandskraft von Einzelnen, Teams und Organisationen.",
        "body": [
            "Im Unternehmen reicht Resilienzförderung von Achtsamkeitspraxis und gezieltem Stressmanagement über Trainings für Führungskräfte bis zu einer Kultur, in der Probleme offen angesprochen und Fehler als Lernchance verstanden werden.",
            "Wird sie vernachlässigt, zeigen sich die Folgen häufig in Überlastung, Konflikten, Fehlzeiten und sinkender Veränderungsbereitschaft.",
        ],
        "related": ["resilienz", "resilienztraining", "resilienz-spiele"],
    },
    {
        "slug": "resilienztraining",
        "term": "Resilienztraining",
        "category": "psychology",
        "short": "Trainings, Seminare oder Kurse, in denen Menschen mit praktischen Übungen ihre Widerstandskraft stärken.",
        "body": [
            "Resilienztrainings vermitteln Strategien für den Umgang mit Stress und Rückschlägen und machen individuelle Resilienzfaktoren erfahrbar. Wirksam sind sie vor allem dann, wenn das Gelernte in den Arbeitsalltag übertragen wird – etwa durch gemeinsame Reflexion im Team und konkrete Vereinbarungen.",
        ],
        "related": ["resilienzfoerderung", "resilienz-spiele", "play2change"],
    },
    {
        "slug": "achtsamkeit",
        "term": "Achtsamkeit",
        "aliases": ["Achtsamkeitspraxis"],
        "category": "psychology",
        "short": "Mit voller Aufmerksamkeit im Hier und Jetzt sein und Gedanken, Gefühle und Situationen wahrnehmen, ohne sich von ihnen mitreißen zu lassen.",
        "body": [
            "Während Stress oft zu Tunnelblick und impulsiven Reaktionen führt, hilft Achtsamkeit, bewusst innezuhalten, Prioritäten zu setzen und fokussiert zu handeln. Kurze Atemübungen oder bewusste Pausen lassen sich leicht in den Arbeitsalltag einbauen. Achtsamkeit gilt als wichtiger Resilienzfaktor.",
        ],
        "related": ["resilienzfaktoren", "stressmanagement", "selbstreflexion"],
    },
    {
        "slug": "positive-psychologie",
        "term": "Positive Psychologie",
        "category": "psychology",
        "short": "Teilbereich der Psychologie, der sich mit Stärken, Wohlbefinden, Resilienz und Optimismus befasst – statt vorrangig mit Problemen.",
        "body": [
            "Als Begründer gilt der US-amerikanische Psychologe Martin Seligman. Im Unterschied zu Ansätzen, die vor allem auf die Behandlung von Störungen ausgerichtet sind, fragt die Positive Psychologie, was Menschen gedeihen lässt.",
            "In der Arbeitswelt gewinnt sie an Bedeutung, weil Beschäftigte neben Sicherheit und Gehalt zunehmend Sinnhaftigkeit, Wertschätzung und Vertrauen suchen. Sie ist eine der wissenschaftlichen Grundlagen von MENSCH DENK AN DICH®.",
        ],
        "related": ["perma", "positive-leadership", "mdad"],
    },
    {
        "slug": "perma",
        "term": "PERMA-Modell",
        "category": "psychology",
        "short": "Modell von Martin Seligman mit fünf Bausteinen für ein erfülltes Leben.",
        "body": [
            "PERMA steht für Positive Emotionen, Engagement, positive Beziehungen (Relationships), Sinnhaftigkeit (Meaning) und Zielerreichung (Accomplishment). Im Unternehmenskontext dient das Modell als Orientierung dafür, welche Bedingungen Wohlbefinden und Leistungsfähigkeit von Mitarbeitenden fördern.",
        ],
        "related": ["positive-psychologie", "positive-leadership"],
    },
    {
        "slug": "selbstwirksamkeit",
        "term": "Selbstwirksamkeit",
        "category": "psychology",
        "short": "Die Überzeugung, durch eigenes Handeln etwas bewirken und Herausforderungen meistern zu können.",
        "body": [
            "Das Konzept geht auf den Psychologen Albert Bandura zurück. Selbstwirksamkeit stärkt das Vertrauen in die eigenen Fähigkeiten und ist eine wichtige Voraussetzung für Veränderungsbereitschaft. Sie wächst vor allem durch eigene Erfolgserlebnisse – zum Beispiel, wenn Mitarbeitende erleben, dass sie selbst Lösungen entwickeln und umsetzen können.",
            "Irene Preußner sieht in ihr einen zentralen Wirkfaktor für Veränderung: Wissen und Appelle verändern selten Verhalten, erlebte Selbstwirksamkeit dagegen schon. Sie lässt sich deshalb nicht erklären, sondern nur durch Erfahrung aufbauen – etwa im geschützten Spielraum.",
        ],
        "related": ["veraenderungskompetenz", "probehandeln", "playfulness", "resilienz"],
    },
    {
        "slug": "intrinsische-motivation",
        "term": "Intrinsische und extrinsische Motivation",
        "aliases": ["Intrinsische Motivation", "Extrinsische Motivation"],
        "category": "psychology",
        "short": "Intrinsisch motiviert handelt, wer etwas um seiner selbst willen tut; extrinsisch motiviert, wer wegen eines Anreizes von außen handelt.",
        "body": [
            "Extrinsische Motivation entsteht durch Belohnungen, Punkte, Prämien, Lob oder die Vermeidung von Nachteilen. Sie wirkt gut bei klar umrissenen, wiederholbaren Aufgaben. Intrinsische Motivation entsteht aus Freude am Tun, Neugier und Sinn – und gilt als nachhaltiger.",
            "Nach der Selbstbestimmungstheorie von Edward Deci und Richard Ryan wächst intrinsische Motivation, wenn drei Grundbedürfnisse erfüllt sind: Autonomie, Kompetenzerleben und soziale Eingebundenheit.",
            "Die Unterscheidung ist der Kern der Abgrenzung zwischen Gamification, die vor allem extrinsisch über Anreize wirkt, und Playfulness, die auf intrinsische Motivation setzt. Gerade Kreativität, kritisches Denken und Innovation lassen sich kaum durch Belohnungssysteme erzwingen.",
        ],
        "related": ["playfulness", "gamification", "flow"],
    },
    {
        "slug": "flow",
        "term": "Flow",
        "aliases": ["Flow-Erleben"],
        "category": "psychology",
        "short": "Zustand völliger Vertiefung in eine Tätigkeit, in dem Zeit und Selbstzweifel in den Hintergrund treten.",
        "body": [
            "Beschrieben hat das Flow-Erleben der Psychologe Mihaly Csikszentmihalyi. Es entsteht, wenn Anforderung und eigene Fähigkeiten im Gleichgewicht sind, das Ziel klar ist und unmittelbare Rückmeldung erfolgt.",
            "Spiele erzeugen leicht Flow. Irene Preußner sieht darin einen Grund, warum spielerisches Lernen wirkt: Im Flow entsteht eher intrinsische Motivation – und die sorgt dafür, dass Erkenntnisse nachhaltig bleiben.",
        ],
        "related": ["intrinsische-motivation", "playfulness", "serious-games"],
    },
    {
        "slug": "emotionale-intelligenz",
        "term": "Emotionale Intelligenz",
        "category": "psychology",
        "short": "Die Fähigkeit, eigene und fremde Gefühle wahrzunehmen, zu verstehen und angemessen mit ihnen umzugehen.",
        "body": [
            "Das Konzept wurde von Peter Salovey und John D. Mayer beschrieben und durch Daniel Goleman bekannt. Dazu gehören Selbstwahrnehmung, Emotionsregulation, Empathie und soziale Kompetenz.",
            "Menschen mit hoher emotionaler Intelligenz gehen besser mit Konflikten um, zeigen mehr Empathie und tragen zu einem positiven Arbeitsklima bei – für Führungskräfte ist sie eine Schlüsselkompetenz.",
        ],
        "related": ["arbeitsklima", "selbstreflexion", "fuehrungskraefte-coaching"],
    },
    {
        "slug": "psychologische-sicherheit",
        "term": "Psychologische Sicherheit",
        "aliases": ["Psychological Safety"],
        "category": "psychology",
        "short": "Die gemeinsame Überzeugung in einem Team, dass man Fragen, Ideen, Bedenken und Fehler offen ansprechen kann, ohne negative Folgen befürchten zu müssen.",
        "body": [
            "Geprägt wurde der Begriff vor allem durch die Organisationsforscherin Amy Edmondson. Fehlt psychologische Sicherheit, herrscht in Meetings Zurückhaltung, Probleme bleiben unausgesprochen und Innovation stockt.",
            "Teams mit hoher psychologischer Sicherheit lernen schneller und sprechen auch sensible Themen an – ein wichtiger Faktor für Gesundheit, Zusammenarbeit und Leistungsfähigkeit.",
        ],
        "related": ["fehlerkultur", "feedbackkultur", "mentale-gesundheit"],
    },
    {
        "slug": "innere-kuendigung",
        "term": "Innere Kündigung",
        "category": "psychology",
        "short": "Zustand, in dem Mitarbeitende zwar anwesend sind, sich emotional aber längst vom Unternehmen gelöst haben.",
        "body": [
            "Betroffene machen nur noch „Dienst nach Vorschrift“, bringen kaum eigene Ideen ein und identifizieren sich nicht mehr mit ihrer Arbeit. Ursachen sind häufig fehlende Wertschätzung, mangelnde Kommunikation, Veränderungen ohne Beteiligung oder Isolation in hybriden Arbeitsmodellen.",
            "Innere Kündigung geht oft mit steigender Fluktuation, Unzufriedenheit und sinkender Produktivität einher.",
        ],
        "related": ["mitarbeiterbindung", "fluktuation", "unternehmenskultur"],
    },
    {
        "slug": "selbstreflexion",
        "term": "Selbstreflexion",
        "category": "psychology",
        "short": "Die Fähigkeit, das eigene Denken, Fühlen und Handeln bewusst zu betrachten und daraus zu lernen.",
        "body": [
            "Selbstreflexion ist ein Resilienzfaktor und eine Kernkompetenz guter Führung. Wer bewusst wahrnimmt, was in ihm vorgeht, kann besser auf Stress reagieren, eigene Stärken erkennen und blinde Flecken aufdecken. In Coaching und spielbasierten Methoden wird sie gezielt angeregt.",
        ],
        "related": ["resilienzfaktoren", "coaching", "potenzialentfaltung"],
    },
    {
        "slug": "loesungsorientierung",
        "term": "Lösungsorientiertes Denken",
        "aliases": ["Lösungsorientierung"],
        "category": "psychology",
        "short": "Haltung, den Blick auf Lösungen, Ressourcen und nächste Schritte zu richten, statt sich von Problemen lähmen zu lassen.",
        "body": [
            "Lösungsorientierte Menschen suchen aktiv nach Möglichkeiten und leiten konkrete Schritte zur Bewältigung schwieriger Situationen ein. In der Beratung ist besonders der lösungsfokussierte Ansatz nach Steve de Shazer und Insoo Kim Berg bekannt, der danach fragt, was bereits funktioniert und wie das gewünschte Ziel aussieht.",
        ],
        "related": ["resilienzfaktoren", "systemische-beratung", "coaching"],
    },
    {
        "slug": "hochstapler-syndrom",
        "term": "Hochstapler-Syndrom",
        "aliases": ["Impostor-Phänomen"],
        "category": "psychology",
        "short": "Verzerrte Selbstwahrnehmung, bei der Menschen ihre Erfolge als unverdient erleben und ihre Fähigkeiten unterschätzen.",
        "body": [
            "Betroffene führen Erfolge eher auf Glück oder Zufall zurück und fürchten, als „Hochstapler“ entlarvt zu werden. Das kann dazu führen, dass vorhandene Potenziale ungenutzt bleiben. Feedback und Coaching helfen, zu einer realistischeren Selbsteinschätzung zu finden.",
        ],
        "related": ["dunning-kruger", "potenzialentfaltung"],
    },
    {
        "slug": "dunning-kruger",
        "term": "Dunning-Kruger-Effekt",
        "category": "psychology",
        "short": "Kognitive Verzerrung, bei der Personen mit geringerer Kompetenz in einem Bereich ihre Fähigkeiten überschätzen.",
        "body": [
            "Benannt ist der Effekt nach den Psychologen David Dunning und Justin Kruger. Wie das Hochstapler-Syndrom erschwert er eine realistische Einschätzung der eigenen Stärken und Schwächen. Regelmäßiges, wertschätzendes Feedback und Selbstreflexion wirken dem entgegen.",
        ],
        "related": ["hochstapler-syndrom", "feedbackkultur"],
    },
    {
        "slug": "systemische-beratung",
        "term": "Systemische Beratung",
        "category": "psychology",
        "short": "Beratungsansatz, der Menschen nicht isoliert betrachtet, sondern im Zusammenhang ihrer Beziehungen, Rollen und Organisationen.",
        "body": [
            "Probleme und Lösungen werden als Teil eines Systems verstanden – etwa eines Teams oder Unternehmens. Systemisch Beratende arbeiten mit Fragetechniken, Perspektivwechseln und einem Fokus auf Ressourcen. Der Ansatz ist neben der Positiven Psychologie eine Grundlage von MENSCH DENK AN DICH®.",
        ],
        "related": ["coaching", "loesungsorientierung", "mdad"],
    },
    {
        "slug": "gruppendynamik",
        "term": "Gruppendynamik",
        "category": "psychology",
        "short": "Die Kräfte und Prozesse, die das Verhalten von Menschen in Gruppen beeinflussen.",
        "body": [
            "Der Begriff geht auf den Sozialpsychologen Kurt Lewin zurück. Dazu gehören Rollen, Beziehungen, Machtverhältnisse, unausgesprochene Regeln und die Art, wie Konflikte ausgetragen werden. Gruppendynamische Prozesse können Zusammenarbeit beflügeln oder blockieren – spielbasierte und erfahrungsorientierte Methoden machen sie sichtbar und besprechbar.",
        ],
        "related": ["teamentwicklung", "tuckman", "serious-play"],
    },

    # ------------------------------------------------------------------
    # Transformation & Wandel
    # ------------------------------------------------------------------
    {
        "slug": "transformation",
        "term": "Transformation",
        "category": "change",
        "short": "Tiefgreifender Veränderungsprozess, durch den sich Menschen, Organisationen oder Gesellschaften an neue Bedingungen anpassen und weiterentwickeln.",
        "body": [
            "Auslöser sind etwa Digitalisierung, Globalisierung, neue Technologien oder gesellschaftlicher Wandel wie das Ziel der Klimaneutralität. Transformation verändert Strategien, Strukturen, Prozesse und Kompetenzen – und damit auch die Arbeit jedes Einzelnen.",
            "Sie bringt Unsicherheit mit sich, eröffnet aber vor allem neue Chancen: Neue Arbeitsfelder entstehen, Zusammenarbeit wird neu gedacht.",
        ],
        "related": ["business-transformation", "change-management", "veraenderungskompetenz"],
    },
    {
        "slug": "business-transformation",
        "term": "Business Transformation",
        "category": "change",
        "short": "Strategische Neuausrichtung eines Unternehmens, um sich an veränderte Märkte, Technologien und Kundenanforderungen anzupassen.",
        "body": [
            "Business Transformation ist kein einmaliges Projekt, sondern ein kontinuierlicher Prozess. Unternehmen, die den Wandel scheuen, riskieren Wettbewerbsfähigkeit, Effizienz und qualifizierte Fachkräfte. Gelingen kann sie nur, wenn die Menschen den Wandel verstehen und aktiv mitgestalten.",
        ],
        "related": ["transformation", "unternehmensentwicklung", "change-management"],
    },
    {
        "slug": "industrie-4-0",
        "term": "Industrie 4.0",
        "category": "change",
        "short": "Bezeichnung für die Vernetzung und Digitalisierung der industriellen Produktion.",
        "body": [
            "Durch intelligente Maschinen, Datenaustausch und Automatisierung verändern sich Arbeitsabläufe und Berufsbilder grundlegend: Neue Tätigkeiten entstehen, traditionelle verändern sich oder fallen weg. Damit ist Industrie 4.0 ein zentraler Treiber der Transformation in der Arbeitswelt.",
        ],
        "related": ["transformation", "weiterbildung"],
    },
    {
        "slug": "change-management",
        "term": "Change Management",
        "aliases": ["Veränderungsmanagement", "Change-Prozess"],
        "category": "change",
        "short": "Gezielte Planung und Steuerung von Veränderungsprozessen in Unternehmen.",
        "body": [
            "Statt Veränderungen einfach geschehen zu lassen, sorgt Change Management mit einem strukturierten Vorgehen dafür, dass sie erfolgreich umgesetzt und die betroffenen Menschen mitgenommen werden. Entscheidend sind Transparenz, Mitgestaltungsmöglichkeiten und eine klare Kommunikation, die Ängste ernst nimmt.",
            "Veränderungen am Arbeitsplatz können ganz unterschiedliche Formen haben:",
        ],
        "points": [
            ("Technologische Innovationen", "neue Software oder Automatisierung, die neue Kompetenzen verlangen."),
            ("Organisatorische Umstrukturierungen", "Fusionen, Abteilungswechsel oder neue Hierarchien."),
            ("Neue Arbeitsmodelle", "Remote Work, flexible Arbeitszeiten oder hybride Modelle."),
            ("Veränderte Unternehmensziele", "strategische Neuausrichtungen auf neue Märkte, Produkte oder Dienstleistungen."),
        ],
        "body_after": [
            "Gutes Change Management verringert Widerstände, erhöht Akzeptanz und Motivation und beschleunigt die Einführung neuer Strategien und Technologien. Entscheidend ist, die Beschäftigten aktiv einzubinden – ohne Beteiligung scheitern Veränderungsprozesse besonders häufig.",
        ],
        "related": ["widerstand", "partizipation", "veraenderungskompetenz", "transformation"],
    },
    {
        "slug": "partizipation",
        "term": "Partizipation",
        "aliases": ["Mitarbeiterbeteiligung", "Kollektive Intelligenz"],
        "category": "change",
        "short": "Aktive Einbindung von Mitarbeitenden und Führungskräften in Entscheidungen und Veränderungsprozesse.",
        "body": [
            "Wer den Wandel mitgestaltet, versteht seine Hintergründe, unterstützt die Umsetzung und fühlt sich mitverantwortlich für das Ergebnis. Partizipation erhöht so die Akzeptanz, reduziert Widerstände und stärkt Motivation und Mitarbeiterbindung.",
            "Zugleich nutzt sie die kollektive Intelligenz einer Organisation: Mitarbeitende kennen die operativen Abläufe am besten. Werden verschiedene Perspektiven einbezogen, entstehen kreativere und fundiertere Entscheidungen. Ohne Einbindung bleiben dagegen wertvolle Ideen unentdeckt, und Mitarbeitende fühlen sich übergangen.",
        ],
        "related": ["change-management", "widerstand", "mitarbeiterbindung"],
    },
    {
        "slug": "veraenderungskompetenz",
        "term": "Veränderungskompetenz",
        "aliases": ["Veränderungsbereitschaft"],
        "category": "change",
        "short": "Die Fähigkeit, sich an neue Situationen anzupassen, Veränderungen aktiv zu gestalten und aus ihnen zu lernen.",
        "body": [
            "Sie setzt sich aus Offenheit für Neues, Lernbereitschaft, emotionaler Stabilität, Problemlösungskompetenz und Selbstwirksamkeit zusammen.",
            "Veränderungskompetenz ist nicht angeboren: Sie wächst, wenn man sich bewusst mit eigenen Ängsten und Widerständen auseinandersetzt, regelmäßig kleine neue Herausforderungen annimmt, die eigene Resilienz stärkt und Netzwerke nutzt.",
        ],
        "related": ["selbstwirksamkeit", "change-management", "resilienz"],
    },
    {
        "slug": "widerstand",
        "term": "Widerstand gegen Veränderung",
        "aliases": ["Veränderungswiderstand"],
        "category": "change",
        "short": "Natürliche Reaktion von Menschen auf Veränderungen, die sie als unsicher oder bedrohlich erleben.",
        "body": [
            "Typisch sind Sätze wie „Das haben wir schon immer so gemacht“ oder „Das haben wir doch alles schon versucht“. Ursachen sind häufig die Angst vor Misserfolg oder Kontrollverlust, mangelnde Information und fehlende Beteiligung.",
            "Widerstand ist kein bloßer Störfaktor, sondern ein wichtiges Signal: Wird er offen besprochen, lassen sich Bedenken lösungsorientiert bearbeiten.",
        ],
        "related": ["change-management", "veraenderungskompetenz", "probehandeln"],
    },
    {
        "slug": "lernende-organisation",
        "term": "Lernende Organisation",
        "aliases": ["Organizational Learning", "Lernkultur"],
        "category": "change",
        "short": "Organisation, die sich kontinuierlich an neue Herausforderungen anpasst, Wissen offen teilt und ihre Mitarbeitenden ermutigt, sich weiterzuentwickeln.",
        "body": [
            "Merkmale sind eine gemeinsame Vision, eine offene Kommunikations- und Fehlerkultur, Flexibilität, Wissensaustausch und das Verständnis, dass Lernen Teil des Arbeitsalltags ist. Lernende Organisationen sind anpassungsfähiger, innovativer und bieten ein Umfeld, in dem Mitarbeitende motiviert bleiben.",
            "Bekannt wurde das Konzept besonders durch den US-amerikanischen Organisationswissenschaftler Peter M. Senge. Als Beispiele gelten Unternehmen wie Netflix, Salesforce und Patagonia; in Deutschland setzt etwa das Bundesinstitut für Berufsbildung auf kontinuierliches Lernen.",
            "Auf dem Weg zur lernenden Organisation helfen:",
        ],
        "points": [
            ("Schulungen und Weiterbildungen", "Lernen wird Teil des Arbeitsalltags."),
            ("Offene Fehlerkultur", "Fehler gelten als Lernchance und werden nicht bestraft."),
            ("Wissenstransfer", "Teams teilen Wissen und Best Practices, etwa in regelmäßigen Austauschformaten."),
            ("Technologien", "E-Learning-Plattformen und digitale Tools erleichtern den Zugang zu Wissen und speichern es."),
        ],
        "related": ["fehlerkultur", "innovationskultur", "weiterbildung", "organisationsentwicklung"],
    },
    {
        "slug": "innovationskultur",
        "term": "Innovationskultur",
        "category": "change",
        "short": "Unternehmenskultur, in der neue Ideen entstehen, ausgesprochen, ausprobiert und umgesetzt werden können.",
        "body": [
            "Kennzeichen sind offene Kommunikation über Abteilungs- und Hierarchiegrenzen hinweg, Wissensaustausch, Freiräume zum Experimentieren und ein konstruktiver Umgang mit Fehlern. Hierarchische Entscheidungsstrukturen, Angst vor Misserfolg und schlechte Zusammenarbeit führen dagegen zum Innovationsstau.",
            "Innovationskultur lässt sich nicht verordnen: Kreativität entsteht eher in Entspannung und Sicherheit als unter Druck. Spielerische Formate können helfen, eingefahrene Denkmuster zu durchbrechen.",
        ],
        "related": ["lernende-organisation", "fehlerkultur", "playfulness", "psychologische-sicherheit"],
    },
    {
        "slug": "fehlerkultur",
        "term": "Fehlerkultur",
        "category": "change",
        "short": "Die Art und Weise, wie eine Organisation mit Fehlern umgeht.",
        "body": [
            "In einer offenen Fehlerkultur werden Fehler nicht bestraft, sondern als Lernmöglichkeit verstanden und offen besprochen. Das fördert psychologische Sicherheit, Innovation und kontinuierliche Verbesserung – und ist ein Kernmerkmal lernender Organisationen.",
        ],
        "related": ["lernende-organisation", "psychologische-sicherheit"],
    },
    {
        "slug": "unternehmensentwicklung",
        "term": "Unternehmensentwicklung",
        "aliases": ["Corporate Development", "Corp Dev"],
        "category": "change",
        "short": "Gezielte Weiterentwicklung eines Unternehmens, um es an Marktanforderungen und Wachstumsziele anzupassen.",
        "body": [
            "Unternehmenserfolg ist kein Zufall. Als Grundlagen gelten klare Ziele und eine Vision, eine flexible Organisationsstruktur, Innovationen und Technologien, eine starke Unternehmenskultur mit inspirierender Führung sowie eine gezielte Planung von Fachleuten, Kapital und Zeit.",
            "Die strategische Unternehmensentwicklung umfasst Marktanalyse und strategische Planung, Fusionen und Übernahmen, Digitalisierung und Innovationsförderung sowie die Anpassung der Organisationsstruktur. Ebenso wichtig sind Partnerschaften, datengestützte Entscheidungen und die Entwicklung der Mitarbeitenden und der Unternehmenskultur.",
            "Stillstand ist dabei ein Risiko: Ohne Weiterentwicklung drohen Verluste an Wettbewerbsfähigkeit, Innovationskraft und Fachkräften.",
        ],
        "related": ["organisationsentwicklung", "business-transformation", "personalentwicklung"],
    },
    {
        "slug": "organisationsentwicklung",
        "term": "Organisationsentwicklung",
        "category": "change",
        "short": "Langfristiger, geplanter Veränderungsprozess, der Strukturen, Prozesse und Kultur einer Organisation gemeinsam mit den Menschen weiterentwickelt.",
        "body": [
            "Im Unterschied zu einer rein strategischen Unternehmensentwicklung setzt Organisationsentwicklung auf die Beteiligung der Mitarbeitenden: Sie sollen den Wandel verstehen, mitgestalten und dabei selbst lernen. Typische Ansätze sind Workshops, Teamentwicklung, Coaching und Formate der Co-Creation – zunehmend auch spielbasierte Methoden.",
        ],
        "related": ["unternehmensentwicklung", "teamentwicklung", "serious-play"],
    },
    {
        "slug": "fachkraeftemangel",
        "term": "Fachkräftemangel",
        "aliases": ["Demografischer Wandel"],
        "category": "change",
        "short": "Situation, in der Unternehmen offene Stellen nicht oder nur schwer mit qualifiziertem Personal besetzen können.",
        "body": [
            "Ein wesentlicher Treiber ist der demografische Wandel: Weniger junge Menschen rücken nach, während erfahrene Beschäftigte in den Ruhestand gehen. Personalmangel erhöht den Termin- und Leistungsdruck für die verbleibenden Teams.",
            "Umso wichtiger werden Mitarbeiterbindung, Weiterbildung, Gesundheitsförderung und eine attraktive Arbeitgebermarke.",
        ],
        "related": ["mitarbeiterbindung", "employer-branding", "weiterbildung"],
    },
    {
        "slug": "hybride-arbeit",
        "term": "Hybride Arbeitsmodelle",
        "aliases": ["Hybride Arbeit", "Remote Work"],
        "category": "change",
        "short": "Arbeitsformen, bei denen Beschäftigte teils im Büro und teils mobil oder im Homeoffice arbeiten.",
        "body": [
            "Hybride Modelle bieten Flexibilität und erleichtern die Vereinbarkeit von Beruf und Privatleben. Sie stellen Teams aber auch vor neue Herausforderungen: Isolation im Homeoffice, unstrukturierte Meetings und weniger informeller Austausch können Teamkultur und Kommunikation schwächen.",
            "Klare Absprachen, regelmäßige Check-ins und bewusst gestaltete Begegnungen wirken dem entgegen.",
        ],
        "related": ["work-life-balance", "teamentwicklung", "innere-kuendigung"],
    },

    # ------------------------------------------------------------------
    # Fuehrung, Team & Organisation
    # ------------------------------------------------------------------
    {
        "slug": "unternehmenskultur",
        "term": "Unternehmenskultur",
        "category": "leadership",
        "short": "Gemeinsame Werte, Normen, Haltungen und Verhaltensweisen, die das Miteinander in einem Unternehmen prägen.",
        "body": [
            "Die Unternehmenskultur zeigt sich darin, wie kommuniziert, entschieden, geführt und mit Fehlern umgegangen wird. Eine gesundheitsorientierte, wertschätzende Kultur stärkt Bindung, Motivation und Veränderungsbereitschaft; eine Kultur, die von Druck, Misstrauen und fehlender Anerkennung geprägt ist, begünstigt dagegen Stress und innere Kündigung.",
        ],
        "related": ["fehlerkultur", "feedbackkultur", "arbeitsklima", "mitarbeiterbindung"],
    },
    {
        "slug": "arbeitsklima",
        "term": "Arbeitsklima",
        "aliases": ["Betriebsklima"],
        "category": "leadership",
        "short": "Die erlebte Atmosphäre der Zusammenarbeit in einem Team oder Unternehmen – wie Menschen miteinander umgehen, kommunizieren und sich gegenseitig wertschätzen.",
        "body": [
            "Ein positives Arbeitsklima ist entscheidend für Produktivität, Zufriedenheit und Gesundheit. Es lebt von Vertrauen, offener Kommunikation, Wertschätzung und einem konstruktiven Umgang mit Konflikten. Ein schlechtes Klima führt dagegen zu Missverständnissen, häufigeren Konflikten, weniger Innovation und höherer Fluktuation.",
            "Schon einfache Maßnahmen wirken: regelmäßige Teammeetings mit offenen Gesprächsrunden, gemeinsame (auch virtuelle) Pausen für informellen Austausch, Anerkennung für gute Leistungen und Teamaktivitäten, die Vertrauen aufbauen.",
        ],
        "related": ["teamgeist", "teambuilding", "unternehmenskultur", "emotionale-intelligenz"],
    },
    {
        "slug": "teamgeist",
        "term": "Teamgeist",
        "aliases": ["Wir-Gefühl", "Teamkultur", "Zusammenhalt"],
        "category": "leadership",
        "short": "Das Gefühl von Zusammengehörigkeit und gegenseitiger Unterstützung, das ein Team über die gemeinsame Aufgabe hinaus verbindet.",
        "body": [
            "Ein starkes Wir-Gefühl entsteht durch gemeinsame Erlebnisse, Vertrauen, offene Kommunikation und eine geteilte Teamkultur. Jedes Team entwickelt über die Zeit eine eigene Kultur – bewusst oder unbewusst. Eine gezielte Teamentwicklung sorgt dafür, dass gemeinsame Vision und Werte, klare Ziele und ein offenes Feedbackklima diese Kultur positiv prägen.",
        ],
        "related": ["teamentwicklung", "teambuilding", "arbeitsklima"],
    },
    {
        "slug": "positive-leadership",
        "term": "Positive Leadership",
        "category": "leadership",
        "short": "Führungsansatz auf Basis der Positiven Psychologie, der die Stärken der Mitarbeitenden in den Mittelpunkt stellt.",
        "body": [
            "Kennzeichen sind ein optimistischer Blick auf Herausforderungen, ein konstruktiver Umgang mit Fehlern, gezielte Stärkenförderung, Achtsamkeit, Vertrauen und Anerkennung. Positive Leadership soll ein Klima schaffen, in dem Motivation, Engagement, Eigenverantwortung und Resilienz wachsen.",
        ],
        "related": ["positive-psychologie", "fuehrungskraefte-coaching", "selbstwirksamkeit"],
    },
    {
        "slug": "mitarbeiterbindung",
        "term": "Mitarbeiterbindung",
        "aliases": ["Emotionale Mitarbeiterbindung", "Retention"],
        "category": "leadership",
        "short": "Alle Faktoren und Maßnahmen, die dazu beitragen, dass Mitarbeitende einem Unternehmen langfristig verbunden bleiben.",
        "body": [
            "Besonders wirksam ist die emotionale Bindung: Mitarbeitende, die sich mit ihrem Unternehmen identifizieren, sind motivierter, leistungsbereiter und fehlen seltener. Förderlich sind eine offene Feedbackkultur, Weiterbildungs- und Entwicklungsmöglichkeiten, Wertschätzung, sinnstiftende Aufgaben, eine gute Work-Life-Balance und eine gesundheitsorientierte Unternehmenskultur.",
            "Mangelnde Bindung zeigt sich in hoher Fluktuation, dem Verlust von Know-how und innerer Kündigung.",
        ],
        "related": ["fluktuation", "innere-kuendigung", "employer-branding"],
    },
    {
        "slug": "fluktuation",
        "term": "Fluktuation",
        "aliases": ["Mitarbeiterfluktuation"],
        "category": "leadership",
        "short": "Personalbewegung durch Kündigungen und Abgänge, meist als Quote im Verhältnis zur Belegschaft angegeben.",
        "body": [
            "Hohe Fluktuation verursacht Kosten für Recruiting und Einarbeitung, führt zum Verlust von Wissen über Prozesse und Kunden und belastet Teamklima und Motivation. Sie ist oft ein Warnsignal für mangelnde Mitarbeiterbindung, Überlastung oder ein angespanntes Arbeitsklima.",
        ],
        "related": ["mitarbeiterbindung", "fachkraeftemangel"],
    },
    {
        "slug": "employer-branding",
        "term": "Employer Branding",
        "aliases": ["Arbeitgebermarke"],
        "category": "leadership",
        "short": "Aufbau und Pflege einer attraktiven Arbeitgebermarke.",
        "body": [
            "Ein starkes Image als guter Arbeitgeber erleichtert es, neue Talente zu gewinnen und bestehende Mitarbeitende zu halten. Glaubwürdig ist Employer Branding dann, wenn es auf gelebter Kultur beruht – etwa auf Gesundheitsförderung, Entwicklungsmöglichkeiten und einem wertschätzenden Miteinander.",
        ],
        "related": ["mitarbeiterbindung", "fachkraeftemangel", "bgm"],
    },
    {
        "slug": "feedbackkultur",
        "term": "Feedbackkultur",
        "category": "leadership",
        "short": "Gelebte Praxis in einer Organisation, sich regelmäßig, offen und wertschätzend Rückmeldung zu geben.",
        "body": [
            "Eine gute Feedbackkultur macht Leistungen sichtbar, hilft, Missverständnisse früh zu klären, und unterstützt eine realistische Selbsteinschätzung. Sie ist eine wichtige Maßnahme zur Mitarbeiterbindung und eng mit psychologischer Sicherheit und Fehlerkultur verbunden.",
        ],
        "related": ["psychologische-sicherheit", "fehlerkultur", "mitarbeiterbindung"],
    },
    {
        "slug": "personalentwicklung",
        "term": "Personalentwicklung",
        "category": "leadership",
        "short": "Alle Maßnahmen, mit denen ein Unternehmen Kompetenzen, Potenziale und die berufliche Entwicklung seiner Mitarbeitenden systematisch fördert.",
        "body": [
            "Dazu zählen Entwicklungspläne, Weiterbildungen, Coaching, Mentoring und die Entwicklung von Führungskräften. Gute Personalentwicklung verbindet die Ziele des Unternehmens mit den individuellen Entwicklungswünschen der Beschäftigten – und ist damit ein wichtiger Hebel gegen Fachkräftemangel und Fluktuation.",
        ],
        "related": ["weiterbildung", "potenzialentfaltung", "spiele-coach"],
    },
    {
        "slug": "weiterbildung",
        "term": "Weiterbildung",
        "aliases": ["Fortbildung", "Schulung"],
        "category": "leadership",
        "short": "Lernformen, mit denen Beschäftigte ihre Kompetenzen erweitern – die Begriffe werden oft gleichbedeutend verwendet, meinen aber Unterschiedliches.",
        "points": [
            ("Weiterbildung", "allgemeine Lernprozesse, mit denen neue Fähigkeiten und Kompetenzen erworben werden, etwa im Projektmanagement."),
            ("Fortbildung", "spezifische Qualifikationen innerhalb des bestehenden Berufs, zur Spezialisierung oder für den Aufstieg in neue Positionen."),
            ("Schulung", "meist kürzere Maßnahmen, die konkrete Fähigkeiten vermitteln, zum Beispiel zu neuer Software oder zu Soft Skills wie Kommunikation."),
        ],
        "body_after": [
            "Regelmäßige Weiterbildung sichert Wettbewerbsfähigkeit, stärkt Arbeitszufriedenheit und Mitarbeiterbindung und hilft, Talente intern zu entwickeln. Mitarbeitende gewinnen neue Qualifikationen, bessere Karrierechancen und Sicherheit in einem sich wandelnden Arbeitsmarkt.",
            "Erfolgreich ist Weiterbildung mit einem strukturierten Konzept in fünf Schritten: Bedarfsanalyse (welche Fähigkeiten fehlen?), Zielsetzung, Auswahl passender Angebote, zeitliche und finanzielle Unterstützung der Teilnehmenden und schließlich die Erfolgsmessung im Arbeitsalltag. Nachhaltig wirkt sie vor allem dann, wenn Wissen erlebt und in den Alltag übertragen wird.",
        ],
        "related": ["personalentwicklung", "lernende-organisation", "spiele-coach"],
    },
    {
        "slug": "potenzialentfaltung",
        "term": "Potenzialentfaltung",
        "category": "leadership",
        "short": "Prozess, in dem Menschen, Teams und Organisationen ungenutzte Stärken, Talente und Ressourcen entdecken und gezielt weiterentwickeln.",
        "points": [
            ("Individuell", "Selbstzweifel und unbewusste Denkmuster erkennen, persönliche Stärken schärfen."),
            ("Im Team", "Synergien schaffen, eine gemeinsame Vision entwickeln, individuelle Stärken in Einklang bringen."),
            ("In der Organisation", "veraltete Denkweisen aufbrechen und eine nachhaltige Führungskultur etablieren."),
        ],
        "body_after": [
            "Bleiben Potenziale unentdeckt, führt das häufig zu Frustration und Demotivation. Coaching, Feedback und Selbstreflexion helfen, sie sichtbar zu machen.",
        ],
        "related": ["coaching", "hochstapler-syndrom", "personalentwicklung"],
    },
    {
        "slug": "coaching",
        "term": "Coaching",
        "aliases": ["Business Coaching", "Coachee"],
        "category": "leadership",
        "short": "Professionelle, prozessorientierte Beratung, die Menschen dabei unterstützt, ihre Potenziale zu entdecken und eigene Lösungen zu entwickeln.",
        "body": [
            "Ein Coach liefert keine fertigen Antworten, sondern begleitet den Coachee – also die Person, die sich coachen lässt – mit gezielten Fragen, psychologischem Wissen und praxisnahen Methoden. Ziel sind mehr Klarheit, Motivation und Handlungsfähigkeit, etwa bei Konflikten, Entscheidungen oder beruflichen Veränderungen.",
            "Business Coaching richtet sich speziell auf berufliche Fragestellungen und den Organisationskontext.",
            "Zum Methodenkoffer eines Coaches gehören gezielte Fragetechniken, systemische Analysen und kreative Visualisierungstechniken, ergänzt durch Ansätze aus Resilienztraining, Stressmanagement und achtsamer Führung. Gute Coaches gestalten den Prozess individuell statt nach starrem Programm.",
        ],
        "related": ["fuehrungskraefte-coaching", "potenzialentfaltung", "systemische-beratung"],
    },
    {
        "slug": "fuehrungskraefte-coaching",
        "term": "Führungskräfte-Coaching",
        "aliases": ["Executive Coaching"],
        "category": "leadership",
        "short": "Form des Business Coachings, die speziell auf die Anforderungen und Herausforderungen von Führungskräften ausgerichtet ist.",
        "body": [
            "Im Mittelpunkt stehen die Führungspersönlichkeit und der individuelle Führungsstil. Typische Themen sind Klarheit in der Führungsverantwortung, wertschätzende Kommunikation, Konfliktmanagement, Stressmanagement und strategische Zielsetzung.",
            "Coaching stärkt die Selbstwahrnehmung, verbessert die Kommunikationsfähigkeit und unterstützt fundierte Entscheidungen. Führungskräfte, die sich nicht weiterentwickeln, verharren dagegen leichter in gewohnten Denkmustern – mit Folgen für Innovation, Anpassungsfähigkeit und Mitarbeiterbindung.",
            "Führungskräfte-Coaching ist kein einmaliges Seminar, sondern ein Entwicklungsprozess – denn gute Führung beginnt bei der Selbstführung.",
        ],
        "related": ["coaching", "positive-leadership", "playful-leadership", "selbstreflexion"],
    },
    {
        "slug": "playful-leadership",
        "term": "Playful Leadership",
        "aliases": ["Spielerische Führung"],
        "category": "leadership",
        "short": "Führungsverständnis, das spielerische Formate nicht als Auflockerung am Rand, sondern als Kern ernsthafter Führungsarbeit begreift.",
        "body": [
            "Irene Preußner beschreibt die play2change-Methode als Playful Leadership: Im ergebnisoffenen Spielraum erleben Führungskräfte hierarchieübergreifend ihre eigene Innovationskraft und Selbstwirksamkeit. Weil Wissen und Appelle Verhalten selten verändern, setzt dieser Ansatz auf Erfahrung – notwendige Veränderungen lassen sich dann leichter und schneller umsetzen.",
            "Spielerische Führung bedeutet nicht, Arbeit in einen Wettbewerb um Punkte zu verwandeln. Sie schafft Räume, in denen Menschen sich trauen, Neues auszuprobieren, Fehler als Lernschritte zu sehen und gemeinsam Lösungen zu entwickeln.",
        ],
        "related": ["playfulness", "selbstwirksamkeit", "play2change", "positive-leadership"],
    },
    {
        "slug": "playful-work-design",
        "term": "Playful Work Design",
        "category": "leadership",
        "short": "Konzept aus der Arbeitspsychologie, das beschreibt, wie Beschäftigte ihre Arbeit von sich aus spielerischer gestalten.",
        "body": [
            "Untersucht wurde Playful Work Design vor allem von Yuri Scharp und Arnold B. Bakker. Gemeint ist, dass Menschen in ihre alltäglichen Aufgaben selbst Spaß und Herausforderung hineinbringen – etwa durch Fantasie, Humor oder selbst gesetzte Ziele –, ohne dass sich die Aufgabe selbst verändert. Studien bringen dies mit mehr Engagement und Kreativität in Verbindung.",
            "Der Ansatz passt zur Idee der Playfulness: Spielerisches entsteht von innen heraus und ist keine Belohnungsmechanik, die von außen übergestülpt wird.",
        ],
        "related": ["playfulness", "intrinsische-motivation", "flow"],
    },
    {
        "slug": "teamentwicklung",
        "term": "Teamentwicklung",
        "category": "leadership",
        "short": "Fortlaufender Prozess, in dem eine Gruppe von Menschen zu einem leistungsfähigen Team mit gutem Zusammenhalt wird.",
        "body": [
            "Teamentwicklung geht deutlich tiefer als einzelne Teambuilding-Events: Sie analysiert und verbessert Strukturen, bezieht die Stärken und Schwächen der Teammitglieder ein, klärt Kommunikation und Verantwortlichkeiten und zielt auf ein dauerhaft stabiles Teamgefüge.",
            "Typische Herausforderungen sind unterschiedliche Persönlichkeiten und Arbeitsstile, Kommunikationsbarrieren, unklare Verantwortlichkeiten und gruppendynamische Spannungen. Hilfreich sind regelmäßige Teamreflexion, eine klare Teamkultur und eine Führung, die eher moderiert als kontrolliert. Dazu kommen kontinuierliche Weiterbildung auch auf sozialer und methodischer Ebene – etwa Kommunikationstrainings, Workshops zur Konfliktlösung und Coaching für Führungskräfte – sowie Teambuilding mit echtem Bezug zum Arbeitsalltag.",
        ],
        "related": ["teambuilding", "teamgeist", "tuckman", "gruppendynamik"],
    },
    {
        "slug": "teambuilding",
        "term": "Teambuilding",
        "category": "leadership",
        "short": "Aktivitäten und Maßnahmen, die Vertrauen, Zusammenhalt und das Wir-Gefühl in einem Team stärken.",
        "body": [
            "Beispiele sind Kooperationsspiele, Escape-Room-Challenges, Outdoor-Erlebnisse, gemeinsame Kochkurse oder soziale Projekte. Teambuilding ist oft ein guter erster Schritt; nachhaltig wirkt es vor allem als Teil einer langfristigen Teamentwicklung mit echtem Bezug zum Arbeitsalltag.",
            "Gut gemachtes Teambuilding verbessert das Arbeitsklima: Die Kommunikation wird leichter, der Zusammenhalt wächst, Konflikte werden früher erkannt und konstruktiv gelöst, und die Motivation steigt.",
        ],
        "related": ["teamentwicklung", "teamgeist", "arbeitsklima", "spiele-am-arbeitsplatz"],
    },
    {
        "slug": "tuckman",
        "term": "Teamphasen nach Tuckman",
        "aliases": ["Forming, Storming, Norming, Performing", "Teamuhr"],
        "category": "leadership",
        "short": "Phasenmodell des Psychologen Bruce Tuckman, das beschreibt, welche Entwicklungsstufen Teams typischerweise durchlaufen.",
        "points": [
            ("Forming (Orientierung)", "Die Teammitglieder lernen sich kennen und bringen eigene Erwartungen, Stärken und Schwächen mit. Klare Strukturen und Ziele geben Halt."),
            ("Storming (Konflikt)", "Unterschiedliche Persönlichkeiten, Arbeitsweisen und Ziele treffen aufeinander. Offene Kommunikation und klare Verantwortung helfen durch diese Phase."),
            ("Norming (Regelung)", "Das Team einigt sich auf gemeinsame Regeln, das Zusammengehörigkeitsgefühl wächst."),
            ("Performing (Leistung)", "Das Team arbeitet eingespielt, effizient und mit starkem Wir-Gefühl."),
        ],
        "body_after": [
            "Später ergänzte Tuckman gemeinsam mit Mary Ann Jensen eine fünfte Phase, Adjourning, in der ein Team aufgelöst oder neu aufgestellt wird. Der zyklische Verlauf wird häufig als „Teamuhr“ dargestellt.",
        ],
        "related": ["teamentwicklung", "gruppendynamik"],
    },

    # ------------------------------------------------------------------
    # Spielbasierte Methoden
    # ------------------------------------------------------------------
    {
        "slug": "serious-games",
        "term": "Serious Games",
        "category": "play",
        "short": "Spiele, die ein Ziel über die reine Unterhaltung hinaus verfolgen: Wissen vermitteln, Fähigkeiten trainieren oder Verhaltensänderungen anstoßen.",
        "body": [
            "Der Unterschied zu herkömmlichen Spielen liegt im Zweck: Serious Games sind gezielt so gestaltet, dass die Spielenden etwas für ihr persönliches oder berufliches Leben mitnehmen.",
            "Eingesetzt werden sie in Bildung und Training, zur Problemlösung im Team und in der Persönlichkeitsentwicklung – etwa als Plan-, Rollen- oder Simulationsspiel.",
        ],
        "related": ["serious-play", "gamification", "mdad"],
    },
    {
        "slug": "serious-play",
        "term": "Serious Play",
        "category": "play",
        "short": "Methode, die spielerisches Handeln nutzt, um komplexe Zusammenhänge greifbar zu machen, neue Perspektiven zu eröffnen und kreative Lösungen zu fördern.",
        "body": [
            "Anders als klassische Besprechungen schafft Serious Play eine dynamische Umgebung, in der Teilnehmende experimentieren und sich aktiv einbringen. Einsatzfelder sind Team- und Organisationsentwicklung, Strategieentwicklung, Innovationsworkshops, Change Management und Mitarbeitertrainings.",
        ],
        "related": ["serious-games", "lego-serious-play", "probehandeln"],
    },
    {
        "slug": "lego-serious-play",
        "term": "LEGO® Serious Play®",
        "aliases": ["LSP"],
        "category": "play",
        "short": "Workshop-Methode, bei der Teilnehmende mit LEGO-Steinen Modelle bauen, um abstrakte Themen sichtbar und besprechbar zu machen.",
        "body": [
            "Entwickelt wurde der Ansatz Ende der 1990er-Jahre von LEGO in Zusammenarbeit mit Wissenschaftlern. Grundidee ist, dass Hände und Denken eng verknüpft sind: Jede Person baut ein eigenes Modell – etwa zu Werten, Zielen oder Konflikten –, erklärt es und bringt es in ein gemeinsames Bild ein.",
            "Der Schwerpunkt liegt auf Visualisierung, Innovation und strategischer Planung.",
        ],
        "related": ["serious-play", "serious-games"],
    },
    {
        "slug": "gamification",
        "term": "Gamification",
        "category": "play",
        "short": "Einsatz spieltypischer Elemente wie Punkte, Badges und Ranglisten in Zusammenhängen, die selbst kein Spiel sind – mit dem Ziel, gewünschtes Verhalten zu verstärken.",
        "body": [
            "Gamification setzt vor allem auf extrinsische Motivation: Menschen handeln wegen des Anreizes, nicht wegen der Tätigkeit selbst. Belohnung und sichtbarer Fortschritt dienen als Verstärker, damit ein Verhalten wiederholt wird. Die Leitfrage lautet sinngemäß: Wie bringen wir Menschen dazu, das zu tun, was wir wollen?",
            "Bei klar umrissenen, wiederholbaren Aufgaben funktioniert das gut. Bei Kreativität, kritischem Denken und Innovation stößt Gamification nach Irene Preußner jedoch an Grenzen – diese Fähigkeiten lassen sich kaum durch Belohnungssysteme erzwingen. Wettbewerb um Punkte und Rankings kann echte Zusammenarbeit sogar verdrängen.",
            "Ebenso wenig macht eine Ausstattung mit Tischkicker oder Bällebad eine Arbeitskultur spielerisch, solange der Arbeitsalltag selbst keinen Spielraum lässt. Den Gegenentwurf beschreibt der Begriff Playfulness.",
        ],
        "related": ["playfulness", "intrinsische-motivation", "serious-games"],
    },
    {
        "slug": "playfulness",
        "term": "Playfulness",
        "aliases": ["Spielerische Haltung", "Playfulness vs. Gamification"],
        "category": "play",
        "short": "Spielerische Grundhaltung und Kultur, die auf intrinsische Motivation setzt: Kreativität, Neugier, soziale Verbundenheit, Selbstbestimmung, Selbstwirksamkeit und Entdeckerfreude.",
        "body": [
            "Playfulness und Gamification greifen beide die Idee des Spiels auf, beruhen aber auf grundlegend verschiedenen Vorstellungen von Motivation. Irene Preußner, Entwicklerin von MENSCH DENK AN DICH®, macht diese Unterscheidung zum Kern ihrer Arbeit: Spielen ist für sie kein Belohnungssystem, sondern ein Erfahrungsraum.",
        ],
        "points": [
            ("Motivation", "Gamification wirkt extrinsisch über Anreize von außen; Playfulness wirkt intrinsisch – Menschen handeln, weil das Tun selbst Freude macht und Sinn ergibt."),
            ("Leitfrage", "Gamification fragt, wie man Menschen dazu bringt, das Gewünschte zu tun; Playfulness fragt, wie ein Raum entsteht, in dem Menschen ihre Potenziale selbst entdecken und entfalten."),
            ("Wirkprinzip", "Gamification verstärkt mit Punkten, Badges und Fortschrittsanzeigen; Playfulness schafft Freiräume – die Energie entsteht im System selbst, aus den Menschen, die darin handeln."),
            ("Fehler", "Bei Playfulness sind Fehler Teil des Lernens, nicht Scheitern."),
            ("Zusammenarbeit", "Sie entsteht aus echtem Interesse am gemeinsamen Gestalten statt aus dem Wettbewerb um Punkte oder Rankings."),
            ("Einsatzfeld", "Gamification eignet sich für klar umrissene Aufgaben; Playfulness für komplexe Herausforderungen, die Kreativität und Innovation verlangen."),
        ],
        "body_after": [
            "In einer Arbeitswelt voller Komplexität, Unsicherheit und schnellem Wandel gewinnt Playfulness deshalb an Bedeutung. Voraussetzung ist ein geschützter Rahmen: Kreativität entsteht in Entspannung und Sicherheit, während Stress zu Tunnelblick führt. Lachen schafft nach Preußner die „Kaffeepausenatmosphäre“, in der gute Ideen entstehen – und niemand wird zum Mitspielen gezwungen.",
        ],
        "related": ["gamification", "intrinsische-motivation", "playful-leadership", "probehandeln"],
    },
    {
        "slug": "planspiel",
        "term": "Planspiel",
        "aliases": ["Simulationsspiel"],
        "category": "play",
        "short": "Simulationsspiel, in dem Teilnehmende Rollen übernehmen und in einem realitätsnahen Szenario Entscheidungen treffen.",
        "body": [
            "Planspiele werden in Erwachsenenbildung, Training und Unternehmen eingesetzt, um etwa Entscheidungsfindung, Konfliktlösung oder wirtschaftliche Zusammenhänge erfahrbar zu machen. Die Teilnehmenden lernen ganz nebenbei Strategien, die sie im echten Leben anwenden können.",
        ],
        "related": ["serious-games", "probehandeln"],
    },
    {
        "slug": "probehandeln",
        "term": "Probehandeln",
        "category": "play",
        "short": "Ausprobieren neuer Denk- und Handlungsweisen in einem geschützten Rahmen, ohne Angst vor realen Konsequenzen.",
        "body": [
            "Im Spiel lassen sich Lösungen entwickeln, simulieren und testen, bevor sie im Arbeitsalltag zum Einsatz kommen. Weil zunächst keine echten Konsequenzen drohen, können Teilnehmende auch Schwächen zeigen und ohne ständige Selbstzensur ausprobieren. Das senkt Hemmschwellen, fördert Kreativität und stärkt die Selbstwirksamkeit.",
            "Probehandeln ist ein Grundgedanke von MENSCH DENK AN DICH®: Wer eine Aktionskarte zieht, nimmt eine Aufgabe aus dem Alltag gedanklich vorweg. Spielpausen und Versuch und Irrtum erzeugen Lernschleifen, die Irene Preußner mit agilen Methoden wie Scrum oder Design Thinking vergleicht.",
        ],
        "related": ["selbstwirksamkeit", "mdad", "planspiel"],
    },
    {
        "slug": "spiele-am-arbeitsplatz",
        "term": "Spiele am Arbeitsplatz",
        "aliases": ["Bürospiele", "Teambuildingspiele"],
        "category": "play",
        "short": "Spielerische Formate im Büro oder Homeoffice, die Teamgeist, Kommunikation und Kreativität fördern.",
        "body": [
            "Spiele schaffen eine informelle Atmosphäre, in der sich Kolleginnen und Kollegen auf Augenhöhe begegnen. Sie bauen Barrieren ab, stärken Vertrauen und das Wir-Gefühl, bringen auch interkulturelle Teams zusammen und helfen, gewohnte Denkmuster zu durchbrechen. Zudem lockern sie monotone Abläufe auf und senken den Stresspegel.",
            "Eine Viertelstunde am Tischkicker verändert einen durchgetakteten Arbeitstag allerdings wenig. Nachhaltig wirken spielerische Formate, wenn sie echten Spielraum im Arbeitsalltag schaffen – nicht als Dekoration, sondern als Haltung.",
        ],
        "related": ["playfulness", "teambuilding", "serious-games", "resilienz-spiele"],
    },
    {
        "slug": "resilienz-spiele",
        "term": "Resilienzspiele",
        "category": "play",
        "short": "Spiele, die gezielt die Widerstandskraft von Mitarbeitenden und Teams fördern.",
        "body": [
            "Mit Spielkarten und einem interaktiven Spielfeld werden berufliche Situationen aufgegriffen, in denen Teilnehmende Entscheidungen treffen, mit Belastungen umgehen und Krisen bewältigen. So werden Resilienzfaktoren erlebbar und individuelle Unterschiede im Umgang mit Stress bewusst.",
        ],
        "related": ["resilienz", "resilienzfoerderung", "mdad", "resilienzfaktoren"],
    },
    {
        "slug": "play2change",
        "term": "play2change-Methode",
        "aliases": ["PLAY, EARN, TRANSFER"],
        "category": "play",
        "short": "Methode von MENSCH DENK AN DICH®, die Veränderungsprozesse in drei Phasen strukturiert – vom Spiel bis zur Umsetzung im Alltag.",
        "points": [
            ("PLAY", "gemeinsame Ideenentwicklung: Gezielte Fragen bringen Menschen ins Gespräch, Hierarchien treten zurück, Herausforderungen können ohne Druck angesprochen werden."),
            ("EARN", "Erkenntnisse festigen: Die Teilnehmenden reflektieren eigene Stärken und Ressourcen und entwickeln Lösungsansätze."),
            ("TRANSFER", "Umsetzung: Ideen werden in konkrete Maßnahmen und Ziele für den Arbeitsalltag übersetzt."),
        ],
        "body_after": [
            "Der Transfer sorgt dafür, dass die im Spiel erarbeiteten Lösungen nicht im Workshop bleiben, sondern langfristig wirken. Dafür ist das Spiel in einen übergeordneten Veränderungsprozess eingebettet: Interventionsfragen, Vereinbarungen, Workshops oder Prozessbegleitung verankern das neue Verhalten.",
            "play2change versteht Spielen ausdrücklich nicht als Belohnungssystem, sondern als Erfahrungsraum – im Sinne von Playfulness statt Gamification.",
        ],
        "related": ["mdad", "playfulness", "probehandeln", "change-management"],
    },
    {
        "slug": "mdad",
        "term": "MENSCH DENK AN DICH®",
        "category": "play",
        "short": "Wissenschaftlich evaluiertes Serious Game für Resilienz, Gesundheitsförderung und Organisationsentwicklung, entwickelt von der Psychologin Dr. Irene Preußner.",
        "body": [
            "Die Idee zu dem Brettspiel entstand 2016 aus der Erfahrung, wie schwer es vielen Menschen fällt, ihre Ressourcen im Arbeitsalltag zur Stressbewältigung zu nutzen. Gespielt wird mit Spielbrett, Figuren und Aktionskarten, meist rund 90 Minuten mit bis zu zwölf Personen in kleinen Teams. Das Motto lautet, sich selbst und andere zu stärken.",
            "MENSCH DENK AN DICH® ist bewusst kein Wettkampf und kein Belohnungssystem, sondern ein Erfahrungsraum im Sinne von Playfulness. Anders als in klassischen Planspielen gibt es kein künstliches Szenario: Die Spielenden bringen echte Situationen aus ihrem Arbeitsalltag ein. Die Regeln dürfen gemeinsam angepasst werden, wenn eine Aufgabe zu stressig wirkt. Das Spiel verbindet Ansätze aus der Positiven Psychologie und der Systemischen Beratung.",
            "Es gibt Spielvarianten für das Handeln als Führungskraft und für die eigene Resilienz. Eingesetzt wird das Spiel branchen- und hierarchieübergreifend in Trainings, Teamentwicklung, Führungskräfte-Coaching und Veränderungsprozessen. Die Methode wurde 2024 mit dem Europäischen Trainingspreis in Gold und 2026 mit dem ersten Platz beim NewWork Business Award in der Kategorie Leadership Training ausgezeichnet.",
        ],
        "related": ["playfulness", "play2change", "spiele-coach", "probehandeln"],
    },
    {
        "slug": "spiele-coach",
        "term": "Spiele-Coach",
        "aliases": ["Spielleiterin", "Spielleiter"],
        "category": "play",
        "short": "Für MENSCH DENK AN DICH® qualifizierte Spielleitung, die das Spiel in Teams und Organisationen professionell anleitet.",
        "body": [
            "Die Qualifizierung erfolgt in einem zweitägigen, intensiven Training mit Selbstlernphasen sowie Erfahrungs- und Wissensinput. Unternehmen können auch interne Coaches, Beratende, Trainerinnen und Trainer oder Führungskräfte zu Spiele-Coaches ausbilden lassen und so spielerische Methoden dauerhaft in der eigenen Personal- und Organisationsentwicklung verankern.",
        ],
        "related": ["mdad", "personalentwicklung", "weiterbildung"],
    },
]


# "Haeufig gesucht"-Links oben auf der Lexikonseite (Slug, Anzeigetext).
LEXICON_QUICK_TERMS = [
    ("playfulness", "Playfulness"),
    ("gamification", "Gamification"),
    ("resilienz", "Resilienz"),
    ("bgm", "BGM"),
    ("change-management", "Change Management"),
]


def _sort_key(text):
    """Alphabetische Sortierung ohne Umlaut-Sonderfaelle (Ä wie A usw.)."""
    text = text.replace("ß", "ss")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.casefold()


def _letter(term):
    first = _sort_key(term)[:1].upper()
    return first if first.isalpha() else "#"


def build_lexicon():
    """Begriffe nach Anfangsbuchstaben gruppieren und Querverweise pruefen.

    Gibt (groups, terms_by_slug) zurueck; groups ist eine sortierte Liste von
    (Buchstabe, [Eintraege]). Fehlerhafte Slugs in "related" fallen auf
    (statt einen 500er auszuloesen) einfach heraus.
    """
    terms_by_slug = {t["slug"]: t for t in LEXICON_TERMS}
    groups = {}
    for term in sorted(LEXICON_TERMS, key=lambda t: _sort_key(t["term"])):
        entry = dict(term)
        entry["category_label"] = LEXICON_CATEGORY_LABELS.get(term["category"], "")
        entry["related"] = [
            terms_by_slug[slug] for slug in term.get("related", []) if slug in terms_by_slug
        ]
        groups.setdefault(_letter(term["term"]), []).append(entry)
    return sorted(groups.items()), terms_by_slug
