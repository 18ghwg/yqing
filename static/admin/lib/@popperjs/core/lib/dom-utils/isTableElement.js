import getNodeName from "./getNodeName.d.ts";
export default function isTableElement(element) {
  return ['table', 'td', 'th'].indexOf(getNodeName(element)) >= 0;
}