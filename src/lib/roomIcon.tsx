import { BathIcon, BedIcon, DoorIcon, KitchenIcon, SofaIcon } from "../components/icons";
import type { RoomIcon } from "../types";
import type { SVGProps } from "react";

export function getRoomIcon(icon: RoomIcon) {
  switch (icon) {
    case "living-room":
      return SofaIcon;
    case "bedroom":
      return BedIcon;
    case "bathroom":
      return BathIcon;
    case "kitchen":
      return KitchenIcon;
    case "hallway":
    case "other":
    default:
      return DoorIcon;
  }
}

export function RoomIconGlyph({ icon, ...props }: { icon: RoomIcon } & SVGProps<SVGSVGElement>) {
  const Cmp = getRoomIcon(icon);
  return <Cmp {...props} />;
}
