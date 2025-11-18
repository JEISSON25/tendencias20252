// MisCompras.jsx - VERSIÓN PROFESIONAL Y DINÁMICA
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import {
  ArrowLeft,
  ShoppingCart,
  Download,
  AlertCircle,
  Package,
  DollarSign,
  Calendar,
  FileText,
  TrendingUp,
  RefreshCw,
} from "lucide-react";

export default function MisCompras() {
  const navigate = useNavigate();
  const [detalles, setDetalles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState("");
  const [sinCompras, setSinCompras] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const cargarMisCompras = async (isRefresh = false) => {
    if (isRefresh) {
      setRefreshing(true);
    } else {
      setLoading(true);
    }

    try {
      const userData = JSON.parse(localStorage.getItem("user") || "{}");
      const userId = userData.id;

      if (!userId) {
        throw new Error("No se pudo obtener la información del usuario");
      }

      console.log("🔍 Cargando compras para usuario:", userId);

      let comprasCargadas = false;

      // ✅ ESTRATEGIA 1: Cargar todas las facturas y filtrar
      try {
        const facturasRes = await api.get("/farmacia/facturasventa/");
        console.log("✅ Facturas cargadas:", facturasRes.data);

        // Filtrar facturas del usuario actual
        const facturasUsuario = facturasRes.data.filter(
          (factura) =>
            factura.id_cliente && factura.id_cliente.usuario === userId
        );

        console.log("✅ Facturas del usuario:", facturasUsuario);

        if (facturasUsuario.length > 0) {
          // Cargar detalles para cada factura
          const detallesPromises = facturasUsuario.map(async (factura) => {
            try {
              const detallesRes = await api.get(
                `/farmacia/detallesventa/?id_factura=${factura.id}`
              );
              return detallesRes.data.map((detalle) => ({
                ...detalle,
                factura_fecha: factura.fecha,
                factura_id: factura.id,
                cliente_nombre: factura.id_cliente?.nombre || "Cliente",
              }));
            } catch (error) {
              console.log(`ℹ️ No hay detalles para factura ${factura.id}`, error);
              return [];
            }
          });

          const resultados = await Promise.all(detallesPromises);
          const todosDetalles = resultados.flat();

          if (todosDetalles.length > 0) {
            setDetalles(todosDetalles);
            comprasCargadas = true;
            setSinCompras(false);
            console.log("✅ Compras cargadas exitosamente:", todosDetalles);
          }
        }
      } catch (facturasError) {
        console.log("ℹ️ No se pudieron cargar facturas generales", facturasError);
      }

      // ✅ ESTRATEGIA 2: Solo intentar endpoint personalizado si no hay compras
      if (!comprasCargadas) {
        try {
          console.log("🔄 Intentando endpoint personalizado...");
          const detallesRes = await api.get(
            "/farmacia/detallesventa/mis_detalles/"
          );
          if (detallesRes.data && detallesRes.data.length > 0) {
            setDetalles(detallesRes.data);
            comprasCargadas = true;
            setSinCompras(false);
            console.log("✅ Compras cargadas desde endpoint personalizado");
          }
        } catch (personalizadoError) {
          console.log(
            "ℹ️ Endpoint personalizado no disponible para este usuario",
            personalizadoError
          );
        }
      }

      // ✅ Si no se cargaron compras, mostrar estado "sin compras"
      if (!comprasCargadas) {
        setSinCompras(true);
        setDetalles([]);
        console.log("ℹ️ Usuario no tiene compras registradas");
      }
    } catch (error) {
      console.error("❌ Error general:", error);
      if (error.response?.status === 401) {
        localStorage.clear();
        navigate("/login");
      } else {
        setError("Error al cargar tus compras. Intenta recargar la página.");
      }
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    cargarMisCompras();
  }, [navigate]);

  const descargarPDF = async () => {
    if (detalles.length === 0) {
      alert("No tienes compras para generar PDF");
      return;
    }

    setDownloading(true);
    try {
      const response = await api.get(
        "/farmacia/detallesventa/all_pdf_cliente/",
        {
          responseType: "blob",
        }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `mis_compras_${new Date().toISOString().split("T")[0]}.pdf`
      );
      document.body.appendChild(link);
      link.click();
      link.remove();

      // Efecto visual de descarga exitosa
      const btn = document.querySelector(".btn-download");
      if (btn) {
        btn.classList.add("download-success");
        setTimeout(() => btn.classList.remove("download-success"), 2000);
      }
    } catch (pdfError) {
      console.log("ℹ️ PDF no disponible", pdfError);
      alert("La descarga de PDF no está disponible en este momento.");
    } finally {
      setDownloading(false);
    }
  };

  const recargarCompras = () => {
    cargarMisCompras(true);
  };

  // Calcular estadísticas
  const calcularTotalGeneral = () => {
    return detalles.reduce((acc, d) => acc + Number(d.subtotal || 0), 0);
  };

  const calcularPromedioCompra = () => {
    const facturasUnicas = [
      ...new Set(detalles.map((d) => d.factura_id || d.id_factura)),
    ];
    return facturasUnicas.length > 0
      ? calcularTotalGeneral() / facturasUnicas.length
      : 0;
  };

  const obtenerUltimaCompra = () => {
    if (detalles.length === 0) return null;
    const fechas = detalles.map((d) => new Date(d.factura_fecha));
    return new Date(Math.max(...fechas));
  };

  // Agrupar detalles por factura
  const detallesAgrupados = detalles.reduce((acc, detalle) => {
    const facturaId = detalle.factura_id || detalle.id_factura;
    if (!acc[facturaId]) {
      acc[facturaId] = {
        factura: {
          id: facturaId,
          fecha: detalle.factura_fecha,
          total: 0,
          productosCount: 0,
        },
        detalles: [],
      };
    }
    acc[facturaId].detalles.push(detalle);
    acc[facturaId].factura.total += Number(detalle.subtotal || 0);
    acc[facturaId].factura.productosCount += detalle.cantidad || 1;
    return acc;
  }, {});

  // Ordenar facturas por fecha (más reciente primero)
  const facturasOrdenadas = Object.values(detallesAgrupados).sort(
    (a, b) => new Date(b.factura.fecha) - new Date(a.factura.fecha)
  );

  if (loading) {
    return (
      <div
        className="min-vh-100 d-flex justify-content-center align-items-center"
        style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}
      >
        <div className="text-center">
          <div
            className="spinner-border text-success mb-3"
            role="status"
            style={{ width: "3rem", height: "3rem" }}
          >
            <span className="visually-hidden">Cargando...</span>
          </div>
          <h5 className="text-success fw-semibold mb-2">
            Cargando tu historial
          </h5>
          <p className="text-muted">
            Estamos preparando toda tu información de compras...
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div
        className="min-vh-100 d-flex justify-content-center align-items-center"
        style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}
      >
        <div className="container">
          <div className="row justify-content-center">
            <div className="col-md-6">
              <div className="card shadow-lg border-0 rounded-4 text-center p-5">
                <AlertCircle size={80} className="text-warning mb-4 mx-auto" />
                <h3 className="text-warning fw-bold mb-3">Error al cargar</h3>
                <p className="text-muted mb-4 fs-5">{error}</p>
                <div className="d-flex gap-3 justify-content-center">
                  <button
                    onClick={() => window.location.reload()}
                    className="btn btn-success px-4 py-2 fw-semibold"
                  >
                    🔄 Recargar Página
                  </button>
                  <button
                    onClick={() => navigate("/cliente")}
                    className="btn btn-outline-success px-4 py-2 fw-semibold"
                  >
                    🏠 Volver al Dashboard
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className="min-vh-100 py-4"
      style={{ background: "linear-gradient(135deg, #d0f0c0, #b2dfdb)" }}
    >
      <div className="container" style={{ maxWidth: "1200px" }}>
        {/* Header Mejorado */}
        <div className="d-flex justify-content-between align-items-center mb-4">
          <div className="d-flex align-items-center gap-3">
            <button
              onClick={() => navigate("/cliente")}
              className="btn btn-outline-success d-flex align-items-center gap-2 shadow-sm hover-lift"
            >
              <ArrowLeft size={18} />
              Volver al Dashboard
            </button>
            <div className="vr"></div>
            <h1 className="h3 mb-0 text-success fw-bold d-flex align-items-center gap-2">
              <ShoppingCart size={28} />
              Mis Compras
            </h1>
          </div>

          <div className="d-flex gap-2">
            <button
              onClick={recargarCompras}
              disabled={refreshing}
              className="btn btn-outline-success d-flex align-items-center gap-2 shadow-sm hover-lift"
            >
              <RefreshCw size={16} className={refreshing ? "spinning" : ""} />
              {refreshing ? "Actualizando..." : "Actualizar"}
            </button>

            {detalles.length > 0 && (
              <button
                onClick={descargarPDF}
                disabled={downloading}
                className="btn btn-success d-flex align-items-center gap-2 shadow-sm hover-lift btn-download"
              >
                {downloading ? (
                  <>
                    <div className="spinner-border spinner-border-sm me-2" />
                    Generando...
                  </>
                ) : (
                  <>
                    <Download size={18} />
                    Descargar PDF
                  </>
                )}
              </button>
            )}
          </div>
        </div>

        {/* Tarjeta Principal Mejorada */}
        <div className="card shadow-lg border-0 rounded-4 overflow-hidden mb-4 hover-lift">
          <div className="bg-success text-white p-5 position-relative overflow-hidden">
            <div className="position-absolute top-0 end-0 w-100 h-100 bg-white bg-opacity-10 wave-bg"></div>
            <div className="position-relative text-center">
              <div
                className="bg-white text-success rounded-circle mx-auto mb-4 d-flex align-items-center justify-content-center shadow-lg icon-bounce"
                style={{ width: "90px", height: "90px" }}
              >
                <ShoppingCart size={40} />
              </div>
              <h2 className="fw-bold mb-2 display-6">Historial de Compras</h2>
              <p className="mb-0 opacity-90 fs-5">
                Consulta y gestiona todas tus transacciones
              </p>
            </div>
          </div>

          <div className="card-body p-4">
            {detalles.length === 0 || sinCompras ? (
              <div className="text-center py-5">
                <div className="bg-light rounded-circle p-4 d-inline-flex mb-4">
                  <ShoppingCart size={64} className="text-muted opacity-50" />
                </div>
                <h4 className="text-muted fw-bold mb-3">
                  Aún no tienes compras registradas
                </h4>
                <p className="text-muted fs-5 mb-4">
                  Tu historial de compras aparecerá aquí cuando realices tu
                  primera compra en nuestra farmacia.
                </p>
                <div className="d-flex gap-3 justify-content-center">
                  <button
                    onClick={() => navigate("/cliente")}
                    className="btn btn-success px-4 py-2 fw-semibold"
                  >
                    Volver al Dashboard
                  </button>
                  <button
                    onClick={recargarCompras}
                    className="btn btn-outline-success px-4 py-2 fw-semibold"
                  >
                    Revisar Nuevamente
                  </button>
                </div>
              </div>
            ) : (
              <>
                {/* Panel de Estadísticas Mejorado */}
                <div className="row g-4 mb-5">
                  <div className="col-md-3">
                    <div className="card border-0 bg-gradient-primary text-white shadow-sm h-100 hover-scale">
                      <div className="card-body text-center p-4">
                        <div className="bg-white bg-opacity-20 rounded-circle p-3 d-inline-flex mb-3">
                          <FileText size={24} />
                        </div>
                        <h3 className="fw-bold display-6 mb-1">
                          {Object.keys(detallesAgrupados).length}
                        </h3>
                        <p className="mb-0 opacity-90">Facturas Totales</p>
                      </div>
                    </div>
                  </div>

                  <div className="col-md-3">
                    <div className="card border-0 bg-gradient-success text-white shadow-sm h-100 hover-scale">
                      <div className="card-body text-center p-4">
                        <div className="bg-white bg-opacity-20 rounded-circle p-3 d-inline-flex mb-3">
                          <Package size={24} />
                        </div>
                        <h3 className="fw-bold display-6 mb-1">
                          {detalles.length}
                        </h3>
                        <p className="mb-0 opacity-90">Productos Comprados</p>
                      </div>
                    </div>
                  </div>

                  <div className="col-md-3">
                    <div className="card border-0 bg-gradient-warning text-white shadow-sm h-100 hover-scale">
                      <div className="card-body text-center p-4">
                        <div className="bg-white bg-opacity-20 rounded-circle p-3 d-inline-flex mb-3">
                          <DollarSign size={24} />
                        </div>
                        <h3 className="fw-bold display-6 mb-1">
                          ${calcularTotalGeneral().toFixed(0)}
                        </h3>
                        <p className="mb-0 opacity-90">Total Invertido</p>
                      </div>
                    </div>
                  </div>

                  <div className="col-md-3">
                    <div className="card border-0 bg-gradient-info text-white shadow-sm h-100 hover-scale">
                      <div className="card-body text-center p-4">
                        <div className="bg-white bg-opacity-20 rounded-circle p-3 d-inline-flex mb-3">
                          <TrendingUp size={24} />
                        </div>
                        <h3 className="fw-bold display-6 mb-1">
                          ${calcularPromedioCompra().toFixed(2)}
                        </h3>
                        <p className="mb-0 opacity-90">Promedio por Factura</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Lista de Compras Mejorada */}
                <div className="mb-4">
                  <h4 className="fw-bold text-success mb-4 d-flex align-items-center gap-2">
                    <Calendar size={24} />
                    Detalles de Compras por Factura
                  </h4>

                  {facturasOrdenadas.map((grupo) => (
                    <div
                      key={grupo.factura.id}
                      className="card border-0 shadow-sm mb-4 hover-lift"
                    >
                      <div className="card-header bg-light border-0 py-3">
                        <div className="row align-items-center">
                          <div className="col-md-6">
                            <h5 className="fw-bold text-success mb-1 d-flex align-items-center gap-2">
                              <FileText size={20} />
                              Factura #{grupo.factura.id}
                            </h5>
                            <small className="text-muted d-flex align-items-center gap-1">
                              <Calendar size={14} />
                              {new Date(grupo.factura.fecha).toLocaleDateString(
                                "es-ES",
                                {
                                  weekday: "long",
                                  year: "numeric",
                                  month: "long",
                                  day: "numeric",
                                }
                              )}
                            </small>
                          </div>
                          <div className="col-md-6 text-md-end">
                            <div className="d-flex flex-column">
                              <span className="fw-bold text-success fs-4">
                                ${grupo.factura.total.toFixed(2)}
                              </span>
                              <small className="text-muted">
                                {grupo.factura.productosCount} productos
                              </small>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="card-body p-0">
                        <div className="table-responsive">
                          <table className="table table-hover align-middle mb-0">
                            <thead className="table-success">
                              <tr>
                                <th className="ps-4">Producto</th>
                                <th className="text-center">Cantidad</th>
                                <th className="text-end">Precio Unitario</th>
                                <th className="text-end pe-4">Subtotal</th>
                              </tr>
                            </thead>
                            <tbody>
                              {grupo.detalles.map((detalle, index) => (
                                <tr
                                  key={detalle.id}
                                  className={
                                    index % 2 === 0 ? "table-light" : ""
                                  }
                                >
                                  <td className="ps-4">
                                    <div className="d-flex align-items-center gap-2">
                                      <div className="bg-success bg-opacity-10 rounded p-1">
                                        <Package
                                          size={16}
                                          className="text-success"
                                        />
                                      </div>
                                      <strong>
                                        {detalle.producto_nombre ||
                                          detalle.id_producto?.nombre ||
                                          "Producto"}
                                      </strong>
                                    </div>
                                  </td>
                                  <td className="text-center">
                                    <span className="badge bg-primary rounded-pill fs-6">
                                      {detalle.cantidad}
                                    </span>
                                  </td>
                                  <td className="text-end">
                                    <span className="text-muted fw-semibold">
                                      $
                                      {Number(
                                        detalle.precio_unitario || 0
                                      ).toFixed(2)}
                                    </span>
                                  </td>
                                  <td className="text-end pe-4">
                                    <span className="fw-bold text-success fs-6">
                                      $
                                      {Number(detalle.subtotal || 0).toFixed(2)}
                                    </span>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {/* Resumen Final Mejorado */}
                <div className="card border-success bg-gradient-light shadow-lg mt-4">
                  <div className="card-body p-4">
                    <div className="row align-items-center">
                      <div className="col-md-8">
                        <h5 className="fw-bold text-success mb-2">
                          Resumen General de Compras
                        </h5>
                        <p className="text-muted mb-0">
                          Has realizado {Object.keys(detallesAgrupados).length}{" "}
                          compras con un total de {detalles.length} productos
                          adquiridos.
                          {obtenerUltimaCompra() && (
                            <span>
                              {" "}
                              Tu última compra fue el{" "}
                              {obtenerUltimaCompra().toLocaleDateString(
                                "es-ES"
                              )}
                              .
                            </span>
                          )}
                        </p>
                      </div>
                      <div className="col-md-4 text-md-end">
                        <div className="d-flex flex-column">
                          <span className="text-muted fs-6">Total General</span>
                          <span className="fw-bold text-success display-6">
                            ${calcularTotalGeneral().toFixed(2)}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>

        {/* Footer Mejorado */}
        <div className="text-center mt-4">
          <small className="text-muted d-block mb-1">
            © 2025 Farmacia Salud+ • Sistema de Gestión de Compras
          </small>
          <small className="text-muted">
            {detalles.length > 0
              ? `Mostrando ${detalles.length} productos en ${
                  Object.keys(detallesAgrupados).length
                } facturas`
              : "Listo para registrar tu primera compra"}
          </small>
        </div>
      </div>

      {/* Estilos CSS para efectos dinámicos */}
      <style jsx>{`
        .hover-lift:hover {
          transform: translateY(-3px);
          transition: all 0.3s ease;
        }

        .hover-scale:hover {
          transform: scale(1.02);
          transition: all 0.3s ease;
        }

        .wave-bg {
          background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
          );
          animation: wave 8s infinite linear;
        }

        .icon-bounce {
          animation: bounce 2s infinite;
        }

        .spinning {
          animation: spin 1s linear infinite;
        }

        .btn-download.download-success {
          background-color: #198754 !important;
          animation: pulse 0.6s;
        }

        .bg-gradient-primary {
          background: linear-gradient(135deg, #007bff, #0056b3);
        }

        .bg-gradient-success {
          background: linear-gradient(135deg, #198754, #0f5132);
        }

        .bg-gradient-warning {
          background: linear-gradient(135deg, #ffc107, #fd7e14);
        }

        .bg-gradient-info {
          background: linear-gradient(135deg, #0dcaf0, #0aa2c0);
        }

        .bg-gradient-light {
          background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        }

        @keyframes wave {
          0% {
            transform: translateX(-100%);
          }
          100% {
            transform: translateX(100%);
          }
        }

        @keyframes bounce {
          0%,
          20%,
          50%,
          80%,
          100% {
            transform: translateY(0);
          }
          40% {
            transform: translateY(-8px);
          }
          60% {
            transform: translateY(-4px);
          }
        }

        @keyframes spin {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }

        @keyframes pulse {
          0% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
          100% {
            transform: scale(1);
          }
        }
      `}</style>
    </div>
  );
}
