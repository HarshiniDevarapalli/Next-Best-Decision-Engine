import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Database, ChevronDown } from "lucide-react";

function Field({ label, value }) {
  if (value === undefined || value === null || value === "") return null;

  return (
    <div className="flex justify-between gap-4 py-1.5 text-sm border-b border-slate-100 dark:border-slate-800 last:border-0">
      <span className="text-slate-400 dark:text-slate-500">{label}</span>
      <span className="text-slate-700 dark:text-slate-200 font-medium text-right">
        {Array.isArray(value) ? value.join(", ") : String(value)}
      </span>
    </div>
  );
}

function SupplierSection({ data }) {
  return (
    <div>
      <Field label="Supplier" value={data.supplier} />
      <Field label="Contract Type" value={data.contract_type} />
      <Field label="Contract Expiry" value={data.contract_expiry} />
      <Field label="Penalty Clause" value={data.penalty_clause ? "Yes" : "No"} />
      <Field label="Critical Components" value={data.critical_components} />
      <Field label="Service Level" value={data.service_level} />
    </div>
  );
}

function InventorySection({ data }) {
  return (
    <div>
      <Field label="Component" value={data.component} />
      <Field label="Warehouse" value={data.warehouse} />
      <Field label="Stock Days Remaining" value={data.stock_days_remaining} />
      <Field label="Daily Consumption" value={data.daily_consumption} />
      <Field label="Production Impact" value={data.production_impact} />
    </div>
  );
}

function VendorSection({ data }) {
  const vendors = data.vendors || [];
  return (
    <div className="flex flex-col gap-3">
      {vendors.map((v, i) => (
        <div key={i} className="bg-slate-50 dark:bg-slate-800/60 rounded-xl p-3">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 mb-1">
            {v.vendor_name}
          </p>
          <Field label="Approved Vendor" value={v.approved_vendor ? "Yes" : "No"} />
          <Field label="Lead Time" value={`${v.lead_time_days} days`} />
          <Field label="Capacity Available" value={v.capacity_available ? "Yes" : "No"} />
          <Field label="Estimated Cost Increase" value={v.estimated_cost_increase} />
        </div>
      ))}
    </div>
  );
}

function PolicySection({ data }) {
  const policies = data.policies || [];
  return (
    <ul className="flex flex-col gap-2">
      {policies.map((p, i) => (
        <li key={i} className="flex gap-2 text-sm text-slate-600 dark:text-slate-300">
          <span className="mt-1.5 w-1 h-1 rounded-full bg-brand-darkest dark:bg-brand-light shrink-0" />
          <span>{p.rule}</span>
        </li>
      ))}
    </ul>
  );
}

function NewsSection({ data }) {
  return (
    <div>
      <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 mb-1">
        {data.headline}
      </p>
      <Field label="Source" value={data.source} />
      <Field label="Impact" value={data.impact} />
      <p className="text-sm text-slate-500 dark:text-slate-400 mt-2">{data.summary}</p>
    </div>
  );
}

function IncidentHistorySection({ data }) {
  const incidents = data.incident_history || [];
  return (
    <div className="flex flex-col gap-3">
      {incidents.map((inc, i) => (
        <div key={i} className="bg-slate-50 dark:bg-slate-800/60 rounded-xl p-3">
          <p className="text-sm font-semibold text-slate-700 dark:text-slate-200 mb-1">
            {inc.incident_type} — {inc.incident_date}
          </p>
          <p className="text-sm text-slate-500 dark:text-slate-400">{inc.resolution}</p>
          <Field label="Downtime" value={`${inc.downtime_days} day(s)`} />
        </div>
      ))}
    </div>
  );
}

const SECTION_RENDERERS = {
  supplier_contract: { label: "Supplier Contract", Component: SupplierSection },
  inventory: { label: "Inventory", Component: InventorySection },
  vendor: { label: "Vendors", Component: VendorSection },
  policy: { label: "Policies", Component: PolicySection },
  news: { label: "News", Component: NewsSection },
  incident_history: { label: "Incident History", Component: IncidentHistorySection },
};

function EvidenceCard({ contextData }) {
  const [open, setOpen] = useState(false);

  if (!contextData) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.25 }}
      className="rounded-2xl border border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 p-6"
    >
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between text-left"
      >
        <div className="flex items-center gap-2">
          <Database size={18} className="text-brand-darkest dark:text-brand-light" />
          <h2 className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
            Supporting Evidence
          </h2>
        </div>
        <motion.div animate={{ rotate: open ? 180 : 0 }} transition={{ duration: 0.2 }}>
          <ChevronDown size={18} className="text-slate-400" />
        </motion.div>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden"
          >
            <div className="mt-5 flex flex-col gap-5">
              {Object.entries(SECTION_RENDERERS).map(([key, { label, Component }]) => {
                const data = contextData[key];
                if (!data) return null;

                return (
                  <div
                    key={key}
                    className="pt-4 border-t border-slate-100 dark:border-slate-800 first:border-0 first:pt-0"
                  >
                    <p className="text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2">
                      {label}
                    </p>
                    <Component data={data} />
                  </div>
                );
              })}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default EvidenceCard;