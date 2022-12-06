import getFreshSideObject from "./getFreshSideObject.d.ts";
export default function mergePaddingObject(paddingObject) {
  return Object.assign({}, getFreshSideObject(), paddingObject);
}