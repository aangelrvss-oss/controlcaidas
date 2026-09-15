export interface ServiceOption {
  id: string;
  name: string;
  description: string;
}

export const serviceOptions: ServiceOption[] = [
  { id: "golpe", name: "Golpe", description: "Abolladuras y daños por impacto" },
  { id: "rozadura", name: "Rozadura", description: "Arañazos y roces de pintura" },
  { id: "parte", name: "Parte de Seguro", description: "Siniestro con compañía aseguradora" },
  { id: "mecanica", name: "Mecánica de Siniestro", description: "Daños mecánicos tras un accidente" },
  { id: "pulido", name: "Pulido", description: "Detailing y pulido de carrocería" },
];
