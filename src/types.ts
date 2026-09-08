export type SensorStatus = "online" | "offline";

export interface Sensor {
  id: string;
  name: string;
  roomId: string;
  status: SensorStatus;
  battery: number | null; // null = alimentado por cable, sin batería
  lastSeen: string; // ISO
  firmware: string;
}

export interface Room {
  id: string;
  name: string;
  icon: RoomIcon;
}

export type RoomIcon =
  | "living-room"
  | "bedroom"
  | "bathroom"
  | "kitchen"
  | "hallway"
  | "other";

export type EventStatus =
  | "active" // alerta disparada, sin resolver, cuenta regresiva corriendo
  | "escalated" // nadie confirmó a tiempo, se llamó al siguiente contacto
  | "confirmed_fall" // un cuidador confirmó que es una caída real
  | "confirmed_ok" // un cuidador confirmó que la persona está bien
  | "false_alarm"; // descartada como falsa alarma

export type EventConfidence = "alta" | "media";

export interface FallEvent {
  id: string;
  roomId: string;
  sensorId: string;
  detectedAt: string; // ISO
  status: EventStatus;
  confidence: EventConfidence;
  resolvedAt?: string;
  resolvedBy?: string; // memberId
}

export type MemberRole = "admin" | "cuidador";

export interface FamilyMember {
  id: string;
  name: string;
  role: MemberRole;
  phone: string;
  avatarColor: string;
  isEmergencyContact: boolean;
  escalationOrder: number | null; // 1 = primero al que se llama, null = no participa del escalado
  isYou?: boolean;
}

export interface FamilySettings {
  sensitivity: "baja" | "media" | "alta";
  doNotDisturbUntil: string | null; // ISO, null = desactivado
  escalationTimeoutSeconds: number;
  notifyPush: boolean;
  notifySms: boolean;
  notifyCall: boolean;
}

export interface FamilyState {
  familyName: string;
  houseName: string;
  rooms: Room[];
  sensors: Sensor[];
  members: FamilyMember[];
  events: FallEvent[];
  settings: FamilySettings;
}
