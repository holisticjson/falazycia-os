import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const NeonBackground: React.FC<{ primaryColor: string; secondaryColor: string }> = ({
  primaryColor,
  secondaryColor,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const pulse = interpolate(
    Math.sin(frame / 15),
    [-1, 1],
    [0.4, 0.8]
  );

  const rotate = interpolate(frame, [0, durationInFrames], [0, 360]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "#0B0F17",
        overflow: "hidden",
        zIndex: 0,
      }}
    >
      {/* Dynamic Animated Neon Glow Blob 1 */}
      <div
        style={{
          position: "absolute",
          top: "-10%",
          left: "-20%",
          width: "800px",
          height: "800px",
          borderRadius: "50%",
          background: `radial-gradient(circle, ${primaryColor} 0%, rgba(0,0,0,0) 70%)`,
          opacity: pulse * 0.45,
          filter: "blur(90px)",
          transform: `rotate(${rotate}deg) scale(${pulse + 0.5})`,
        }}
      />

      {/* Dynamic Animated Neon Glow Blob 2 */}
      <div
        style={{
          position: "absolute",
          bottom: "-15%",
          right: "-20%",
          width: "900px",
          height: "900px",
          borderRadius: "50%",
          background: `radial-gradient(circle, ${secondaryColor} 0%, rgba(0,0,0,0) 70%)`,
          opacity: pulse * 0.4,
          filter: "blur(100px)",
          transform: `rotate(-${rotate * 0.8}deg) scale(${1.2 - pulse * 0.3})`,
        }}
      />

      {/* Subtle Grid Overlay Pattern */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          backgroundImage:
            "linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
          opacity: 0.6,
        }}
      />
    </div>
  );
};
