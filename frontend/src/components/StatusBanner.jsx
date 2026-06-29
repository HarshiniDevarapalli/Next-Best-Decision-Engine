import { motion } from "framer-motion";
import { CheckCircle2, XCircle } from "lucide-react";

function StatusBanner({ type, message }) {
  const isSuccess = type === "success";

  return (
    <div className="flex flex-col items-center justify-center py-20 px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3, ease: "easeOut" }}
        className={`flex items-center gap-3 px-6 py-4 rounded-2xl ${
          isSuccess
            ? "bg-brand-lightest dark:bg-slate-800 text-brand-darkest dark:text-brand-light"
            : "bg-red-50 dark:bg-red-950/40 text-red-600 dark:text-red-400"
        }`}
      >
        {isSuccess ? <CheckCircle2 size={24} /> : <XCircle size={24} />}
        <span className="font-semibold">{message}</span>
      </motion.div>
    </div>
  );
}

export default StatusBanner;