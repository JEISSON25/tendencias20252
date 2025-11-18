// main.jsx - CON EXPORT DEFAULT
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

// Componentes
import Login from "./components/Login";
import Register from "./components/Register";
import AdminDashboard from "./components/AdminDashboard";
import EmpleadoDashboard from "./components/EmpleadoDashboard";
import RegistrarSalida from "./components/RegistrarSalida";
import ConsultarProductos from "./components/ConsultarProducto";
import MisVentas from "./components/MisVentas";
import Movimientos from "./components/Movimientos";
import ClienteDashboard from "./components/ClienteDashboard";
import MisCompras from "./components/MisCompras";
import PerfilCliente from "./components/PerfilCliente";
import Usuarios from "./components/Usuarios";
import Reportes from "./components/Reporte";
import RegistrarVenta from "./components/RegistrarVenta";
import Productos from "./components/Productos";   
import Gmovimientos from "./components/GestionMovimiento"

// PrivateRoute
import PrivateRoute from "./router/PrivateRoute";

// ✅ APP PRINCIPAL ÚNICA - CON EXPORT DEFAULT
function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Rutas Públicas */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* === ADMINISTRADOR === */}
        <Route
          path="/admin"
          element={
            <PrivateRoute rolPermitido="administrador">
              <AdminDashboard />
            </PrivateRoute>
          }
        />

        <Route
          path="/admin"
          element={
            <PrivateRoute rolPermitido="administrador">
              <Gmovimientos />
            </PrivateRoute>
          }
        />
        <Route
          path="/usuarios"
          element={
            <PrivateRoute rolPermitido="administrador">
              <Usuarios />
            </PrivateRoute>
          }
        />
        <Route
          path="/reportes"
          element={
            <PrivateRoute rolPermitido="administrador">
              <Reportes />
            </PrivateRoute>
          }
        />

        {/* === EMPLEADO === */}
        <Route
          path="/empleado"
          element={
            <PrivateRoute rolPermitido="empleado">
              <EmpleadoDashboard />
            </PrivateRoute>
          }
        />

        <Route
          path="/empleado"
          element={
            <PrivateRoute rolPermitido="empleado">
              <Movimientos />
            </PrivateRoute>
          }
        />
        <Route
          path="/registrar-venta"
          element={
            <PrivateRoute rolPermitido="empleado">
              <RegistrarVenta />
            </PrivateRoute>
          }
        />

        <Route
          path="/empleado/registrar-salida"
          element={
            <PrivateRoute rolPermitido="empleado">
              <RegistrarSalida />
            </PrivateRoute>
          }
        />
        <Route
          path="/empleado/productos"
          element={
            <PrivateRoute rolPermitido="empleado">
              <ConsultarProductos />
            </PrivateRoute>
          }
        />
        <Route
          path="/empleado/movimientos"
          element={
            <PrivateRoute rolPermitido="empleado">
              <Movimientos />
            </PrivateRoute>
          }
        />
        <Route
          path="/mis-ventas"
          element={
            <PrivateRoute rolPermitido="empleado">
              <MisVentas />
            </PrivateRoute>
          }
        />

        {/* === CLIENTE === */}
        <Route
          path="/cliente"
          element={
            <PrivateRoute rolPermitido="cliente">
              <ClienteDashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/cliente/mis-compras"
          element={
            <PrivateRoute rolPermitido="cliente">
              <MisCompras />
            </PrivateRoute>
          }
        />
        <Route
          path="/cliente/perfil"
          element={
            <PrivateRoute rolPermitido="cliente">
              <PerfilCliente />
            </PrivateRoute>
          }
        />

        {/* Ruta por defecto */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

// ✅ EXPORT DEFAULT PARA FAST REFRESH
export default App;

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
