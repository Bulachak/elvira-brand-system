/**
 * Factory v2: Shared Component Logic
 * Features: Theme Switching, PDF Export (html-to-image + jsPDF), Content Injection, Author Attribution, Typography Fixes
 */

(function factoryV2() {
  const cfg = window.factoryConfig || window.clientConfig || {};

  // 1. Theme and CSS Variable Injection
  const updateStyles = (theme) => {
    document.documentElement.className = theme || 'theme-light';
    localStorage.setItem('factory-theme', theme);
  };

  const initTheme = () => {
    const savedTheme = localStorage.getItem('factory-theme') || 'theme-light';
    updateStyles(savedTheme);
  };

  // 2. Control Bar Rendering (Unified for all deliverables)
  const injectControlBar = () => {};

  // 3. Export Logic (Using html-to-image + jspdf as per preferred methodology)
  const loadScript = (src) => new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) return resolve();
    const s = document.createElement('script');
    s.src = src;
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });

  const exportPDF = async () => {
    const btn = document.querySelector('.cb-actions button:nth-child(2)') || document.body;
    const originalText = btn.innerText;
    if (btn.innerText) btn.innerText = "⏳ Loading...";

    if (typeof window.htmlToImage === 'undefined' || typeof window.jspdf === 'undefined') {
      try {
        await loadScript('https://cdnjs.cloudflare.com/ajax/libs/html-to-image/1.11.11/html-to-image.min.js');
        await loadScript('https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js');
      } catch (e) {
        alert('Failed to load PDF export engine. Check your internet connection.');
        if (btn.innerText) btn.innerText = originalText;
        return;
      }
    }

    if (btn.innerText) btn.innerText = "⏳ Generating...";

    setTimeout(() => {
      // Find the best capture area. Exclude the factory-control-bar if capturing the body.
      const node = document.getElementById('capture-area') || document.querySelector('.canvas-area') || document.body;
      const optFilename = (cfg.clientName || 'brand-strategy').toLowerCase().replace(/\s+/g, '-') + '.pdf';

      // Temporarily hide the control bar during body capture
      const controlBar = document.getElementById('factory-control-bar');
      if (node === document.body && controlBar) controlBar.style.display = 'none';

      window.htmlToImage.toPng(node, { backgroundColor: getComputedStyle(document.body).backgroundColor, pixelRatio: 1.5 })
        .then(function (dataUrl) {
            if (node === document.body && controlBar) controlBar.style.display = 'flex';
            
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF({ 
                orientation: node.offsetWidth > node.offsetHeight ? 'landscape' : 'portrait', 
                unit: 'px', 
                format: [node.offsetWidth, node.offsetHeight] 
            });
            
            pdf.addImage(dataUrl, 'PNG', 0, 0, node.offsetWidth, node.offsetHeight);
            pdf.save(optFilename);
            
            if (btn.innerText) btn.innerText = "✅ Done"; 
            setTimeout(() => { if (btn.innerText) btn.innerText = originalText; }, 2000);
        })
        .catch(function (error) {
            if (node === document.body && controlBar) controlBar.style.display = 'flex';
            console.error('PDF export failed!', error);
            if (btn.innerText) btn.innerText = "❌ Error"; 
            setTimeout(() => { if (btn.innerText) btn.innerText = originalText; }, 2000);
        });
    }, 100);
  };

  // 3.5. Smart Typography: Prevent Orphaned Words & Eradicate Em Dashes
  const fixTypography = () => {
    const elements = document.querySelectorAll('p, h1, h2, h3, h4, h5, h6, li, td, th, figcaption, blockquote');
    elements.forEach(el => {
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null, false);
      let node;
      while ((node = walker.nextNode())) {
        let text = node.nodeValue;
        
        // 0. Eradicate Em Dashes and En Dashes (Strict Copywriting Rule)
        text = text.replace(/\s*[—–]\s*/g, ' - ');
        
        // 1. Prevent single word orphans at the end of a block of text
        text = text.replace(/\s+([^\s]+)\s*$/, '\u00A0$1');
        
        // 2. Prevent strings of exactly 2 words from breaking
        text = text.replace(/^\s*([^\s]+)\s+([^\s]+)\s*$/, '$1\u00A0$2');
        
        if (node.nodeValue !== text) {
          node.nodeValue = text;
        }
      }
    });
  };

  // 4. Author Attribution Pattern (The "Invisible Signature")
  const injectFooterSignature = () => {
    const footer = document.querySelector('footer.brand-footer');
    if (footer) {
      footer.innerHTML = `
        <div class="footer-sign">
          Strategy &amp; Brand Architecture by <a href="https://bulachak.com" target="_blank" rel="noopener">Kamilla Gafurzianova, OLY</a> 
        </div>
      `;
    }
  };

  // 5. Fit to Screen for Slide Layouts (e.g., IG Stories, Carousels)
  const fitToScreen = () => {
    const wrappers = document.querySelectorAll('.slide-wrapper');
    wrappers.forEach(wrapper => {
      const slide = wrapper.querySelector('.slide');
      if (!slide) return;
      
      const originalW = slide.offsetWidth || 1080;
      const originalH = slide.offsetHeight || 1920;

      const controlBar = document.getElementById('factory-control-bar');
      const controls = document.querySelector('.controls');
      let offset = 80; 
      if (controlBar) offset += controlBar.offsetHeight;
      if (controls) offset += controls.offsetHeight;

      const availableW = window.innerWidth - 80; // Padding
      const availableH = window.innerHeight - offset;

      // Calculate scale to ensure it fits completely within the viewport
      const scale = Math.min(availableW / originalW, availableH / originalH);

      wrapper.style.width = `${originalW * scale}px`;
      wrapper.style.height = `${originalH * scale}px`;
      slide.style.transform = `scale(${scale})`;
      slide.style.transformOrigin = 'top left';
    });
  };

  // Export as Global API
  window.factory = {
    setTheme: updateStyles,
    exportPDF,
    toggleEdit: () => {
      document.body.classList.toggle('edit-mode');
    },
    init: () => {
      initTheme();
      injectControlBar();
      injectFooterSignature();
      fixTypography();
      fitToScreen();
    }
  };

  // Auto-init on load
  document.addEventListener('DOMContentLoaded', window.factory.init);
  window.addEventListener('resize', fitToScreen);
})();
