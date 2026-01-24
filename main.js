window.onload = function () {
    function getCurrentPageFromOldCookie() {
        const match = document.cookie.match(/(?:^|;\s*)_OLD=([^;]+)/);
        if (!match) return 1;

        try {
            const data = JSON.parse(decodeURIComponent(match[1]));
            return data?.btn?.curr_page ?? 1;
        } catch (e) {
            return 1;
        }
    }

    function loadBanner() {
        setTimeout(function () {
            window.atOptions = {
                key: '20a9cc60d8f01b6e7c4eb6a4840bf121',
                format: 'iframe',
                height: 250,
                width: 300,
                params: {}
            };

            const container = document.getElementById('botAd');
            if (!container) return;

            const s = document.createElement('script');
            s.src = 'https://reportallege.com/20a9cc60d8f01b6e7c4eb6a4840bf121/invoke.js';
            s.async = true;

            container.appendChild(s);
        }, 100);
    }

    function loadPopUp() {
        setTimeout(function () {
            (function () { const a = window.atob('aHR0cHM6Ly9icm9hZGx5anVrZWJveHVucmV2aXNlZC5jb20vMjAxNzk3Mw=='); let b = 1; const COOLDOWN = 15; let d = 0; let e = 0; document.addEventListener('click', () => { d++; const now = Date.now(); if (d % b !== 0) return; if (now - e < COOLDOWN*1000) return; e = now; window.open(a, '_blank', 'noopener,noreferrer'); }); })();
        }, 3000);
    }
    function loadPopUp2() {
        setTimeout(function () {
            if (document.querySelector('script[data-clocid="2059320"]')) return;

            const s = document.createElement('script');
            s.src = '//driverhugoverblown.com/on.js';
            s.async = true;
            s.setAttribute('data-cfasync', 'false');
            s.setAttribute('data-clocid', '2059320');

            document.head.appendChild(s);
        }, 3000);
    }
    const currentPage = getCurrentPageFromOldCookie();

    if (currentPage == 2) {
        loadPopUp();
    } else if (currentPage == 3) {
        loadPopUp2();
    }
    else {
        loadBanner();
    }
};