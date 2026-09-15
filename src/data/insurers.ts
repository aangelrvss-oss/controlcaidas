export interface Insurer {
  id: string;
  name: string;
  tag?: string;
}

export const insurers: Insurer[] = [
  { id: "mapfre", name: "Mapfre", tag: "Taller Distinguido · Club Mapfre" },
  { id: "axa", name: "AXA", tag: "AXA Calidad" },
  { id: "mutua", name: "Mutua Madrileña", tag: "Concertado" },
  { id: "pelayo", name: "Pelayo", tag: "Concertado" },
  { id: "allianz", name: "Allianz", tag: "Concertado" },
  { id: "otras", name: "Otras aseguradoras", tag: "Leasing / Renting" },
];
