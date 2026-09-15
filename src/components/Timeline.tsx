import { useLayoutEffect, useRef } from "react";
import { ensureGsapRegistered, gsap } from "../lib/gsap";
import { timelineMilestones } from "../data/timeline";

export function Timeline() {
  const sectionRef = useRef<HTMLElement>(null);

  useLayoutEffect(() => {
    ensureGsapRegistered();
    const ctx = gsap.context(() => {
      gsap.to(".timeline-progress", {
        scaleY: 1,
        ease: "none",
        scrollTrigger: {
          trigger: sectionRef.current,
          start: "top 60%",
          end: "bottom 70%",
          scrub: true,
        },
      });

      gsap.utils.toArray<HTMLElement>(".timeline-item").forEach((item) => {
        gsap.fromTo(
          item,
          { opacity: 0, x: -30 },
          {
            opacity: 1,
            x: 0,
            duration: 0.7,
            ease: "power2.out",
            scrollTrigger: {
              trigger: item,
              start: "top 80%",
            },
          },
        );
      });
    }, sectionRef);

    return () => ctx.revert();
  }, []);

  return (
    <section id="trayectoria" ref={sectionRef} className="relative bg-titanium-950 px-6 py-28 sm:px-10">
      <div className="mx-auto max-w-4xl">
        <p className="font-kinetic text-center text-xs uppercase tracking-[0.35em] text-cyan-400">
          Nuestra historia
        </p>
        <h2 className="font-kinetic mt-2 text-center text-3xl font-bold uppercase text-white sm:text-5xl">
          1968 → Hoy
        </h2>

        <div className="relative mt-20 pl-10 sm:pl-16">
          <div className="absolute left-3 top-0 h-full w-[2px] bg-white/10 sm:left-5" />
          <div className="timeline-progress absolute left-3 top-0 h-full w-[2px] origin-top scale-y-0 bg-gradient-to-b from-cyan-400 to-yellow-500 sm:left-5" />

          <div className="flex flex-col gap-16">
            {timelineMilestones.map((milestone) => (
              <div key={milestone.year} className="timeline-item relative">
                <span className="absolute -left-10 top-1 flex h-6 w-6 items-center justify-center rounded-full border-2 border-yellow-500 bg-titanium-950 sm:-left-16">
                  <span className="h-2.5 w-2.5 rounded-full bg-yellow-500" />
                </span>
                <span className="font-kinetic text-sm font-bold uppercase tracking-widest text-yellow-500">
                  {milestone.year}
                </span>
                <h3 className="font-kinetic mt-1 text-2xl font-bold text-white sm:text-3xl">
                  {milestone.title}
                </h3>
                <p className="mt-2 max-w-xl text-sm text-white/60 sm:text-base">
                  {milestone.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
