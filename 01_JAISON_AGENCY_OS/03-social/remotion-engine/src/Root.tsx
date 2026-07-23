import { Composition } from "remotion";
import { JaisonReel } from "./JaisonReel/Index";
import { defaultJaisonReelProps } from "./JaisonReel/types";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="JaisonReel"
        component={JaisonReel}
        durationInFrames={450} // 15 seconds at 30fps
        fps={30}
        width={1080}
        height={1920}
        defaultProps={defaultJaisonReelProps}
      />
    </>
  );
};
