# Lexikon

<!--
Inhalte der Lexikonseite (/lexicon). Diese Datei wird von lexicon_data.py
eingelesen; Aenderungen sind nach dem Speichern sofort auf der Seite sichtbar.

Aufbau:
- "# Kategorien": eine Zeile je Thema, "- schluessel: Anzeigename".
- "# Häufig gesucht": Links unter dem Suchfeld, "- slug: Anzeigetext".
- "# Begriffe": je Begriff ein Abschnitt "## Begriff", darunter
  - eine Liste mit festen Feldern:
      - Slug: Anker auf der Seite (/lexicon#slug), nur a-z, 0-9 und "-"
      - Kategorie: Anzeigename oder Schluessel aus "# Kategorien"
      - Auch: weitere Bezeichnungen, getrennt durch Semikolon (optional)
      - Kurz: Kurzdefinition (ein Satz, wird hervorgehoben)
      - Siehe auch: Slugs verwandter Eintraege, getrennt durch Semikolon (optional)
  - danach Absaetze (durch Leerzeilen getrennt),
  - optional eine Aufzaehlung "- **Stichwort:** Text",
  - optional weitere Absaetze nach der Aufzaehlung.
Die Reihenfolge der Begriffe in dieser Datei spielt keine Rolle; die Seite
sortiert alphabetisch. Pruefen: "python lexicon_data.py".
-->

# Kategorien

- health: Gesundheit & BGM
- psychology: Psychologie in der Arbeitswelt
- change: Transformation & Wandel
- leadership: Führung, Team & Organisation
- play: Spielbasierte Methoden

# Häufig gesucht

- playfulness: Playfulness
- gamification: Gamification
- resilienz: Resilienz
- bgm: BGM
- change-management: Change Management

# Begriffe

## Gesundheit

- Slug: gesundheit
- Kategorie: Gesundheit & BGM
- Kurz: Mehr als die Abwesenheit von Krankheit: ein Zusammenspiel aus körperlichem, psychischem und sozialem Wohlbefinden.
- Siehe auch: physische-gesundheit; mentale-gesundheit; gesundheitsfoerderung; bgm

Physische und psychische Gesundheit sind eng miteinander verknüpft. Chronischer Stress kann sich etwa in Rückenschmerzen oder Herz-Kreislauf-Beschwerden zeigen, während körperliche Erkrankungen häufig das seelische Wohl beeinträchtigen. Gesundheit wird deshalb als Balance verschiedener Bereiche verstanden.

Im Arbeitskontext ist Gesundheit ein oft unterschätzter Erfolgsfaktor: Ein gesunder Arbeitsplatz fördert das Wohlbefinden der Mitarbeitenden ebenso wie Produktivität, Motivation und Innovationskraft eines Unternehmens.

## Physische Gesundheit

- Slug: physische-gesundheit
- Kategorie: Gesundheit & BGM
- Auch: Körperliche Gesundheit
- Kurz: Die Funktionsfähigkeit des Körpers, ein stabiles Immunsystem und allgemeine körperliche Fitness – die Grundlage für ein aktives Leben.
- Siehe auch: gesundheit; ergonomie; mentale-gesundheit

Ausgewogene Ernährung, regelmäßige Bewegung und ausreichend Schlaf sind die wichtigsten Stellschrauben; Vorsorgeuntersuchungen und Impfungen ergänzen sie präventiv.

Am Arbeitsplatz wird die physische Gesundheit vor allem durch ergonomische Arbeitsplätze, Bewegung und Pausen unterstützt. Langes Sitzen, monotone Bewegungsabläufe und fehlende Pausen führen dagegen häufig zu Rückenschmerzen, Müdigkeit und langfristigen Erkrankungen. Körperliche und psychische Gesundheit beeinflussen sich dabei gegenseitig.

## Betriebliches Gesundheitsmanagement (BGM)

- Slug: bgm
- Kategorie: Gesundheit & BGM
- Auch: BGM; Gesundheitsmanagement
- Kurz: Strategische Planung, Steuerung und Verankerung aller Maßnahmen, die Gesundheit und Leistungsfähigkeit der Menschen im Betrieb erhalten und fördern.
- Siehe auch: bgf; gefaehrdungsbeurteilung; bem; praevention

Anders als einzelne Gesundheitstage oder sporadische Workshops setzt BGM auf eine dauerhafte Integration in die Betriebsstruktur: klare Ziele, Prävention, eine gesundheitsgerechte Gestaltung von Arbeitsprozessen und die aktive Beteiligung der Beschäftigten.

Typische Handlungsfelder sind Arbeitsplatzgestaltung, gesundheitsfördernde Angebote, psychische Gesundheit, Work-Life-Balance sowie Kommunikation und Führung. Führungskräfte spielen eine Schlüsselrolle, weil sie das Arbeitsklima prägen und als Vorbild wirken.

Gut umgesetzt kann BGM Fehlzeiten senken, die Zufriedenheit der Mitarbeitenden erhöhen und die Attraktivität als Arbeitgeber stärken.

## Betriebliche Gesundheitsförderung (BGF)

- Slug: bgf
- Kategorie: Gesundheit & BGM
- Auch: BGF
- Kurz: Alle konkreten Maßnahmen im Betrieb, die die physische und psychische Gesundheit der Beschäftigten erhalten, fördern und verbessern.
- Siehe auch: bgm; gesundheitsfoerderung; ergonomie

Zur BGF gehören etwa ergonomische Arbeitsplätze, Bewegungsprogramme und bewegte Pausen, Angebote zu Stressbewältigung und Achtsamkeit, Coachings, ein gesundes Verpflegungsangebot sowie Vorsorge- und Check-up-Aktionen.

BGF ist ein Baustein des betrieblichen Gesundheitsmanagements: Während das BGM den strategischen Rahmen setzt, beschreibt die BGF die Maßnahmen, die im Arbeitsalltag ankommen. Ein wertschätzendes Betriebsklima gilt dabei selbst als wirksamer Gesundheitsfaktor.

## Gesundheitsförderung

- Slug: gesundheitsfoerderung
- Kategorie: Gesundheit & BGM
- Kurz: Ganzheitlicher Ansatz, der Bedingungen für ein gesundes Leben schafft, statt nur Krankheiten zu vermeiden.
- Siehe auch: bgf; praevention; gesundheit

Die zwei zentralen Säulen sind die physische Gesundheit – Bewegung, ausgewogene Ernährung, ausreichend Schlaf – und die psychische Gesundheit, etwa durch Stressbewältigung, Entspannungstechniken, ein stabiles soziales Netzwerk und einen offenen Umgang mit mentalen Herausforderungen. Ergänzt wird beides durch Prävention.

In Zeiten zunehmender Belastungen durch Stress, Bewegungsmangel oder ungesunde Lebensgewohnheiten gewinnt Gesundheitsförderung im privaten wie im beruflichen Umfeld an Bedeutung.

## Prävention

- Slug: praevention
- Kategorie: Gesundheit & BGM
- Kurz: Vorbeugende Maßnahmen, die gesundheitliche Risiken frühzeitig erkennen und Erkrankungen verhindern sollen.
- Siehe auch: bgf; gefaehrdungsbeurteilung; fehlzeiten

Dazu zählen Vorsorgeuntersuchungen, Impfaktionen und Gesundheits-Check-ups ebenso wie die vorbeugende Gestaltung der Arbeitsbedingungen – etwa durch Ergonomie, klare Aufgaben und eine realistische Arbeitslast. Präventive Maßnahmen wirken langfristig und können krankheitsbedingte Fehlzeiten reduzieren.

## Gefährdungsbeurteilung

- Slug: gefaehrdungsbeurteilung
- Kategorie: Gesundheit & BGM
- Kurz: Systematische Analyse, welche Belastungen und Gefährdungen an einem Arbeitsplatz bestehen und welche Schutzmaßnahmen nötig sind.
- Siehe auch: bgm; praevention; stressoren

In Deutschland ist sie für Arbeitgeber nach dem Arbeitsschutzgesetz verpflichtend und umfasst ausdrücklich auch psychische Belastungen – etwa durch Zeitdruck, unklare Aufgaben oder Konflikte. Ihre Ergebnisse sind häufig der Ausgangspunkt für Maßnahmen des betrieblichen Gesundheitsmanagements.

## Betriebliches Eingliederungsmanagement (BEM)

- Slug: bem
- Kategorie: Gesundheit & BGM
- Auch: BEM
- Kurz: Verfahren, mit dem Arbeitgeber Beschäftigte nach längerer Arbeitsunfähigkeit bei der Rückkehr unterstützen und erneuten Ausfällen vorbeugen.
- Siehe auch: bgm; fehlzeiten

Arbeitgeber müssen ein BEM anbieten, wenn Beschäftigte innerhalb von zwölf Monaten länger als sechs Wochen ununterbrochen oder wiederholt arbeitsunfähig waren (§ 167 Abs. 2 SGB IX). Die Teilnahme ist für die Beschäftigten freiwillig.

Steigende BEM-Fallzahlen können ein Hinweis darauf sein, dass Belastungen im Unternehmen zunehmen – und dass präventive Ansätze des Gesundheitsmanagements gestärkt werden sollten.

## Fehlzeiten und Krankenstand

- Slug: fehlzeiten
- Kategorie: Gesundheit & BGM
- Auch: Krankenstand
- Kurz: Krankheitsbedingte Abwesenheiten von Beschäftigten; der Krankenstand gibt ihren Anteil an der Sollarbeitszeit an.
- Siehe auch: praevention; praesentismus; bgm; bem

Häufige Ursachen sind Atemwegs- und Muskel-Skelett-Erkrankungen sowie psychische Erkrankungen. Hohe Fehlzeiten belasten nicht nur die Betroffenen, sondern auch die Teams, die ihre Aufgaben übernehmen müssen.

Präventive Gesundheitsförderung, ein gutes Arbeitsklima und Resilienzförderung können krankheitsbedingte Ausfälle senken.

## Präsentismus

- Slug: praesentismus
- Kategorie: Gesundheit & BGM
- Kurz: Arbeiten trotz Krankheit – Beschäftigte sind anwesend, aber gesundheitlich eingeschränkt und weniger leistungsfähig.
- Siehe auch: fehlzeiten; bgf; unternehmenskultur

Präsentismus entsteht häufig aus Pflichtgefühl, Angst um den Arbeitsplatz, hoher Arbeitslast oder der Sorge, Kolleginnen und Kollegen im Stich zu lassen. Er kann Erkrankungen verschleppen, Fehler begünstigen und Ansteckungen im Team fördern.

Weil Präsentismus in keiner Fehlzeitenstatistik auftaucht, wird er leicht übersehen – dabei kann er die Produktivität eines Unternehmens stärker beeinträchtigen als krankheitsbedingte Abwesenheit. Eine Kultur, in der Erholung erlaubt ist, und ein wirksames Gesundheitsmanagement wirken dem entgegen.

## Ergonomische Arbeitsplatzgestaltung

- Slug: ergonomie
- Kategorie: Gesundheit & BGM
- Auch: Ergonomie; Arbeitsplatzgestaltung
- Kurz: Gestaltung von Arbeitsplätzen und Arbeitsabläufen, die körperliche Belastungen verringert und Langzeitschäden vorbeugt.
- Siehe auch: bgf; praevention

Beispiele sind höhenverstellbare Schreibtische, gut angepasste Stühle, ein optimal eingerichteter Bildschirmarbeitsplatz, natürliche Beleuchtung und Lärmschutz. Langes Sitzen, monotone Bewegungsabläufe und fehlende Pausen gelten als typische Risikofaktoren.

## Work-Life-Balance

- Slug: work-life-balance
- Kategorie: Gesundheit & BGM
- Kurz: Ausgewogenes Verhältnis zwischen beruflichen Anforderungen und privatem Leben.
- Siehe auch: mentale-gesundheit; hybride-arbeit; mitarbeiterbindung

Flexible Arbeitszeiten, Homeoffice-Optionen, Angebote zur Kinderbetreuung und die Möglichkeit, wirklich abzuschalten, erleichtern die Vereinbarkeit von Beruf und Privatleben. Eine gesunde Balance beugt Erschöpfung vor, stärkt die mentale Gesundheit und ist für viele Beschäftigte ein wichtiges Kriterium bei der Wahl ihres Arbeitgebers.

## Mentale Gesundheit

- Slug: mentale-gesundheit
- Kategorie: Gesundheit & BGM
- Auch: Mental Health; Psychische Gesundheit
- Kurz: Emotionales, psychisches und soziales Gleichgewicht – und die Fähigkeit, mit den Höhen und Tiefen des Lebens umzugehen.
- Siehe auch: resilienz; psychologische-sicherheit; stress; burnout

Mentale Gesundheit ist mehr als die Abwesenheit psychischer Erkrankungen. Dazu gehört, sich selbst zu verstehen, Emotionen zu regulieren und gesunde Entscheidungen zu treffen. Sie ist ein dynamischer Zustand, der von persönlichen Erfahrungen, sozialen Beziehungen und äußeren Faktoren wie Stress oder Veränderungen beeinflusst wird.

Im Arbeitsalltag wirken vor allem Arbeitsbelastung, Arbeitsklima und Beziehungen, die Sinnhaftigkeit der Tätigkeit und die Work-Life-Balance auf die mentale Gesundheit. Unternehmen, die offen mit dem Thema umgehen und Unterstützung anbieten, schaffen Vertrauen – und profitieren von engagierten, leistungsfähigen Teams.

## Burnout

- Slug: burnout
- Kategorie: Gesundheit & BGM
- Auch: Burn-out
- Kurz: Zustand tiefer emotionaler, körperlicher und geistiger Erschöpfung, der mit anhaltender Überlastung im Beruf in Verbindung gebracht wird.
- Siehe auch: stress; mentale-gesundheit; stressmanagement

Die Weltgesundheitsorganisation beschreibt Burn-out in der ICD-11 als berufsbezogenes Phänomen, das aus chronischem Stress am Arbeitsplatz entsteht, der nicht erfolgreich bewältigt wurde. Als Risikofaktoren gelten unter anderem hoher Leistungsdruck, unrealistische Deadlines, ständige Erreichbarkeit, fehlende Anerkennung und ein angespanntes Betriebsklima.

Wer Anzeichen bei sich bemerkt, sollte ärztliche oder psychotherapeutische Unterstützung suchen. Unternehmen können vor allem vorbeugend wirken – durch gesunde Arbeitsbedingungen, eine realistische Arbeitsplanung und eine Kultur, in der Belastungen offen angesprochen werden dürfen.

## Stress

- Slug: stress
- Kategorie: Gesundheit & BGM
- Kurz: Körperliche und psychische Reaktion auf Anforderungen, die als belastend wahrgenommen werden.
- Siehe auch: stressoren; stressmanagement; resilienz

In Situationen, die als bedrohlich empfunden werden, aktiviert der Körper das sympathische Nervensystem und schüttet Stresshormone wie Adrenalin und Cortisol aus – die sogenannte Kampf-oder-Flucht-Reaktion. Herzschlag und Atmung beschleunigen sich, die Muskeln spannen sich an.

Kurzfristig ist diese Reaktion hilfreich. Hält die Belastung jedoch an, kann chronischer Stress zu Erschöpfung, Schlaf- und Konzentrationsproblemen sowie zu Herz-Kreislauf-Erkrankungen oder psychischen Störungen beitragen.

## Stressoren

- Slug: stressoren
- Kategorie: Gesundheit & BGM
- Auch: Stressfaktoren
- Kurz: Auslöser von Stress – von außen kommend oder in der Person selbst liegend.
- Siehe auch: stress; stressmanagement

Äußere Stressoren im Arbeitsalltag sind etwa Zeitdruck, Überforderung durch Aufgabenfülle oder Komplexität, mangelnde Anerkennung, Konflikte und fehlende oder unklare Kommunikation. Innere Stressoren sind zum Beispiel Perfektionismus oder die Angst vor Fehlern. Wirksame Stressbewältigung setzt an beiden Bereichen an.

## Stressmanagement

- Slug: stressmanagement
- Kategorie: Gesundheit & BGM
- Auch: Stressbewältigung
- Kurz: Strategien und Techniken, um Stressauslöser zu verringern und besser mit Belastungen umzugehen.
- Siehe auch: stress; entspannungstechniken; achtsamkeit; resilienzfoerderung

Ziel ist nicht, Stress vollständig zu vermeiden, sondern die Balance zwischen den Anforderungen des Alltags und den individuellen Ressourcen herzustellen. Zentrale Ansätze sind das Erkennen von Stressfaktoren, Entspannungstechniken wie Progressive Muskelentspannung, Meditation oder Atemübungen sowie ein gesunder Lebensstil mit Bewegung, Ernährung und ausreichend Schlaf.

Stress entsteht häufig in den Strukturen, nicht nur beim Einzelnen. Arbeitgeber können deshalb viel beitragen:

- **Klare Strukturen:** eindeutige Verantwortlichkeiten und transparente Kommunikation nehmen Unsicherheit.
- **Flexibilität:** Homeoffice und flexible Arbeitszeiten erleichtern eine gute Work-Life-Balance.
- **Gesundheitsförderung:** Workshops zu Stressmanagement, Bewegungsangebote und ergonomische Arbeitsplätze wirken präventiv.
- **Wertschätzung:** regelmäßiges Feedback, Lob und die Förderung individueller Stärken stärken das Selbstvertrauen.

Stress ist auch ein gesellschaftliches Thema: Stressbedingte Ausfälle verursachen erhebliche Kosten, während ein bewusster Umgang mit Stress die Lebensqualität deutlich verbessern kann.

## Entspannungstechniken

- Slug: entspannungstechniken
- Kategorie: Gesundheit & BGM
- Auch: Progressive Muskelentspannung; Autogenes Training
- Kurz: Übungen, die Körper und Geist gezielt beruhigen und so helfen, Stress abzubauen.
- Siehe auch: stressmanagement; achtsamkeit; bgf

Bekannte Verfahren sind die Progressive Muskelentspannung nach Edmund Jacobson, bei der Muskelgruppen nacheinander an- und wieder entspannt werden, und das Autogene Training nach Johannes Heinrich Schultz, eine Form der konzentrativen Selbstentspannung. Hinzu kommen Meditation, Atemübungen und Yoga.

Regelmäßig geübt, wirken Entspannungstechniken nachweislich positiv auf die Stressbewältigung. Im Betrieb lassen sie sich als Kurse, kurze Übungseinheiten oder bewusste Pausen in den Alltag integrieren.

## Resilienz

- Slug: resilienz
- Kategorie: Psychologie in der Arbeitswelt
- Auch: psychische Widerstandskraft
- Kurz: Psychische Widerstandskraft: die Fähigkeit, Stress, Rückschläge und Krisen zu bewältigen und gestärkt daraus hervorzugehen.
- Siehe auch: resilienz-spiele; resilienzfaktoren; resilienzfoerderung; resilienztraining

Der Begriff geht auf das lateinische „resilire“ zurück – „zurückspringen“ oder „abprallen“. Resiliente Menschen lassen sich nicht so leicht aus der Bahn werfen, bleiben auch in schwierigen Zeiten handlungsfähig und wachsen an Herausforderungen.

Die Resilienzforschung – unter anderem mit den Arbeiten von Emmy Werner und Ann Masten – zeigt: Resilienz ist keine angeborene Eigenschaft, sondern lässt sich wie ein Muskel trainieren. Sie ist nicht nur für Einzelne bedeutsam, sondern auch für Teams und ganze Organisationen, die sich in einer schnell wandelnden Arbeitswelt immer wieder anpassen müssen.

Im Alltag zeigt sich Resilienz in einem resilienten Lebensstil: einer gesunden Lebensführung mit Bewegung, Ernährung und Schlaf, einem wirksamen Umgang mit Stress, tragfähigen sozialen Beziehungen und einer optimistischen Grundhaltung, die Herausforderungen auch als Chance zum Wachsen sieht.

Für Dr. Irene Preußner, die Entwicklerin von MENSCH DENK AN DICH®, soll Resilienz nicht erklärt, sondern erlebt werden – erst die eigene Erfahrung macht sie im Arbeitsalltag verfügbar.

## Resilienzfaktoren

- Slug: resilienzfaktoren
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Eigenschaften, Fähigkeiten und Bedingungen, die Menschen widerstandsfähiger machen.
- Siehe auch: resilienz; achtsamkeit; loesungsorientierung

Häufig genannt werden Achtsamkeit und Selbstreflexion, Akzeptanz und Anpassungsfähigkeit, lösungsorientiertes Denken, positives Denken und realistischer Optimismus, der Fokus auf das, was sich beeinflussen lässt, Selbstwirksamkeit, emotionale Stabilität und Emotionsregulation, Empathie, soziale Unterstützung durch ein stabiles Netzwerk, ein klares Bild der eigenen Ziele, die Bereitschaft, Verantwortung zu übernehmen, sowie gesunde Routinen.

Viele dieser Faktoren entfalten sich im Miteinander: Das Umfeld und die Unterstützung durch andere spielen für die Resilienz eine zentrale Rolle.

## Resilienzförderung

- Slug: resilienzfoerderung
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Gezielte Stärkung der Widerstandskraft von Einzelnen, Teams und Organisationen.
- Siehe auch: resilienz; resilienztraining; resilienz-spiele

Im Unternehmen reicht Resilienzförderung von Achtsamkeitspraxis und gezieltem Stressmanagement über Trainings für Führungskräfte bis zu einer Kultur, in der Probleme offen angesprochen und Fehler als Lernchance verstanden werden.

Wird sie vernachlässigt, zeigen sich die Folgen häufig in Überlastung, Konflikten, Fehlzeiten und sinkender Veränderungsbereitschaft.

## Resilienztraining

- Slug: resilienztraining
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Trainings, Seminare oder Kurse, in denen Menschen mit praktischen Übungen ihre Widerstandskraft stärken.
- Siehe auch: resilienzfoerderung; resilienz-spiele; play2change

Resilienztrainings vermitteln Strategien für den Umgang mit Stress und Rückschlägen und machen individuelle Resilienzfaktoren erfahrbar. Wirksam sind sie vor allem dann, wenn das Gelernte in den Arbeitsalltag übertragen wird – etwa durch gemeinsame Reflexion im Team und konkrete Vereinbarungen.

## Achtsamkeit

- Slug: achtsamkeit
- Kategorie: Psychologie in der Arbeitswelt
- Auch: Achtsamkeitspraxis
- Kurz: Mit voller Aufmerksamkeit im Hier und Jetzt sein und Gedanken, Gefühle und Situationen wahrnehmen, ohne sich von ihnen mitreißen zu lassen.
- Siehe auch: resilienzfaktoren; stressmanagement; selbstreflexion

Während Stress oft zu Tunnelblick und impulsiven Reaktionen führt, hilft Achtsamkeit, bewusst innezuhalten, Prioritäten zu setzen und fokussiert zu handeln. Kurze Atemübungen oder bewusste Pausen lassen sich leicht in den Arbeitsalltag einbauen. Achtsamkeit gilt als wichtiger Resilienzfaktor.

## Positive Psychologie

- Slug: positive-psychologie
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Teilbereich der Psychologie, der sich mit Stärken, Wohlbefinden, Resilienz und Optimismus befasst – statt vorrangig mit Problemen.
- Siehe auch: perma; positive-leadership; mdad

Als Begründer gilt der US-amerikanische Psychologe Martin Seligman. Im Unterschied zu Ansätzen, die vor allem auf die Behandlung von Störungen ausgerichtet sind, fragt die Positive Psychologie, was Menschen gedeihen lässt.

In der Arbeitswelt gewinnt sie an Bedeutung, weil Beschäftigte neben Sicherheit und Gehalt zunehmend Sinnhaftigkeit, Wertschätzung und Vertrauen suchen. Sie ist eine der wissenschaftlichen Grundlagen von MENSCH DENK AN DICH®.

## PERMA-Modell

- Slug: perma
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Modell von Martin Seligman mit fünf Bausteinen für ein erfülltes Leben.
- Siehe auch: positive-psychologie; positive-leadership

PERMA steht für Positive Emotionen, Engagement, positive Beziehungen (Relationships), Sinnhaftigkeit (Meaning) und Zielerreichung (Accomplishment). Im Unternehmenskontext dient das Modell als Orientierung dafür, welche Bedingungen Wohlbefinden und Leistungsfähigkeit von Mitarbeitenden fördern.

## Selbstwirksamkeit

- Slug: selbstwirksamkeit
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Die Überzeugung, durch eigenes Handeln etwas bewirken und Herausforderungen meistern zu können.
- Siehe auch: veraenderungskompetenz; probehandeln; playfulness; resilienz

Das Konzept geht auf den Psychologen Albert Bandura zurück. Selbstwirksamkeit stärkt das Vertrauen in die eigenen Fähigkeiten und ist eine wichtige Voraussetzung für Veränderungsbereitschaft. Sie wächst vor allem durch eigene Erfolgserlebnisse – zum Beispiel, wenn Mitarbeitende erleben, dass sie selbst Lösungen entwickeln und umsetzen können.

Irene Preußner sieht in ihr einen zentralen Wirkfaktor für Veränderung: Wissen und Appelle verändern selten Verhalten, erlebte Selbstwirksamkeit dagegen schon. Sie lässt sich deshalb nicht erklären, sondern nur durch Erfahrung aufbauen – etwa im geschützten Spielraum.

## Intrinsische und extrinsische Motivation

- Slug: intrinsische-motivation
- Kategorie: Psychologie in der Arbeitswelt
- Auch: Intrinsische Motivation; Extrinsische Motivation
- Kurz: Intrinsisch motiviert handelt, wer etwas um seiner selbst willen tut; extrinsisch motiviert, wer wegen eines Anreizes von außen handelt.
- Siehe auch: playfulness; gamification; flow

Extrinsische Motivation entsteht durch Belohnungen, Punkte, Prämien, Lob oder die Vermeidung von Nachteilen. Sie wirkt gut bei klar umrissenen, wiederholbaren Aufgaben. Intrinsische Motivation entsteht aus Freude am Tun, Neugier und Sinn – und gilt als nachhaltiger.

Nach der Selbstbestimmungstheorie von Edward Deci und Richard Ryan wächst intrinsische Motivation, wenn drei Grundbedürfnisse erfüllt sind: Autonomie, Kompetenzerleben und soziale Eingebundenheit.

Die Unterscheidung ist der Kern der Abgrenzung zwischen Gamification, die vor allem extrinsisch über Anreize wirkt, und Playfulness, die auf intrinsische Motivation setzt. Gerade Kreativität, kritisches Denken und Innovation lassen sich kaum durch Belohnungssysteme erzwingen.

## Flow

- Slug: flow
- Kategorie: Psychologie in der Arbeitswelt
- Auch: Flow-Erleben
- Kurz: Zustand völliger Vertiefung in eine Tätigkeit, in dem Zeit und Selbstzweifel in den Hintergrund treten.
- Siehe auch: intrinsische-motivation; playfulness; serious-games

Beschrieben hat das Flow-Erleben der Psychologe Mihaly Csikszentmihalyi. Es entsteht, wenn Anforderung und eigene Fähigkeiten im Gleichgewicht sind, das Ziel klar ist und unmittelbare Rückmeldung erfolgt.

Spiele erzeugen leicht Flow. Irene Preußner sieht darin einen Grund, warum spielerisches Lernen wirkt: Im Flow entsteht eher intrinsische Motivation – und die sorgt dafür, dass Erkenntnisse nachhaltig bleiben.

## Emotionale Intelligenz

- Slug: emotionale-intelligenz
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Die Fähigkeit, eigene und fremde Gefühle wahrzunehmen, zu verstehen und angemessen mit ihnen umzugehen.
- Siehe auch: arbeitsklima; selbstreflexion; fuehrungskraefte-coaching

Das Konzept wurde von Peter Salovey und John D. Mayer beschrieben und durch Daniel Goleman bekannt. Dazu gehören Selbstwahrnehmung, Emotionsregulation, Empathie und soziale Kompetenz.

Menschen mit hoher emotionaler Intelligenz gehen besser mit Konflikten um, zeigen mehr Empathie und tragen zu einem positiven Arbeitsklima bei – für Führungskräfte ist sie eine Schlüsselkompetenz.

## Psychologische Sicherheit

- Slug: psychologische-sicherheit
- Kategorie: Psychologie in der Arbeitswelt
- Auch: Psychological Safety
- Kurz: Die gemeinsame Überzeugung in einem Team, dass man Fragen, Ideen, Bedenken und Fehler offen ansprechen kann, ohne negative Folgen befürchten zu müssen.
- Siehe auch: fehlerkultur; feedbackkultur; mentale-gesundheit

Geprägt wurde der Begriff vor allem durch die Organisationsforscherin Amy Edmondson. Fehlt psychologische Sicherheit, herrscht in Meetings Zurückhaltung, Probleme bleiben unausgesprochen und Innovation stockt.

Teams mit hoher psychologischer Sicherheit lernen schneller und sprechen auch sensible Themen an – ein wichtiger Faktor für Gesundheit, Zusammenarbeit und Leistungsfähigkeit.

## Innere Kündigung

- Slug: innere-kuendigung
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Zustand, in dem Mitarbeitende zwar anwesend sind, sich emotional aber längst vom Unternehmen gelöst haben.
- Siehe auch: mitarbeiterbindung; fluktuation; unternehmenskultur

Betroffene machen nur noch „Dienst nach Vorschrift“, bringen kaum eigene Ideen ein und identifizieren sich nicht mehr mit ihrer Arbeit. Ursachen sind häufig fehlende Wertschätzung, mangelnde Kommunikation, Veränderungen ohne Beteiligung oder Isolation in hybriden Arbeitsmodellen.

Innere Kündigung geht oft mit steigender Fluktuation, Unzufriedenheit und sinkender Produktivität einher.

## Selbstreflexion

- Slug: selbstreflexion
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Die Fähigkeit, das eigene Denken, Fühlen und Handeln bewusst zu betrachten und daraus zu lernen.
- Siehe auch: resilienzfaktoren; coaching; potenzialentfaltung

Selbstreflexion ist ein Resilienzfaktor und eine Kernkompetenz guter Führung. Wer bewusst wahrnimmt, was in ihm vorgeht, kann besser auf Stress reagieren, eigene Stärken erkennen und blinde Flecken aufdecken. In Coaching und spielbasierten Methoden wird sie gezielt angeregt.

## Lösungsorientiertes Denken

- Slug: loesungsorientierung
- Kategorie: Psychologie in der Arbeitswelt
- Auch: Lösungsorientierung
- Kurz: Haltung, den Blick auf Lösungen, Ressourcen und nächste Schritte zu richten, statt sich von Problemen lähmen zu lassen.
- Siehe auch: resilienzfaktoren; systemische-beratung; coaching

Lösungsorientierte Menschen suchen aktiv nach Möglichkeiten und leiten konkrete Schritte zur Bewältigung schwieriger Situationen ein. In der Beratung ist besonders der lösungsfokussierte Ansatz nach Steve de Shazer und Insoo Kim Berg bekannt, der danach fragt, was bereits funktioniert und wie das gewünschte Ziel aussieht.

## Hochstapler-Syndrom

- Slug: hochstapler-syndrom
- Kategorie: Psychologie in der Arbeitswelt
- Auch: Impostor-Phänomen
- Kurz: Verzerrte Selbstwahrnehmung, bei der Menschen ihre Erfolge als unverdient erleben und ihre Fähigkeiten unterschätzen.
- Siehe auch: dunning-kruger; potenzialentfaltung

Betroffene führen Erfolge eher auf Glück oder Zufall zurück und fürchten, als „Hochstapler“ entlarvt zu werden. Das kann dazu führen, dass vorhandene Potenziale ungenutzt bleiben. Feedback und Coaching helfen, zu einer realistischeren Selbsteinschätzung zu finden.

## Dunning-Kruger-Effekt

- Slug: dunning-kruger
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Kognitive Verzerrung, bei der Personen mit geringerer Kompetenz in einem Bereich ihre Fähigkeiten überschätzen.
- Siehe auch: hochstapler-syndrom; feedbackkultur

Benannt ist der Effekt nach den Psychologen David Dunning und Justin Kruger. Wie das Hochstapler-Syndrom erschwert er eine realistische Einschätzung der eigenen Stärken und Schwächen. Regelmäßiges, wertschätzendes Feedback und Selbstreflexion wirken dem entgegen.

## Systemische Beratung

- Slug: systemische-beratung
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Beratungsansatz, der Menschen nicht isoliert betrachtet, sondern im Zusammenhang ihrer Beziehungen, Rollen und Organisationen.
- Siehe auch: coaching; loesungsorientierung; mdad

Probleme und Lösungen werden als Teil eines Systems verstanden – etwa eines Teams oder Unternehmens. Systemisch Beratende arbeiten mit Fragetechniken, Perspektivwechseln und einem Fokus auf Ressourcen. Der Ansatz ist neben der Positiven Psychologie eine Grundlage von MENSCH DENK AN DICH®.

## Gruppendynamik

- Slug: gruppendynamik
- Kategorie: Psychologie in der Arbeitswelt
- Kurz: Die Kräfte und Prozesse, die das Verhalten von Menschen in Gruppen beeinflussen.
- Siehe auch: teamentwicklung; tuckman; serious-play

Der Begriff geht auf den Sozialpsychologen Kurt Lewin zurück. Dazu gehören Rollen, Beziehungen, Machtverhältnisse, unausgesprochene Regeln und die Art, wie Konflikte ausgetragen werden. Gruppendynamische Prozesse können Zusammenarbeit beflügeln oder blockieren – spielbasierte und erfahrungsorientierte Methoden machen sie sichtbar und besprechbar.

## Transformation

- Slug: transformation
- Kategorie: Transformation & Wandel
- Kurz: Tiefgreifender Veränderungsprozess, durch den sich Menschen, Organisationen oder Gesellschaften an neue Bedingungen anpassen und weiterentwickeln.
- Siehe auch: business-transformation; change-management; veraenderungskompetenz

Auslöser sind etwa Digitalisierung, Globalisierung, neue Technologien oder gesellschaftlicher Wandel wie das Ziel der Klimaneutralität. Transformation verändert Strategien, Strukturen, Prozesse und Kompetenzen – und damit auch die Arbeit jedes Einzelnen.

Sie bringt Unsicherheit mit sich, eröffnet aber vor allem neue Chancen: Neue Arbeitsfelder entstehen, Zusammenarbeit wird neu gedacht.

## Business Transformation

- Slug: business-transformation
- Kategorie: Transformation & Wandel
- Kurz: Strategische Neuausrichtung eines Unternehmens, um sich an veränderte Märkte, Technologien und Kundenanforderungen anzupassen.
- Siehe auch: transformation; unternehmensentwicklung; change-management

Business Transformation ist kein einmaliges Projekt, sondern ein kontinuierlicher Prozess. Unternehmen, die den Wandel scheuen, riskieren Wettbewerbsfähigkeit, Effizienz und qualifizierte Fachkräfte. Gelingen kann sie nur, wenn die Menschen den Wandel verstehen und aktiv mitgestalten.

## Industrie 4.0

- Slug: industrie-4-0
- Kategorie: Transformation & Wandel
- Kurz: Bezeichnung für die Vernetzung und Digitalisierung der industriellen Produktion.
- Siehe auch: transformation; weiterbildung

Durch intelligente Maschinen, Datenaustausch und Automatisierung verändern sich Arbeitsabläufe und Berufsbilder grundlegend: Neue Tätigkeiten entstehen, traditionelle verändern sich oder fallen weg. Damit ist Industrie 4.0 ein zentraler Treiber der Transformation in der Arbeitswelt.

## Change Management

- Slug: change-management
- Kategorie: Transformation & Wandel
- Auch: Veränderungsmanagement; Change-Prozess
- Kurz: Gezielte Planung und Steuerung von Veränderungsprozessen in Unternehmen.
- Siehe auch: widerstand; partizipation; veraenderungskompetenz; transformation

Statt Veränderungen einfach geschehen zu lassen, sorgt Change Management mit einem strukturierten Vorgehen dafür, dass sie erfolgreich umgesetzt und die betroffenen Menschen mitgenommen werden. Entscheidend sind Transparenz, Mitgestaltungsmöglichkeiten und eine klare Kommunikation, die Ängste ernst nimmt.

Veränderungen am Arbeitsplatz können ganz unterschiedliche Formen haben:

- **Technologische Innovationen:** neue Software oder Automatisierung, die neue Kompetenzen verlangen.
- **Organisatorische Umstrukturierungen:** Fusionen, Abteilungswechsel oder neue Hierarchien.
- **Neue Arbeitsmodelle:** Remote Work, flexible Arbeitszeiten oder hybride Modelle.
- **Veränderte Unternehmensziele:** strategische Neuausrichtungen auf neue Märkte, Produkte oder Dienstleistungen.

Gutes Change Management verringert Widerstände, erhöht Akzeptanz und Motivation und beschleunigt die Einführung neuer Strategien und Technologien. Entscheidend ist, die Beschäftigten aktiv einzubinden – ohne Beteiligung scheitern Veränderungsprozesse besonders häufig.

## Partizipation

- Slug: partizipation
- Kategorie: Transformation & Wandel
- Auch: Mitarbeiterbeteiligung; Kollektive Intelligenz
- Kurz: Aktive Einbindung von Mitarbeitenden und Führungskräften in Entscheidungen und Veränderungsprozesse.
- Siehe auch: change-management; widerstand; mitarbeiterbindung

Wer den Wandel mitgestaltet, versteht seine Hintergründe, unterstützt die Umsetzung und fühlt sich mitverantwortlich für das Ergebnis. Partizipation erhöht so die Akzeptanz, reduziert Widerstände und stärkt Motivation und Mitarbeiterbindung.

Zugleich nutzt sie die kollektive Intelligenz einer Organisation: Mitarbeitende kennen die operativen Abläufe am besten. Werden verschiedene Perspektiven einbezogen, entstehen kreativere und fundiertere Entscheidungen. Ohne Einbindung bleiben dagegen wertvolle Ideen unentdeckt, und Mitarbeitende fühlen sich übergangen.

## Veränderungskompetenz

- Slug: veraenderungskompetenz
- Kategorie: Transformation & Wandel
- Auch: Veränderungsbereitschaft
- Kurz: Die Fähigkeit, sich an neue Situationen anzupassen, Veränderungen aktiv zu gestalten und aus ihnen zu lernen.
- Siehe auch: selbstwirksamkeit; change-management; resilienz

Sie setzt sich aus Offenheit für Neues, Lernbereitschaft, emotionaler Stabilität, Problemlösungskompetenz und Selbstwirksamkeit zusammen.

Veränderungskompetenz ist nicht angeboren: Sie wächst, wenn man sich bewusst mit eigenen Ängsten und Widerständen auseinandersetzt, regelmäßig kleine neue Herausforderungen annimmt, die eigene Resilienz stärkt und Netzwerke nutzt.

## Widerstand gegen Veränderung

- Slug: widerstand
- Kategorie: Transformation & Wandel
- Auch: Veränderungswiderstand
- Kurz: Natürliche Reaktion von Menschen auf Veränderungen, die sie als unsicher oder bedrohlich erleben.
- Siehe auch: change-management; veraenderungskompetenz; probehandeln

Typisch sind Sätze wie „Das haben wir schon immer so gemacht“ oder „Das haben wir doch alles schon versucht“. Ursachen sind häufig die Angst vor Misserfolg oder Kontrollverlust, mangelnde Information und fehlende Beteiligung.

Widerstand ist kein bloßer Störfaktor, sondern ein wichtiges Signal: Wird er offen besprochen, lassen sich Bedenken lösungsorientiert bearbeiten.

## Lernende Organisation

- Slug: lernende-organisation
- Kategorie: Transformation & Wandel
- Auch: Organizational Learning; Lernkultur
- Kurz: Organisation, die sich kontinuierlich an neue Herausforderungen anpasst, Wissen offen teilt und ihre Mitarbeitenden ermutigt, sich weiterzuentwickeln.
- Siehe auch: fehlerkultur; innovationskultur; weiterbildung; organisationsentwicklung

Merkmale sind eine gemeinsame Vision, eine offene Kommunikations- und Fehlerkultur, Flexibilität, Wissensaustausch und das Verständnis, dass Lernen Teil des Arbeitsalltags ist. Lernende Organisationen sind anpassungsfähiger, innovativer und bieten ein Umfeld, in dem Mitarbeitende motiviert bleiben.

Bekannt wurde das Konzept besonders durch den US-amerikanischen Organisationswissenschaftler Peter M. Senge. Als Beispiele gelten Unternehmen wie Netflix, Salesforce und Patagonia; in Deutschland setzt etwa das Bundesinstitut für Berufsbildung auf kontinuierliches Lernen.

Auf dem Weg zur lernenden Organisation helfen:

- **Schulungen und Weiterbildungen:** Lernen wird Teil des Arbeitsalltags.
- **Offene Fehlerkultur:** Fehler gelten als Lernchance und werden nicht bestraft.
- **Wissenstransfer:** Teams teilen Wissen und Best Practices, etwa in regelmäßigen Austauschformaten.
- **Technologien:** E-Learning-Plattformen und digitale Tools erleichtern den Zugang zu Wissen und speichern es.

## Innovationskultur

- Slug: innovationskultur
- Kategorie: Transformation & Wandel
- Kurz: Unternehmenskultur, in der neue Ideen entstehen, ausgesprochen, ausprobiert und umgesetzt werden können.
- Siehe auch: lernende-organisation; fehlerkultur; playfulness; psychologische-sicherheit

Kennzeichen sind offene Kommunikation über Abteilungs- und Hierarchiegrenzen hinweg, Wissensaustausch, Freiräume zum Experimentieren und ein konstruktiver Umgang mit Fehlern. Hierarchische Entscheidungsstrukturen, Angst vor Misserfolg und schlechte Zusammenarbeit führen dagegen zum Innovationsstau.

Innovationskultur lässt sich nicht verordnen: Kreativität entsteht eher in Entspannung und Sicherheit als unter Druck. Spielerische Formate können helfen, eingefahrene Denkmuster zu durchbrechen.

## Fehlerkultur

- Slug: fehlerkultur
- Kategorie: Transformation & Wandel
- Kurz: Die Art und Weise, wie eine Organisation mit Fehlern umgeht.
- Siehe auch: lernende-organisation; psychologische-sicherheit

In einer offenen Fehlerkultur werden Fehler nicht bestraft, sondern als Lernmöglichkeit verstanden und offen besprochen. Das fördert psychologische Sicherheit, Innovation und kontinuierliche Verbesserung – und ist ein Kernmerkmal lernender Organisationen.

## Unternehmensentwicklung

- Slug: unternehmensentwicklung
- Kategorie: Transformation & Wandel
- Auch: Corporate Development; Corp Dev
- Kurz: Gezielte Weiterentwicklung eines Unternehmens, um es an Marktanforderungen und Wachstumsziele anzupassen.
- Siehe auch: organisationsentwicklung; business-transformation; personalentwicklung

Unternehmenserfolg ist kein Zufall. Als Grundlagen gelten klare Ziele und eine Vision, eine flexible Organisationsstruktur, Innovationen und Technologien, eine starke Unternehmenskultur mit inspirierender Führung sowie eine gezielte Planung von Fachleuten, Kapital und Zeit.

Die strategische Unternehmensentwicklung umfasst Marktanalyse und strategische Planung, Fusionen und Übernahmen, Digitalisierung und Innovationsförderung sowie die Anpassung der Organisationsstruktur. Ebenso wichtig sind Partnerschaften, datengestützte Entscheidungen und die Entwicklung der Mitarbeitenden und der Unternehmenskultur.

Stillstand ist dabei ein Risiko: Ohne Weiterentwicklung drohen Verluste an Wettbewerbsfähigkeit, Innovationskraft und Fachkräften.

## Organisationsentwicklung

- Slug: organisationsentwicklung
- Kategorie: Transformation & Wandel
- Kurz: Langfristiger, geplanter Veränderungsprozess, der Strukturen, Prozesse und Kultur einer Organisation gemeinsam mit den Menschen weiterentwickelt.
- Siehe auch: unternehmensentwicklung; teamentwicklung; serious-play

Im Unterschied zu einer rein strategischen Unternehmensentwicklung setzt Organisationsentwicklung auf die Beteiligung der Mitarbeitenden: Sie sollen den Wandel verstehen, mitgestalten und dabei selbst lernen. Typische Ansätze sind Workshops, Teamentwicklung, Coaching und Formate der Co-Creation – zunehmend auch spielbasierte Methoden.

## Fachkräftemangel

- Slug: fachkraeftemangel
- Kategorie: Transformation & Wandel
- Auch: Demografischer Wandel
- Kurz: Situation, in der Unternehmen offene Stellen nicht oder nur schwer mit qualifiziertem Personal besetzen können.
- Siehe auch: mitarbeiterbindung; employer-branding; weiterbildung

Ein wesentlicher Treiber ist der demografische Wandel: Weniger junge Menschen rücken nach, während erfahrene Beschäftigte in den Ruhestand gehen. Personalmangel erhöht den Termin- und Leistungsdruck für die verbleibenden Teams.

Umso wichtiger werden Mitarbeiterbindung, Weiterbildung, Gesundheitsförderung und eine attraktive Arbeitgebermarke.

## Hybride Arbeitsmodelle

- Slug: hybride-arbeit
- Kategorie: Transformation & Wandel
- Auch: Hybride Arbeit; Remote Work
- Kurz: Arbeitsformen, bei denen Beschäftigte teils im Büro und teils mobil oder im Homeoffice arbeiten.
- Siehe auch: work-life-balance; teamentwicklung; innere-kuendigung

Hybride Modelle bieten Flexibilität und erleichtern die Vereinbarkeit von Beruf und Privatleben. Sie stellen Teams aber auch vor neue Herausforderungen: Isolation im Homeoffice, unstrukturierte Meetings und weniger informeller Austausch können Teamkultur und Kommunikation schwächen.

Klare Absprachen, regelmäßige Check-ins und bewusst gestaltete Begegnungen wirken dem entgegen.

## Unternehmenskultur

- Slug: unternehmenskultur
- Kategorie: Führung, Team & Organisation
- Kurz: Gemeinsame Werte, Normen, Haltungen und Verhaltensweisen, die das Miteinander in einem Unternehmen prägen.
- Siehe auch: fehlerkultur; feedbackkultur; arbeitsklima; mitarbeiterbindung

Die Unternehmenskultur zeigt sich darin, wie kommuniziert, entschieden, geführt und mit Fehlern umgegangen wird. Eine gesundheitsorientierte, wertschätzende Kultur stärkt Bindung, Motivation und Veränderungsbereitschaft; eine Kultur, die von Druck, Misstrauen und fehlender Anerkennung geprägt ist, begünstigt dagegen Stress und innere Kündigung.

## Arbeitsklima

- Slug: arbeitsklima
- Kategorie: Führung, Team & Organisation
- Auch: Betriebsklima
- Kurz: Die erlebte Atmosphäre der Zusammenarbeit in einem Team oder Unternehmen – wie Menschen miteinander umgehen, kommunizieren und sich gegenseitig wertschätzen.
- Siehe auch: teamgeist; teambuilding; unternehmenskultur; emotionale-intelligenz

Ein positives Arbeitsklima ist entscheidend für Produktivität, Zufriedenheit und Gesundheit. Es lebt von Vertrauen, offener Kommunikation, Wertschätzung und einem konstruktiven Umgang mit Konflikten. Ein schlechtes Klima führt dagegen zu Missverständnissen, häufigeren Konflikten, weniger Innovation und höherer Fluktuation.

Schon einfache Maßnahmen wirken: regelmäßige Teammeetings mit offenen Gesprächsrunden, gemeinsame (auch virtuelle) Pausen für informellen Austausch, Anerkennung für gute Leistungen und Teamaktivitäten, die Vertrauen aufbauen.

## Teamgeist

- Slug: teamgeist
- Kategorie: Führung, Team & Organisation
- Auch: Wir-Gefühl; Teamkultur; Zusammenhalt
- Kurz: Das Gefühl von Zusammengehörigkeit und gegenseitiger Unterstützung, das ein Team über die gemeinsame Aufgabe hinaus verbindet.
- Siehe auch: teamentwicklung; teambuilding; arbeitsklima

Ein starkes Wir-Gefühl entsteht durch gemeinsame Erlebnisse, Vertrauen, offene Kommunikation und eine geteilte Teamkultur. Jedes Team entwickelt über die Zeit eine eigene Kultur – bewusst oder unbewusst. Eine gezielte Teamentwicklung sorgt dafür, dass gemeinsame Vision und Werte, klare Ziele und ein offenes Feedbackklima diese Kultur positiv prägen.

## Positive Leadership

- Slug: positive-leadership
- Kategorie: Führung, Team & Organisation
- Kurz: Führungsansatz auf Basis der Positiven Psychologie, der die Stärken der Mitarbeitenden in den Mittelpunkt stellt.
- Siehe auch: positive-psychologie; fuehrungskraefte-coaching; selbstwirksamkeit

Kennzeichen sind ein optimistischer Blick auf Herausforderungen, ein konstruktiver Umgang mit Fehlern, gezielte Stärkenförderung, Achtsamkeit, Vertrauen und Anerkennung. Positive Leadership soll ein Klima schaffen, in dem Motivation, Engagement, Eigenverantwortung und Resilienz wachsen.

## Mitarbeiterbindung

- Slug: mitarbeiterbindung
- Kategorie: Führung, Team & Organisation
- Auch: Emotionale Mitarbeiterbindung; Retention
- Kurz: Alle Faktoren und Maßnahmen, die dazu beitragen, dass Mitarbeitende einem Unternehmen langfristig verbunden bleiben.
- Siehe auch: fluktuation; innere-kuendigung; employer-branding

Besonders wirksam ist die emotionale Bindung: Mitarbeitende, die sich mit ihrem Unternehmen identifizieren, sind motivierter, leistungsbereiter und fehlen seltener. Förderlich sind eine offene Feedbackkultur, Weiterbildungs- und Entwicklungsmöglichkeiten, Wertschätzung, sinnstiftende Aufgaben, eine gute Work-Life-Balance und eine gesundheitsorientierte Unternehmenskultur.

Mangelnde Bindung zeigt sich in hoher Fluktuation, dem Verlust von Know-how und innerer Kündigung.

## Fluktuation

- Slug: fluktuation
- Kategorie: Führung, Team & Organisation
- Auch: Mitarbeiterfluktuation
- Kurz: Personalbewegung durch Kündigungen und Abgänge, meist als Quote im Verhältnis zur Belegschaft angegeben.
- Siehe auch: mitarbeiterbindung; fachkraeftemangel

Hohe Fluktuation verursacht Kosten für Recruiting und Einarbeitung, führt zum Verlust von Wissen über Prozesse und Kunden und belastet Teamklima und Motivation. Sie ist oft ein Warnsignal für mangelnde Mitarbeiterbindung, Überlastung oder ein angespanntes Arbeitsklima.

## Employer Branding

- Slug: employer-branding
- Kategorie: Führung, Team & Organisation
- Auch: Arbeitgebermarke
- Kurz: Aufbau und Pflege einer attraktiven Arbeitgebermarke.
- Siehe auch: mitarbeiterbindung; fachkraeftemangel; bgm

Ein starkes Image als guter Arbeitgeber erleichtert es, neue Talente zu gewinnen und bestehende Mitarbeitende zu halten. Glaubwürdig ist Employer Branding dann, wenn es auf gelebter Kultur beruht – etwa auf Gesundheitsförderung, Entwicklungsmöglichkeiten und einem wertschätzenden Miteinander.

## Feedbackkultur

- Slug: feedbackkultur
- Kategorie: Führung, Team & Organisation
- Kurz: Gelebte Praxis in einer Organisation, sich regelmäßig, offen und wertschätzend Rückmeldung zu geben.
- Siehe auch: psychologische-sicherheit; fehlerkultur; mitarbeiterbindung

Eine gute Feedbackkultur macht Leistungen sichtbar, hilft, Missverständnisse früh zu klären, und unterstützt eine realistische Selbsteinschätzung. Sie ist eine wichtige Maßnahme zur Mitarbeiterbindung und eng mit psychologischer Sicherheit und Fehlerkultur verbunden.

## Personalentwicklung

- Slug: personalentwicklung
- Kategorie: Führung, Team & Organisation
- Kurz: Alle Maßnahmen, mit denen ein Unternehmen Kompetenzen, Potenziale und die berufliche Entwicklung seiner Mitarbeitenden systematisch fördert.
- Siehe auch: weiterbildung; potenzialentfaltung; spiele-coach

Dazu zählen Entwicklungspläne, Weiterbildungen, Coaching, Mentoring und die Entwicklung von Führungskräften. Gute Personalentwicklung verbindet die Ziele des Unternehmens mit den individuellen Entwicklungswünschen der Beschäftigten – und ist damit ein wichtiger Hebel gegen Fachkräftemangel und Fluktuation.

## Weiterbildung

- Slug: weiterbildung
- Kategorie: Führung, Team & Organisation
- Auch: Fortbildung; Schulung
- Kurz: Lernformen, mit denen Beschäftigte ihre Kompetenzen erweitern – die Begriffe werden oft gleichbedeutend verwendet, meinen aber Unterschiedliches.
- Siehe auch: personalentwicklung; lernende-organisation; spiele-coach

- **Weiterbildung:** allgemeine Lernprozesse, mit denen neue Fähigkeiten und Kompetenzen erworben werden, etwa im Projektmanagement.
- **Fortbildung:** spezifische Qualifikationen innerhalb des bestehenden Berufs, zur Spezialisierung oder für den Aufstieg in neue Positionen.
- **Schulung:** meist kürzere Maßnahmen, die konkrete Fähigkeiten vermitteln, zum Beispiel zu neuer Software oder zu Soft Skills wie Kommunikation.

Regelmäßige Weiterbildung sichert Wettbewerbsfähigkeit, stärkt Arbeitszufriedenheit und Mitarbeiterbindung und hilft, Talente intern zu entwickeln. Mitarbeitende gewinnen neue Qualifikationen, bessere Karrierechancen und Sicherheit in einem sich wandelnden Arbeitsmarkt.

Erfolgreich ist Weiterbildung mit einem strukturierten Konzept in fünf Schritten: Bedarfsanalyse (welche Fähigkeiten fehlen?), Zielsetzung, Auswahl passender Angebote, zeitliche und finanzielle Unterstützung der Teilnehmenden und schließlich die Erfolgsmessung im Arbeitsalltag. Nachhaltig wirkt sie vor allem dann, wenn Wissen erlebt und in den Alltag übertragen wird.

## Potenzialentfaltung

- Slug: potenzialentfaltung
- Kategorie: Führung, Team & Organisation
- Kurz: Prozess, in dem Menschen, Teams und Organisationen ungenutzte Stärken, Talente und Ressourcen entdecken und gezielt weiterentwickeln.
- Siehe auch: coaching; hochstapler-syndrom; personalentwicklung

- **Individuell:** Selbstzweifel und unbewusste Denkmuster erkennen, persönliche Stärken schärfen.
- **Im Team:** Synergien schaffen, eine gemeinsame Vision entwickeln, individuelle Stärken in Einklang bringen.
- **In der Organisation:** veraltete Denkweisen aufbrechen und eine nachhaltige Führungskultur etablieren.

Bleiben Potenziale unentdeckt, führt das häufig zu Frustration und Demotivation. Coaching, Feedback und Selbstreflexion helfen, sie sichtbar zu machen.

## Coaching

- Slug: coaching
- Kategorie: Führung, Team & Organisation
- Auch: Business Coaching; Coachee
- Kurz: Professionelle, prozessorientierte Beratung, die Menschen dabei unterstützt, ihre Potenziale zu entdecken und eigene Lösungen zu entwickeln.
- Siehe auch: fuehrungskraefte-coaching; potenzialentfaltung; systemische-beratung

Ein Coach liefert keine fertigen Antworten, sondern begleitet den Coachee – also die Person, die sich coachen lässt – mit gezielten Fragen, psychologischem Wissen und praxisnahen Methoden. Ziel sind mehr Klarheit, Motivation und Handlungsfähigkeit, etwa bei Konflikten, Entscheidungen oder beruflichen Veränderungen.

Business Coaching richtet sich speziell auf berufliche Fragestellungen und den Organisationskontext.

Zum Methodenkoffer eines Coaches gehören gezielte Fragetechniken, systemische Analysen und kreative Visualisierungstechniken, ergänzt durch Ansätze aus Resilienztraining, Stressmanagement und achtsamer Führung. Gute Coaches gestalten den Prozess individuell statt nach starrem Programm.

## Führungskräfte-Coaching

- Slug: fuehrungskraefte-coaching
- Kategorie: Führung, Team & Organisation
- Auch: Executive Coaching
- Kurz: Form des Business Coachings, die speziell auf die Anforderungen und Herausforderungen von Führungskräften ausgerichtet ist.
- Siehe auch: coaching; positive-leadership; playful-leadership; selbstreflexion

Im Mittelpunkt stehen die Führungspersönlichkeit und der individuelle Führungsstil. Typische Themen sind Klarheit in der Führungsverantwortung, wertschätzende Kommunikation, Konfliktmanagement, Stressmanagement und strategische Zielsetzung.

Coaching stärkt die Selbstwahrnehmung, verbessert die Kommunikationsfähigkeit und unterstützt fundierte Entscheidungen. Führungskräfte, die sich nicht weiterentwickeln, verharren dagegen leichter in gewohnten Denkmustern – mit Folgen für Innovation, Anpassungsfähigkeit und Mitarbeiterbindung.

Führungskräfte-Coaching ist kein einmaliges Seminar, sondern ein Entwicklungsprozess – denn gute Führung beginnt bei der Selbstführung.

## Playful Leadership

- Slug: playful-leadership
- Kategorie: Führung, Team & Organisation
- Auch: Spielerische Führung
- Kurz: Führungsverständnis, das spielerische Formate nicht als Auflockerung am Rand, sondern als Kern ernsthafter Führungsarbeit begreift.
- Siehe auch: playfulness; selbstwirksamkeit; play2change; positive-leadership

Irene Preußner beschreibt die play2change-Methode als Playful Leadership: Im ergebnisoffenen Spielraum erleben Führungskräfte hierarchieübergreifend ihre eigene Innovationskraft und Selbstwirksamkeit. Weil Wissen und Appelle Verhalten selten verändern, setzt dieser Ansatz auf Erfahrung – notwendige Veränderungen lassen sich dann leichter und schneller umsetzen.

Spielerische Führung bedeutet nicht, Arbeit in einen Wettbewerb um Punkte zu verwandeln. Sie schafft Räume, in denen Menschen sich trauen, Neues auszuprobieren, Fehler als Lernschritte zu sehen und gemeinsam Lösungen zu entwickeln.

## Playful Work Design

- Slug: playful-work-design
- Kategorie: Führung, Team & Organisation
- Kurz: Konzept aus der Arbeitspsychologie, das beschreibt, wie Beschäftigte ihre Arbeit von sich aus spielerischer gestalten.
- Siehe auch: playfulness; intrinsische-motivation; flow

Untersucht wurde Playful Work Design vor allem von Yuri Scharp und Arnold B. Bakker. Gemeint ist, dass Menschen in ihre alltäglichen Aufgaben selbst Spaß und Herausforderung hineinbringen – etwa durch Fantasie, Humor oder selbst gesetzte Ziele –, ohne dass sich die Aufgabe selbst verändert. Studien bringen dies mit mehr Engagement und Kreativität in Verbindung.

Der Ansatz passt zur Idee der Playfulness: Spielerisches entsteht von innen heraus und ist keine Belohnungsmechanik, die von außen übergestülpt wird.

## Teamentwicklung

- Slug: teamentwicklung
- Kategorie: Führung, Team & Organisation
- Kurz: Fortlaufender Prozess, in dem eine Gruppe von Menschen zu einem leistungsfähigen Team mit gutem Zusammenhalt wird.
- Siehe auch: teambuilding; teamgeist; tuckman; gruppendynamik

Teamentwicklung geht deutlich tiefer als einzelne Teambuilding-Events: Sie analysiert und verbessert Strukturen, bezieht die Stärken und Schwächen der Teammitglieder ein, klärt Kommunikation und Verantwortlichkeiten und zielt auf ein dauerhaft stabiles Teamgefüge.

Typische Herausforderungen sind unterschiedliche Persönlichkeiten und Arbeitsstile, Kommunikationsbarrieren, unklare Verantwortlichkeiten und gruppendynamische Spannungen. Hilfreich sind regelmäßige Teamreflexion, eine klare Teamkultur und eine Führung, die eher moderiert als kontrolliert. Dazu kommen kontinuierliche Weiterbildung auch auf sozialer und methodischer Ebene – etwa Kommunikationstrainings, Workshops zur Konfliktlösung und Coaching für Führungskräfte – sowie Teambuilding mit echtem Bezug zum Arbeitsalltag.

## Teambuilding

- Slug: teambuilding
- Kategorie: Führung, Team & Organisation
- Kurz: Aktivitäten und Maßnahmen, die Vertrauen, Zusammenhalt und das Wir-Gefühl in einem Team stärken.
- Siehe auch: teamentwicklung; teamgeist; arbeitsklima; spiele-am-arbeitsplatz

Beispiele sind Kooperationsspiele, Escape-Room-Challenges, Outdoor-Erlebnisse, gemeinsame Kochkurse oder soziale Projekte. Teambuilding ist oft ein guter erster Schritt; nachhaltig wirkt es vor allem als Teil einer langfristigen Teamentwicklung mit echtem Bezug zum Arbeitsalltag.

Gut gemachtes Teambuilding verbessert das Arbeitsklima: Die Kommunikation wird leichter, der Zusammenhalt wächst, Konflikte werden früher erkannt und konstruktiv gelöst, und die Motivation steigt.

## Teamphasen nach Tuckman

- Slug: tuckman
- Kategorie: Führung, Team & Organisation
- Auch: Forming, Storming, Norming, Performing; Teamuhr
- Kurz: Phasenmodell des Psychologen Bruce Tuckman, das beschreibt, welche Entwicklungsstufen Teams typischerweise durchlaufen.
- Siehe auch: teamentwicklung; gruppendynamik

- **Forming (Orientierung):** Die Teammitglieder lernen sich kennen und bringen eigene Erwartungen, Stärken und Schwächen mit. Klare Strukturen und Ziele geben Halt.
- **Storming (Konflikt):** Unterschiedliche Persönlichkeiten, Arbeitsweisen und Ziele treffen aufeinander. Offene Kommunikation und klare Verantwortung helfen durch diese Phase.
- **Norming (Regelung):** Das Team einigt sich auf gemeinsame Regeln, das Zusammengehörigkeitsgefühl wächst.
- **Performing (Leistung):** Das Team arbeitet eingespielt, effizient und mit starkem Wir-Gefühl.

Später ergänzte Tuckman gemeinsam mit Mary Ann Jensen eine fünfte Phase, Adjourning, in der ein Team aufgelöst oder neu aufgestellt wird. Der zyklische Verlauf wird häufig als „Teamuhr“ dargestellt.

## Serious Games

- Slug: serious-games
- Kategorie: Spielbasierte Methoden
- Kurz: Spiele, die ein Ziel über die reine Unterhaltung hinaus verfolgen: Wissen vermitteln, Fähigkeiten trainieren oder Verhaltensänderungen anstoßen.
- Siehe auch: serious-play; gamification; mdad

Der Unterschied zu herkömmlichen Spielen liegt im Zweck: Serious Games sind gezielt so gestaltet, dass die Spielenden etwas für ihr persönliches oder berufliches Leben mitnehmen.

Eingesetzt werden sie in Bildung und Training, zur Problemlösung im Team und in der Persönlichkeitsentwicklung – etwa als Plan-, Rollen- oder Simulationsspiel.

## Serious Play

- Slug: serious-play
- Kategorie: Spielbasierte Methoden
- Kurz: Methode, die spielerisches Handeln nutzt, um komplexe Zusammenhänge greifbar zu machen, neue Perspektiven zu eröffnen und kreative Lösungen zu fördern.
- Siehe auch: serious-games; lego-serious-play; probehandeln

Anders als klassische Besprechungen schafft Serious Play eine dynamische Umgebung, in der Teilnehmende experimentieren und sich aktiv einbringen. Einsatzfelder sind Team- und Organisationsentwicklung, Strategieentwicklung, Innovationsworkshops, Change Management und Mitarbeitertrainings.

## LEGO® Serious Play®

- Slug: lego-serious-play
- Kategorie: Spielbasierte Methoden
- Auch: LSP
- Kurz: Workshop-Methode, bei der Teilnehmende mit LEGO-Steinen Modelle bauen, um abstrakte Themen sichtbar und besprechbar zu machen.
- Siehe auch: serious-play; serious-games

Entwickelt wurde der Ansatz Ende der 1990er-Jahre von LEGO in Zusammenarbeit mit Wissenschaftlern. Grundidee ist, dass Hände und Denken eng verknüpft sind: Jede Person baut ein eigenes Modell – etwa zu Werten, Zielen oder Konflikten –, erklärt es und bringt es in ein gemeinsames Bild ein.

Der Schwerpunkt liegt auf Visualisierung, Innovation und strategischer Planung.

## Gamification

- Slug: gamification
- Kategorie: Spielbasierte Methoden
- Kurz: Einsatz spieltypischer Elemente wie Punkte, Badges und Ranglisten in Zusammenhängen, die selbst kein Spiel sind – mit dem Ziel, gewünschtes Verhalten zu verstärken.
- Siehe auch: playfulness; intrinsische-motivation; serious-games

Gamification setzt vor allem auf extrinsische Motivation: Menschen handeln wegen des Anreizes, nicht wegen der Tätigkeit selbst. Belohnung und sichtbarer Fortschritt dienen als Verstärker, damit ein Verhalten wiederholt wird. Die Leitfrage lautet sinngemäß: Wie bringen wir Menschen dazu, das zu tun, was wir wollen?

Bei klar umrissenen, wiederholbaren Aufgaben funktioniert das gut. Bei Kreativität, kritischem Denken und Innovation stößt Gamification nach Irene Preußner jedoch an Grenzen – diese Fähigkeiten lassen sich kaum durch Belohnungssysteme erzwingen. Wettbewerb um Punkte und Rankings kann echte Zusammenarbeit sogar verdrängen.

Ebenso wenig macht eine Ausstattung mit Tischkicker oder Bällebad eine Arbeitskultur spielerisch, solange der Arbeitsalltag selbst keinen Spielraum lässt. Den Gegenentwurf beschreibt der Begriff Playfulness.

## Playfulness

- Slug: playfulness
- Kategorie: Spielbasierte Methoden
- Auch: Spielerische Haltung; Playfulness vs. Gamification
- Kurz: Spielerische Grundhaltung und Kultur, die auf intrinsische Motivation setzt: Kreativität, Neugier, soziale Verbundenheit, Selbstbestimmung, Selbstwirksamkeit und Entdeckerfreude.
- Siehe auch: gamification; intrinsische-motivation; playful-leadership; probehandeln

Playfulness und Gamification greifen beide die Idee des Spiels auf, beruhen aber auf grundlegend verschiedenen Vorstellungen von Motivation. Irene Preußner, Entwicklerin von MENSCH DENK AN DICH®, macht diese Unterscheidung zum Kern ihrer Arbeit: Spielen ist für sie kein Belohnungssystem, sondern ein Erfahrungsraum.

- **Motivation:** Gamification wirkt extrinsisch über Anreize von außen; Playfulness wirkt intrinsisch – Menschen handeln, weil das Tun selbst Freude macht und Sinn ergibt.
- **Leitfrage:** Gamification fragt, wie man Menschen dazu bringt, das Gewünschte zu tun; Playfulness fragt, wie ein Raum entsteht, in dem Menschen ihre Potenziale selbst entdecken und entfalten.
- **Wirkprinzip:** Gamification verstärkt mit Punkten, Badges und Fortschrittsanzeigen; Playfulness schafft Freiräume – die Energie entsteht im System selbst, aus den Menschen, die darin handeln.
- **Fehler:** Bei Playfulness sind Fehler Teil des Lernens, nicht Scheitern.
- **Zusammenarbeit:** Sie entsteht aus echtem Interesse am gemeinsamen Gestalten statt aus dem Wettbewerb um Punkte oder Rankings.
- **Einsatzfeld:** Gamification eignet sich für klar umrissene Aufgaben; Playfulness für komplexe Herausforderungen, die Kreativität und Innovation verlangen.

In einer Arbeitswelt voller Komplexität, Unsicherheit und schnellem Wandel gewinnt Playfulness deshalb an Bedeutung. Voraussetzung ist ein geschützter Rahmen: Kreativität entsteht in Entspannung und Sicherheit, während Stress zu Tunnelblick führt. Lachen schafft nach Preußner die „Kaffeepausenatmosphäre“, in der gute Ideen entstehen – und niemand wird zum Mitspielen gezwungen.

## Planspiel

- Slug: planspiel
- Kategorie: Spielbasierte Methoden
- Auch: Simulationsspiel
- Kurz: Simulationsspiel, in dem Teilnehmende Rollen übernehmen und in einem realitätsnahen Szenario Entscheidungen treffen.
- Siehe auch: serious-games; probehandeln

Planspiele werden in Erwachsenenbildung, Training und Unternehmen eingesetzt, um etwa Entscheidungsfindung, Konfliktlösung oder wirtschaftliche Zusammenhänge erfahrbar zu machen. Die Teilnehmenden lernen ganz nebenbei Strategien, die sie im echten Leben anwenden können.

## Probehandeln

- Slug: probehandeln
- Kategorie: Spielbasierte Methoden
- Kurz: Ausprobieren neuer Denk- und Handlungsweisen in einem geschützten Rahmen, ohne Angst vor realen Konsequenzen.
- Siehe auch: selbstwirksamkeit; mdad; planspiel

Im Spiel lassen sich Lösungen entwickeln, simulieren und testen, bevor sie im Arbeitsalltag zum Einsatz kommen. Weil zunächst keine echten Konsequenzen drohen, können Teilnehmende auch Schwächen zeigen und ohne ständige Selbstzensur ausprobieren. Das senkt Hemmschwellen, fördert Kreativität und stärkt die Selbstwirksamkeit.

Probehandeln ist ein Grundgedanke von MENSCH DENK AN DICH®: Wer eine Aktionskarte zieht, nimmt eine Aufgabe aus dem Alltag gedanklich vorweg. Spielpausen und Versuch und Irrtum erzeugen Lernschleifen, die Irene Preußner mit agilen Methoden wie Scrum oder Design Thinking vergleicht.

## Spiele am Arbeitsplatz

- Slug: spiele-am-arbeitsplatz
- Kategorie: Spielbasierte Methoden
- Auch: Bürospiele; Teambuildingspiele
- Kurz: Spielerische Formate im Büro oder Homeoffice, die Teamgeist, Kommunikation und Kreativität fördern.
- Siehe auch: playfulness; teambuilding; serious-games; resilienz-spiele

Spiele schaffen eine informelle Atmosphäre, in der sich Kolleginnen und Kollegen auf Augenhöhe begegnen. Sie bauen Barrieren ab, stärken Vertrauen und das Wir-Gefühl, bringen auch interkulturelle Teams zusammen und helfen, gewohnte Denkmuster zu durchbrechen. Zudem lockern sie monotone Abläufe auf und senken den Stresspegel.

Eine Viertelstunde am Tischkicker verändert einen durchgetakteten Arbeitstag allerdings wenig. Nachhaltig wirken spielerische Formate, wenn sie echten Spielraum im Arbeitsalltag schaffen – nicht als Dekoration, sondern als Haltung.

## Resilienzspiele

- Slug: resilienz-spiele
- Kategorie: Spielbasierte Methoden
- Kurz: Spiele, die gezielt die Widerstandskraft von Mitarbeitenden und Teams fördern.
- Siehe auch: resilienz; resilienzfoerderung; mdad; resilienzfaktoren

Mit Spielkarten und einem interaktiven Spielfeld werden berufliche Situationen aufgegriffen, in denen Teilnehmende Entscheidungen treffen, mit Belastungen umgehen und Krisen bewältigen. So werden Resilienzfaktoren erlebbar und individuelle Unterschiede im Umgang mit Stress bewusst.

## play2change-Methode

- Slug: play2change
- Kategorie: Spielbasierte Methoden
- Auch: PLAY, EARN, TRANSFER
- Kurz: Methode von MENSCH DENK AN DICH®, die Veränderungsprozesse in drei Phasen strukturiert – vom Spiel bis zur Umsetzung im Alltag.
- Siehe auch: mdad; playfulness; probehandeln; change-management

- **PLAY:** gemeinsame Ideenentwicklung: Gezielte Fragen bringen Menschen ins Gespräch, Hierarchien treten zurück, Herausforderungen können ohne Druck angesprochen werden.
- **EARN:** Erkenntnisse festigen: Die Teilnehmenden reflektieren eigene Stärken und Ressourcen und entwickeln Lösungsansätze.
- **TRANSFER:** Umsetzung: Ideen werden in konkrete Maßnahmen und Ziele für den Arbeitsalltag übersetzt.

Der Transfer sorgt dafür, dass die im Spiel erarbeiteten Lösungen nicht im Workshop bleiben, sondern langfristig wirken. Dafür ist das Spiel in einen übergeordneten Veränderungsprozess eingebettet: Interventionsfragen, Vereinbarungen, Workshops oder Prozessbegleitung verankern das neue Verhalten.

play2change versteht Spielen ausdrücklich nicht als Belohnungssystem, sondern als Erfahrungsraum – im Sinne von Playfulness statt Gamification.

## MENSCH DENK AN DICH®

- Slug: mdad
- Kategorie: Spielbasierte Methoden
- Kurz: Wissenschaftlich evaluiertes Serious Game für Resilienz, Gesundheitsförderung und Organisationsentwicklung, entwickelt von der Psychologin Dr. Irene Preußner.
- Siehe auch: playfulness; play2change; spiele-coach; probehandeln

Die Idee zu dem Brettspiel entstand 2016 aus der Erfahrung, wie schwer es vielen Menschen fällt, ihre Ressourcen im Arbeitsalltag zur Stressbewältigung zu nutzen. Gespielt wird mit Spielbrett, Figuren und Aktionskarten, meist rund 90 Minuten mit bis zu zwölf Personen in kleinen Teams. Das Motto lautet, sich selbst und andere zu stärken.

MENSCH DENK AN DICH® ist bewusst kein Wettkampf und kein Belohnungssystem, sondern ein Erfahrungsraum im Sinne von Playfulness. Anders als in klassischen Planspielen gibt es kein künstliches Szenario: Die Spielenden bringen echte Situationen aus ihrem Arbeitsalltag ein. Die Regeln dürfen gemeinsam angepasst werden, wenn eine Aufgabe zu stressig wirkt. Das Spiel verbindet Ansätze aus der Positiven Psychologie und der Systemischen Beratung.

Es gibt Spielvarianten für das Handeln als Führungskraft und für die eigene Resilienz. Eingesetzt wird das Spiel branchen- und hierarchieübergreifend in Trainings, Teamentwicklung, Führungskräfte-Coaching und Veränderungsprozessen. Die Methode wurde 2024 mit dem Europäischen Trainingspreis in Gold und 2026 mit dem ersten Platz beim NewWork Business Award in der Kategorie Leadership Training ausgezeichnet.

## Spiele-Coach

- Slug: spiele-coach
- Kategorie: Spielbasierte Methoden
- Auch: Spielleiterin; Spielleiter
- Kurz: Für MENSCH DENK AN DICH® qualifizierte Spielleitung, die das Spiel in Teams und Organisationen professionell anleitet.
- Siehe auch: mdad; personalentwicklung; weiterbildung

Die Qualifizierung erfolgt in einem zweitägigen, intensiven Training mit Selbstlernphasen sowie Erfahrungs- und Wissensinput. Unternehmen können auch interne Coaches, Beratende, Trainerinnen und Trainer oder Führungskräfte zu Spiele-Coaches ausbilden lassen und so spielerische Methoden dauerhaft in der eigenen Personal- und Organisationsentwicklung verankern.
