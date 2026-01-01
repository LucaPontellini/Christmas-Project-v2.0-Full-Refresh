document.addEventListener("DOMContentLoaded", () => {

    /* MUSICA DI BACKGROUND */
    const audio = new Audio("/static/music/Invisible_Cities.mp3");
    audio.loop = true;
    audio.volume = 1;

    audio.play().catch(() => {
        document.addEventListener("click", () => {
            audio.play();
        }, { once: true });
    });

    /* FUNZIONE REVEAL */
    function revealElement(el, duration = 1.6) {
        el.style.transition =
            `opacity ${duration}s cubic-bezier(0.22, 1, 0.36, 1),
             transform ${duration}s cubic-bezier(0.22, 1, 0.36, 1)`;
        el.style.opacity = "1";
        el.style.transform = "translateY(0)";
        el.classList.add("is-visible");
    }

    /* TIMELINE UX FRIENDLY (~15s) */

    // OMINO + TITOLO — 2.5s
    setTimeout(() => {
        document.querySelectorAll(".reveal-hero")
            .forEach(el => revealElement(el, 2));
    }, 2500);

    // BOX INFO — 5.5s
    setTimeout(() => {
        const box = document.querySelector(".reveal-box");
        revealElement(box, 1.8);
    }, 5500);

    // LINK — 6s → 11s
    const links = document.querySelectorAll(".reveal-link");
    let linkDelay = 6500;

    links.forEach(link => {
        setTimeout(() => {
            revealElement(link, 1.5);
        }, linkDelay);

        linkDelay += 1500; // ritmo elegante ma vivo
    });

    // PLAY — 12.5s (chiusura)
    setTimeout(() => {
        const play = document.querySelector(".reveal-play");
        revealElement(play, 1.6);
    }, 12500);

});