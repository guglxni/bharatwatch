"use client";

import { useEffect, useRef } from "react";
import { useInView, animate } from "motion/react";
import { cn } from "@/lib/utils";

export function NumberTicker({
  value,
  decimals = 0,
  className,
  suffix = "",
  prefix = "",
}: {
  value: number;
  decimals?: number;
  className?: string;
  suffix?: string;
  prefix?: string;
}) {
  const ref = useRef<HTMLSpanElement>(null);
  const inView = useInView(ref, { once: true, margin: "-40px" });

  useEffect(() => {
    if (!inView || !ref.current) return;
    const controls = animate(0, value, {
      duration: 1.4,
      ease: [0.16, 1, 0.3, 1],
      onUpdate: (v) => {
        if (ref.current) {
          ref.current.textContent =
            prefix + v.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ",") + suffix;
        }
      },
    });
    return () => controls.stop();
  }, [inView, value, decimals, prefix, suffix]);

  return (
    <span ref={ref} className={cn("tabular", className)}>
      {prefix}0{suffix}
    </span>
  );
}
