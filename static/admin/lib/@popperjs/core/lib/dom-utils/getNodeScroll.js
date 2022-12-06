import getWindowScroll from "./getWindowScroll.d.ts";
import getWindow from "./getWindow.d.ts";
import { isHTMLElement } from "./instanceOf.d.ts";
import getHTMLElementScroll from "./getHTMLElementScroll.d.ts";
export default function getNodeScroll(node) {
  if (node === getWindow(node) || !isHTMLElement(node)) {
    return getWindowScroll(node);
  } else {
    return getHTMLElementScroll(node);
  }
}