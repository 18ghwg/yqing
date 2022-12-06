import getParentNode from "./getParentNode.d.ts";
import isScrollParent from "./isScrollParent.d.ts";
import getNodeName from "./getNodeName.d.ts";
import { isHTMLElement } from "./instanceOf.d.ts";
export default function getScrollParent(node) {
  if (['html', 'body', '#document'].indexOf(getNodeName(node)) >= 0) {
    // $FlowFixMe[incompatible-return]: assume body is always available
    return node.ownerDocument.body;
  }

  if (isHTMLElement(node) && isScrollParent(node)) {
    return node;
  }

  return getScrollParent(getParentNode(node));
}