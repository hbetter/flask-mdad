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

      function applyBrandStyles(root) {
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
         zu einem Durchlauf pro Frame zusammengefasst. */
      function applyAll() {
        document.querySelectorAll('form._form').forEach(applyBrandStyles);
      }
      var scheduled = false;
      new MutationObserver(function () {
        if (scheduled) return;
        scheduled = true;
        requestAnimationFrame(function () { scheduled = false; applyAll(); });
      }).observe(document.body, { childList: true, subtree: true });
      applyAll();
    })();
