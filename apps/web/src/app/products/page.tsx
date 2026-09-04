"use client";

import { useState, useMemo, useEffect } from "react";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { products as initialProducts } from "@/data/fixtures/demo-scenario";
import { formatINR } from "@/lib/formatters";
import type { Product } from "@/data/fixtures/types";
import { Search, Plus, Edit2, CheckCircle2, X, Sparkles, Filter, ArrowUpDown, Layers } from "lucide-react";
import { getProducts, createProduct, patchProduct, adjustStock } from "@/lib/api-client";

const CATEGORIES = [
  "All",
  "Laptops",
  "CPUs",
  "PC Cases",
  "Graphics Cards",
  "Motherboards",
  "RAM",
  "SSD",
  "HDD",
  "Monitors",
  "Keyboards",
  "Mice",
  "Docks",
  "Audio",
  "Accessories",
];

export default function ProductsPage() {
  const [productList, setProductList] = useState<Product[]>(initialProducts);
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  const [stockFilter, setStockFilter] = useState<"all" | "in_stock" | "low_stock">("all");
  const [readinessFilter, setReadinessFilter] = useState<"all" | "ready" | "needs_attention">("all");
  const [sortBy, setSortBy] = useState<"name" | "price_asc" | "price_desc" | "inventory" | "readiness">("name");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [isAddingProduct, setIsAddingProduct] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  useEffect(() => {
    async function loadCatalog() {
      try {
        const data = await getProducts({ limit: 100 });
        if (data?.items && Array.isArray(data.items) && data.items.length > 0) {
          setProductList(data.items);
        }
      } catch {
        // fallback
      }
    }
    loadCatalog();

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setEditingProduct(null);
        setIsAddingProduct(false);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  // Filter & sort products
  const filteredProducts = useMemo(() => {
    return productList
      .filter((p) => {
        const matchesCategory =
          selectedCategory === "All" ||
          (p.category && p.category.toLowerCase() === selectedCategory.toLowerCase()) ||
          (!p.category && selectedCategory === "Accessories");

        const matchesStock =
          stockFilter === "all" ||
          (stockFilter === "in_stock" && p.inventory > 10) ||
          (stockFilter === "low_stock" && p.inventory <= 10);

        const matchesReadiness =
          readinessFilter === "all" ||
          (readinessFilter === "ready" && p.aiReadiness >= 85) ||
          (readinessFilter === "needs_attention" && p.aiReadiness < 85);

        const query = searchQuery.toLowerCase();
        const matchesSearch =
          !searchQuery ||
          p.name.toLowerCase().includes(query) ||
          (p.sku && p.sku.toLowerCase().includes(query)) ||
          (p.brand && p.brand.toLowerCase().includes(query));

        return matchesCategory && matchesStock && matchesReadiness && matchesSearch;
      })
      .sort((a, b) => {
        if (sortBy === "price_asc") return a.price - b.price;
        if (sortBy === "price_desc") return b.price - a.price;
        if (sortBy === "inventory") return b.inventory - a.inventory;
        if (sortBy === "readiness") return b.aiReadiness - a.aiReadiness;
        return a.name.localeCompare(b.name);
      });
  }, [productList, selectedCategory, stockFilter, readinessFilter, sortBy, searchQuery]);

  function showToast(msg: string) {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 2500);
  }

  async function handleSaveProduct(updated: Product) {
    // Recalculate AI readiness score based on metadata completeness
    let score = 70;
    if (updated.price > 0) score += 5;
    if (updated.inventory > 0) score += 5;
    if (updated.category) score += 5;
    if (updated.sku) score += 5;
    if (updated.shipping?.weightKg && updated.shipping?.dimensionsCm) {
      score += 10;
      updated.issues = [];
      updated.status = "ready";
    } else {
      updated.issues = ["Shipping metadata"];
      updated.status = "needs_attention";
    }
    updated.aiReadiness = Math.min(100, score);

    setProductList((prev) => prev.map((p) => (p.id === updated.id ? updated : p)));
    setEditingProduct(null);
    showToast(`Saved ${updated.name} successfully.`);
    patchProduct(updated.id, {
      name: updated.name,
      price: updated.price,
      inventory: updated.inventory,
      shipping: updated.shipping,
      sku: updated.sku,
      brand: updated.brand,
    }).catch(() => null);
  }

  async function handleAddProduct(newProd: Partial<Product>) {
    const id = `prod_custom_${Date.now()}`;
    const product: Product = {
      id,
      name: newProd.name || "New Hardware Product",
      category: newProd.category || "Accessories",
      price: Number(newProd.price) || 999,
      inventory: Number(newProd.inventory) || 10,
      aiReadiness: 92,
      brand: newProd.brand || "NovaTech",
      sku: newProd.sku || `NT-CUS-${Date.now().toString().slice(-4)}`,
      status: "ready",
      issues: [],
      shipping: {
        weightKg: Number(newProd.shipping?.weightKg) || 0.5,
        dimensionsCm: newProd.shipping?.dimensionsCm || "20x15x5",
        tier: "Standard",
      },
    };
    setProductList((prev) => [product, ...prev]);
    setIsAddingProduct(false);
    showToast(`Added ${product.name} to catalog.`);
    createProduct({
      id: product.id,
      name: product.name,
      categoryId: (product.category || "ACCESSORIES").toUpperCase(),
      price: product.price,
      inventory: product.inventory,
      sku: product.sku,
      brand: product.brand,
      shipping: product.shipping,
    }).catch(() => null);
  }

  return (
    <AppShell>
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
        <PageHeader title="Product Catalog & Inventory" description="Merchant control plane for category management, pricing, stock, and AI readiness." />
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              setProductList(prev => prev.map(p => {
                adjustStock(p.id, p.inventory + 10, "Merchant catalog restock").catch(() => null);
                return { ...p, inventory: p.inventory + 10 };
              }));
              showToast("Restocked all catalog products (+10 inventory).");
            }}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 border border-border-subtle bg-white text-on-surface rounded-lg font-medium text-xs hover:bg-surface-container transition-all"
          >
            <Layers className="w-3.5 h-3.5" /> Restock All (+10)
          </button>
          <button
            onClick={() => setIsAddingProduct(true)}
            className="inline-flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg font-medium text-xs hover:bg-opacity-90 shadow-sm transition-all"
          >
            <Plus className="w-4 h-4" /> Add Product
          </button>
        </div>
      </div>

      {/* Toast alert */}
      {toastMessage && (
        <div className="fixed top-4 right-4 z-50 flex items-center gap-2 px-4 py-2.5 bg-emerald-600 text-white text-sm font-medium rounded-lg shadow-lg animate-fade-in">
          <CheckCircle2 className="w-4 h-4" /> {toastMessage}
        </div>
      )}

      {/* Filters and Controls */}
      <div className="mb-6 space-y-3">
        <div className="flex flex-col sm:flex-row items-center gap-3">
          <div className="relative flex-1 w-full">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant" />
            <input
              type="text"
              placeholder="Search catalog by name, SKU, or brand..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-4 py-2 text-sm bg-white border border-border-subtle rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto">
            {/* Stock Filter */}
            <select
              value={stockFilter}
              onChange={(e) => setStockFilter(e.target.value as "all" | "in_stock" | "low_stock")}
              className="px-3 py-2 text-xs bg-white border border-border-subtle rounded-lg font-medium text-on-surface focus:outline-none"
            >
              <option value="all">Stock: All</option>
              <option value="in_stock">In Stock (&gt;10)</option>
              <option value="low_stock">Low Stock (≤10)</option>
            </select>

            {/* Readiness Filter */}
            <select
              value={readinessFilter}
              onChange={(e) => setReadinessFilter(e.target.value as "all" | "ready" | "needs_attention")}
              className="px-3 py-2 text-xs bg-white border border-border-subtle rounded-lg font-medium text-on-surface focus:outline-none"
            >
              <option value="all">AI Readiness: All</option>
              <option value="ready">Ready (≥85%)</option>
              <option value="needs_attention">Needs Attention (&lt;85%)</option>
            </select>

            {/* Sort Filter */}
            <div className="flex items-center gap-1.5 bg-white border border-border-subtle px-2.5 py-1.5 rounded-lg">
              <ArrowUpDown className="w-3.5 h-3.5 text-on-surface-variant" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as "name" | "price_asc" | "price_desc" | "inventory" | "readiness")}
                className="text-xs bg-transparent text-on-surface font-medium focus:outline-none"
              >
                <option value="name">Name (A-Z)</option>
                <option value="price_asc">Price (Low → High)</option>
                <option value="price_desc">Price (High → Low)</option>
                <option value="inventory">Stock (High → Low)</option>
                <option value="readiness">AI Readiness</option>
              </select>
            </div>
          </div>
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-2 scrollbar-thin">
          <Filter className="w-4 h-4 text-on-surface-variant mr-1 shrink-0" />
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-colors ${
                selectedCategory === cat
                  ? "bg-primary text-white shadow-sm"
                  : "bg-surface-container text-on-surface-variant hover:bg-surface-container-high"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Main Table */}
      <SolidPanel className="!p-0 overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-border-subtle bg-surface-container-low/50">
              {["Product & SKU", "Category", "Price", "Stock Inventory", "AI Readiness", "Status", "Actions"].map((h) => (
                <th key={h} className="px-5 py-3.5 font-label-bold text-label-bold text-on-surface-variant whitespace-nowrap">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredProducts.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-5 py-8 text-center text-on-surface-variant text-sm">
                  No products found matching &quot;{searchQuery}&quot; in category &quot;{selectedCategory}&quot;.
                </td>
              </tr>
            ) : (
              filteredProducts.map((p) => {
                const needsAttention = p.aiReadiness < 85 || (p.issues && p.issues.length > 0);
                return (
                  <tr key={p.id} className="border-b border-border-subtle last:border-0 hover:bg-surface-container-low/30 transition-colors">
                    <td className="px-5 py-4 whitespace-nowrap">
                      <div className="font-semibold text-sm text-on-surface">{p.name}</div>
                      <div className="text-xs text-on-surface-variant font-mono">{p.sku || p.id} {p.brand && `• ${p.brand}`}</div>
                    </td>
                    <td className="px-5 py-4 text-sm text-on-surface whitespace-nowrap">
                      <span className="px-2 py-0.5 rounded bg-surface-container text-xs font-medium">
                        {p.category || "General"}
                      </span>
                    </td>
                    <td className="px-5 py-4 font-mono font-medium text-sm whitespace-nowrap">
                      {formatINR(p.price)}
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold ${
                        p.inventory > 10 ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-700"
                      }`}>
                        <span className={`w-1.5 h-1.5 rounded-full ${p.inventory > 10 ? "bg-emerald-500" : "bg-amber-500"}`} />
                        {p.inventory} in stock
                      </span>
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-sm font-semibold">{p.aiReadiness}%</span>
                        <div className="w-16 h-1.5 bg-surface-container rounded-full overflow-hidden">
                          <div
                            className={`h-full rounded-full ${p.aiReadiness >= 90 ? "bg-emerald-500" : p.aiReadiness >= 80 ? "bg-blue-500" : "bg-amber-500"}`}
                            style={{ width: `${p.aiReadiness}%` }}
                          />
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap">
                      <StatusBadge
                        status={needsAttention ? "ready_for_review" : "active"}
                        label={needsAttention ? "Needs Attention" : "Ready"}
                      />
                    </td>
                    <td className="px-5 py-4 whitespace-nowrap">
                      <button
                        onClick={() => setEditingProduct(p)}
                        className="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium text-primary hover:bg-surface-container rounded transition-colors"
                      >
                        <Edit2 className="w-3.5 h-3.5" /> Edit & Fix
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </SolidPanel>

      {/* Edit Product Modal */}
      {editingProduct && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-fade-in">
          <div className="w-full max-w-lg bg-white rounded-xl shadow-2xl border border-border-subtle p-6 overflow-hidden">
            <div className="flex items-center justify-between pb-4 border-b border-border-subtle mb-4">
              <div>
                <h3 className="text-lg font-bold text-on-surface">Edit Product & Metadata</h3>
                <p className="text-xs text-on-surface-variant font-mono">{editingProduct.id}</p>
              </div>
              <button onClick={() => setEditingProduct(null)} className="p-1 text-on-surface-variant hover:text-on-surface">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSaveProduct(editingProduct);
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-xs font-medium text-on-surface-variant mb-1">Product Name</label>
                <input
                  type="text"
                  value={editingProduct.name}
                  onChange={(e) => setEditingProduct({ ...editingProduct, name: e.target.value })}
                  className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg focus:ring-2 focus:ring-primary/20"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Price (₹ INR)</label>
                  <input
                    type="number"
                    value={editingProduct.price}
                    onChange={(e) => setEditingProduct({ ...editingProduct, price: Number(e.target.value) })}
                    className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg font-mono focus:ring-2 focus:ring-primary/20"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Stock Quantity</label>
                  <input
                    type="number"
                    value={editingProduct.inventory}
                    onChange={(e) => setEditingProduct({ ...editingProduct, inventory: Number(e.target.value) })}
                    className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg font-mono focus:ring-2 focus:ring-primary/20"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Category</label>
                  <select
                    value={editingProduct.category || "Accessories"}
                    onChange={(e) => setEditingProduct({ ...editingProduct, category: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg bg-white focus:ring-2 focus:ring-primary/20"
                  >
                    {CATEGORIES.filter(c => c !== "All").map(c => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Brand</label>
                  <input
                    type="text"
                    value={editingProduct.brand || ""}
                    onChange={(e) => setEditingProduct({ ...editingProduct, brand: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg focus:ring-2 focus:ring-primary/20"
                  />
                </div>
              </div>

              {/* Shipping Metadata Section */}
              <div className="p-3 bg-surface-container rounded-lg space-y-3">
                <div className="flex items-center gap-1.5 text-xs font-semibold text-primary">
                  <Sparkles className="w-3.5 h-3.5" /> Shipping & AI Commerce Metadata
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs text-on-surface-variant mb-1">Weight (kg)</label>
                    <input
                      type="number"
                      step="0.01"
                      value={editingProduct.shipping?.weightKg || ""}
                      placeholder="e.g. 0.45"
                      onChange={(e) => setEditingProduct({
                        ...editingProduct,
                        shipping: { ...editingProduct.shipping, weightKg: Number(e.target.value) }
                      })}
                      className="w-full px-2.5 py-1.5 text-xs border border-border-subtle rounded bg-white font-mono"
                    />
                  </div>
                  <div>
                    <label className="block text-xs text-on-surface-variant mb-1">Dimensions (LxWxH cm)</label>
                    <input
                      type="text"
                      value={editingProduct.shipping?.dimensionsCm || ""}
                      placeholder="e.g. 26x24x4"
                      onChange={(e) => setEditingProduct({
                        ...editingProduct,
                        shipping: { ...editingProduct.shipping, dimensionsCm: e.target.value }
                      })}
                      className="w-full px-2.5 py-1.5 text-xs border border-border-subtle rounded bg-white font-mono"
                    />
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-border-subtle">
                <button
                  type="button"
                  onClick={() => setEditingProduct(null)}
                  className="px-4 py-2 text-xs font-medium text-on-surface-variant hover:bg-surface-container rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 text-xs font-semibold bg-primary text-white rounded-lg hover:bg-opacity-90 shadow-sm"
                >
                  Save & Recalculate Readiness
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Product Modal */}
      {isAddingProduct && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-fade-in">
          <div className="w-full max-w-lg bg-white rounded-xl shadow-2xl border border-border-subtle p-6">
            <div className="flex items-center justify-between pb-4 border-b border-border-subtle mb-4">
              <h3 className="text-lg font-bold text-on-surface">Add New Hardware Product</h3>
              <button onClick={() => setIsAddingProduct(false)} className="p-1 text-on-surface-variant hover:text-on-surface">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form
              onSubmit={(e) => {
                e.preventDefault();
                const form = e.target as HTMLFormElement;
                const fd = new FormData(form);
                handleAddProduct({
                  name: fd.get("name") as string,
                  category: fd.get("category") as string,
                  price: Number(fd.get("price")),
                  inventory: Number(fd.get("inventory")),
                  brand: fd.get("brand") as string,
                  shipping: {
                    weightKg: Number(fd.get("weightKg")),
                    dimensionsCm: fd.get("dimensionsCm") as string,
                  }
                });
              }}
              className="space-y-4"
            >
              <div>
                <label className="block text-xs font-medium text-on-surface-variant mb-1">Product Title</label>
                <input required name="name" type="text" placeholder="e.g. RTX 4080 Super 16GB" className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg" />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Category</label>
                  <select name="category" className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg bg-white">
                    {CATEGORIES.filter(c => c !== "All").map(c => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Brand</label>
                  <input name="brand" type="text" placeholder="e.g. ASUS, Corsair" className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Price (₹ INR)</label>
                  <input required name="price" type="number" placeholder="5999" className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg font-mono" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Stock Quantity</label>
                  <input required name="inventory" type="number" placeholder="25" className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg font-mono" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Package Weight (kg)</label>
                  <input name="weightKg" type="number" step="0.01" placeholder="0.75" className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg font-mono" />
                </div>
                <div>
                  <label className="block text-xs font-medium text-on-surface-variant mb-1">Dimensions (cm)</label>
                  <input name="dimensionsCm" type="text" placeholder="30x20x8" className="w-full px-3 py-2 text-sm border border-border-subtle rounded-lg font-mono" />
                </div>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-border-subtle">
                <button type="button" onClick={() => setIsAddingProduct(false)} className="px-4 py-2 text-xs font-medium text-on-surface-variant">
                  Cancel
                </button>
                <button type="submit" className="px-4 py-2 text-xs font-semibold bg-primary text-white rounded-lg hover:bg-opacity-90 shadow-sm">
                  Add to Catalog
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </AppShell>
  );
}
