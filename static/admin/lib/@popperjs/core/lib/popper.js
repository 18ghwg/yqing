import { popperGenerator, detectOverflow } from "./createPopper.d.ts";
import eventListeners from "./modifiers/eventListeners.d.ts";
import popperOffsets from "./modifiers/popperOffsets.d.ts";
import computeStyles from "./modifiers/computeStyles.d.ts";
import applyStyles from "./modifiers/applyStyles.d.ts";
import offset from "./modifiers/offset.d.ts";
import flip from "./modifiers/flip.d.ts";
import preventOverflow from "./modifiers/preventOverflow.d.ts";
import arrow from "./modifiers/arrow.d.ts";
import hide from "./modifiers/hide.d.ts";
var defaultModifiers = [eventListeners, popperOffsets, computeStyles, applyStyles, offset, flip, preventOverflow, arrow, hide];
var createPopper = /*#__PURE__*/popperGenerator({
  defaultModifiers: defaultModifiers
}); // eslint-disable-next-line import/no-unused-modules

export { createPopper, popperGenerator, defaultModifiers, detectOverflow }; // eslint-disable-next-line import/no-unused-modules

export { createPopper as createPopperLite } from "./popper-lite.d.ts"; // eslint-disable-next-line import/no-unused-modules

export * from "./modifiers/index.d.ts";