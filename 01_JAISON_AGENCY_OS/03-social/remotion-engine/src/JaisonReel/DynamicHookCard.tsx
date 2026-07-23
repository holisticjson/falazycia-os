import React from "react";
import { spring, useCurrentFrame, useVideoConfig } from "remotion";

export const DynamicHookCard: React.FC<{
  title: string;
  subtitle: string;
  hookText: string;
  primaryColor: string;
}> = ({ title, subtitle, hookText, primaryColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrance spring animation starting around frame 15
  const scale = spring({
    frame: frame - 15,
    fps,
    config: { damping: 10, stiffness: 100 },
  });

  const opacity = spring({
    frame: frame - 10,
    fps,
    config: { damping: 15 },
  });

  return (
    <div
      style={{
        position: "absolute",
        top: "220px",
        left: "50%",
        transform: `translateX(-50%) scale(${Math.max(0, scale)})`,
        opacity: Math.max(0, opacity),
        width: "88%",
        padding: "32px 28px",
        backgroundColor: "rgba(15, 23, 42, 0.85)",
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        border: `2px solid ${primaryColor}`,
        borderRadius: "28px",
        boxShadow: `0 20px 50px rgba(0,0,0,0.6), 0 0 25px ${primaryColor}44`,
        zIndex: 5,
        display: "flex",
        flexDirection: "column",
        gap: "16px",
      }}
    >
      {/* Scroll Stopper Hook Badge */}
      <div
        style={{
          alignSelf: "flex-start",
          backgroundColor: primaryColor,
          color: "#090D16",
          padding: "8px 18px",
          borderRadius: "30px",
          fontWeight: 800,
          fontSize: "16px",
          letterSpacing: "1px",
          textTransform: "uppercase",
          boxShadow: `0 0 15px ${primaryColor}`,
          fontFamily: "system-ui, -apple-system, sans-serif",
        }}
      >
        {hookText}
      </div>

      {/* Main Title */}
      <h1
        style={{
          margin: 0,
          color: "#FFFFFF",
          fontSize: "44px",
          fontWeight: 900,
          lineHeight: "1.15",
          letterSpacing: "-0.5px",
          fontFamily: "system-ui, -apple-system, sans-serif",
          textShadow: "0 4px 10px rgba(0,0,0,0.5)",
        }}
      >
        {title}
      </h1>

      {/* Subtitle / Promise */}
      <p
        style={{
          margin: 0,
          color: "#CBD5E1",
          fontSize: "22px",
          fontWeight: 500,
          lineHeight: "1.4",
          fontFamily: "system-ui, -apple-system, sans-serif",
        }}
      >
        {subtitle}
      </p>
    </div>
  );
};
