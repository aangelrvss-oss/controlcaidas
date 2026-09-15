export const CONTACT = {
  address: "C. de la Polea, 29-31, 28522 Rivas-Vaciamadrid",
  phones: ["91 408 93 01", "91 499 05 84"],
  whatsapp: "638 93 16 12",
  whatsappNumber: "34638931612",
  jefeTaller: {
    name: "Agustín de la Fuente",
    role: "Jefe de Taller",
    phone: "687 89 69 05",
  },
  rating: 4.7,
  reviews: 360,
  founded: 1968,
  mapEmbedUrl:
    "https://www.google.com/maps?q=C.+de+la+Polea,+29,+28522+Rivas-Vaciamadrid&output=embed",
} as const;

export function buildWhatsappUrl(params: { aseguradora?: string; servicio?: string; vehiculo?: string }) {
  const { aseguradora, servicio, vehiculo } = params;
  const message =
    `¡Hola Carrocerías Pintauto! Quiero tramitar un parte/presupuesto. ` +
    `Aseguradora: ${aseguradora ?? "-"}. Servicio: ${servicio ?? "-"}. ` +
    `Mi vehículo es ${vehiculo ?? "-"}. At: Agustín de la Fuente.`;
  return `https://wa.me/${CONTACT.whatsappNumber}?text=${encodeURIComponent(message)}`;
}
