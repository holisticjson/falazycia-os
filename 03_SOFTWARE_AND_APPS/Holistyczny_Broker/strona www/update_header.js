const fs = require('fs');
const glob = require('glob');

const newHeader = `    <header class="fixed w-full z-50 glass-panel border-b border-white/10 transition-all duration-300">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-24">
                <a href="index.html" class="flex items-center gap-4 group">
                    <img src="logo.png" alt="Logo Holistyczny Broker" class="h-16 w-16 object-contain transition-all duration-500 group-hover:scale-110">
                    <span class="text-2xl md:text-3xl font-bold tracking-widest text-white uppercase flex flex-col leading-none">
                        <span>Holistyczny</span><span class="text-brand-gold text-xs md:text-sm tracking-[0.4em] mt-1">Broker</span>
                    </span>
                </a>
                <nav class="hidden md:flex items-center text-sm font-medium text-slate-300">
                    <!-- Dropdown B2B & Inwestycje -->
                    <div class="relative group px-4 py-6">
                        <button class="hover:text-white transition-colors flex items-center gap-1">B2B & Inwestycje 
                            <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                        </button>
                        <div class="absolute left-0 mt-2 w-64 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                            <div class="bg-brand-dark/90 backdrop-blur border border-brand-gold/30 rounded-lg shadow-xl py-2 mt-2">
                                <a href="inwestor-zastepczy-lodz-warszawa.html" class="block px-4 py-2 hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Inwestor Zastępczy</a>
                                <a href="grunty-komercyjne-off-market.html" class="block px-4 py-2 hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Grunty Off-Market</a>
                                <a href="technologia-ai-due-diligence.html" class="block px-4 py-2 hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">AI Due Diligence</a>
                            </div>
                        </div>
                    </div>

                    <!-- Dropdown B2C Premium -->
                    <div class="relative group px-4 py-6">
                        <button class="hover:text-white transition-colors flex items-center gap-1">B2C Premium 
                            <svg class="w-4 h-4 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                        </button>
                        <div class="absolute left-0 mt-2 w-56 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 z-50">
                            <div class="bg-brand-dark/90 backdrop-blur border border-brand-gold/30 rounded-lg shadow-xl py-2 mt-2">
                                <a href="nieruchomosci-premium.html" class="block px-4 py-2 hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Kolekcja Nieruchomości</a>
                                <a href="dla-ciebie.html" class="block px-4 py-2 hover:bg-brand-gold/10 hover:text-brand-gold transition-colors">Zgłoś do sprzedaży</a>
                            </div>
                        </div>
                    </div>

                    <!-- Single link -->
                    <a href="zasady-wspolpracy.html" class="px-4 hover:text-white transition-colors">Bezpieczeństwo (NDA)</a>

                    <a href="https://wa.me/48730882961?text=Dzie%C5%84%20dobry,%20kontaktuj%C4%99%20si%C4%99%20w%20sprawie%20wsp%C3%B3%C5%82pracy." target="_blank" class="ml-6 px-6 py-2.5 bg-brand-gold/10 border border-brand-gold/50 text-brand-gold hover:bg-brand-gold hover:text-brand-dark rounded transition-all">WhatsApp</a>
                </nav>
            </div>
        </div>
    </header>`;

const files = fs.readdirSync('.').filter(fn => fn.endsWith('.html'));

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    content = content.replace(/<header[\s\S]*?<\/header>/, newHeader);
    fs.writeFileSync(file, content, 'utf8');
    console.log('Updated', file);
});
