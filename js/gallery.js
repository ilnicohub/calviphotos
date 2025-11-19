function qs(name){
  return new URLSearchParams(location.search).get(name);
}

async function loadGallery(){
  const folder = qs('g');
  const titleEl = document.getElementById('gallery-title');
  const photosEl = document.getElementById('photos');
  if(!folder){ titleEl.textContent = 'Galleria non specificata'; return }
  try{
    const res = await fetch(`/photos/${encodeURIComponent(folder)}/index.json`);
    if(!res.ok) throw new Error('index.json della galleria non trovato');
    const data = await res.json();
    titleEl.textContent = data.title || folder;
    data.images.forEach(img=>{
      const a = document.createElement('button');
      a.className = 'card';
      a.innerHTML = `<img loading="lazy" src="${img.thumb}" alt=""><div class="meta"><div class="title">${img.name}</div></div>`;
      a.addEventListener('click',()=> openLightbox(img.file));
      photosEl.appendChild(a);
    })
  }catch(err){
    photosEl.innerHTML = `<p class="subtitle">Errore: ${err.message}</p>`
  }
}

function openLightbox(src){
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lightbox-img');
  img.src = src; lb.classList.remove('hidden');
}

function closeLightbox(){
  const lb = document.getElementById('lightbox');
  const img = document.getElementById('lightbox-img');
  img.src = '';
  lb.classList.add('hidden');
}

document.getElementById('close-lightbox').addEventListener('click',closeLightbox);
document.getElementById('lightbox').addEventListener('click',(e)=>{ if(e.target.id==='lightbox') closeLightbox() });

loadGallery();
