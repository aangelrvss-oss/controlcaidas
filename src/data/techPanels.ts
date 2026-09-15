import { MEDIA } from "./media";

export interface TechPanel {
  index: string;
  title: string;
  description: string;
  video: string;
}

export const techPanels: TechPanel[] = [
  {
    index: "01",
    title: "Pintura Ecológica al Agua RM",
    description:
      "Sistema de pintura al agua respetuoso con el medio ambiente, con réplica idéntica del color de fábrica gracias a cabinas de última generación.",
    video: MEDIA.paintBooth,
  },
  {
    index: "02",
    title: "Bancada Universal de Alta Precisión",
    description:
      "Estructura y alineación perfecta del chasis tras una colisión, con escaneo digital y medición milimétrica.",
    video: MEDIA.chassisScan,
  },
  {
    index: "03",
    title: "Servicio Integral de Siniestros",
    description:
      "Mecánica pesada, recarga de aire acondicionado y diagnosis completa de averías derivadas de un impacto.",
    video: MEDIA.ceramicParticles,
  },
  {
    index: "04",
    title: "Detailing & Entrega VIP",
    description:
      "Pulido de precisión y lavado exterior completo gratuito tras cada reparación. Tu coche, como el primer día.",
    video: MEDIA.waterDroplet,
  },
];
