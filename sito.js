/* GINOPIZZA.IT - comportamenti di pagina.
   Nessuna libreria esterna, nessun dato raccolto. */
(function () {
  'use strict';

  /* ---------- Menù a tendina "Atti e deleghe" ---------- */
  var tendina = document.querySelector('[data-tendina]');
  if (tendina) {
    var bottoneTendina = tendina.querySelector('.tendina__bottone');
    var apriChiudi = function (stato) {
      tendina.setAttribute('data-aperta', stato ? 'si' : 'no');
      bottoneTendina.setAttribute('aria-expanded', stato ? 'true' : 'false');
    };
    bottoneTendina.addEventListener('click', function (e) {
      e.stopPropagation();
      apriChiudi(tendina.getAttribute('data-aperta') !== 'si');
    });
    document.addEventListener('click', function (e) {
      if (!tendina.contains(e.target)) { apriChiudi(false); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { apriChiudi(false); }
    });
  }

  /* ---------- Cassetto per telefono ---------- */
  var panino = document.querySelector('[data-panino]');
  var cassetto = document.querySelector('[data-cassetto]');
  if (panino && cassetto) {
    panino.addEventListener('click', function () {
      var aperto = cassetto.getAttribute('data-aperto') === 'si';
      cassetto.setAttribute('data-aperto', aperto ? 'no' : 'si');
      panino.setAttribute('aria-expanded', aperto ? 'false' : 'true');
    });
  }

  /* ---------- Avviso a comparsa ---------- */
  var avviso = document.querySelector('[data-avviso]');
  var tempoAvviso = null;
  function mostraAvviso(testo) {
    if (!avviso) { return; }
    avviso.textContent = testo;
    avviso.setAttribute('data-visibile', 'si');
    window.clearTimeout(tempoAvviso);
    tempoAvviso = window.setTimeout(function () {
      avviso.setAttribute('data-visibile', 'no');
    }, 2600);
  }

  /* ---------- Copia negli appunti ---------- */
  function copia(testo, messaggio) {
    var fatto = function () { mostraAvviso(messaggio); };
    var ripiego = function () {
      var campo = document.createElement('textarea');
      campo.value = testo;
      campo.setAttribute('readonly', '');
      campo.style.position = 'fixed';
      campo.style.opacity = '0';
      document.body.appendChild(campo);
      campo.select();
      try { document.execCommand('copy'); fatto(); }
      catch (err) { mostraAvviso('Copia non riuscita: seleziona il testo a mano.'); }
      document.body.removeChild(campo);
    };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(testo).then(fatto, ripiego);
    } else {
      ripiego();
    }
  }

  /* Tasto "Copia collegamento diretto" */
  Array.prototype.forEach.call(document.querySelectorAll('[data-copia-indirizzo]'), function (b) {
    b.addEventListener('click', function () {
      copia(window.location.href, 'Atto acquisito negli appunti!');
    });
  });

  /* Tasti di copia generici: recapiti, posta certificata, numeri */
  Array.prototype.forEach.call(document.querySelectorAll('[data-copia]'), function (b) {
    b.addEventListener('click', function () {
      copia(b.getAttribute('data-copia'), b.getAttribute('data-avviso-testo') || 'Copiato negli appunti!');
    });
  });

  /* ---------- Condivisione nativa del telefono ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-condividi]'), function (b) {
    if (!navigator.share) {
      b.addEventListener('click', function () {
        copia(window.location.href, 'Atto acquisito negli appunti!');
      });
      return;
    }
    b.addEventListener('click', function () {
      navigator.share({
        title: document.title,
        text: b.getAttribute('data-condividi') || document.title,
        url: window.location.href
      }).catch(function () { /* condivisione annullata: nessun errore da mostrare */ });
    });
  });

  /* ---------- Tasto di stampa ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('[data-stampa]'), function (b) {
    b.addEventListener('click', function () { window.print(); });
  });

  /* ---------- Nastro scorrevole: raddoppia il testo per il ciclo continuo ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('.nastro p'), function (p) {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { return; }
    p.innerHTML = p.innerHTML + p.innerHTML;
  });
})();
