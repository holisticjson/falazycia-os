export interface JaisonReelProps {
  title: string;
  subtitle: string;
  hookText: string;
  authorName: string;
  authorHandle: string;
  primaryColor: string;
  secondaryColor: string;
  motto: string;
  captions: Array<{ word: string; startFrame: number; endFrame: number }>;
}

export const defaultJaisonReelProps: JaisonReelProps = {
  title: "Zewnętrzny Mózg z AI",
  subtitle: "Jak okiełznałem paraliż decyzyjny i ADHD za pomocą suwerennego bota",
  hookText: "Przestań budować na ślepo! 🚀",
  authorName: "Tomasz Duda",
  authorHandle: "@jaison.aidhd",
  primaryColor: "#10B981", // Emerald Green
  secondaryColor: "#3B82F6", // Cyber Blue
  motto: "Robimy to co ważne. Resztę robi kod.",
  captions: [
    { word: "Masz", startFrame: 90, endFrame: 110 },
    { word: "dość", startFrame: 111, endFrame: 130 },
    { word: "chaosu", startFrame: 131, endFrame: 150 },
    { word: "kognitywnego?", startFrame: 151, endFrame: 180 },
    { word: "Oto", startFrame: 190, endFrame: 210 },
    { word: "Twój", startFrame: 211, endFrame: 230 },
    { word: "osobisty", startFrame: 231, endFrame: 250 },
    { word: "Co-Pilot", startFrame: 251, endFrame: 280 },
    { word: "Jaison", startFrame: 281, endFrame: 300 },
    { word: "OS!", startFrame: 301, endFrame: 330 },
  ],
};
