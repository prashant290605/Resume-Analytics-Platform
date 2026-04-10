import { Route, Routes } from "react-router-dom";

import CandidateDetailPage from "./pages/CandidateDetailPage";
import DashboardPage from "./pages/DashboardPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/candidates/:resumeId" element={<CandidateDetailPage />} />
    </Routes>
  );
}
