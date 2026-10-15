/* Script zu static/css/ac-formulare.css - erzwingt per Inline-Style
   (mit !important) die wenigen Werte, die ActiveCampaign selbst per
   id-basiertem "!important"-CSS setzt (Absende-Button, Eingabefarbe),
   und blendet vergangene Termine aus den Auswahllisten aus. Ausgelagert
   aus templates/alle_ac_formulare.html - siehe dort fuer den
   Einbindungs-Kontext. Erfasst automatisch jedes AC-Formular der Seite
   (form._form), auch nachtraeglich eingefuegte. */
    (function () {
      var SUBMIT_STYLE = {
        'background-color': '#9C0E17',
        'background-image': 'none',
        'border': 'none',
        'border-radius': '.5rem',
        'padding': '.625rem 1rem',
        'color': '#ffffff',
      };
      var SUBMIT_HOVER_BG = '#e30613';
      var INPUT_TEXT_COLOR = '#212529';

      function setImportant(el, styles) {
        Object.keys(styles).forEach(function (prop) {
          el.style.setProperty(prop, styles[prop], 'important');
        });
      }

      function styleSubmit(el) {
        if (el.dataset.brandStyled) return;
        el.dataset.brandStyled = '1';
        setImportant(el, SUBMIT_STYLE);
        el.addEventListener('mouseenter', function () {
          el.style.setProperty('background-color', SUBMIT_HOVER_BG, 'important');
        });
        el.addEventListener('mouseleave', function () {
          el.style.setProperty('background-color', SUBMIT_STYLE['background-color'], 'important');
        });
      }

      /* Vergangene Termine aus den Auswahllisten entfernen.
         Die Optionen sind in ActiveCampaign in zwei Formaten gepflegt:
           - eintägig:  "Ort - TT.MM.JJ"     (z. B. "Berlin - 21.01.27")
           - zweitägig: "Ort - TT/TT.MM.JJ"  (z. B. "Essen - 28/29.10.26")
         Maßgeblich ist jeweils der (erste) Veranstaltungstag: Jede
         Option, deren erster Tag vor dem heutigen Tag liegt, wird
         entfernt; am ersten Veranstaltungstag selbst bleibt sie noch
         sichtbar. Optionen ohne erkennbares Datum
         (z. B. die leere Platzhalter-Option) bleiben unangetastet.
         Stichtag ist die Uhr des Besuchers. Sind keine Termine mehr
         übrig, erscheint ein deaktivierter Hinweis in der Liste. */
      // Gruppe 1: (erster) Tag, Gruppe 2: optionaler zweiter Tag nach "/",
      // Gruppe 3: Monat, Gruppe 4: Jahr (zwei- oder vierstellig).
      var DATE_RE = /(\d{1,2})(?:\s*\/\s*(\d{1,2}))?\.(\d{1,2})\.(\d{2}|\d{4})(?!\d)/;
      var NO_DATES_TEXT = 'Aktuell keine Termine verfügbar';

      function filterPastDates(select) {
        var today = new Date();
        today.setHours(0, 0, 0, 0);
        var hadDates = false;
        Array.prototype.slice.call(select.options).forEach(function (opt) {
          var m = (opt.value || opt.textContent).match(DATE_RE);
          if (!m) return;
          hadDates = true;
          var year = parseInt(m[4], 10);
          if (year < 100) year += 2000;
          var date = new Date(year, parseInt(m[3], 10) - 1, parseInt(m[1], 10));
          if (date < today) opt.remove();
        });
        if (hadDates && !select.dataset.noDatesHint) {
          var left = Array.prototype.some.call(select.options, function (o) {
            return DATE_RE.test(o.value || o.textContent);
          });
          if (!left) {
            select.dataset.noDatesHint = '1';
            var hint = document.createElement('option');
            hint.textContent = NO_DATES_TEXT;
            hint.value = '';
            hint.disabled = true;
            select.appendChild(hint);
          }
        }
      }

      /* Layout-Klassen (siehe ac-formulare.css, "Kompakte, handy-
         freundliche Anordnung") und passende Tastatur/Autovervoll-
         staendigung je Feld. Erkannt wird ueber den Feldnamen, weil die
         CSS-Klassen der Felder bei ActiveCampaign je Formular variieren.
         field[9]..field[13] sind in allen Formularen Firma, Strasse,
         PLZ und Stadt. */
      var FIELD_SETUP = {
        'firstname':  { layout: 'ac-half', autocomplete: 'given-name' },
        'lastname':   { layout: 'ac-half', autocomplete: 'family-name' },
        // type bewusst NICHT aendern: ActiveCampaign erkennt E-Mail- und
        // Telefonfeld am type="text" und meldet sonst beim Absenden
        // "Formulare muessen ein E-Mail-Feld oder ein Telefonfeld enthalten".
        // inputmode reicht fuer die passende Handy-Tastatur.
        'email':      { layout: 'ac-half-md', inputmode: 'email', autocomplete: 'email' },
        'phone-iti':  { layout: 'ac-half-md', inputmode: 'tel', autocomplete: 'tel' },
        'field[9]':   { autocomplete: 'organization' },
        'field[10]':  { autocomplete: 'street-address' },
        'field[12]':  { layout: 'ac-zip', inputmode: 'numeric', autocomplete: 'postal-code' },
        'field[13]':  { layout: 'ac-city', autocomplete: 'address-level2' },
      };

      function setupFields(root) {
        root.querySelectorAll('input[name]').forEach(function (input) {
          var setup = FIELD_SETUP[input.name];
          // Versteckte Hilfsfelder (z. B. das von intl-tel-input befuellte
          // "phone") nie anfassen - ein geaenderter type macht sie sichtbar.
          if (!setup || input.type === 'hidden' || input.dataset.fieldSetup) return;
          input.dataset.fieldSetup = '1';
          if (setup.type) input.type = setup.type;
          if (setup.inputmode) input.setAttribute('inputmode', setup.inputmode);
          if (setup.autocomplete) input.setAttribute('autocomplete', setup.autocomplete);
          var wrapper = input.closest('._form_element');
          if (wrapper && setup.layout) wrapper.classList.add(setup.layout);
        });
      }

      /* Doppelte IDs vermeiden: Alle AC-Formulare stehen gleichzeitig auf
         jeder Seite (base.html) und verwenden dieselben IDs ("firstname",
         "email", "phone", die Laenderauswahl "iti-0__..."). Dann zeigt
         <label for="email"> im Webinar-Formular auf das Feld im Spielraum-
         Formular - Screenreader lesen falsche Bezuege vor, ein Klick auf die
         Beschriftung springt ins falsche Formular. Jede ID, die im Dokument
         mehrfach vorkommt, bekommt deshalb das Formular als Praefix; Verweise
         darauf (label[for], aria-*) innerhalb des Formulars werden mitgezogen.
         Laeuft bei jeder Aenderung erneut, damit auch spaeter eingefuegte
         Elemente (Fehlermeldungen, Laenderliste) erfasst werden. */
      var REF_ATTRS = ['aria-controls', 'aria-describedby', 'aria-labelledby',
                       'aria-owns', 'aria-activedescendant', 'list'];

      // idCounts: Anzahl je ID im ganzen Dokument, einmal pro Durchlauf
      // gezaehlt (sonst muesste fuer jedes der ~250 Elemente der
      // Laenderliste das ganze Dokument durchsucht werden).
      function countIds() {
        var counts = Object.create(null);
        document.querySelectorAll('[id]').forEach(function (el) {
          counts[el.id] = (counts[el.id] || 0) + 1;
        });
        return counts;
      }

      function uniquifyIds(form, index, idCounts) {
        var prefix = (form.id || ('acform' + index)).replace(/[^A-Za-z0-9_-]/g, '');
        var renamed = Object.create(null);
        form.querySelectorAll('[id]').forEach(function (el) {
          var id = el.id;
          if (!id || id.indexOf(prefix + '-') === 0 || (idCounts[id] || 0) < 2) return;
          var newId = prefix + '-' + id;
          el.id = newId;
          idCounts[id] -= 1;
          idCounts[newId] = 1;
          renamed[id] = newId;
        });
        if (!Object.keys(renamed).length) return;
        form.querySelectorAll('label[for]').forEach(function (label) {
          if (renamed[label.htmlFor]) label.htmlFor = renamed[label.htmlFor];
        });
        REF_ATTRS.forEach(function (attr) {
          form.querySelectorAll('[' + attr + ']').forEach(function (ref) {
            var parts = ref.getAttribute(attr).split(/\s+/);
            var changed = false;
            parts = parts.map(function (p) {
              if (renamed[p]) { changed = true; return renamed[p]; }
              return p;
            });
            if (changed) ref.setAttribute(attr, parts.join(' '));
          });
        });
      }

      function applyBrandStyles(root, index, idCounts) {
        uniquifyIds(root, index, idCounts);
        setupFields(root);
        root.querySelectorAll('select').forEach(filterPastDates);
        root.querySelectorAll('._submit').forEach(styleSubmit);
        root.querySelectorAll(
          'input[type="text"], input[type="email"], input[type="tel"], input[type="date"], input[type="number"], select, textarea'
        ).forEach(function (el) {
          el.style.setProperty('color', INPUT_TEXT_COLOR, 'important');
        });
      }

      /* Alle AC-Formulare der Seite erfassen - auch solche, die
         ActiveCampaign erst nach dem Laden einsetzt. Kein Pflegen einer
         Formularliste nötig. Mehrere Änderungen in kurzer Folge werden
         zu einem Durchlauf zusammengefasst. */
      function applyAll() {
        var idCounts = countIds();
        document.querySelectorAll('form._form').forEach(function (form, index) {
          applyBrandStyles(form, index, idCounts);
        });
      }
      var scheduled = false;
      new MutationObserver(function () {
        if (scheduled) return;
        scheduled = true;
        // setTimeout statt requestAnimationFrame: laeuft auch in Hintergrund-
        // Tabs, wo die Formulare von ActiveCampaign ebenfalls nachladen.
        setTimeout(function () { scheduled = false; applyAll(); }, 50);
      }).observe(document.body, { childList: true, subtree: true });
      applyAll();
    })();
