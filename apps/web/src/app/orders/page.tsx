"use client";

import { useState } from "react";
import { AppShell } from "@/components/app-shell/shell";
import { PageHeader, GlassPanel, SolidPanel, StatusBadge } from "@/components/shared/primitives";
import { paymentResult } from "@/data/fixtures/demo-scenario";
import { formatINR } from "@/lib/formatters";
import { Eye, X, ShieldCheck, Filter } from "lucide-react";

interface OrderItem {
  name: string;
  quantity: number;
  price: number;
}

interface OrderRecord {
  id: string;
  customer: string;
  amount: number;
  source: string;
  payment: string;
  status: "success" | "failed" | "pending";
  date: string;
  paymentId?: string;
  items: OrderItem[];
}

const initialOrders: OrderRecord[] = [
  {
    id: paymentResult.orderId,
    customer: "AI Buyer Demo",
    amount: paymentResult.amount,
    source: "AI Buyer",
    payment: "Razorpay Test Mode",
    status: "success",
    date: "Just now",
    paymentId: "pay_test_ai_001",
    items: [
      { name: "ProBook 14", quantity: 1, price: 62999 },
      { name: "USB-C Dock", quantity: 1, price: 4999 },
      { name: "Laptop Stand", quantity: 1, price: 1799 },
    ],
  },
  {
    id: "#RGO-10471",
    customer: "Priya Sharma",
    amount: 4999,
    source: "Storefront",
    payment: "Razorpay Test Mode",
    status: "success",
    date: "Today, 10:14 AM",
    paymentId: "pay_test_sf_042",
    items: [{ name: "USB-C Dock", quantity: 1, price: 4999 }],
  },
  {
    id: "#RGO-10465",
    customer: "Arjun Mehta",
    amount: 62999,
    source: "Storefront",
    payment: "Razorpay Test Mode",
    status: "failed",
    date: "Yesterday, 4:20 PM",
    paymentId: "pay_test_declined_019",
    items: [{ name: "ProBook 14", quantity: 1, price: 62999 }],
  },
  {
    id: "#RGO-10460",
    customer: "Rahul Verma",
    amount: 38999,
    source: "AI Buyer",
    payment: "Razorpay Test Mode",
    status: "success",
    date: "2 days ago",
    paymentId: "pay_test_ai_002",
    items: [{ name: "Ryzen 7 7800X3D CPU", quantity: 1, price: 38999 }],
  },
];

