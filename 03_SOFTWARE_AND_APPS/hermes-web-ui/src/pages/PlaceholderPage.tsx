import React from "react";
import { Typography } from "@/components/NouiTypography";

export default function PlaceholderPage() {
  return (
    <div className="flex h-full flex-col items-center justify-center p-8 text-center">
      <Typography variant="display" className="mb-4 text-3xl text-midground">
        Coming Soon
      </Typography>
      <Typography className="text-text-secondary max-w-md">
        Ten moduł jest w trakcie budowy. Będzie zintegrowany z agentem Hermes OS w następnej fazie.
      </Typography>
    </div>
  );
}
