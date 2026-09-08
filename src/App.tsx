import { BrowserRouter, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/AppShell";
import { AppStoreProvider, useAppStore } from "./store/AppStore";
import { HomePage } from "./pages/HomePage";
import { HistoryPage } from "./pages/HistoryPage";
import { SensorsPage } from "./pages/SensorsPage";
import { FamilyPage } from "./pages/FamilyPage";
import { SettingsPage } from "./pages/SettingsPage";
import { AlertOverlay } from "./pages/AlertOverlay";
import { DevSimulateButton } from "./components/DevSimulateButton";

function AppContent() {
  const { activeAlert } = useAppStore();

  return (
    <>
      <AppShell>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/historial" element={<HistoryPage />} />
          <Route path="/sensores" element={<SensorsPage />} />
          <Route path="/familia" element={<FamilyPage />} />
          <Route path="/ajustes" element={<SettingsPage />} />
        </Routes>
      </AppShell>
      {activeAlert && <AlertOverlay event={activeAlert} />}
      <DevSimulateButton />
    </>
  );
}

export default function App() {
  return (
    <AppStoreProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </AppStoreProvider>
  );
}