export default function OrdersPage() {
  const [orderList] = useState<OrderRecord[]>(initialOrders);
  const [channelFilter, setChannelFilter] = useState<string>("all");
  const [selectedOrder, setSelectedOrder] = useState<OrderRecord | null>(null);

  const filteredOrders = orderList.filter((o) => {
    if (channelFilter === "all") return true;
    return o.source.toLowerCase().includes(channelFilter.toLowerCase());
  });

  const gmv = orderList.filter(o => o.status === "success").reduce((sum, o) => sum + o.amount, 0);
  const successCount = orderList.filter((o) => o.status === "success").length;
  const failedCount = orderList.filter((o) => o.status === "failed").length;
  const aiBuyerCount = orderList.filter((o) => o.source === "AI Buyer").length;

  return (
    <AppShell>
      <PageHeader title="Orders & Settlements" description="Commerce transactions, AI Buyer purchases, and Razorpay settlements." />

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <GlassPanel className="!p-4 shadow-sm">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Captured GMV</p>
          <p className="font-metric-display-sm text-metric-display-sm text-on-surface">{formatINR(gmv)}</p>
        </GlassPanel>
        <GlassPanel className="!p-4 shadow-sm">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Successful Payments</p>
          <p className="font-metric-display-sm text-metric-display-sm text-emerald-600">{successCount}</p>
        </GlassPanel>
        <GlassPanel className="!p-4 shadow-sm">
          <p className="font-body-sm text-body-sm text-on-surface-variant">Declined / Failed</p>
          <p className="font-metric-display-sm text-metric-display-sm text-red-600">{failedCount}</p>
        </GlassPanel>
        <GlassPanel className="!p-4 shadow-sm">
          <p className="font-body-sm text-body-sm text-on-surface-variant">AI Buyer Orders</p>
          <p className="font-metric-display-sm text-metric-display-sm text-blue-600">{aiBuyerCount}</p>
        </GlassPanel>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 mb-4">
        <Filter className="w-4 h-4 text-on-surface-variant mr-1" />
        {["all", "AI Buyer", "Storefront"].map((ch) => (
          <button
            key={ch}
            onClick={() => setChannelFilter(ch)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
              channelFilter === ch
                ? "bg-primary text-white shadow-sm"
                : "bg-surface-container text-on-surface-variant hover:bg-surface-container-high"
            }`}
          >
            {ch === "all" ? "All Channels" : ch}
          </button>
        ))}
      </div>

      <SolidPanel className="!p-0 overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-border-subtle bg-surface-container-low/50">
              {["Order ID", "Customer", "Amount", "Channel", "Gateway / Mode", "Status", "Date", "Action"].map((h) => (
                <th key={h} className="px-5 py-3.5 font-label-bold text-label-bold text-on-surface-variant whitespace-nowrap">
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredOrders.map((o) => (
              <tr key={o.id} className="border-b border-border-subtle last:border-0 hover:bg-surface-container-low/30 transition-colors">
                <td className="px-5 py-4 font-data-mono text-data-mono font-semibold text-primary whitespace-nowrap">{o.id}</td>
                <td className="px-5 py-4 font-body-sm text-body-sm whitespace-nowrap font-medium text-on-surface">{o.customer}</td>
                <td className="px-5 py-4 font-data-mono text-data-mono font-semibold whitespace-nowrap">{formatINR(o.amount)}</td>
                <td className="px-5 py-4 whitespace-nowrap">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                    o.source === "AI Buyer" ? "bg-blue-50 text-blue-700" : "bg-purple-50 text-purple-700"
                  }`}>
                    {o.source}
                  </span>
                </td>
                <td className="px-5 py-4 font-body-sm text-body-sm text-on-surface-variant whitespace-nowrap">{o.payment}</td>
                <td className="px-5 py-4 whitespace-nowrap">
                  <StatusBadge status={o.status} label={o.status === "success" ? "Captured" : "Failed"} />
                </td>
                <td className="px-5 py-4 font-body-sm text-body-sm text-on-surface-variant whitespace-nowrap">{o.date}</td>
                <td className="px-5 py-4 whitespace-nowrap">
                  <button
                    onClick={() => setSelectedOrder(o)}
                    className="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium text-primary hover:bg-surface-container rounded transition-colors"
                  >
                    <Eye className="w-3.5 h-3.5" /> Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </SolidPanel>

      {/* Order Detail Modal */}
      {selectedOrder && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-fade-in">
          <div className="w-full max-w-lg bg-white rounded-xl shadow-2xl border border-border-subtle p-6 overflow-hidden">
            <div className="flex items-center justify-between pb-4 border-b border-border-subtle mb-4">
              <div>
                <h3 className="text-lg font-bold text-on-surface">Order Details</h3>
                <p className="text-xs text-on-surface-variant font-mono">{selectedOrder.id} • {selectedOrder.customer}</p>
              </div>
              <button onClick={() => setSelectedOrder(null)} className="p-1 text-on-surface-variant hover:text-on-surface">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4 text-sm">
              <div className="flex items-center justify-between p-3 rounded-lg bg-surface-container">
                <span className="text-xs text-on-surface-variant">Payment Status</span>
                <StatusBadge status={selectedOrder.status} label={selectedOrder.status === "success" ? "Captured (Paid)" : "Failed"} />
              </div>

              {selectedOrder.paymentId && (
                <div className="flex items-center justify-between text-xs py-1 border-b border-border-subtle">
                  <span className="text-on-surface-variant">Razorpay Payment ID</span>
                  <span className="font-mono font-medium">{selectedOrder.paymentId}</span>
                </div>
              )}

              <div>
                <p className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider mb-2">Purchased Items</p>
                <div className="space-y-2 border border-border-subtle rounded-lg p-3">
                  {selectedOrder.items.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between text-xs">
                      <span className="font-medium text-on-surface">{item.name} <span className="text-on-surface-variant font-mono">× {item.quantity}</span></span>
                      <span className="font-mono font-semibold">{formatINR(item.price * item.quantity)}</span>
                    </div>
                  ))}
                  <div className="border-t border-border-subtle pt-2 flex items-center justify-between font-bold text-sm">
                    <span>Total Amount</span>
                    <span className="font-mono text-primary">{formatINR(selectedOrder.amount)}</span>
                  </div>
                </div>
              </div>

              <div className="p-3 bg-emerald-50 rounded-lg flex items-center gap-2 text-xs text-emerald-800">
                <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>Verified by Merchant Policy Guard &amp; Razorpay Standard Signature</span>
              </div>
            </div>

            <div className="flex items-center justify-end pt-4 mt-4 border-t border-border-subtle">
              <button
                onClick={() => setSelectedOrder(null)}
                className="px-4 py-2 text-xs font-semibold bg-surface-container text-on-surface hover:bg-surface-container-high rounded-lg"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </AppShell>
  );
}
