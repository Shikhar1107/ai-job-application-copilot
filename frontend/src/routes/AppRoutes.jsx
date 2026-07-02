import { Navigate, Route, Routes } from "react-router";
import AnalyzeJob from "../pages/AnalyzeJob";
import AnalysisHistory from "../pages/AnalysisHistory";
import AnalysisDetail from "../pages/AnalysisDetail";

export default function AppRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/analyze" replace />} />
            <Route path="/analyze" element={<AnalyzeJob />} />
            <Route path="/history" element={<AnalysisHistory />} />
            <Route path="/history/:id" element={<AnalysisDetail />} />
        </Routes>
    );
}