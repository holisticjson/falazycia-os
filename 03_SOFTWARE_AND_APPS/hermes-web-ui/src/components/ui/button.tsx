import * as React from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "default" | "outline" | "ghost" | "destructive" | "secondary" | "link";
  size?: "default" | "sm" | "lg" | "icon";
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center whitespace-nowrap text-sm font-medium transition-colors",
          "focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-midground",
          "disabled:pointer-events-none disabled:opacity-50",
          variant === "default" && "bg-midground text-background-base shadow hover:bg-midground/90",
          variant === "outline" && "border border-current/25 bg-transparent shadow-sm hover:bg-midground/10 hover:text-midground text-text-secondary",
          variant === "ghost" && "hover:bg-midground/10 hover:text-midground text-text-secondary",
          variant === "destructive" && "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
          variant === "secondary" && "bg-card text-midground shadow-sm hover:bg-card/80",
          variant === "link" && "text-midground underline-offset-4 hover:underline",
          size === "default" && "h-9 px-4 py-2",
          size === "sm" && "h-7 px-3 text-xs",
          size === "lg" && "h-10 px-8",
          size === "icon" && "h-9 w-9",
          className,
        )}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";

export { Button };
