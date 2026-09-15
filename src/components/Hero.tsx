import { useLayoutEffect, useRef } from "react";
import { ensureGsapRegistered, gsap } from "../lib/gsap";
import { CONTACT } from "../data/contact";
import { MEDIA } from "../data/media";

export function Hero() {
  const sectionRef = useRef<HTMLElement>(null);
  const headlineRef = useRef<HTMLHeadingElement>(null);

  useLayoutEffect(() => {
    ensureGsapRegistered();
    const ctx = gsap.context(() => {
      gsap.fromTo(
        headlineRef.current,
        { letterSpacing: "0em", scale: 0.9, opacity: 0 },
        { letterSpacing: "0em", scale: 1, opacity: 1, duration: 1.4, ease: "power3.out", delay: 0.3 },
      );

      gsap.to(headlineRef.current, {
        letterSpacing: "0.05em",
        scale: 1.12,
        ease: "none",
        scrollTrigger: {
          trigger: sectionRef.current,
          start: "top top",
          end: "bottom top",
          scrub: true,
        },
      });

      gsap.to(".hero-bg-video", {
        scale: 1.25,
        ease: "none",
        scrollTrigger: {
          trigger: sectionRef.current,
          start: "top top",
          end: "bottom top",
          scrub: true,
        },
      });

      gsap.from(".hero-badge", {
        y: 24,
        opacity: 0,
        stagger: 0.15,
        duration: 0.9,
        delay: 0.9,
        ease: "power2.out",
      });
    }, sectionRef);

    return () => ctx.revert();
  }, []);

  return (
    <section
      id="inicio"
      ref={sectionRef}
      className="relative flex h-[100svh] min-h-[640px] w-full items-center justify-center overflow-hidden bg-titanium-950"
    >
      <video
        className="hero-bg-video absolute inset-0 h-full w-full object-cover opacity-60"
        autoPlay
        muted
        loop
        playsInline
      >
        <source src={MEDIA.heroTransformation} type="video/mp4" />
      </video>

      <div className="absolute inset-0 bg-gradient-to-b from-titanium-950/70 via-titanium-950/60 to-titanium-950" />
      <div className="bg-grid absolute inset-0 opacity-40" />

      <div className="relative z-10 flex w-full max-w-5xl flex-col items-center px-6 text-center">
        <p className="hero-badge font-kinetic mb-4 text-sm uppercase tracking-[0.4em] text-cyan-400">
          Rivas-Vaciamadrid · Desde {CONTACT.founded}
        </p>

        <h1
          ref={headlineRef}
          className="font-kinetic text-metal-shine text-4xl font-bold leading-[0.95] sm:text-6xl md:text-7xl lg:text-8xl"
        >
          MÁS DE 50 AÑOS
          <br />
          DE PERFECCIÓN
          <br />
          EN CARROCERÍA
        </h1>

        <p className="hero-badge mt-6 max-w-2xl text-base text-white/70 sm:text-lg">
          Chapa, pintura ecológica al agua y gestión integral de tu siniestro. Sin papeleos,
          sin complicaciones — nosotros hablamos con tu aseguradora.
        </p>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-3">
          <span className="hero-badge rounded-full border border-white/15 bg-white/5 px-4 py-2 font-kinetic text-xs uppercase tracking-widest text-white/80 backdrop-blur">
            Desde 1968
          </span>
          <span className="hero-badge rounded-full border border-cyan-500/30 bg-cyan-500/10 px-4 py-2 font-kinetic text-xs uppercase tracking-widest text-cyan-300 backdrop-blur">
            ★ {CONTACT.rating} ({CONTACT.reviews}+ Reseñas)
          </span>
          <span className="hero-badge rounded-full border border-red-500/30 bg-red-500/10 px-4 py-2 font-kinetic text-xs uppercase tracking-widest text-red-300 backdrop-blur">
            Taller Concertado Oficial
          </span>
        </div>

        <a
          href="#parte"
          className="hero-badge animate-neon-pulse mt-12 rounded-full bg-cyan-500 px-10 py-4 font-kinetic text-lg font-bold uppercase tracking-wide text-titanium-950 transition hover:bg-cyan-400"
        >
          Abrir Parte / Solicitar Cita
        </a>
      </div>

      <div className="absolute bottom-8 left-1/2 z-10 -translate-x-1/2 animate-bounce text-white/40">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M12 4v16m0 0-6-6m6 6 6-6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        </svg>
      </div>
    </section>
  );
}
