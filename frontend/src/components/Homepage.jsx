import { motion } from "framer-motion";
import {
  Radar,
  ShieldCheck,
  ListChecks,
  Database,
  Sparkles,
  ArrowRight,
  Network,
} from "lucide-react";

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0 },
};

function Homepage({ onGetStarted }) {
  return (
    <div className="min-h-screen bg-white dark:bg-slate-950 overflow-y-auto">
      {/* Top nav */}
      <nav className="flex items-center justify-between px-8 py-6 max-w-6xl mx-auto">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-brand-darkest dark:bg-brand-light flex items-center justify-center text-white dark:text-slate-900 font-bold text-lg">
            N
          </div>
          <span className="text-lg font-bold text-slate-900 dark:text-white tracking-tight">
            NBDE
          </span>
        </div>
        <button
          onClick={onGetStarted}
          className="px-5 py-2 rounded-full bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900 text-sm font-semibold hover:opacity-90 transition"
        >
          Sign In
        </button>
      </nav>

      {/* Hero */}
      <section className="max-w-4xl mx-auto px-8 pt-20 pb-24 text-center">
        <motion.div
          initial="hidden"
          animate="visible"
          variants={fadeUp}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-lightest dark:bg-slate-800 text-brand-darkest dark:text-brand-light text-sm font-medium mb-8"
        >
          <Sparkles size={14} />
          Agentic Decision Intelligence Platform
        </motion.div>

        <motion.h1
          initial="hidden"
          animate="visible"
          variants={fadeUp}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-5xl md:text-6xl font-bold text-slate-900 dark:text-white tracking-tight leading-[1.1] mb-6"
        >
          Next Best Decision
          <br />
          <span className="text-brand-darkest dark:text-brand-light">Engine</span>
        </motion.h1>

        <motion.p
          initial="hidden"
          animate="visible"
          variants={fadeUp}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-lg text-slate-500 dark:text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed"
        >
          When crisis strikes, information is scattered across a dozen systems.
          NBDE orchestrates a network of AI agents to gather the facts, detect
          weak signals, assess risk, and recommend the next best action —
          explained, not just predicted.
        </motion.p>

        <motion.button
          initial="hidden"
          animate="visible"
          variants={fadeUp}
          transition={{ duration: 0.6, delay: 0.3 }}
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.97 }}
          onClick={onGetStarted}
          className="inline-flex items-center gap-2 px-8 py-3.5 rounded-full bg-brand-darkest dark:bg-brand-light text-white dark:text-slate-900 font-semibold text-base hover:opacity-90 transition shadow-lg shadow-brand-darkest/20"
        >
          Get Started
          <ArrowRight size={18} />
        </motion.button>
      </section>

      {/* Feature highlights */}
      <section className="max-w-5xl mx-auto px-8 pb-24">
        <div className="grid md:grid-cols-3 gap-6">
          <FeatureCard
            icon={Radar}
            title="Weak Signal Detection"
            description="Surfaces early operational risks across contracts, inventory, vendors, and external news before they escalate."
            delay={0}
          />
          <FeatureCard
            icon={ShieldCheck}
            title="Explainable Risk Scoring"
            description="Every risk score is traced back to the exact signals and evidence that produced it — no black box."
            delay={0.1}
          />
          <FeatureCard
            icon={ListChecks}
            title="Actionable Recommendations"
            description="Immediate, short-term, and long-term response plans, with stakeholders identified automatically."
            delay={0.2}
          />
        </div>
      </section>

      {/* How it works */}
      <section className="max-w-5xl mx-auto px-8 pb-28">
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.5 }}
          transition={{ duration: 0.5 }}
          className="text-2xl font-bold text-slate-900 dark:text-white text-center mb-3"
        >
          How it works
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.5 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="text-center text-slate-500 dark:text-slate-400 mb-14 max-w-xl mx-auto"
        >
          A pipeline of independent agents, each building on the last.
        </motion.p>

        <div className="flex flex-col gap-6">
          <PipelineStep
            icon={Database}
            number="01"
            title="Gather Data"
            description="Independent datasource agents collect supplier contracts, inventory levels, vendor status, policies, news, and incident history."
            align="left"
          />
          <PipelineStep
            icon={Network}
            number="02"
            title="Detect Weak Signals"
            description="Patterns across the gathered data are scanned for early warning signs of operational risk."
            align="right"
          />
          <PipelineStep
            icon={ShieldCheck}
            number="03"
            title="Assess Risk"
            description="Detected signals are weighted and combined into a single operational risk score and severity level."
            align="left"
          />
          <PipelineStep
            icon={ListChecks}
            number="04"
            title="Recommend Action"
            description="A prioritized response plan is generated, with stakeholders to notify and the reasoning behind every decision."
            align="right"
          />
        </div>
      </section>

      <footer className="border-t border-slate-100 dark:border-slate-800 py-8 text-center text-sm text-slate-400 dark:text-slate-500">
        Next Best Decision Engine — Built by Team NBDE
      </footer>
    </div>
  );
}

function FeatureCard({ icon: Icon, title, description, delay }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.4 }}
      transition={{ duration: 0.5, delay }}
      whileHover={{ y: -4 }}
      className="p-6 rounded-2xl border border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 transition-shadow hover:shadow-lg"
    >
      <div className="w-11 h-11 rounded-xl bg-brand-lightest dark:bg-slate-800 flex items-center justify-center mb-4">
        <Icon size={20} className="text-brand-darkest dark:text-brand-light" />
      </div>
      <h3 className="font-bold text-slate-900 dark:text-white mb-2">{title}</h3>
      <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
        {description}
      </p>
    </motion.div>
  );
}

function PipelineStep({ icon: Icon, number, title, description, align }) {
  const isLeft = align === "left";

  return (
    <motion.div
      initial={{ opacity: 0, x: isLeft ? -30 : 30 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true, amount: 0.5 }}
      transition={{ duration: 0.5 }}
      className={`flex items-center gap-5 ${isLeft ? "" : "md:flex-row-reverse md:text-right"}`}
    >
      <div className="shrink-0 w-14 h-14 rounded-2xl bg-brand-darkest dark:bg-brand-light flex items-center justify-center text-white dark:text-slate-900">
        <Icon size={24} />
      </div>
      <div className="flex-1 p-5 rounded-2xl bg-slate-50 dark:bg-slate-900 border border-slate-100 dark:border-slate-800">
        <span className="text-xs font-bold text-brand-darkest dark:text-brand-light tracking-wider">
          STEP {number}
        </span>
        <h3 className="font-bold text-slate-900 dark:text-white text-lg mt-1 mb-1.5">
          {title}
        </h3>
        <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
          {description}
        </p>
      </div>
    </motion.div>
  );
}

export default Homepage;