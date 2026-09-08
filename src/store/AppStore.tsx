import { createContext, useCallback, useContext, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { initialFamilyState } from "../mockData";
import type { FallEvent, FamilyState } from "../types";

interface AppStoreValue {
  state: FamilyState;
  activeAlert: FallEvent | null;
  simulateFall: (roomId: string) => void;
  resolveEvent: (eventId: string, status: FallEvent["status"], memberId: string) => void;
  escalateEvent: (eventId: string) => void;
  toggleSensor: (sensorId: string) => void;
  updateSettings: (patch: Partial<FamilyState["settings"]>) => void;
  addMember: (name: string, phone: string) => void;
  removeMember: (memberId: string) => void;
  pairNewSensor: (roomName: string) => void;
}

const AppStoreContext = createContext<AppStoreValue | null>(null);

let eventCounter = 1000;

export function AppStoreProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<FamilyState>(initialFamilyState);

  const simulateFall = useCallback((roomId: string) => {
    setState((prev) => {
      const sensor = prev.sensors.find((s) => s.roomId === roomId);
      if (!sensor) return prev;
      const newEvent: FallEvent = {
        id: `event-sim-${eventCounter++}`,
        roomId,
        sensorId: sensor.id,
        detectedAt: new Date().toISOString(),
        status: "active",
        confidence: Math.random() > 0.3 ? "alta" : "media",
      };
      return { ...prev, events: [newEvent, ...prev.events] };
    });
  }, []);

  const resolveEvent = useCallback(
    (eventId: string, status: FallEvent["status"], memberId: string) => {
      setState((prev) => ({
        ...prev,
        events: prev.events.map((e) =>
          e.id === eventId
            ? { ...e, status, resolvedAt: new Date().toISOString(), resolvedBy: memberId }
            : e
        ),
      }));
    },
    []
  );

  const escalateEvent = useCallback((eventId: string) => {
    setState((prev) => ({
      ...prev,
      events: prev.events.map((e) => (e.id === eventId ? { ...e, status: "escalated" } : e)),
    }));
  }, []);

  const toggleSensor = useCallback((sensorId: string) => {
    setState((prev) => ({
      ...prev,
      sensors: prev.sensors.map((s) =>
        s.id === sensorId
          ? {
              ...s,
              status: s.status === "online" ? "offline" : "online",
              lastSeen: new Date().toISOString(),
            }
          : s
      ),
    }));
  }, []);

  const updateSettings = useCallback((patch: Partial<FamilyState["settings"]>) => {
    setState((prev) => ({ ...prev, settings: { ...prev.settings, ...patch } }));
  }, []);

  const addMember = useCallback((name: string, phone: string) => {
    setState((prev) => {
      const colors = ["#2563eb", "#7c3aed", "#0d9488", "#db2777", "#d97706"];
      const color = colors[prev.members.length % colors.length];
      return {
        ...prev,
        members: [
          ...prev.members,
          {
            id: `member-${Date.now()}`,
            name,
            phone,
            role: "cuidador",
            avatarColor: color,
            isEmergencyContact: true,
            escalationOrder: prev.members.length + 1,
          },
        ],
      };
    });
  }, []);

  const removeMember = useCallback((memberId: string) => {
    setState((prev) => ({
      ...prev,
      members: prev.members.filter((m) => m.id !== memberId),
    }));
  }, []);

  const pairNewSensor = useCallback((roomName: string) => {
    setState((prev) => {
      const roomId = `room-${Date.now()}`;
      const sensorId = `sensor-${Date.now()}`;
      return {
        ...prev,
        rooms: [...prev.rooms, { id: roomId, name: roomName, icon: "other" }],
        sensors: [
          ...prev.sensors,
          {
            id: sensorId,
            name: `Sensor ${roomName}`,
            roomId,
            status: "online",
            battery: null,
            lastSeen: new Date().toISOString(),
            firmware: "1.2.0",
          },
        ],
      };
    });
  }, []);

  const activeAlert = useMemo(
    () =>
      state.events.find((e) => e.status === "active" || e.status === "escalated") ?? null,
    [state.events]
  );

  const value = useMemo(
    () => ({
      state,
      activeAlert,
      simulateFall,
      resolveEvent,
      escalateEvent,
      toggleSensor,
      updateSettings,
      addMember,
      removeMember,
      pairNewSensor,
    }),
    [
      state,
      activeAlert,
      simulateFall,
      resolveEvent,
      escalateEvent,
      toggleSensor,
      updateSettings,
      addMember,
      removeMember,
      pairNewSensor,
    ]
  );

  return <AppStoreContext.Provider value={value}>{children}</AppStoreContext.Provider>;
}

export function useAppStore() {
  const ctx = useContext(AppStoreContext);
  if (!ctx) throw new Error("useAppStore debe usarse dentro de AppStoreProvider");
  return ctx;
}
