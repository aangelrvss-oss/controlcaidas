import gsap from "gsap"
import { ScrollTrigger } from "gsap/ScrollTrigger"

let registered = false

export function getGsapCore() {
  if (!registered) {
    gsap.registerPlugin(ScrollTrigger)
    registered = true
  }
  return { gsap, ScrollTrigger }
}
