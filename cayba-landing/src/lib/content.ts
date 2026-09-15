export const BRAND = {
  name: "CAYBA",
  legalName: "CAYBA S.L. — Mobiliario y Decoración",
  slogan: "Los Carpinteros del Barrio: de la tradición artesanal a la alta ebanistería a medida.",
  rating: 4.8,
  ratingCount: "Google Maps",
  since: "Siglo XX",
  city: "Rivas-Vaciamadrid",
  address: "C. de la Fresadora, 14, 28522 Rivas-Vaciamadrid, Madrid",
  phone: "635 42 89 69",
  phoneHref: "tel:+34635428969",
  whatsappHref: "https://wa.me/34635428969",
  email: "cayba@cayba.es",
  founders: "Manuel Carrillo y Manuel Barato",
} as const

export const WHATSAPP_MESSAGE_BASE =
  "Hola CAYBA, quiero pedir presupuesto para un mueble a medida."

export const SERVICES = [
  {
    id: "armarios",
    index: "01",
    title: "Armarios & Vestidores a Medida",
    description:
      "Interiores de vestidor diseñados al milímetro, puertas correderas silenciosas y herrajes de alta gama. Cada armario se fabrica para tu espacio, no al revés.",
    image: "/images/armario-vestidor.png",
    accent: "door",
  },
  {
    id: "palilleria",
    index: "02",
    title: "Palillería & Escaleras de Autor",
    description:
      "Listones de madera maciza compuestos como una partitura: escaleras, cabeceros y paneles con ritmo y sombra propios de la alta ebanistería.",
    image: "/images/palilleria-escaleras.png",
    accent: "slats",
  },
  {
    id: "bano-salon",
    index: "03",
    title: "Mobiliario de Baño & Salón",
    description:
      "Acabados resistentes a la humedad y al uso diario, con el mismo lenguaje de diseño contemporáneo en cada estancia de la casa.",
    image: "/images/bano-salon.png",
    accent: "panel",
  },
  {
    id: "reformas",
    index: "04",
    title: "Reformas Integrales & Locales",
    description:
      "Proyectos llave en mano para hogares y locales de Rivas-Vaciamadrid: del plano a la última mano de barniz, con un único interlocutor.",
    image: "/images/reformas-integrales.png",
    accent: "build",
  },
] as const

export const PROCESS_STEPS = [
  {
    id: 1,
    title: "Asesoramiento y Medición",
    description: "Visitamos tu espacio en Rivas-Vaciamadrid y tomamos medidas exactas al milímetro.",
  },
  {
    id: 2,
    title: "Diseño y Presupuesto",
    description: "Plano técnico, elección de maderas y acabados, y presupuesto cerrado sin sorpresas.",
  },
  {
    id: 3,
    title: "Fabricación Artesanal",
    description: "Cada pieza se corta, ensambla y lija en nuestro taller con oficio de generaciones.",
  },
  {
    id: 4,
    title: "Montaje Impecable",
    description: "Instalación cuidadosa en tu hogar, dejando el espacio listo para vivir.",
  },
] as const

export const FURNITURE_TYPES = [
  "Armario / Vestidor",
  "Escalera de diseño",
  "Cocina",
  "Mueble de salón",
  "Baño",
  "Reforma integral",
] as const

export const BEFORE_AFTER = {
  before: {
    label: "Antes",
    image: "/images/antes-despues-before.png",
  },
  after: {
    label: "Después",
    image: "/images/antes-despues-after.png",
  },
} as const
