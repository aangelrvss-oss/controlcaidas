import { useLayoutEffect, useRef } from "react";
import { ensureGsapRegistered, gsap, ScrollTrigger } from "../lib/gsap";
import { techPanels } from "../data/techPanels";

export function TechShowcase() {
  const sectionRef = useRef<HTMLElement>(null);
  const trackRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    ensureGsapRegistered();
    const ctx = gsap.context(() => {
      const track = trackRef.current;
      const section = sectionRef.current;
      if (!track || !section) return;

      const panels = gsap.utils.toArray<HTMLElement>(".tech-panel");
      const scrollDistance = () => track.scrollWidth - window.innerWidth;

      const tween = gsap.to(track, {
        x: () => -scrollDistance(),
        ease: "none",
      });

      ScrollTrigger.create({
        trigger: section,
        start: "top top",
        end: () => `+=${scrollDistance()}`,
        pin: true,
        scrub: 1,
        animation: tween,
        invalidateOnRefresh: true,
      });

      panels.forEach((panel) => {
        gsap.fromTo(
          panel.querySelector(".tech-panel-content"),
          { opacity: 0.3, y: 40 },
          {
            opacity: 1,
            y: 0,
            ease: "none",
            scrollTrigger: {
              trigger: panel,
              containerAnimation: tween,
              start: "left 70%",
              end: "left 30%",
              scrub: true,
            },
          },
        );
      });
    }, sectionRef);

    return () => ctx.revert();
  }, []);

  return (
    <section id="tecnologia" ref={sectionRef} className="relative overflow-hidden bg-titanium-900">
      <div ref={trackRef} className="flex h-screen w-max">
        {techPanels.map((panel) => (
          <div
            key={panel.index}
            className="tech-panel relative flex h-screen w-screen shrink-0 items-center justify-center overflow-hidden border-r border-white/5"
          >
            <video
              className="absolute inset-0 h-full w-full object-cover opacity-45"
              autoPlay
              muted
              loop
              playsInline
            >
              <source src={panel.video} type="video/mp4" />
            </video>
            <div className="absolute inset-0 bg-gradient-to-t from-titanium-950 via-titanium-950/50 to-titanium-950/70" />

            <div className="tech-panel-content relative z-10 mx-auto flex max-w-2xl flex-col px-8 text-left sm:px-16">
              <span className="text-outline font-kinetic text-7xl font-extrabold sm:text-9xl">
                {panel.index}
              </span>
              <h3 className="font-kinetic mt-4 text-3xl font-bold uppercase text-white sm:text-5xl">
                {panel.title}
              </h3>
              <p className="mt-4 max-w-md text-sm text-white/70 sm:text-base">{panel.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
