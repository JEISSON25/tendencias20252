
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import { ArrowLeft, ShoppingCart, User, FileText, LogOut, DollarSign, Package, AlertCircle } from "lucide-react";

export default function ClienteDashboard() {
  const navigate = useNavigate();
  const [cliente, setCliente] = useState(null);
  const [facturas, setFacturas] = useState([]);
  const [detallesVenta, setDetallesVenta] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const cargarDatosCliente = async () => {
      try {
        // ✅ OBTENER DATOS DEL USUARIO DESDE LOCALSTORAGE
        const userData = JSON.parse(localStorage.getItem("user") || "{}");
        const userId = userData.id;
        
        console.log("🔍 Cargando dashboard para usuario:", userData);

        if (!userId) {
          throw new Error("No se pudo obtener la información del usuario");
        }

        // ✅ ESTRATEGIA: Usar datos del localStorage como cliente
        // Ya que no podemos acceder al endpoint de clientes
        const clienteFromLocalStorage = {
          id: userId,
          nombre: userData.first_name || userData.username,
          correo: userData.email,
          telefono: userData.telefono,
          usuario: userId
        };

        setCliente(clienteFromLocalStorage);
        console.log("✅ Cliente creado desde localStorage:", clienteFromLocalStorage);

        // ✅ INTENTAR CARGAR DETALLES DE VENTA PERSONALIZADOS
        try {
          const detallesRes = await api.get("/farmacia/detallesventa/mis_detalles/");
          console.log("✅ Detalles de venta del cliente:", detallesRes.data);
          setDetallesVenta(detallesRes.data);

          // Procesar facturas desde los detalles
          const facturasMap = new Map();
          
          detallesRes.data.forEach(detalle => {
            if (detalle.id_factura) {
              if (!facturasMap.has(detalle.id_factura)) {
                facturasMap.set(detalle.id_factura, {
                  id: detalle.id_factura,
                  fecha: detalle.factura_fecha,
                  productos: [],
                  total: 0
                });
              }
              
              const factura = facturasMap.get(detalle.id_factura);
              factura.productos.push(detalle);
              factura.total += parseFloat(detalle.subtotal || 0);
            }
          });

          const facturasProcesadas = Array.from(facturasMap.values()).map(factura => ({
            ...factura,
            total: factura.total.toFixed(2)
          }));

          setFacturas(facturasProcesadas);
          
        } catch (detallesError) {
          console.warn("⚠️ No se pudieron cargar los detalles de venta:", detallesError);
          
          // ✅ ESTRATEGIA ALTERNATIVA: Cargar todas las facturas y filtrar por cliente
          try {
            console.log("🔄 Intentando cargar facturas generales...");
            const facturasRes = await api.get("/farmacia/facturasventa/");
            
            // Filtrar facturas por cliente (usando el ID del usuario actual)
            const facturasCliente = facturasRes.data.filter(factura => 
              factura.id_cliente && factura.id_cliente.usuario === userId
            );
            
            console.log("✅ Facturas del cliente encontradas:", facturasCliente);
            
            // Cargar detalles para estas facturas
            const detallesPromises = facturasCliente.map(async (factura) => {
              try {
                const detallesRes = await api.get(`/farmacia/detallesventa/?id_factura=${factura.id}`);
                return {
                  factura,
                  detalles: detallesRes.data
                };
              } catch (error) {
                console.warn(`⚠️ No se pudieron cargar detalles para factura ${factura.id}:`, error);
                return { factura, detalles: [] };
              }
            });

            const resultados = await Promise.all(detallesPromises);
            const todosDetalles = resultados.flatMap(r => r.detalles);
            setDetallesVenta(todosDetalles);

            // Procesar facturas con detalles
            const facturasConDetalles = facturasCliente.map(factura => {
              const detallesFactura = todosDetalles.filter(d => d.id_factura === factura.id);
              const total = detallesFactura.reduce((sum, d) => sum + parseFloat(d.subtotal || 0), 0);
              
              return {
                id: factura.id,
                fecha: factura.fecha,
                productos: detallesFactura,
                total: total.toFixed(2)
              };
            });

            setFacturas(facturasConDetalles);
            
          } catch (facturasError) {
            console.warn("⚠️ No se pudieron cargar las facturas:", facturasError);
            // Continuar sin datos de compras
          }
        }

      } catch (error) {
        console.error("❌ Error cargando dashboard:", error);
        if (error.response?.status === 401) {
          localStorage.clear();
          navigate("/login");
        } else if (error.response?.status === 403) {
          // Error 403 manejado de forma elegante
          setError("No tienes permisos para acceder a esta información. Contacta al administrador.");
        } else {
          setError("Error al cargar el dashboard. Intenta recargar la página.");
        }
      } finally {
        setLoading(false);
      }
    };

    cargarDatosCliente();
  }, [navigate]);

  // ✅ CÁLCULOS
  const totalGastado = facturas.reduce((sum, f) => sum + parseFloat(f.total || 0), 0).toFixed(2);
  const totalProductosComprados = detallesVenta.reduce((sum, d) => sum + (d.cantidad || 0), 0);
  const totalCompras = facturas.length;

  if (loading) {
    return (
      <div className="min-vh-100 d-flex justify-content-center align-items-center" 
           style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
        <div className="text-center">
          <div className="spinner-border text-success mb-3" role="status">
            <span className="visually-hidden">Cargando...</span>
          </div>
          <p className="text-success fw-semibold">Cargando tu dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-vh-100 d-flex justify-content-center align-items-center" 
           style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
        <div className="card shadow-lg border-0 rounded-4 text-center p-4" style={{ maxWidth: "500px" }}>
          <AlertCircle size={64} className="text-warning mb-3" />
          <h4 className="text-warning fw-bold mb-3">Acceso Restringido</h4>
          <p className="text-muted mb-4">{error}</p>
          <div className="d-flex gap-2 justify-content-center">
            <button
              onClick={() => navigate("/login")}
              className="btn btn-success"
            >
              🔑 Ir al Login
            </button>
            <button
              onClick={() => navigate("/")}
              className="btn btn-outline-success"
            >
              🏠 Ir al Inicio
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-vh-100 py-4" 
         style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}>
      <div className="container" style={{ maxWidth: "1000px" }}>
        
        {/* Header */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <button
            onClick={() => navigate(-1)}
            className="btn btn-outline-success d-flex align-items-center gap-2"
          >
            <ArrowLeft size={18} />
            Volver
          </button>
          <div className="text-end">
            <small className="text-muted d-block">Bienvenido</small>
            <strong className="text-success">{cliente?.nombre || "Cliente"}</strong>
          </div>
        </div>

        {/* Tarjeta Principal */}
        <div className="card shadow-lg border-0 rounded-4 overflow-hidden mb-4">
          <div className="bg-success text-white p-4 text-center">
            <div className="bg-white bg-opacity-20 rounded-circle p-3 d-inline-flex mb-3">
              <Package size={32} />
            </div>
            <h2 className="fw-bold mb-2">Mi Área Personal</h2>
            <p className="mb-0 opacity-90">
              {cliente?.correo} • 📞 {cliente?.telefono || "No registrado"}
            </p>
          </div>

          <div className="card-body p-4">
            
            {/* Estadísticas */}
            <div className="row g-3 mb-4">
              <div className="col-md-4">
                <div className="bg-light border border-success rounded-3 p-3 text-center">
                  <DollarSign size={28} className="text-success mb-2" />
                  <h5 className="fw-bold text-success">${totalGastado}</h5>
                  <small className="text-muted">Total Gastado</small>
                </div>
              </div>
              <div className="col-md-4">
                <div className="bg-light border border-primary rounded-3 p-3 text-center">
                  <ShoppingCart size={28} className="text-primary mb-2" />
                  <h5 className="fw-bold text-primary">{totalCompras}</h5>
                  <small className="text-muted">Compras Realizadas</small>
                </div>
              </div>
              <div className="col-md-4">
                <div className="bg-light border border-warning rounded-3 p-3 text-center">
                  <Package size={28} className="text-warning mb-2" />
                  <h5 className="fw-bold text-warning">{totalProductosComprados}</h5>
                  <small className="text-muted">Productos Comprados</small>
                </div>
              </div>
            </div>

            {/* Información del Sistema */}
            <div className="alert alert-info mb-4">
              <div className="d-flex align-items-center">
                <Info size={20} className="me-2" />
                <small>
                  <strong>💡 Información:</strong> Esta área muestra tus compras y datos personales.
                </small>
              </div>
            </div>

            {/* Acciones */}
            <div className="row g-3 mb-4">
              <div className="col-md-6">
                <Link
                  to="/cliente/mis-compras"
                  className="btn btn-success btn-lg w-100 d-flex align-items-center justify-content-center gap-3 p-3"
                >
                  <ShoppingCart size={24} />
                  <div className="text-start">
                    <div className="fw-bold">Mis Compras</div>
                    <small>Historial y facturas</small>
                  </div>
                </Link>
              </div>
              <div className="col-md-6">
                <Link
                  to="/cliente/perfil"
                  className="btn btn-outline-success btn-lg w-100 d-flex align-items-center justify-content-center gap-3 p-3"
                >
                  <User size={24} />
                  <div className="text-start">
                    <div className="fw-bold">Mi Perfil</div>
                    <small>Ver mis datos</small>
                  </div>
                </Link>
              </div>
            </div>

            {/* Historial de Compras */}
            {facturas.length > 0 ? (
              <div className="mt-4">
                <h5 className="fw-bold text-success mb-3">📋 Mis Últimas Compras</h5>
                <div className="table-responsive">
                  <table className="table table-hover align-middle">
                    <thead className="table-success">
                      <tr>
                        <th>Fecha</th>
                        <th>Productos</th>
                        <th>Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      {facturas.slice(0, 5).map((factura) => (
                        <tr key={factura.id}>
                          <td>{new Date(factura.fecha).toLocaleDateString()}</td>
                          <td>
                            <span className="badge bg-primary">
                              {factura.productos.length} items
                            </span>
                          </td>
                          <td className="fw-bold text-success">${factura.total}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                {facturas.length > 5 && (
                  <div className="text-center mt-3">
                    <Link to="/cliente/mis-compras" className="btn btn-outline-success btn-sm">
                      Ver todas mis compras →
                    </Link>
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-4">
                <ShoppingCart size={48} className="text-muted mb-3" />
                <h5 className="text-muted">Aún no tienes compras registradas</h5>
                <p className="text-muted">Tu historial de compras aparecerá aquí cuando realices tu primera compra.</p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="card-footer bg-light text-center p-3">
            <button
              onClick={() => {
                localStorage.clear();
                navigate("/login");
              }}
              className="btn btn-danger d-flex align-items-center gap-2 mx-auto"
            >
              <LogOut size={18} />
              Cerrar Sesión
            </button>
          </div>
        </div>

        <div className="text-center">
          <small className="text-muted">© 2025 Farmacia Salud+ • Área Personal del Cliente</small>
        </div>
      </div>
    </div>
  );
}

function Info(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <line x1="12" x2="12" y1="16" y2="12" />
      <line x1="12" x2="12.01" y1="8" y2="8" />
    </svg>
  );
}