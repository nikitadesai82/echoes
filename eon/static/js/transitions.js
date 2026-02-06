document.addEventListener("DOMContentLoaded", () => {

    gsap.registerPlugin(ScrollTrigger);

    // Utility: splits headline lines and prepares them for animation
    function setupLineReveal(el) {
        const lines = el.innerHTML.split("<br>");
        el.innerHTML = "";
        return lines.map(line => {
            const wrap = document.createElement("div");
            wrap.classList.add("line-wrap");
            wrap.style.overflow = "hidden";

            const inner = document.createElement("div");
            inner.classList.add("line-inner");
            inner.style.transform = "translateY(100%)";
            inner.innerHTML = line;

            wrap.appendChild(inner);
            el.appendChild(wrap);

            return inner;
        });
    }

    // Initialize reveal for one section
    function initSection(section) {
        const bg = section.querySelector('[data-gsap="background"]');
        const headline = section.querySelector('[data-gsap="headline"]');
        const bodytext = section.querySelector('[data-gsap="bodytext"]');
        const visual = section.querySelector('[data-gsap="visual"]');

        let lines = [];
        if (headline) {
            lines = setupLineReveal(headline);
        }

        const tl = gsap.timeline({
            defaults: { ease: "power1.out" },
            scrollTrigger: {
                trigger: section,
                start: "top 75%",
            },
        });

        // HEADLINE REVEAL
        if (headline) {
            tl.to(lines.reverse(), {
                yPercent: 0,
                stagger: 0.15,
                duration: 0.6
            }, 0);
        }

        // BACKGROUND WIPE (if present)
        if (bg) {
            gsap.set(bg, { opacity: 0, clipPath: "inset(100% 0% 0% 0%)" });
            tl.to(bg, {
                opacity: 1,
                clipPath: "inset(0% 0% 0% 0%)",
                duration: 0.8,
                ease: "power1.inOut"
            }, 0.1);
        }

        // VISUAL IMAGE / VIDEO CLIPPATH REVEAL
        if (visual) {
            gsap.set(visual, { clipPath: "polygon(0 0, 100% 0, 100% 100%, 0 100%)", opacity: 0 });
            tl.to(visual, {
                opacity: 1,
                duration: 0.5
            }, ">-0.3");
        }

        // BODY TEXT FADE-IN
        if (bodytext) {
            gsap.set(bodytext, { opacity: 0, y: 20 });
            tl.to(bodytext, {
                opacity: 1,
                y: 0,
                duration: 0.4
            }, ">-0.3");
        }
    }

    // Apply animation to ANY section that contains GSAP elements
    document.querySelectorAll("[data-gsap-section]").forEach(section => {
        initSection(section);
    });

});
