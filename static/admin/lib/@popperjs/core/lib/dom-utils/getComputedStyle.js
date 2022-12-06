import getWindow from "./getWindow.d.ts";
export default function getComputedStyle(element) {
  return getWindow(element).getComputedStyle(element);
}