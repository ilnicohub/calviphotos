async function loadGalleries(){
  const container = document.getElementById('galleries');
  try{
    const res = await fetch('/galleries.json');
    if(!res.ok) throw new Error('galleries.json non trovato');
    const galleries = await res.json();
    if(!galleries.length){ container.innerHTML = '<p class="subtitle">Nessuna galleria trovata. Carica le tue foto nella cartella `photos/`.</p>'; return }

    galleries.forEach(g=>{
      const a = document.createElement('a');
      a.className = 'card';
      a.href = `/gallery.html?g=${encodeURIComponent(g.folder)}`;
      a.innerHTML = `
        <img loading="lazy" src="${g.preview}" alt="${escapeHtml(g.title)}">
        <div class="meta">
          <div class="title">${escapeHtml(g.title)}</div>
          <div class="subtitle">${g.count} foto</div>
        </div>`;
      container.appendChild(a);
    })
  }catch(err){
    container.innerHTML = `<p class="subtitle">Errore: ${err.message}</p>`
  }
}

function escapeHtml(s){ return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])) }

loadGalleries();
