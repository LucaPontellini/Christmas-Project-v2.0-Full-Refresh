document.addEventListener("DOMContentLoaded", () => {

    let audio = document.getElementById("bg-music");

    if (!audio) {
        audio = document.createElement("audio");
        audio.id = "bg-music";
        audio.src = "/static/music/Jazzy_Smile.mp3";
        audio.loop = true;
        audio.volume = 0.35;
        document.body.appendChild(audio);
    }

    audio.play().catch(() => {
        document.addEventListener("click", () => audio.play(), { once: true });
    });

});